from django.shortcuts import render, redirect, reverse
from django.http.response import JsonResponse
from django.urls.base import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET

from .models import BlogCategory, Blog, BlogComment

from .forms import PubBlogForm
from django.db.models import Q


# Create your views here.
def index(request):
    blogs = Blog.objects.all()
    return render(request, "index.html", context={"blogs": blogs})


def blog_detail(request, blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
    except Exception as e:
        print(e)
    return render(request, "blog_detail.html", context={"blog": blog})


# @login_required(login_url=reverse_lazy("linauth:login"))
# @login_required(login_url="/auth/login")
@require_http_methods(["GET", "POST"])
@login_required()
def pub_blog(request):
    # 如果是Get请求，说明只是访问发布博客
    if request.method == "GET":
        # 查询所有分类
        categories = BlogCategory.objects.all()
        # 把分类传给模版
        return render(request, "pub_blog.html", context={"categories": categories})
    # 如果是post请求，说明是在提交表达
    else:
        form = PubBlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            content = form.cleaned_data.get("content")
            category_id = form.cleaned_data.get("category")
            blog = Blog.objects.create(
                title=title,
                content=content,
                category_id=category_id,
                author=request.user,
            )
            return JsonResponse(
                # 这里给前端返回一个blog.id的目的是为了发生成功之后，跳转的博客详情页
                {"code": 200, "message": "博客发布成功！", "data": {"blog_id": blog.id}}
            )
        else:
            print(form.errors)
            return JsonResponse({"code": 400, "message": "参数错误！"})


@require_POST
@login_required()
def pub_comment(request):
    blog_id = request.POST.get("blog_id")
    content = request.POST.get("content")
    #  author=request.user: 会自动提取user的id
    BlogComment.objects.create(content=content, blog_id=blog_id, author=request.user)
    # 重新加载博客详情页
    # kwargs可以传参：/blog/detail/{blog_id}
    return redirect(reverse("blog:blog_detail", kwargs={"blog_id": blog_id}))


@require_GET
def search(request):
    # /search?q=xxx
    q = request.GET.get("q")
    # 从博客的标题和内容中查找含有q关键字的博客
    blogs = Blog.objects.filter(Q(title__icontains=q) | Q(content__icontains=q)).all()
    return render(request, "index.html", context={"blogs": blogs})
