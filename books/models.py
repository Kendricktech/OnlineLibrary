from django.db import models
from django.conf import settings
import os

def get_default_book_cover():
    return os.path.join('uploads', 'books', 'images', 'default.png')

def get_default_author_image():
    return os.path.join('uploads', 'users', 'images', 'default.png')

class Book(models.Model):
    title = models.CharField(max_length=255)
    visit_count = models.PositiveBigIntegerField(default=0)
    authors = models.ManyToManyField('Author', related_name='books')
    genres = models.ManyToManyField('Genre', related_name='books')
    categories = models.ManyToManyField('Category', related_name='books')
    cover_image = models.ImageField(
        blank=True,
        null=True,
        default=get_default_book_cover
    )
    # Define related fields for cascading visit counts
    related_fields = ['authors', 'genres', 'categories']

    def __str__(self):
        return self.title


class Author(models.Model):
    image = models.ImageField(
        blank=True,
        null=True,
        default=get_default_author_image
    )
    first_name = models.CharField(max_length=255)
    visit_count = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.first_name


class Genre(models.Model):
    name = models.CharField(max_length=255)
    visit_count = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    visit_count = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return self.name
    
class BookVisit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    visited_on = models.DateTimeField(auto_now_add=True)
    visit_count = models.PositiveBigIntegerField(default=0)

    class Meta:
        # Ensuring uniqueness of visits for each user-book pair
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} visited {self.book.title}"


class AuthorVisit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    visited_on = models.DateTimeField(auto_now_add=True)
    visit_count = models.PositiveBigIntegerField(default=0)

    class Meta:
        # Ensuring uniqueness of visits for each user-author pair
        unique_together = ('user', 'author')

    def __str__(self):
        return f"{self.user.username} visited {self.author.first_name}"


class GenreVisit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    visited_on = models.DateTimeField(auto_now_add=True)
    visit_count = models.PositiveBigIntegerField(default=0)

    class Meta:
        # Ensuring uniqueness of visits for each user-genre pair
        unique_together = ('user', 'genre')

    def __str__(self):
        return f"{self.user.username} visited {self.genre.name}"


class CategoryVisit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    visited_on = models.DateTimeField(auto_now_add=True)
    visit_count = models.PositiveBigIntegerField(default=0)

    class Meta:
        # Ensuring uniqueness of visits for each user-category pair
        unique_together = ('user', 'category')

    def __str__(self):
        return f"{self.user.username} visited {self.category.name}"
