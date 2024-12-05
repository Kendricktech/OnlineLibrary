from django.test import TestCase
from .models import Book, Author, Genre, Category
from .utils import increment_visit_count

class VisitCountTest(TestCase):

    def setUp(self):
        # Setup test data
        self.book = Book.objects.create(title="Test Book")
        self.author = Author.objects.create(first_name="Author 1")
        self.genre = Genre.objects.create(name="Fantasy")
        self.category = Category.objects.create(name="Fiction")

        self.book.authors.add(self.author)
        self.book.genres.add(self.genre)
        self.book.categories.add(self.category)

    def test_increment_book_visit_count(self):
        # Check initial visit count
        self.assertEqual(self.book.visit_count, 0)

        # Increment visit count
        increment_visit_count(self.book)

        # Check if the book's visit count is incremented
        self.book.refresh_from_db()
        self.assertEqual(self.book.visit_count, 1)

    def test_increment_related_visit_counts(self):
        # Check initial visit counts for related fields
        self.assertEqual(self.author.visit_count, 0)
        self.assertEqual(self.genre.visit_count, 0)
        self.assertEqual(self.category.visit_count, 0)

        # Increment visit count for the book
        increment_visit_count(self.book)

        # Refresh and check visit counts for related fields
        self.author.refresh_from_db()
        self.genre.refresh_from_db()
        self.category.refresh_from_db()

        self.assertEqual(self.author.visit_count, 1)
        self.assertEqual(self.genre.visit_count, 1)
        self.assertEqual(self.category.visit_count, 1)
