from django.conf.urls import url
from user import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path, path, include
from django.contrib import admin
from django.urls import path, include
from user.views import RegisterView, ActiveView, \
    LoginView, AddressView, \
    UserInfoView, LogoutView,UserOiderView

# from django.contrib.auth.decorators import

app_name = 'user'
urlpatterns = [
    # path('register', views.register, name='register'),  # 注册
    # path('register_handle', views.register_handle, name='register_handle'),

    # path('show-<int:sid>.html', views.show, name='show'),#内容页
    path('register', RegisterView.as_view(), name='register'),  # 类视图.as_view()  注册
    re_path('active/(?P<token>.*)', ActiveView.as_view(), name='active'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

    re_path('order/(?P<page>\d+)', UserOiderView.as_view(), name='order'),
    path('info', AddressView.as_view(), name='info'),
    path('', UserInfoView.as_view(), name='user'),  # 用户信息页面

]
