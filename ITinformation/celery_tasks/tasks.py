from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
import time
from django.template import loader

from django_redis import get_redis_connection
import os, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ITinformation.settings')

django.setup()
# celery -A celery_tasks.tasks worker -l info

from job.models import JobsType, IndexJobsBanner, \
    IndexPromotionBanner, IndexTypeJobsBanner
# app = Celery('celery_tasks.tasks', broker='redis://10.225.214.38:6379/0 ')
app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/0 ')


@app.task
def send_email(to_email, username, token):
    # 发邮件
    subject = '欢迎注册'
    message = ''
    html_message = '<h1>{0}, 欢迎您成为IT信息港的会员</h1>请点击下面链接激活您的账户<br/>' \
                   '<a href="http://127.0.0.1:8000/user/active/{1}">http://127.0.0.1/user/active/{2}</a>'.format(
        username, token, token)
    from_email = settings.EMAIL_FROM
    receiver = [to_email]
    send_mail(subject, message, from_email, receiver, html_message=html_message)
    time.sleep(5)


@app.task
def generate_static_index():
    types = JobsType.objects.all()

    # 获取轮播图信息
    Jobs_banners = IndexJobsBanner.objects.all().order_by('index')  # -index 倒排

    # 获取畅销信息
    promotion_banners = IndexJobsBanner.objects.all().order_by('index')

    # 获取分类商品信息
    # type_Jobs_banners = IndexJobsBanner.objects.all()
    for type in types:
        # type在首页分类商品的图片
        image_banners = IndexTypeJobsBanner.objects.filter(type=type, display_type=1)
        # type在首页分类商品的文字
        tittle_banners = IndexTypeJobsBanner.objects.filter(type=type, display_type=0)

        # 添加属性
        type.image_banners = image_banners
        type.tittle_banners = tittle_banners

    # 组织上下文
    context = {'types': types,
               'Jobs_banners': Jobs_banners,
               'promotion_banners': promotion_banners,
               # 'type_Jobs_banners':type_Jobs_banners,
               }
    # return render(request, 'index.html', context) httpResponse
    # 加载模板 渲染
    temp = loader.get_template('static_index.html')
    static_index_html = temp.render(context)
    # 生成html静态页面
    save_path = os.path.join(settings.BASE_DIR, 'static/index.html')
    with open(save_path, 'w')as f:
        f.write(static_index_html)
