from django.urls import path, include
from rest_framework.routers import DefaultRouter

from books.views import BookViewSet, RatingViewSet, FavoriteViewSet

router = DefaultRouter()
router.register("books", BookViewSet, basename="book")
router.register("ratings", RatingViewSet, basename="rating")
router.register("favorites", FavoriteViewSet, basename="favorite")

urlpatterns = [
    path("", include(router.urls)),
]
