from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Post
from .forms import CommentForm, PostForm
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data
    

@login_required(login_url='/user/login/')
def create_post(request):
    post_form = PostForm(request.POST, request.FILES)

    if post_form.is_valid():
        new_post = post_form.save(commit=False)
        new_post.author = request.user

        if post_form.cleaned_data.get('title') and not new_post.slug:
            new_post.slug = slugify(post_form.cleaned_data['title'])

        new_post.save()

        return redirect("post-detail-page", slug=new_post.slug)
    else:
        context = {
            "post_form": post_form,
        }
        return render(request, "blog/create_post.html", context)

@login_required(login_url='/user/login/')
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user == post.author:
        post.delete()
    return redirect("user-posts")

@login_required(login_url='/user/login/')
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.user == post.author:
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.slug = slugify(form.cleaned_data['title'])
                post.save()
                return redirect('post-detail-page', slug=post.slug)
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/edit_post.html', {'form': form})
    else:
        return redirect("post-detail-page", slug=slug)

class UserPostsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user-posts.html'
    context_object_name = 'user_posts'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-date')

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_update.html'

    def get_success_url(self):
        return reverse_lazy('post-detail-page', kwargs={'slug': self.object.slug})

    def form_valid(self, form):
        # Get the current post being updated
        current_post = form.save(commit=False)

        # Check if the title has changed
        if form.cleaned_data['title'] != current_post.title:
            # Update the title and slug for the current post
            current_post.title = form.cleaned_data['title']
            current_post.slug = slugify(form.cleaned_data['title'])
            current_post.save()

            # Find all related posts with the same title and update their titles and slugs
            related_posts = Post.objects.filter(title=current_post.title)
            for post in related_posts:
                post.title = current_post.title
                post.slug = current_post.slug
                post.save()

        return super().form_valid(form)

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/post-confirm-delete.html'
    success_url = reverse_lazy('user-posts')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(slug=self.kwargs['slug'])
    
    def delete(self, request, *args, **kwargs):
        current_post = self.get_object()
        related_posts = Post.objects.filter(title=current_post.title)
        related_posts.delete()
        return super().delete(request, *args, **kwargs)

class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"


class SinglePostView(View):
    # template_name = "blog/post-detail.html"
    # model = Post

    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
          is_saved_for_later = post_id in stored_posts
        else:
          is_saved_for_later = False

        return is_saved_for_later

    
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        
        context = {
          "post": post,
          "post_tags": post.tags.all(),
          "comment_form": CommentForm(),
          "comments": post.comments.all().order_by("-id"),
          # "saved_for_later": is_saved_for_later
          "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
          comment = comment_form.save(commit=False)
          comment.post = post
          comment.save()
          
          return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
        
        context = {
          "post": post,
          "post_tags": post.tags.all(),
          "comment_form": comment_form,
          "comments": post.comments.all().order_by("-id"),
          "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)

# @login_required(login_url='/user/login/') 
class ReadLaterView(View):
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/stored-posts.html", context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts
        return HttpResponseRedirect(reverse("starting-page"))  # Burada doğru sayfaya yönlendirme yapmalısınız.