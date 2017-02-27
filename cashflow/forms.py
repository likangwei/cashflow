#coding=utf8
from django import forms

from cashflow.models import CashLoopPlan
from cashflow.models import DaiKuan


class DaiKuanForm(forms.ModelForm):

    class Meta:
        model = DaiKuan
        fields = '__all__'


class CashLoopForm(forms.ModelForm):

    class Meta:
        model = CashLoopPlan
        fields = '__all__'