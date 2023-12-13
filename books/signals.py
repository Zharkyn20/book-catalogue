from django.db.models.signals import post_save
from django.dispatch import receiver

from books.models import Rating


@receiver(post_save, sender=Rating)
def update_book_rating(sender, instance, created, **kwargs):
    if created:
        book = instance.book
        current_rating = book.average_rating
        new_rating = (current_rating + instance.rating)/2
        book.average_rating = new_rating
        book.save()
