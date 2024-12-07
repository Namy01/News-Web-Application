from django.shortcuts import render
from blog_app.models import Post
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# def post_list(request):
#     posts = Post.objects.all()
#     return render(
#         request,
#         "post_list.html",
#         {"posts" : posts},

#     )
# def view_more(request, id):
#     post = Post.objects.get(id=id)
#     title = post.title 
#     author = post.author 
#     content = post.content
#     Published_at = post.Published_at
#     return render(
#         request,
#         "view_more.html",
#         { 
#          "post": post, 
#          "title": title, 
#          "author": author, 
#          "content": content,
#          "published_at":Published_at,
#         })
def post_list(request):
    posts = Post.objects.filter(Published_at__isnull = False).order_by("-Published_at")
    return render(
        request,
        "post_list.html",
        {"posts": posts},
    )
def view_more(request, id):
    post = Post.objects.get(id=id, Published_at__isnull = False)
    return render(
        request,
        "view_more.html",
        {"post": post},
    )
def draft_list(request):
    posts = Post.objects.filter(Published_at__isnull = True).order_by("-Published_at")
    return render(
        request,
        "draft_list.html",
        {"posts": posts},
    )
def draft_detail(request, id):
    post = Post.objects.get(id=id, Published_at__isnull = True)
    return render(
        request,
        "draft_detail.html",
        {"post": post},
    )
def delete(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    return HttpResponseRedirect("/")

def edit(request, id):
    if request.method == "GET":
        post = Post.objects.get(id=id)
        return render (
            request,
            "edit.html",
            {"post" : post},
        )
    else:
        post = Post.objects.get(id=id)
        post.title = request.POST["title"]
        post.content = request.POST["content"]
        post.author.user = request.POST["author"]
        post.save()
        return HttpResponseRedirect("/")

def post_publish(request, pk):
    post = Post.objects.get(pk=pk , Published_at__isnull = True )
    post.Published_at = timezone.now()
    post.save()
    return redirect("post-list")

from blog_app.forms import PostForm
@login_required
def post_create(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("draft-detail", id=post.id)
        
    return render(
        request,
        "post_create.html",
        {"form": form},
    )