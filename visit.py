from books.utils import increment_visit_count_and_track_user
import random
from django.contrib.auth import get_user_model
from books.models import Book, Author, Genre, Category

def visit(rounds=100):
    """
    Simulate random visit tracking for users across Book, Author, Genre, and Category models.
    """
    # Fetch all users from the database
    users = get_user_model().objects.all()
    if not users.exists():
        print("No users found in the database.")
        return

    # Models to visit
    models = [Book, Author, Genre, Category]

    for round_number in range(1, rounds + 1):  # Loop through the number of rounds
        print(f"Starting round {round_number} of visits...")
        
        for user in users:
            # Randomly choose a model type
            model = random.choice(models)

            # Fetch a random instance of the selected model
            count = model.objects.count()
            if count == 0:
                continue  # Skip this model if there are no instances

            random_index = random.randint(0, count - 1)
            instance = model.objects.all()[random_index]

            # Log and track the visit
            print(f"User {user.username} is visiting {model.__name__} (ID: {instance.pk})")
            try:
                increment_visit_count_and_track_user(instance, user)
            except Exception as e:
                print(f"Error tracking visit for {model.__name__} (ID: {instance.pk}): {e}")

        print(f"Round {round_number} visits completed.")
