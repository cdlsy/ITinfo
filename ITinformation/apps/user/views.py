from user.models import User, Address
from job.models import JobsSKU
from order.models import OrderInfo, OrderJobs
# 分页
from django.core.paginator import Paginator
import re
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
# 加密info={'confirm':1}
# serializer=Serializer('key',300)
# res=serializer.dumps(info)
# 解密serializer.loads(res)
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings
from itsdangerous import SignatureExpired  # 异常
from django.http import HttpResponse
from django.core.mail import send_mail
from celery_tasks.tasks import send_email
from django.contrib.auth import authenticate, login, logout
from utils.mixin import LoginRequiredMixin
from django_redis import get_redis_connection


# Create your views here.


# 修改register.html页面action
# 注册页面显示
# def register(request):


# 注册页面管理
# def register_handl
# e(request):

# 注册
class RegisterView(View):
    def get(self, request):
        return render(request, 'signup.html')

    def post(self, request):
        first_name = request.POST.get('s1')
        last_name = request.POST.get('s2')
        username=str(first_name)+str(last_name)
        password = request.POST.get('pwd')
        cpassword = request.POST.get('cpwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        print(username,password,cpassword,email,allow)
        # 数据校验
        # 用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None

        # 协议是否同意了
        # if len(username) > 20 or len(username) < 5:
        #     return render(request, 'singnup.html', {'errmsg': 'user输入有误'})

        if user:
            return render(request, 'signup.html', {'errmsg': '用户名 {}已经存在'.format(username)})
        if len(password) < 8 or len(password) > 20:
            return render(request, 'signup.html', {'errmsg': '密码需为8到29位'})

        if cpassword != password :
            return render(request, 'signup.html', {'errmsg': '两次密码输入不一样'})
        if allow != 'on':
            return render(request, 'signup.html', {'errmsg': '请同意协议'})
        # if not all([username, password, email]):
        #     return render(request, 'signup.html', {'errmsg': '数据不完整'})  # errmsg 传到前端页面
        # 邮箱验证
        # if not re.match(r"^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$", email):
        #     return render(request, 'signup.html', {'errmsg': '邮箱不正确'})

        # 业务处理：注册
        #
        # user=User()
        # user.username=username
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()
        # 邮箱验证码 激活
        # user加密 解密 生成token
        serializer = Serializer(settings.SECRET_KEY, 60)  # key timeout
        info = {'confirm': user.id}
        token = serializer.dumps(info)  # bytes
        token = token.decode()

        # #发邮件
        send_email.delay(email, username, token)
        # subject='欢迎注册'
        # message=''
        # html_message='<h1>{0}, 欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的账户<br/>' \
        #         '<a href="http://127.0.0.1:8000/user/active/{1}">http://127.0.0.1/user/active/{2}</a>'.format(username, token, token)
        # from_email=settings.EMAIL_FROM
        # receiver=[email]
        # send_mail(subject,message,from_email,receiver,html_message=html_message)

        # 返回应答
        return redirect(reverse('job:index'))


# 邮件验证
class ActiveView(View):

    def get(self, requsert, token):
        serializer = Serializer(settings.SECRET_KEY, 180)
        try:
            token = token.encode()
            info = serializer.loads(token)
            # 获取user.id
            user_id = info['confirm']
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            return HttpResponse('激活连接已过期')


# 登陆
class LoginView(View):
    """登录"""

    def get(self, request):
        """显示登录页面"""
        # 判断是否记住了用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''
        # 使用模板
        context = {
            'username': username,
            'checked': checked,

        }
        print(checked)
        return render(request, 'login.html', context)

    def post(self, request):
        # 接受
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        # 校验

        # 业务处理
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            if user.is_active:
                # 记录用户登陆状态
                login(request, user)
                # 在user直接登陆 跳转到用户中心
                next_url = request.GET.get('next', reverse('job:index'))
                # 跳转到首页
                response = redirect(next_url)
                remember = request.POST.get('remember')
                if remember == 'on':
                    # 记住用户名
                    response.set_cookie('username', username, max_age=7 * 24 * 3600)  # 记录一周
                else:
                    # 删除用户名
                    response.delete_cookie('username')
                return response

                return redirect(reverse('job:index'))
            else:

                # 用户未激活
                return render(request, 'login.html', {'errmsg': '账户未激活'})
        else:
            # 用户名密码错误
            return render(request, 'login.html', {'errmsg': '用户名或密码错误'})

        # 应答


class LogoutView(View):
    def get(self, request):
        # clean session
        logout(request)
        return redirect(reverse('job:index'))


# /user
class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        # requesr 添加user属性
        # is_authenticated判断是否登陆
        # no user->django的
        # yes-> User

        # 获取用户个人信息,历史浏览记录

        user = request.user
        info = Address.objects.get_default_address(user)
        con = get_redis_connection('default')
        history_key = 'history_%d' % user.id
        # 最新的五个浏览记录 从list左边插入
        sku_ids = con.lrange(history_key, 0, 4)
        # 从mysql数据库中查redis存储的商品id的goods
        # GoodsSPU.objects.filter(id_in=sku_ids)
        goods_li = []
        for id in sku_ids:
            job = JobsSKU.objects.get(id=id)
            goods_li.append(job)

        # 组织上下文
        context = {'page': 'user',
                   'info':info,
                   'goods_li': goods_li}
        return render(request, 'user_center_info.html', context)


# user/order
class UserOiderView(LoginRequiredMixin, View):
    def get(self, request, page):
        # 获取用户订单信息
        user = request.user
        orders = OrderInfo.objects.filter(user=user).order_by('-create_time')

        for order in orders:
            order_skus = OrderJobs.objects.filter(order_id=order.order_id)

            for order_sku in order_skus:
                amount = order_sku.count * order_sku.price
                order_sku.amount = amount

            #使用字典 加载状态
            order.status_name=OrderInfo.ORDER_STATUS[str(order.order_status)]
            order.order_skus = order_skus
        # 分页 每页5个
        paginator = Paginator(orders, 5)
        # page内容
        try:
            page = int(page)
        except Exception as e:
            page = 1

        if page > paginator.num_pages:
            page = 1

        order_page = paginator.page(page)

        # todo: 进行页码控制， 页面上最多显示5个页面
        num_pages = paginator.num_pages
        if num_pages < 5:
            pages = range(1, num_pages + 1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages - page <= 2:
            pages = range(num_pages - 4, num_pages + 1)
        else:
            pages = range(page - 2, page + 3)

        contex = {'order_page': order_page,
                  'pages': pages,
                  'page': 'order'}
        return render(request, 'user_center_order.html', contex)


# user/address
class AddressView(LoginRequiredMixin, View):
    def get(self, request):
        # 获取用户地址信息
        user = request.user
        # try:
        #     #默认的models.Manager
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        #     address = None
        info = Address.objects.get_default_address(user)
        print(333)
        print(info,info.education)

        return render(request, 'user_center_site.html', {'page': 'info', 'info': info})

    def post(self, request):
        age = request.POST.get('age')
        school = request.POST.get('school')
        education = request.POST.get('education')
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')
        print(education)

        if not all([receiver, age, phone,zip_code]):
            return render(request, 'user_center_site.html', {'errmsg': '数据不完整'})
        if not re.match(r'1[3|4|5|7|8][0-9]{9}$', phone):
            return render(request, 'user_center_site.html', {'errmsg': '手机格式不正确'})
        if zip_code:
            if not re.match(r"^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$", zip_code):
                return render(request, 'user_center_site.html', {'errmsg': '邮箱格式不正确'})
            else:
                return render(request, 'user_center_site.html', {'errmsg': '提交成功'})

        user = request.user
        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist:
        #     address = None
        info = Address.objects.get_default_address(user)
        if info:
            is_default = False
        else:
            is_default = True
        Address.objects.create(user=user,
                               school=school,
                               age=age,
                               education=education,
                               receiver=receiver,
                               addr=addr,
                               zip_code=zip_code,
                               phone=phone,
                               is_default=is_default)
        return redirect(reverse('user:info'))
