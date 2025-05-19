from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
import string
import random
from django.core.mail import send_mail

from .models import CaptchaModel
from django.views.decorators.http import require_http_methods

from .forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.models import User


# User = get_user_model() # 不推荐


@require_http_methods(["GET", "POST"])
def linlogin(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            remember = form.cleaned_data.get("remember")
            User = get_user_model()
            user = User.objects.filter(email=email).first()
            # 验证用户输入的明文密码（password）是否与数据库中存储的加密密码匹配。
            # 返回值是一个布尔值（True 或 False）
            if user and user.check_password(password):
                # 登录
                login(request, user)
                # 判断是否需要记住我:remember=0 为false 其他值为true
                if not remember:
                    # 如果没有点击记住我，那么就要设置过期时间为0，即浏览器关闭后就会过期
                    request.session.set_expiry(0)
                # 如果点击了，那么就什么都不做，使用默认的2周的过期时间
                return redirect("/")
            else:
                print("邮箱或密码错误！")
                # form.add_error('email', '邮箱或者密码错误！')
                # return render(request, 'login.html', context={"form": form})
                return redirect(reverse("linauth:login"))


def linlogout(request):
    # 调用退出登录功能
    logout(request)
    # 重定向到首页
    return redirect("/")


@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    else:
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            User = get_user_model()
            # 存入password是密文，是Django的auth模块底层设置的
            User.objects.create_user(email=email, username=username, password=password)
            # 从定向到登录页面
            return redirect(reverse("linauth:login"))
        else:
            print(form.errors)
            # 重新跳转到登录页面
            return redirect(reverse("linauth:register"))
            # return render(request, "register.html", context={"form": form})


def send_email_captcha(request):
    # ?email=xxx
    email = request.GET.get("email")
    if not email:
        return JsonResponse({"code": 400, "message": "必须传递邮箱！"})
    # 生成验证码（取随机的4位阿拉伯数字）
    # ['0', '2', '9', '8']
    captcha = "".join(random.sample(string.digits, 4))
    # 存储到数据库中
    """
    email=email: 数据库中查找 email 字段等于变量 email 值的记录
    defaults={"captcha": captcha}: 指定要创建或更新的字段值
        - 如果找到匹配记录：更新该记录的 captcha 字段值为变量 captcha 的值
        - 如果没找到：创建新记录，设置 email 和 captcha 字段的值
    """
    CaptchaModel.objects.update_or_create(email=email, defaults={"captcha": captcha})
    send_mail(
        # subject（邮件主题）
        "LinNote注册验证码",
        # message（邮件正文）
        message=f"您的注册验证码是：{captcha}",
        #  recipient_list（收件人列表）
        # recipient_list=["user1@example.com", "user2@example.com"]  # 群发
        recipient_list=[email],
        # from_email（发件人地址），若为 None，则使用 settings.DEFAULT_FROM_EMAIL
        from_email=None,
    )
    return JsonResponse({"code": 200, "message": "邮箱验证码发送成功！"})
