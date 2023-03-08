from django.urls import path
from .apps import SiteappConfig

from .views import *

app_name = SiteappConfig.name

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("page/<str:slug>", PageView.as_view(), name="page_slug"),
    path("pagesvyaz-obratnaya/", contact_sendmail, name="page_site_svyaz_obratnaya"),
]
