from django.db import models

class CarouselItem(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="carousel_images/")
    link = models.URLField()

    def __str__(self):
        return self.title