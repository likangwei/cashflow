#coding=utf8
import json
from django.db import models
from django.contrib.admin.models import ContentType
from datetime import datetime
from django.core.urlresolvers import reverse


class Plan(models.Model):
    TYPE_DAIKUAN = "daikuan"
    TYPE_LOOP_INCOMMING = "loop_incomming"
    name = models.CharField('计划名称', max_length=100, default='')
    enable = models.BooleanField("是否启用", default=False)
    start_date = models.DateTimeField('开始时间', default=None)
    end_date = models.DateTimeField('结束时间', default=None, null=True)
    content = models.TextField("详细介绍", default='')

    def build_cashflow(self):
        raise NotImplementedError

    def get_absolute_url(self):
        raise NotImplementedError

    @property
    def link(self):
        link = PlanLink.objects.filter(content_type=self.content_type, plan_id=self.id).first()
        if link is None:
            link = PlanLink.objects.create(content_type=self.content_type, plan_id=self.id)
        return link

    @property
    def content_type(self):
        return ContentType.objects.get(app_label=self._meta.app_label,
                                       model=self._meta.model_name)

    @property
    def cashflows(self):
        return CashChange.objects.filter(plan_link=self.link)

    def save(self, *args, **kwargs):
        super(Plan, self).save(*args, **kwargs)
        self.link

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


class DateLoopPlan(models.Model):
    cron = models.CharField('cron',  default="0 0 1 * *", max_length=100)

    def get_croniter(self):
        from croniter import croniter
        cr = croniter(self.cron, start_time=self.start_date, ret_type=datetime)
        return cr

    class Meta:
        abstract = True


class CashLoopPlan(Plan, DateLoopPlan):
    cash_per_time = models.FloatField("单次收支")

    def get_absolute_url(self):
        return reverse('cashflow:loop_plan_detail', args=(self.id,))

    def build_cashflow(self):
        self.cashflows.delete()
        cron = self.get_croniter()
        dt = cron.next()
        while self.end_date > dt:
            CashChange.objects.create(
                plan_link=self.link,
                changed_money=self.cash_per_time,
                dt=dt,
                remark=""
            )
            dt = cron.next()


class DaiKuan(Plan, DateLoopPlan):
    DAIKUAN_DEBJ = "debj"
    DAIKUAN_DEBX = "debx"
    DAI_KUAN_TYPE_CHOICES = (
        (DAIKUAN_DEBJ, "等额本金"),
        (DAIKUAN_DEBX, "等额本息"),
    )
    daikuan_total = models.FloatField("贷款本金")
    daikuan_yihuan = models.TextField("贷款已还")
    daikuan_shoufu = models.FloatField("贷款首付")
    daikuan_nianlilv = models.FloatField("贷款年利率")
    daikuan_years = models.IntegerField("贷款年限", default=0)
    daikuan_months = models.IntegerField("贷款月数", default=0)
    daikuan_type = models.CharField('贷款类型', max_length=100, default=DAIKUAN_DEBJ,
                                    choices=DAI_KUAN_TYPE_CHOICES)

    @property
    def yihuanbjs(self):
        return json.loads(self.daikuan_yihuan)

    @property
    def yuelilv(self):
        return self.daikuan_nianlilv / 12

    def build_cashflow(self):
        self.cashflows.delete()
        if self.daikuan_type == self.DAIKUAN_DEBJ:
            self.debj_future_pays()
        elif self.daikuan_type == self.DAIKUAN_DEBX:
            self.debx_future_pays()
        else:
            raise

    @property
    def month_count(self):
        return self.daikuan_years * 12 + self.daikuan_months

    def build_has_pay(self, bj, cron):
        CashChange.objects.create(
            plan_link=self.link,
            changed_money=0 - self.daikuan_shoufu,
            dt=self.start_date,
            remark="首付: %d" % self.daikuan_shoufu
        )
        month_count = self.month_count
        i = -1
        for i in range(len(self.yihuanbjs)):
            pay_total = self.yihuanbjs[i]
            pay_bx = bj * self.yuelilv
            pay_bj = 0 if pay_total < pay_bx else pay_total - pay_bx
            bj -= pay_bj
            CashChange.objects.create(
                plan_link=self.link,
                changed_money=0 - pay_total,
                dt=cron.next(),
                remark="第%d期, 剩余本金: %d. 支付本金: %d 支付本息: %d" % ((i + 1), bj, pay_bj, pay_bx)
            )
            month_count -= 1
        return {"bj": bj, "month_idx": i + 1}

    def debx_future_pays(self):
        """等额本息"""
        cron = self.get_croniter()
        has_pay = self.build_has_pay(self.daikuan_total, cron)
        bj, month_idx = has_pay.get("bj"), has_pay.get("month_idx")

        yll = self.yuelilv
        leave_month = self.month_count - month_idx
        month_to_pay = bj * yll * ((1 + yll) ** leave_month) / ((1 + yll) ** leave_month - 1)

        for i in range(month_idx + 1, self.month_count + 1):
            pay_bx = bj * self.yuelilv
            pay_bj = month_to_pay - pay_bx
            bj -= bj * self.yuelilv
            CashChange.objects.create(
                plan_link=self.link,
                changed_money=0 - month_to_pay,
                dt=cron.next(),
                remark="第%d期, 剩余本金: %d. 支付本金: %d 支付本息: %d" % ((i), bj, pay_bj, pay_bx)
            )

    def debj_future_pays(self):
        """等额本金"""
        cron = self.get_croniter()
        has_pay = self.build_has_pay(self.daikuan_total, cron)
        bj, month_idx = has_pay.get("bj"), has_pay.get("month_idx")

        yuelilv = self.yuelilv
        yuebenjin = bj / (self.month_count - month_idx)

        for i in range(month_idx + 1, self.month_count + 1):
            pay_bx = bj * yuelilv
            pay_bj = yuebenjin
            pay_total = pay_bj + pay_bx
            bj -= yuebenjin
            lave_bj = bj
            CashChange.objects.create(
                plan_link=self.link,
                changed_money=0 - pay_total,
                dt=cron.next(),
                remark="第%d期, 剩余本金: %d. 支付本金: %d 支付本息: %d" % ((i), lave_bj, pay_bj, pay_bx)
            )

    def get_absolute_url(self):
        return reverse('cashflow:daikuan_detail', args=(self.id,))


class PlanLink(models.Model):
    content_type = models.ForeignKey(ContentType, verbose_name="content_type")
    plan_id = models.IntegerField("plan id")
    parent = models.ForeignKey("self", verbose_name="父计划", null=True)

    @property
    def plan(self):
        try:
            model_clz = self.content_type.model_class()
            return self.content_type.get_object_for_this_type(id=self.plan_id)
        except:
            self.delete()

    def __unicode__(self):
        return "link->" + self.plan.name

    class Meta:
        unique_together = ("content_type", "plan_id")


class CashChange(models.Model):
    plan_link = models.ForeignKey(PlanLink, verbose_name="plan_link")
    changed_money = models.FloatField("支出或收入")
    dt = models.DateTimeField('时间')
    remark = models.CharField('备注', max_length=255)

    def dict(self):
        return {
            "plan_name": self.plan_link.plan.name,
            "change_money": self.changed_money,
            "dt": self.dt.strftime("%Y%m%d"),
            "remark": self.remark
        }
    @property
    def plan(self):
        return self.plan_link.plan

    class Meta:
        ordering = ['dt']


class CashTag(models.Model):
    total = models.FloatField('当前金额', default=0)
    dt = models.DateTimeField('dt')


    class Meta:
        ordering = ('-dt', )