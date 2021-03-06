from django.conf.urls import include, url
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^$', views.plan_list, name="plan_list"),
    url(r'^cash_details/$', views.cash_details, name="cash_details"),
    url(r'^cash_change_per_month/$', views.cash_change_per_month, name="cash_change_per_month"),
    url(r'^daikuan/(?P<id>\d+)$', views.get_daikuan_detail, name="daikuan_detail"),
    url(r'^loop_plan/(?P<id>\d+)$', views.get_loop_plan_detail, name="loop_plan_detail"),
]