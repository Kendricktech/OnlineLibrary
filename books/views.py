from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from .forms import SearchForm, BookForm
from .models import Book, Author, Genre, Category
from .utils import increment_visit_count_and_track_user,export_site_data,export_user_data


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = "books/upload-book.html"

    def get_success_url(self):
        return reverse_lazy('books:book_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the current page for pagination
        page = self.request.GET.get('page', 1)
        context['authors_page'] = self.form_class().authors_page
        context['genres_page'] = self.form_class().genres_page
        context['categories_page'] = self.form_class().categories_page
        context['page'] = page
        return context

class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = "books/book-update.html"

    def get_success_url(self):
        return reverse_lazy('books:book_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the page number from the request GET parameters
        page = self.request.GET.get('page', 1)
        
        # Pass the page number to the form to paginate the fields
        context['form'] = self.form_class(self.request.POST or None, instance=self.object, page=page)
        context['authors_page'] = context['form'].authors_page
        context['genres_page'] = context['form'].genres_page
        context['categories_page'] = context['form'].categories_page
        return context
# Delete a book
class BookDeleteView(DeleteView):
    model = Book
    template_name = "books/book-delete.html"
    success_url = reverse_lazy('books:book_list')

# View for displaying details of a single book
class BookDetail(DetailView):
    model = Book
    template_name = 'books/book-detail.html'

    def get_object(self, queryset=None):
        book = super().get_object(queryset)
        if self.request.user.is_authenticated:
            increment_visit_count_and_track_user(book, self.request.user)
        else:
            increment_visit_count_and_track_user(book)
        return book

# List view for all books with search and pagination
class BookList(ListView):
    model = Book
    template_name = 'books/books.html'
    context_object_name = 'books'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query', '')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(categories__name__icontains=query) |
                Q(genres__name__icontains=query) |
                Q(authors__first_name__icontains=query)
            ).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('query', '')
        context['categories'] = Category.objects.all()
        context['genres'] = Genre.objects.all()
        return context


def search_view(request):
    query = request.GET.get('query', '') or request.POST.get('query', '')
    books, authors, genres, categories = [], [], [], []

    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(categories__name__icontains=query) |
            Q(genres__name__icontains=query) |
            Q(authors__first_name__icontains=query)
        ).distinct()

        authors = Author.objects.filter(Q(first_name__icontains=query))
        genres = Genre.objects.filter(Q(name__icontains=query))
        categories = Category.objects.filter(Q(name__icontains=query))

    form = SearchForm(request.GET or None)
    return render(request, 'books/search.html', {
        'form': form,
        'query': query,
        'books': books,
        'authors': authors,
        'genres': genres,
        'categories': categories,
    })

from django.views.generic import DetailView
from django.core.paginator import Paginator
from .models import Author, Book

class AuthorDetail(DetailView):
    model = Author
    template_name = 'books/author-detail.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.get_object()
        
        # Fetch all books by this author
        books_list = author.books.all()

        # Fetch unique genres and categories for the author's books
        genres = set(genre for book in books_list for genre in book.genres.all())
        categories = set(category for book in books_list for category in book.categories.all())

        # Paginate the books list
        paginator = Paginator(books_list, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Add the required data to the context
        context['page_obj'] = page_obj
        context['genres'] = genres
        context['categories'] = categories

        return context
    
    def get_object(self, queryset=None):
        author = super().get_object(queryset)
        if self.request.user.is_authenticated:
            increment_visit_count_and_track_user(author, self.request.user)
        else:
            increment_visit_count_and_track_user(author)
        return author

class GenreDetail(DetailView):
    model = Genre
    template_name = 'books/genre-detail.html'
    context_object_name = 'genre'

    def get_object(self, queryset=None):
        genre = super().get_object(queryset)
        if self.request.user.is_authenticated:
            increment_visit_count_and_track_user(genre, self.request.user)
        else:
            increment_visit_count_and_track_user(genre)
        return genre


class CategoryDetail(DetailView):
    model = Category
    template_name = 'books/category-detail.html'
    context_object_name = 'category'


def library_insights(request):
    visit_data = export_site_data()
    return render(request, 'books/library-insights.html', {'visit_data': visit_data})

def get_object(self, queryset=None):
        category = super().get_object(queryset)
        if self.request.user.is_authenticated:
            increment_visit_count_and_track_user(category, self.request.user)
        else:
            increment_visit_count_and_track_user(category)
        return category


def get_visit_data_json(request):
    visit_data = export_site_data()
    return JsonResponse(visit_data)
