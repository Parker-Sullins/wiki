from django.urls import path

from . import views
app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="home"),
    path("entry/<str:title>/", views.entry, name="entry"),
    path("contribute/", views.contribute, name="contribute"),
    path("entry/<str:title>/edit/", views.edit, name="edit")
]
