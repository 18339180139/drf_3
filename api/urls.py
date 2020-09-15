from django.urls import path, include

from api import views

urlpatterns = [
    path("users/",views.EmployeeAPIViews.as_view()),
    path("users/<str:id>/",views.EmployeeAPIViews.as_view()),
]