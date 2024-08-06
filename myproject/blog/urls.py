from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/new/', views.create_post, name='create_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:pk>/like/', views.like_dislike_post, {'is_like': True}, name='like_post'),
    path('post/<int:pk>/dislike/', views.like_dislike_post, {'is_like': False}, name='dislike_post'),
    path('post/<int:pk>/edit/', views.update_post, name='update_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('category/<slug:category_slug>/', views.category_posts, name='category_posts'),
]
