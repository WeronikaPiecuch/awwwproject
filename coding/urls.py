from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = "coding"
urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="coding/login.html", redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", views.index, name="index"),
    path("file/<int:file_id>/", views.file, name="file"),
    path("add/folder/", views.add_folder, name="add/folder"),
    path("add/file/", views.add_file, name="add/file"),
    path("delete/folder/<int:folder_id>/", views.delete_folder, name="delete/folder"),
    path("delete/file/<int:file_id>/", views.delete_file, name="delete/file"),
    path("compile/<int:file_id>/", views.compile, name="compile"),
    path("save/<int:file_id>/", views.save_file, name="save"),
    # path("delete/section/<int:file_id>/<int:section_id>/", views.delete_section, name="delete/section"),
    # path("add/section/<int:file_id>/", views.add_section, name="add/section"),
    path("download/<int:file_id>/", views.download, name="download"),
    path("standard/", views.standard, name="standard"),
    path("optymalizacje/", views.optymalizacje, name="optymalizacje"),
    path("procesor/", views.procesor, name="procesor"),
    path("zalezne/", views.zalezne, name="zalezne"),
]