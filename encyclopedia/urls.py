from django.urls import path

from . import views
app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("create_page/", views.create_page, name="create_page"),
    path("entry/", views.entry, name="entry")
]
