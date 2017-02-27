#coding=utf8
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


from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from cashflow.forms import DaiKuanForm
from cashflow.forms import CashLoopForm


def index(request):
    money_total = 95400
    cashflow = []
    now = timezone.now()
    for cc in CashChange.objects.all():
        print cc.dt, type(cc.dt)
        print now, type(now)
        if now < cc.dt:
            money_total += cc.changed_money
            cashflow.append({
                "total": '%.2f' % money_total,
                "change": '%.2f' % cc.changed_money,
                "dt": cc.dt.strftime("%Y-%m-%d %H:%M:%S"),
                "remark": cc.remark,
                "plan": cc.plan.__str__()
            })

    return render(
        request,
        'cashflow/index.html',
        {
            'cashflow': cashflow
        }
      )


def plan_list(request):
    plans = []
    plans.extend(DaiKuan.objects.all())
    plans.extend(CashLoopPlan.objects.all())
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

