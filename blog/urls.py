from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('blog/', views.blog, name="blog"),
    path('blog/<int:idArt>/', views.blog_detail, name="blog_detail"),
    path('blog/<int:idArt>/add_command', views.add_comment, name="add_comment"),
    path('like-article/<int:article_id>/', views.like_article, name='like_article'),
    path('dislike-article/<int:article_id>/', views.dislike_article, name='dislike_article'),
    path('myblog/', views.myblog, name="myblog"),
    path('myblog/<str:action>/', views.myblog_article_detail, name="add_article"),
    path('myblog/add/add',views.add_article,name="add_article"),
    path('myblog/<str:action>/<int:idArt>/', views.myblog_article_detail_edit, name="detail_article"),
    path('myblog/edit/<int:idArt>/',views.edit_article,name="edit_article"),
    path('myblog/show/<int:idArt>/',views.show_article,name="show_article"),
    path('myblog/delete/<int:idArt>/',views.delete_article,name="delete_article"),
]