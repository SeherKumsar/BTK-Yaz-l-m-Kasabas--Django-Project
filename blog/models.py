from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.text import slugify

class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return self.caption

# Kullanıcı modülü oluşturulduğu için author admin paneli için kullanıldı.
# class AdminAuthor(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField()

#     def __str__(self):
#         return self.user.username

class Post(models.Model):
    title = models.CharField(max_length=25)
    excerpt = models.CharField(max_length=200, validators=[MinLengthValidator(3)])
    image = models.ImageField(upload_to="posts/", null=True)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True, db_index=True, blank=True, null=True)
    content = RichTextField(validators=[MinLengthValidator(3)])
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="posts")
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if self.title and (not self.slug or self.title != self.slug):
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user_name = models.CharField(max_length=120)
    user_email = models.EmailField()
    text = RichTextField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"