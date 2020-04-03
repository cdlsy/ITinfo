"""ITinformation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include

urlpatterns = [
    re_path('admin/', admin.site.urls),
    # re_path('tinymce/', include('tinymce.urls')),  # 富文本编辑器
    # re_path('search/', include('haystack.urls')),  # 全文检索返回三个对象
    #query：搜索关键字
    #page：当前页的page对象 –>遍历page对象，获取到的是SearchResult类的实例对象，对象的属性object才是模型类的对象。

    #paginator：分页paginator对象
    re_path('', include('job.urls', namespace='job')),
    re_path('user/', include('user.urls', namespace='user')),


]
