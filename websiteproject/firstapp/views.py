from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy

from .models import *
from .forms import *

class HomeNews(ListView):
    model = News
    #extra_context = {'title': 'Самые последние Новости'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published = True)


class CategoryViewNews(ListView):
    model = News
    template_name = 'firstapp/home_news_category.html'
    context_object_name = 'news'
    #extra_context = {'title': 'Заголовок категории'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk = self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return News.objects.filter(category_id = self.kwargs['category_id'],is_published=True)

class ViewNews(DetailView):
    model = News
    #pk_url_kwarg = 'news_id'
    context_object_name = 'news_item'
    template_name = 'firstapp/view_detail_news.html'

class CreateNews(CreateView):
    form_class = NewsForm
    model = News
    template_name = 'firstapp/news_adding.html'
    success_url = reverse_lazy('home')


def hello(request):
    text= """<h1>Welcome to Kyrgyzstan!</h1>"""

    return HttpResponse(text)

# def index(request):
#     allNews = News.objects.order_by('-created_at')
#     content = {'newsAll': allNews,
#                'titleInHtml':'Список всех новостей'
#                }
#
#     return render(request,template_name="firstapp/index.html",context=content)

# def get_category(request,category_id):
#     news = News.objects.filter(category=category_id)
#     category = Category.objects.get(pk = category_id)
#     content = {'news': news,
#                'category': category
#                }
#     return render(request, "firstapp/category.html", content)

def about(request):
    title = 'Страница о Нас! Рад вас приветствовать!'
    content = {
        'title': title,
    }
    return render(request, template_name="firstapp/about.html", context=content)

def contactus(request):
    return HttpResponse("<h2>Страница для связи с нами</h2>")

# def view_news(request, news_id):
#     # try:
#     #     news_item = News.objects.get(pk = news_id)
#     # except News.DoesNotExist:
#     #     raise Http404(" Такой новости не существует!")
#
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, "firstapp/view_news.html", {'news_item': news_item})

# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#
#         if form.is_valid():
#             #print(form.cleaned_data)
#             # title = form.cleaned_data['title']
#             # content = form.cleaned_data['content']
#             News.objects.create(**form.cleaned_data)
#             return redirect('home')
#
#     else:
#         form = NewsForm()
#
#     return render(request, 'firstapp/add_news.html', {"form": form})