#coding=utf8

import json
import time

from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http.response import HttpResponseRedirect
from django.http.response import JsonResponse
from django.shortcuts import render
from .daikuan import DaiKuan
from django.utils import timezone

from cashflow.models import DaiKuan
from cashflow.models import CashChange
from cashflow.models import CashLoopPlan
from cashflow.models import PlanLink
from cashflow.models import CashTag

from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from cashflow.forms import DaiKuanForm
from cashflow.forms import CashLoopForm


def cash_details(request):
    last_cash_tag = CashTag.objects.order_by("-dt").first()
    money_total = 0 if last_cash_tag is None else last_cash_tag.total
    plan_links = request.POST.get('plans', "[]")
    plan_links = json.loads(plan_links)
    ccs = CashChange.objects.filter(plan_link__id__in=plan_links).order_by('dt')
    rst = {"success": True}
    cashflow = rst.setdefault("datas", [])
    now = timezone.now()
    for cc in ccs:
        print cc.dt, type(cc.dt)
        if now < cc.dt:
            money_total += cc.changed_money
            cashflow.append({
                "total": '%.2f' % money_total,
                "change": '%.2f' % cc.changed_money,
                "dt": cc.dt.strftime('%Y-%m-%d %H:%M:%S'),
                "timestamp": time.mktime(cc.dt.timetuple()),
                "remark": cc.remark,
                "plan": cc.plan.__str__()
            })
    return JsonResponse(rst)


def plan_list(request):
    plans = PlanLink.objects.all()
    return render(request, 'cashflow/plan_list.html', {'plans': plans})


def get_daikuan_detail(request, id):
    daikuan = get_object_or_404(DaiKuan, id=id)

    if request.method == "GET":
        form = DaiKuanForm(instance=daikuan)

    elif request.method == "POST":
        form = DaiKuanForm(request.POST, instance=daikuan)
        if form.is_valid():
            instance = form.save()
            instance.build_cashflow()
            return HttpResponseRedirect(reverse("cashflow:daikuan_detail", args=(daikuan.id,)))
    return render(request, 'cashflow/daikuan_detail.html', {'object': daikuan, 'form': form, 'cashflow': daikuan.cashflows})


def get_loop_plan_detail(request, id):
    plan = get_object_or_404(CashLoopPlan, id=id)

    if request.method == "GET":
        form = CashLoopForm(instance=plan)

    elif request.method == "POST":
        form = CashLoopForm(request.POST, instance=plan)
        if form.is_valid():
            instance = form.save()
            instance.build_cashflow()
            return HttpResponseRedirect(reverse("cashflow:loop_plan_detail", args=(plan.id,)))
    return render(request, 'cashflow/daikuan_detail.html', {'object': plan, 'form': form, 'cashflow': plan.cashflows})

