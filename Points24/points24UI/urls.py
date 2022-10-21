# @Author :QinHsiu
# @Email :QinHsiu@163.com
from . import views
from django.urls import path

urlpatterns=[
    path('',views.index,name="index"),
]
