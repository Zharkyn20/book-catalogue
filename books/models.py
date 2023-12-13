from django.db import models
from django.utils.text import slugify

from tinymce.models import HTMLField
from users.models import CustomUser
from .constants import RATING_CHOICES


class Genre(models.Model):
    """Жанр"""

    name = models.CharField(max_length=100, verbose_name="Название")

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Book(models.Model):
    """Книга"""

    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="Автор"
    )
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, verbose_name="Жанр")

    slug = models.SlugField(max_length=100, verbose_name="Слаг", blank=True, null=True)
    title = models.CharField(max_length=100, verbose_name="Название")
    file = models.FileField(upload_to="books/", verbose_name="Файл книги")
    published_date = models.DateField(verbose_name="Дата публикации")
    average_rating = models.FloatField(verbose_name="Рейтинг", blank=True, null=True)
    description = HTMLField(verbose_name="Описание")

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Rating(models.Model):
    """Рейтинг"""

    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, verbose_name="Книга", related_name="ratings"
    )
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Рейтинг")
    comment = models.TextField(verbose_name="Комментарий")

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"

    def __str__(self):
        return f"{self.book} - {self.user} - {self.rating}"


class Favorite(models.Model):
    """Избранное"""

    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь"
    )

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"

    def __str__(self):
        return f"{self.book} - {self.user}"
