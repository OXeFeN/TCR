from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from .models import Article
from .forms import ArticleForm

def article_list(request):
    articles = Article.objects.order_by('-published_date')
    return render(request, 'articles/article_list.html', {'articles': articles})

@permission_required('articles.can_publish_article', raise_exception=True)  # nahraďte app_name názvem vaší aplikace
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'articles/article_form.html', {'form': form})

