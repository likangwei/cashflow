#coding=utf8

import json
import time
import datetime
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
    now = timezone.now() if last_cash_tag is None else last_cash_tag.dt
    money_total = 0 if last_cash_tag is None else last_cash_tag.total
    plan_links = request.POST.get('plans', "[]")
    plan_links = json.loads(plan_links)
    ccs = CashChange.objects.filter(plan_link__id__in=plan_links).order_by('dt')
    rst = {"success": True}
    cashflow = rst.setdefault("datas", [])
    for cc in ccs:
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


def cash_change_per_month(request):
    plan_links = request.POST.get('plans', "[]")
    plan_links = json.loads(plan_links)
    rst = {"success": True, "msg": "", "data": []}
    cron = "0 0 0 * *"
    from croniter import croniter
    croner = croniter(cron, datetime.datetime.now(), ret_type=datetime.datetime)
    months = [croner.next() for i in range(100)]
    for i in range(len(months)-2):
        start, end = months[i], months[i+1]
        ccs = CashChange.objects.filter(plan_link__id__in=plan_links,
                                        dt__range=(start, end)).order_by('dt')
        total, income, expenses = 0, 0, 0
        details = []
        for x in ccs:
            t = x.changed_money
            total += t
            income += 0 if t < 0 else t
            expenses -= 0 if t > 0 else t
            details.append(x.dict())
        rst["data"].append(
            {
                "date": start.strftime("%Y-%m"),
                "total": total,
                "income": income,
                "expenses": expenses,
                "details": details
            }
        )
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

