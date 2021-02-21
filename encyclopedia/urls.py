from django.urls import path

from . import views
app_name = "encyclopedia"
urlpatterns = [
    path("", views.index, name="home"),
    path("contribute/", views.contribute, name="contribute"),
    path("wiki/<str:title>/", views.entry, name="entry"),
    path("wiki/<str:title>/edit/", views.edit, name="edit"),
    path("error/", views.error, name="error"),
    path("<str:catch>/", views.error, name="catch")
 # path("<str:str>/<str:str>/<str:str>", views.error, name="catch_error")
]
