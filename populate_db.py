import os
import django
import random
import requests
from datetime import date, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from books.models import Book, Author, Genre, Category

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

User = get_user_model()

def download_image(image_url):
    """
    Download an image from a URL and return it as a SimpleUploadedFile.
    """
    response = requests.get(image_url)
    if response.status_code == 200:
        image_name = image_url.split("/")[-1]
        image_file = SimpleUploadedFile(image_name, response.content, content_type='image/jpeg')
        return image_file
    return None

def create_authors(num=10):
    authors = []
    author_names = [
        "J.K. Rowling", "Stephen King", "George R.R. Martin", 
        "Agatha Christie", "Dan Brown", "Margaret Atwood", 
        "Neil Gaiman", "Isaac Asimov", "Haruki Murakami", 
        "Virginia Woolf"
    ]
    
    for name in author_names[:num]:
        first_name = name
        author, _ = Author.objects.get_or_create(first_name=first_name)
        authors.append(author)
    
    return authors

def create_genres(num=8):
    genres = []
    genre_names = [
        "Science Fiction", "Fantasy", "Mystery", "Romance", 
        "Thriller", "Historical Fiction", "Horror", "Biography"
    ]
    
    for name in genre_names[:num]:
        genre, _ = Genre.objects.get_or_create(name=name)
        genres.append(genre)
    
    return genres

def create_categories(num=6):
    categories = []
    category_names = [
        "Classic", "Contemporary", "Young Adult", 
        "Non-Fiction", "International", "Award Winners"
    ]
    
    for name in category_names[:num]:
        category, _ = Category.objects.get_or_create(name=name)
        categories.append(category)
    
    return categories

def create_books(authors, genres, categories, num=50):
    books = []
    book_titles = [
        "The Wizard's Quest", "Silent Shadows", "Infinite Horizons", 
        "Crimson Dawn", "Echoes of Eternity", "Whispers in the Wind",
        "The Lost Manuscript", "Quantum Leap", "Midnight's Promise",
        "Realms of Imagination"
    ]
    
    # Example random image URLs (you can replace these with any other image sources)
    image_urls = [
        "https://via.placeholder.com/150/0000FF/808080?Text=Book+Cover",
        "https://via.placeholder.com/150/FF0000/FFFFFF?Text=Book+Cover",
        "https://via.placeholder.com/150/FFFF00/000000?Text=Book+Cover"
    ]
    
    for _ in range(num):
        title = random.choice(book_titles) + f" {random.randint(1, 1000)}"
        
        # Download random book cover image
        image_url = random.choice(image_urls)
        image = download_image(image_url)
        
        book, created = Book.objects.get_or_create(
            title=title,
            cover_image=image
        )
        
        # Add multiple authors, genres, and categories
        book.authors.add(*random.sample(authors, random.randint(1, min(3, len(authors)))))
        book.genres.add(*random.sample(genres, random.randint(1, min(2, len(genres)))))
        book.categories.add(*random.sample(categories, random.randint(1, min(2, len(categories)))))
        
        books.append(book)
    
    return books

def create_users(num=20):
    users = []
    roles = ['student', 'teacher', 'librarian', 'admin']
    subscriptions = ['free', 'basic', 'premium']
    
    # Example random profile image URLs
    profile_image_urls = [
        "https://via.placeholder.com/150/0000FF/808080?Text=Profile+Image",
        "https://via.placeholder.com/150/FF0000/FFFFFF?Text=Profile+Image",
        "https://via.placeholder.com/150/FFFF00/000000?Text=Profile+Image"
    ]
    
    for i in range(num):
        username = f"user_{i}"
        email = f"user{i}@example.com"
        
        # Download random profile image
        profile_image_url = random.choice(profile_image_urls)
        image = download_image(profile_image_url)
        
        user, created = User.objects.get_or_create(
            username=username,
            email=email,
            defaults={
                'role': random.choice(roles),
                'is_premium': random.choice([True, False]),
                'subscription_type': random.choice(subscriptions),
                'subscription_expiry': date.today() + timedelta(days=random.randint(30, 365)),
                'image': image
            }
        )
        
        if created:
            user.set_password('password123')
            user.save()
        
        users.append(user)
    
    return users

def simulate_visits(books, authors, genres, categories, users):
    for user in users:
        # Randomly visit books, authors, genres, categories
        user.books_visited.add(*random.sample(books, random.randint(0, min(10, len(books)))))
        user.authors_visited.add(*random.sample(authors, random.randint(0, min(5, len(authors)))))
        user.genres_visited.add(*random.sample(genres, random.randint(0, min(3, len(genres)))))
        user.categories_visited.add(*random.sample(categories, random.randint(0, min(3, len(categories)))))
        
        # Update visit counts
        for book in user.books_visited.all():
            book.visit_count += 1
            book.users_who_visited.add(user)
            book.save()
        
        for author in user.authors_visited.all():
            author.visit_count += 1
            author.users_who_visited.add(user)
            author.save()
        
        for genre in user.genres_visited.all():
            genre.visit_count += 1
            genre.users_who_visited.add(user)
            genre.save()
        
        for category in user.categories_visited.all():
            category.visit_count += 1
            category.users_who_visited.add(user)
            category.save()

def main():
    # Create base data
    authors = create_authors()
    genres = create_genres()
    categories = create_categories()
    books = create_books(authors, genres, categories)
    users = create_users()
    
    # Simulate user visits and tracking
    simulate_visits(books, authors, genres, categories, users)
    
    print(f"Created {len(authors)} authors")
    print(f"Created {len(genres)} genres")
    print(f"Created {len(categories)} categories")
    print(f"Created {len(books)} books")
    print(f"Created {len(users)} users")

if __name__ == "__main__":
    main()
