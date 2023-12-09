from django.urls import path
from .views import StartingPageView

urlpatterns = [
    path('', StartingPageView.as_view(), name='starting-page'),
    # Buraya başka URL patternleri ekleyebilirsiniz.
]
