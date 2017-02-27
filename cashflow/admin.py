#coding=utf8
from django.contrib import admin
from cashflow.models import Plan
from cashflow.models import CashChange
from cashflow.models import DaiKuan
from cashflow.models import CashLoopPlan
admin.autodiscover()


def build_cashflow(modeladmin, request, queryset):
    """
    启动conn有效
    """
    for p in queryset.all():
        p.build_future()


class PlanAdmin(admin.ModelAdmin):

    list_filter = ['type']
    actions = [build_cashflow]
    list_display = ('name', 'type')

    fieldsets = (
        (None, {
            'fields': ('name', 'is_cron_plan', 'start_date', 'end_date', 'content')
        }),
        ('loop', {
            'classes': ('collapse',),
            'fields': ('cron', 'cash_per_time'),
        }),
        ('daikuan', {
            'classes': ('collapse',),
            'fields': ('daikuan_total', 'cron', 'daikuan_shoufu', 'daikuan_nianlilv', 'daikuan_yihuan',
                       'daikuan_years', 'daikuan_months', 'daikuan_type'),
        }),
    )


class CashAdmin(admin.ModelAdmin):
    def time_seconds(self, obj):
        return obj.dt.strftime("%Y-%m-%d %H:%M:%S")
    time_seconds.short_name = 'dt'
    time_seconds.empty_value_display = '???'
    time_seconds.admin_order_field = 'dt'
    list_filter = []
    actions = [build_cashflow]
    list_display = ('changed_money', 'time_seconds', 'remark')


admin.site.register(DaiKuan)
admin.site.register(CashLoopPlan)
admin.site.register(CashChange, CashAdmin)