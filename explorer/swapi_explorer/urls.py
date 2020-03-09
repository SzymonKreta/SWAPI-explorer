from django.urls import path

from .views import Home, SingleSet

urlpatterns = [
    path('', Home.as_view()),
    path('characters/<filename>', SingleSet.as_view())
]
