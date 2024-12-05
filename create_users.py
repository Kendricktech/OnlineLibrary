import os
import django
from django.contrib.auth import get_user_model
from faker import Faker
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

def main():
    fake = Faker()
    CustomUser = get_user_model()

    def generate_role():
        return random.choice(['student', 'teacher', 'librarian', 'admin'])

    def generate_subscription_type():
        return random.choice(['free', 'basic', 'premium'])

    def generate_subscription_expiry(subscription_type):
        if subscription_type == 'premium':
            return fake.date_between(start_date='today', end_date='+2y')
        return None

    def create_random_users(num_users=10):  # Reduced for testing
        users = []
        try:
            for i in range(num_users):
                print(f"Creating user {i + 1}/{num_users}")
                role = generate_role()
                subscription_type = generate_subscription_type()
                subscription_expiry = generate_subscription_expiry(subscription_type)

                users.append(CustomUser(
                    username=fake.unique.user_name(),
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    email=fake.unique.email(),
                    password=fake.password(length=12),  # Plain text password for testing
                    role=role,
                    is_premium=(subscription_type == 'premium'),
                    subscription_type=subscription_type,
                    subscription_expiry=subscription_expiry,
                ))
            CustomUser.objects.bulk_create(users)
            print(f"{num_users} users created successfully!")
        except Exception as e:
            print(f"Error occurred: {e}")

    # Test with fewer users
    create_random_users(100)

if __name__ == "__main__":
    main()
