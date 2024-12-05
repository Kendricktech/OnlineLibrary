from .utils import export_visit_data
from .models import Book, Author, Genre, Category
from django.test import TestCase
import json

class ExportVisitDataTest(TestCase):

    def setUp(self):
        # Setup test data
        self.book1 = Book.objects.create(title="Book 1", visit_count=5)
        self.book2 = Book.objects.create(title="Book 2", visit_count=3)
        
        self.author1 = Author.objects.create(first_name="Author 1", visit_count=8)
        self.author2 = Author.objects.create(first_name="Author 2", visit_count=6)
        
        self.genre1 = Genre.objects.create(name="Fantasy", visit_count=7)
        self.genre2 = Genre.objects.create(name="Fiction", visit_count=4)
        
        self.category1 = Category.objects.create(name="Category 1", visit_count=10)
        self.category2 = Category.objects.create(name="Category 2", visit_count=2)

    def test_export_visit_data(self):
        # Call the export function
        data = export_visit_data()
        
        # Parse the data
        data = json.loads(data)

        # Assert that books are included
        self.assertEqual(len(data["books"]), 2)
        self.assertEqual(data["books"][0]["title"], "Book 1")
        self.assertEqual(data["books"][0]["visit_count"], 5)

        # Assert that authors are included
        self.assertEqual(len(data["authors"]), 2)
        self.assertEqual(data["authors"][0]["name"], "Author 1")
        self.assertEqual(data["authors"][0]["visit_count"], 8)

        # Assert that genres are included
        self.assertEqual(len(data["genres"]), 2)
        self.assertEqual(data["genres"][0]["name"], "Fantasy")
        self.assertEqual(data["genres"][0]["visit_count"], 7)

        # Assert that categories are included
        self.assertEqual(len(data["categories"]), 2)
        self.assertEqual(data["categories"][0]["name"], "Category 1")
        self.assertEqual(data["categories"][0]["visit_count"], 10)
