from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404

from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .utils import MyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from  django.contrib.auth import login, logout
from django.core.mail import send_mail

from .models import *
from .forms import *


def register(request):
    if request.method =='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('login')
        else:
            messages.error(request, 'Ошибка регистрации%%!')
    else:
        form = UserRegisterForm()

    return render(request, 'firstapp/register.html', {"form":form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data = request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'firstapp/login.html', {"form":form})

def user_logout(request):
    logout(request)
    return redirect('login')

def test(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'],
                      'djangobekov2022@gmail.com',['aman.arykbaev@gmail.com'], fail_silently = False )

            if mail:
                messages.success(request, 'Письмо отправлено!')
            else:
                messages.error(request, 'Ошибка отправки почты!')

        else:
            messages.error(request, 'Ошибка Catpch-и!')
    else:
        form = ContactForm()

    return render(request, 'firstapp/test.html',{"form":form})

class HomeNews(MyMixin, ListView):
    model = News
    template_name = 'firstapp/home_news_list.html'
    context_object_name = 'newsAll'
    mixin_prop = 'hello world'
    paginate_by = 2
    #extra_context = {'title': 'Самые последние Новости'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    def get_queryset(self):
        return News.objects.filter(is_published = True).select_related('category')


class CategoryViewNews(MyMixin, ListView):
    model = News

    template_name = 'firstapp/home_news_category.html'
    context_object_name = 'news'
    #extra_context = {'title': 'Заголовок категории'}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(Category.objects.get(pk = self.kwargs['category_id']))
        return context

    def get_queryset(self):
        return News.objects.filter(category_id = self.kwargs['category_id'],is_published=True)

class ViewNews(MyMixin, DetailView):
    model = News
    #pk_url_kwarg = 'news_id'
    context_object_name = 'news_item'
    template_name = 'firstapp/view_detail_news.html'

class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    model = News
    template_name = 'firstapp/news_adding.html'
    success_url = reverse_lazy('home')
    #login_url = '/admin/'
    raise_exception =  True


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