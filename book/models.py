from django.db import models

# Create your models here.
class Author(models.Model):
    full_name = models.CharField(max_length=255)
    def __str__(self):
        return self.full_name

class Publisher(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Book(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True)
    imageUrl = models.URLField()
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255) #
    place_of_printing = models.CharField(max_length=255)
    year_of_printing = models.IntegerField()
    publisher = models.CharField(max_length=255) #
    category = models.CharField(max_length=255) #
    summary = models.CharField(max_length=500)
    created_date = models.DateTimeField(auto_now_add=True, null=True)


class Comment(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, null=True)
    book = models.ForeignKey('book.Book', on_delete=models.CASCADE, null=True, verbose_name="Book", related_name="comments")
    comment = models.CharField(max_length=500)
    created_date = models.DateTimeField(auto_now_add=True)