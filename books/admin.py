from django.contrib import admin
from .models import Book,Genre,Category,Author,AuthorVisit,BookVisit,CategoryVisit,GenreVisit
# Register your models here.
admin.site.register(Book)
admin.site.register(BookVisit)

admin.site.register(Author)
admin.site.register(AuthorVisit)


admin.site.register(Genre)
admin.site.register(GenreVisit)

admin.site.register(Category)
admin.site.register(CategoryVisit)


