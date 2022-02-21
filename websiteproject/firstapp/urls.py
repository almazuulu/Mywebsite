from django.urls import path
from .views import *

#www.address.com/news/
urlpatterns = [
    #path('',index, name = 'home'),
    path('register/', register, name = 'register'),
    path('login/', user_login, name = 'login'),
    path('logout/', user_logout, name='logout'),
    path('test/', test, name = 'test'),
    path('',HomeNews.as_view(), name = 'home'),
    path('about/', about, name = 'about'),
    path('contactus/', contactus, name = 'contact'),
    #path('category/<int:category_id>',get_category, name = 'category'),
    path('category/<int:category_id>',CategoryViewNews.as_view(extra_context = {'title': 'Заголовок категории'}), name = 'category'),
    path('view_news/<int:pk>',ViewNews.as_view(), name = 'view_news'),
    #path('view_news/<int:news_id>',view_news, name = 'view_news'),
    #path('view_news/add-news',add_news, name = 'add_news')
    path('view_news/add-news',CreateNews.as_view(), name = 'add_news')
]

