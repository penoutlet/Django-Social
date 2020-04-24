from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import (LoginRequiredMixin, PermissionRequiredMixin)

from django.urls import reverse_lazy 
from django.views import generic
from django.http import Http404
from braces.views import SelectRelatedMixin

from . import models
from . import forms

from django.contrib.auth import get_user_model
# gets user from a session.
User = get_user_model()

# what is a mixin? still confused
class PostListView(SelectRelatedMixin, generic.ListView):
    model = models.Post
    select_related('user',group)

class UserPostsView(generic.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        queryset = super(CLASS_NAME, self).get_queryset()
        queryset = queryset # TODO
        try:
            self.post.user = User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context['post_user'] == self.post_user

class PostDetailView(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    group = models.Group
    select_related('user', group)
    # get the posts where the username on the post matches exactly the current user.
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

class CreatePostView(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    fields = ('message','group') #people can edit the message or the group
    model = models.Post

    def form_valid(self,form):
        self.object = form.save(commit=False) #connects user to the post
        self.object.user = self.request.user
        self.object.save
        return super().form_valid(form)

class DeletePostView(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):

    model = models.Post
    select_related('user',group)
    success_url = reverse_lazy('posts:all') #redirects to all posts on success

    def get_queryset(self):
        queryset = super().get_queryset();
        return queryset.filter(user_id = self.request.user.id)
    
    def delete(self, *args, **kwargs):
        messages.success(self.request, 'Post Deleted Baby!')
        return super().delete(*args, **kwargs)