# books/forms.py
from django import forms
from .models import Book
class SearchForm(forms.Form):
    query = forms.CharField(max_length=255, required=False, label="Search")



from django import forms
from django.core.paginator import Paginator
from .models import Book, Author, Genre, Category
from django import forms
from django.core.paginator import Paginator
from .models import Book, Author, Genre, Category

class BookForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Book
        fields = ['title', 'authors', 'genres', 'categories', 'cover_image']

    def __init__(self, *args, **kwargs):
        page = kwargs.pop('page', 1)
        super().__init__(*args, **kwargs)

        # Paginate authors, genres, and categories
        paginator = Paginator(Author.objects.all(), 10)  # Paginate authors (10 per page)
        authors_page = paginator.get_page(page)
        self.fields['authors'].queryset = authors_page.object_list
        self.authors_page = authors_page  # Save the page object for template

        paginator = Paginator(Genre.objects.all(), 10)  # Paginate genres (10 per page)
        genres_page = paginator.get_page(page)
        self.fields['genres'].queryset = genres_page.object_list
        self.genres_page = genres_page  # Save the page object for template

        paginator = Paginator(Category.objects.all(), 10)  # Paginate categories (10 per page)
        categories_page = paginator.get_page(page)
        self.fields['categories'].queryset = categories_page.object_list
        self.categories_page = categories_page  # Save the page object for template
        