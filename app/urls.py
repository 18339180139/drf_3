
from django.urls import path

from app import views

urlpatterns =[
    path("book/",views.BookAPIView.as_view()),
    path("book/<str:id>/",views.BookAPIView.as_view()),
    path("v2/books/",views.BookAPIViewV2.as_view()),
    path("v2/books/<str:id>/",views.BookAPIViewV2.as_view())
]
