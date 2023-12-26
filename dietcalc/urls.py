from django.urls import path
from .apps import DietcalcConfig

from dietcalc.views import *

app_name = DietcalcConfig.name

urlpatterns = [
    path("", MyDietsView.as_view(), name="mydiets"),
    path("ajaxfood/<int:user_pk>/", ajax_food, name="ajax_food"),
    path("calc_bicarbonate/", CalcBicarbonate.as_view() , name="calc_bicarbonate"),
    path("special_food_calc/", special_food_calc , name="special_food_calc"),
    path("create_my_diet/", CreateMyDiet.as_view(), name="create_my_diet"),
    path("update_my_diet/<int:pk>/", UpdateMyDiet.as_view(), name="update_my_diet"),
    path("copy_my_diet/<int:pk>/", copy_my_diet, name="copy_my_diet"),
    path("copy_my_diet_to_user/<int:pk>/", copy_my_diet_to_user, name="copy_my_diet_to_user"),
    path("delete_my_diet/<int:pk>/", DeleteMyDiet.as_view(), name="delete_my_diet"),
    path("add_food_to_diet/", add_food_to_diet , name="add_food_to_diet"),
    path('delete_food_to_diet/<int:pk>/', delete_food_to_diet, name='delete_food_to_diet'),
    path('change_food_in_diet/<int:pk>/', change_food_in_diet, name='change_food_in_diet'),
    path("change_published_my_userdiet/<int:pk>/", ChangePublicMyUserDiet.as_view(), name="change_published_my_diet"),
    path('print/<int:pk>/pdf/', print_diet_pdf,name='print_diet_pdf'),
    path("public/<str:slug>/", PublicDietView.as_view(), name="public_diet_view"),
    path("create_my_food/", CreateMyFood.as_view(), name="create_my_food"),
    path("update_my_food/<int:pk>/", UpdateMyFood.as_view(), name="update_my_food"),
    path("delete_my_food/<int:pk>/", DeleteMyFood.as_view(), name="delete_my_food"),
    path("my_foods/", MyFoodsView.as_view(), name="myfoods"),
    path("food/<int:pk>/", UserFoodView.as_view(), name="food_view"),
    path("<str:slug>/", UserDietView.as_view(), name="diet_view"),

]