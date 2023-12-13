import django_filters

from .models import Book


class BookFilter(django_filters.FilterSet):
    published_after = django_filters.DateFilter(
        field_name="published_date",
        lookup_expr="gte",
        label="Published After",
    )
    published_before = django_filters.DateFilter(
        field_name="published_date",
        lookup_expr="lte",
        help_text="Фильтр по документам начислений, созданным до этой даты (включительно).",
        label="Published Before",
    )

    class Meta:
        model = Book
        fields = (
            "genre",
            "author",
            "published_after",
            "published_before",
        )
