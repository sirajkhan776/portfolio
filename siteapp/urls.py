from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="home"),
    path("profile/", views.profile_page, name="profile"),
    path("preferences/", views.preferences, name="preferences"),
    path("profile/download", views.download_profile, name="download_profile"),
    path("profile/download.vcf", views.download_vcard, name="download_vcard"),
    path("profile/download.pdf", views.download_profile_pdf, name="download_profile_pdf"),
    path("register/", views.register, name="register"),
]
