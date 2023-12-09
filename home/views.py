from django.shortcuts import render
from blog.models import Post  # Blog uygulamanızın Post modelini import edin
from django.views.generic import ListView

class StartingPageView(ListView):
    template_name = "home/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data
        