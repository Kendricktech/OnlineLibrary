from django.shortcuts import render,HttpResponse
from django.contrib.auth.decorators import login_required
from books.models import Book, Genre, Category, Author, BookVisit, AuthorVisit, GenreVisit, CategoryVisit
from books.utils import export_user_data,export_site_data,increment_visit_count_and_track_user
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.generic import TemplateView
from books.models import Category, Genre  # Ensure these models are imported correctly
from django.core.paginator import Paginator
from django.db.models import Sum

class Index(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Fetch all categories and genres
        categories = Category.objects.all().order_by('name')
        genres = Genre.objects.all().order_by('name')

        # Get selected category and genre from the request
        selected_category_name = self.request.GET.get('category', None)
        selected_genre_name = self.request.GET.get('genre', None)

        # Determine the selected category and genre, default to most visited if not specified
        if user.is_authenticated:
            if not selected_category_name:
                selected_category = (
                    CategoryVisit.objects.filter(user=user)
                    .order_by('-visit_count')
                    .first()
                )
                selected_category_name = selected_category.category.name if selected_category else None

            if not selected_genre_name:
                selected_genre = (
                    GenreVisit.objects.filter(user=user)
                    .order_by('-visit_count')
                    .first()
                )
                selected_genre_name = selected_genre.genre.name if selected_genre else None
        else:
            # Use sitewide visit data for unauthenticated users
            if not selected_category_name:
                most_visited_category = (
                    CategoryVisit.objects.values('category__name')
                    .annotate(total_visits=Sum('visit_count'))
                    .order_by('-total_visits')
                    .first()
                )
                selected_category_name = most_visited_category['category__name'] if most_visited_category else None

            if not selected_genre_name:
                most_visited_genre = (
                    GenreVisit.objects.values('genre__name')
                    .annotate(total_visits=Sum('visit_count'))
                    .order_by('-total_visits')
                    .first()
                )
                selected_genre_name = most_visited_genre['genre__name'] if most_visited_genre else None

        # Get the selected category and genre instances
        selected_category = Category.objects.filter(name=selected_category_name).first()
        selected_genre = Genre.objects.filter(name=selected_genre_name).first()

        # Filter books by the selected category and genre
        category_books = Book.objects.filter(categories__name=selected_category_name) if selected_category_name else Book.objects.none()
        genre_books = Book.objects.filter(genres__name=selected_genre_name) if selected_genre_name else Book.objects.none()

        # Pagination logic
        category_page = self.request.GET.get('category_page', 1)
        genre_page = self.request.GET.get('genre_page', 1)

        category_paginator = Paginator(category_books, 8)  # Show 8 books per page
        genre_paginator = Paginator(genre_books, 8)  # Show 8 books per page

        category_books_page = category_paginator.get_page(category_page)
        genre_books_page = genre_paginator.get_page(genre_page)

        # Update context with paginated books
        context.update({
            'categories': categories,
            'genres': genres,
            'category_books': category_books_page,
            'genre_books': genre_books_page,
            'selected_category': selected_category_name,
            'selected_genre': selected_genre_name,
        })
        return context


from django.shortcuts import render
from django.shortcuts import render
from books.utils import export_user_data, export_site_data

class DashboardView(TemplateView):
    template_name = 'core/dashboard.html'
    model=Book



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Fetch the necessary data, limiting to top 10 most visited
        books = Book.objects.all()[:10]
        authors = Author.objects.all()[:10]
        categories = Category.objects.all()[:10]
        genres = Genre.objects.all()[:10]

        # Fetch site and personal insights
        site_insights = export_site_data()
        personal_insights = export_user_data(self.request.user)

        # Fetch site visit data and limit to top 10 by visit_count
        book_visits_data = BookVisit.objects.values('book', 'visit_count').order_by('-visit_count')[:10]
        author_visits_data = AuthorVisit.objects.values('author', 'visit_count').order_by('-visit_count')[:10]
        genre_visits_data = GenreVisit.objects.values('genre', 'visit_count').order_by('-visit_count')[:10]
        category_visits_data = CategoryVisit.objects.values('category', 'visit_count').order_by('-visit_count')[:10]

        # Prepare data to pass into the template for Site Insights
        site_book_visits = [visit['visit_count'] for visit in book_visits_data]
        site_author_visits = [visit['visit_count'] for visit in author_visits_data]
        site_genre_visits = [visit['visit_count'] for visit in genre_visits_data]
        site_category_visits = [visit['visit_count'] for visit in category_visits_data]

        # Prepare data to pass into the template for User Insights (limit to top 10)
        user_book_visits = [visit['visit_count'] for visit in personal_insights.get('bookvisit', [])[:5]]
        user_author_visits = [visit['visit_count'] for visit in personal_insights.get('authorvisit', [])[:5]]
        user_genre_visits = [visit['visit_count'] for visit in personal_insights.get('genrevisit', [])[:5]]
        user_category_visits = [visit['visit_count'] for visit in personal_insights.get('categoryvisit', [])[:5]]

        # Prepare labels for each chart (books, authors, genres, categories)
        book_labels = [book.title for book in books]
        author_labels = [author.first_name for author in authors]
        genre_labels = [genre.name for genre in genres]
        category_labels = [category.name for category in categories]

        # Pass the data into the template context
        context.update({
            'site_book_visits': site_book_visits,
            'site_author_visits': site_author_visits,
            'site_genre_visits': site_genre_visits,
            'site_category_visits': site_category_visits,
            'user_book_visits': user_book_visits,
            'user_author_visits': user_author_visits,
            'user_genre_visits': user_genre_visits,
            'user_category_visits': user_category_visits,
            'book_labels': book_labels,
            'author_labels': author_labels,
            'genre_labels': genre_labels,
            'category_labels': category_labels,
            'site_insights': site_insights,
            'personal_insights': personal_insights,
        })

        return context

