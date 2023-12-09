from django.urls import path, re_path
from . import views

urlpatterns = [
    path("posts", views.AllPostsView.as_view(), name="posts-page"),
    path("posts/<slug:slug>", views.SinglePostView.as_view(),
         name="post-detail-page"),  # /posts/my-first-post
    path('create/', views.create_post, name='create-post'),
    path("read-later", views.ReadLaterView.as_view(), name="read-later"),
    path('user/posts/', views.UserPostsView.as_view(), name='user-posts'),
    path('user/posts/<slug:slug>/update/', views.PostUpdateView.as_view(), name='post-update'),
    path('user/posts/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post-confirm-delete'),
]