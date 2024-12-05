from django.urls import path
from . import views


app_name = 'books'

urlpatterns = [
    path('', views.BookList.as_view(), name='book_list'),
    path('<int:pk>/', views.BookDetail.as_view(), name='book_detail'),
    path('search/', views.search_view, name='search'),
    path('author/<int:pk>/', views.AuthorDetail.as_view(), name='author_detail'),
    path('genre/<int:pk>/', views.GenreDetail.as_view(), name='genre_detail'),
    path('category/<int:pk>/', views.CategoryDetail.as_view(), name='category_detail'),
    path('insights/', views.library_insights, name='library_insights'),  # URL for library insights page
     path('create/', views.BookCreateView.as_view(), name='book_create'),  # Create a new book
    path('<int:pk>/update/', views.BookUpdateView.as_view(), name='book_update'),  # Update book
    path('<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),  # Delete book


]
