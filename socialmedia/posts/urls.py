from django.conf.urls import path 

from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostListView.as_view,name='all'),
    path('new/', views.CreatePostView.as_view(), name='create'),
    path('{username}', views.UserPostsView.as_view(), name='for_user'),
    path('{username}/{pk>}/', views.PostDetailView.as_view(), name="single_post"),
    path('delete/<pk>', views.DeletePostView.as_view(), name='delete')

]