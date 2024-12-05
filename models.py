import os
import django
from django.contrib.auth import get_user_model
from faker import Faker
import random
from books.models import Author, Book, Genre, Category

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

def main():
    fake = Faker()

    # Function to generate random genres and categories
    def generate_genre():
        return random.choice(['Fiction', 'Non-Fiction', 'Science', 'Fantasy', 'History', 'Thriller', 'Biography'])

    def generate_category():
        return random.choice(['Mystery', 'Adventure', 'Romance', 'Young Adult', 'Children', 'Science Fiction', 'Horror'])

    def create_random_authors(num_authors=10):
        authors = []
        try:
            for i in range(num_authors):
                print(f"Creating author {i + 1}/{num_authors}")
                authors.append(Author(
                    first_name=fake.first_name(),
                    image=fake.image_url(),  # You can link an image URL or use a default image path
                ))
            Author.objects.bulk_create(authors)
            print(f"{num_authors} authors created successfully!")
        except Exception as e:
            print(f"Error occurred: {e}")

    def create_random_genres(num_genres=5):
        genres = []
        try:
            for i in range(num_genres):
                genre_name = generate_genre()
                print(f"Creating genre {i + 1}/{num_genres}: {genre_name}")
                genres.append(Genre(name=genre_name))
            Genre.objects.bulk_create(genres)
            print(f"{num_genres} genres created successfully!")
        except Exception as e:
            print(f"Error occurred: {e}")

    def create_random_categories(num_categories=5):
        categories = []
        try:
            for i in range(num_categories):
                category_name = generate_category()
                print(f"Creating category {i + 1}/{num_categories}: {category_name}")
                categories.append(Category(name=category_name))
            Category.objects.bulk_create(categories)
            print(f"{num_categories} categories created successfully!")
        except Exception as e:
            print(f"Error occurred: {e}")

    def create_random_books(num_books=10):
        books = []
        try:
            authors = Author.objects.all()
            genres = Genre.objects.all()
            categories = Category.objects.all()

            for i in range(num_books):
                print(f"Creating book {i + 1}/{num_books}")
                # Randomly choose authors, genres, and categories
                book_authors = random.sample(list(authors), k=random.randint(1, 3))  # Choose 1-3 authors
                book_genres = random.sample(list(genres), k=random.randint(1, 2))  # Choose 1-2 genres
                book_categories = random.sample(list(categories), k=random.randint(1, 2))  # Choose 1-2 categories

                # Create the book instance first
                book = Book(
                    title=fake.sentence(nb_words=5),
                )

                
                book.save()  # Save the book instance to generate an ID

                # Now use .set() to assign related objects to the ManyToManyField
                book.authors.set(book_authors)
                book.genres.set(book_genres)
                book.categories.set(book_categories)

                books.append(book)

            print(f"{num_books} books created successfully!")
        except Exception as e:
            print(f"Error occurred: {e}")

    # Create random data
    create_random_authors(10)  # Create 10 authors
    create_random_genres(5)  # Create 5 genres
    create_random_categories(5)  # Create 5 categories
    create_random_books(10)  # Create 10 books

if __name__ == "__main__":
    main()
