from django.urls import path
from .apps import SiteappConfig

from .views import *

app_name = SiteappConfig.name

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("page/description-of-diseases", DescriptionDiasesVideoPage.as_view()),
    path("page/calculation-of-the-diet", CalculationDietVideoPage.as_view()),
    path("page/<str:slug>", PageView.as_view(), name="page_slug"),
    path("pagesvyaz-obratnaya/", contact_sendmail, name="page_site_svyaz_obratnaya"),
    path("userstore/<str:slug>", UserStoreDetail.as_view(), name="user_store"),
    path("userstores/", UserStoreList.as_view(), name="user_stores_list"),
    path("myuserstores/", MyUserStoreList.as_view(),name="my_user_stores_list"),
    path("create_my_userstore/", CreateMyUserStore.as_view(), name="create_my_userstore"),
    path("delete_my_userstore/<int:pk>/", MyUserStoreDelete.as_view(), name="delete_my_userstore"),
    path("update_my_userstore/<int:pk>/", UpdateMyUserStore.as_view(), name="update_my_userstore"),
    path("change_published_my_userstore/<int:pk>/", ChangePublicMyUserStore.as_view(), name="change_published_my_userstore"),

]
