from django.db.models import F
from books.models import BookVisit, AuthorVisit, GenreVisit, CategoryVisit
from django.db.models import F
from django.db.models import F
from django.utils import timezone
from .models import Book, BookVisit, AuthorVisit, GenreVisit, CategoryVisit

def increment_visit_count_and_track_user(instance, user):
    """
    Increment the visit count of the given instance and track user visits in the corresponding visit model.
    :param instance: The model instance (Book, Author, Genre, Category) to update.
    :param user: The user visiting the instance.
    """
    if not hasattr(instance, 'visit_count'):
        raise AttributeError(f"The model {instance.__class__.__name__} does not have a 'visit_count' field.")

    # Increment visit count for the instance
    instance.visit_count = F('visit_count') + 1
    instance.save(update_fields=["visit_count"])

    # Define related visit models for cascading
    visit_models = {
        Book: (BookVisit, "book"),
        Author: (AuthorVisit, "author"),
        Genre: (GenreVisit, "genre"),
        Category: (CategoryVisit, "category"),
    }

    visit_model, related_field = visit_models.get(type(instance), (None, None))
    if visit_model:
        # Handle visit tracking for the given instance
        visit = visit_model.objects.filter(user=user, **{related_field: instance}).first()
        if visit:
            visit.visit_count = F('visit_count') + 1
            visit.save(update_fields=["visit_count"])
        else:
            visit_model.objects.create(user=user, **{related_field: instance}, visit_count=1, visited_on=timezone.now())

    # Cascade visits to related fields (for Books only)
    if isinstance(instance, Book):
        for related_field in ["authors", "genres", "categories"]:
            related_objects = getattr(instance, related_field).all()
            for related_object in related_objects:
                increment_visit_count_and_track_user(related_object, user)


import json
from django.core.serializers.json import DjangoJSONEncoder
from .models import Book, Author, Genre, Category, BookVisit, AuthorVisit, GenreVisit, CategoryVisit
from django.db.models import Prefetch


def export_user_data(user):
    """
    Export visit data specific to a user.
    """
    visit_data = {}
    models = [BookVisit, AuthorVisit, GenreVisit, CategoryVisit]

    for model in models:
        model_name = model.__name__.lower()  # e.g., bookvisit -> bookvisit
        visit_data[model_name] = list(model.objects.filter(user=user).values())

    return visit_data


def export_site_data():
    """
    Export all site-wide visit data.
    """
    visit_data = {}
    models = [BookVisit, AuthorVisit, GenreVisit, CategoryVisit]

    for model in models:
        model_name = model.__name__.lower()  # e.g., bookvisit -> bookvisit
        visit_data[model_name] = list(model.objects.all().values())

    return visit_data

def serialize_to_json(context):
    return json.dumps(context,cls=DjangoJSONEncoder)