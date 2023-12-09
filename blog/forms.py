from django import forms
from .models import Comment, Post
from ckeditor.fields import RichTextField
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ["post"]
        labels = {
          "user_name": "Your Name",
          "user_email": "Your Email",
          "text": "Your Comment"
        }

# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = ['title', 'excerpt', 'image', 'content', 'tags']
#         labels = {
#           'title': 'Title',
#           'excerpt': 'Excerpt',
#           'image': 'Image',
#           'content': 'Content',
#           'tags': 'Tags'
#         }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'excerpt', 'image', 'content', 'tags']
        labels = {
            'title': 'Başlık',
            'excerpt': 'Kısa Alıntı',
            'image': 'Resim',
            'content': 'İçerik',
            'tags': 'Etiketler',
        }
        widgets = {
            'title': forms.TextInput(attrs={'required': True}),
            'excerpt': forms.TextInput(attrs={'required': True}),
            'image': forms.FileInput(attrs={'required': True}),
            'tags': forms.SelectMultiple(attrs={'required': True}),
        }
        error_messages = {
            'title': {'required': 'Başlık alanı zorunludur.'},
            'excerpt': {'required': 'Kısa alıntı alanı zorunludur.'},
            'image': {'required': 'Resim alanı zorunludur.'},
            'content': {'required': 'İçerik alanı zorunludur.'},
            'tags': {'required': 'En az bir etiket seçmelisiniz.'},
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = True
        self.fields['excerpt'].required = True
        self.fields['image'].required = True
        self.fields['content'].required = True
        self.fields['tags'].required = True