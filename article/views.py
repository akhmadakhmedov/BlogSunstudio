from urllib.parse import quote
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib import messages
from .models import Article, Comment
from .forms import ArticleForm
from django.contrib.auth.decorators import login_required


def articles(request):
    keyword = request.GET.get('keyword')
    if keyword:
        articles = Article.objects.filter(title__contains=keyword)
        return render(request, "articles.html", {"articles":articles})
    articles = Article.objects.all()

    articles = Article.objects.all()
    return render(request, "articles.html", {"articles":articles})

def index(request):
    keyword = request.GET.get('keyword')
    if keyword:
        articles = Article.objects.filter(title__contains=keyword)
        return render(request, "index.html", {"articles":articles})
    articles = Article.objects.all()

    articles = Article.objects.all()
    return render(request, "index.html", {"articles":articles})

def about(request):
    return render(request, 'about.html')

@login_required(login_url="user:login")
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    context = {
        "articles": articles
    }
    return render(request, "dashboard.html", context)

@login_required(login_url="user:login")
def addarticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request,"Ваша статья успешно создана")
        return redirect("article:dashboard")
    return render(request, "addarticle.html", {"form": form})

def detail(request, id):
    article = get_object_or_404(Article, id=id)
    comments = article.comments.all()
    share_string = quote(article.content)
    context = {
        'article': article,
        'comments': comments,
        'share_string': share_string,
    }
    return render(request, "detail.html", context)

@login_required(login_url="user:login")
def updatearticle(request, id):
    article = get_object_or_404(Article, id=id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, "Ваша статья успешно обновлена...")
        return redirect("index")
    return render(request, "update.html", {"form": form})

@login_required(login_url="user:login")
def deletearticle(request, id):
    article = get_object_or_404(Article, id=id)
    article.delete()
    messages.success(request, "Ваша статья успешно удалена...")
    return redirect("article:dashboard")

def addcomment(request, id):
    article = get_object_or_404(Article, id=id)
    if request.method == 'POST':
        comment_author = request.POST.get('comment_author')
        comment_content = request.POST.get('comment_content')
        
        newComment = Comment(comment_author = comment_author, comment_content = comment_content)
        newComment.article = article
        newComment.save()
        return redirect(reverse("article:detail", kwargs = {"id":id}))