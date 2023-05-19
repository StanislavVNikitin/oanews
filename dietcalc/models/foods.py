__all__ = ['CategoryFood', 'Food']

from django.db import models
from django.urls import reverse

from authapp.models import CustomUser


class CategoryFood(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    photo = models.ImageField(upload_to="photo/foods/category/", blank=True, verbose_name="Картинка")
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def __str__(self):
        return self.name

    def delete(self, *args):
        self.deleted = True
        self.save()

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]


class Food(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    photo = models.ImageField(upload_to="photo/foods/", blank=True, verbose_name="Картинка")
    protein = models.DecimalField(max_digits=4, decimal_places=1, verbose_name='Белки')
    carbohydrates = models.DecimalField(max_digits=4, decimal_places=1, verbose_name='Углеводы')
    fat = models.DecimalField(max_digits=4, decimal_places=1, verbose_name='Жиры')
    calories = models.DecimalField(max_digits=4, decimal_places=0, verbose_name='Калорийность')
    special_food = models.BooleanField(default=False, verbose_name='Спецпитание')
    is_published = models.BooleanField(default=False, verbose_name='Видин всем')
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL, related_name="userfood",
                             verbose_name="Пользователь")
    category_food = models.ForeignKey("CategoryFood", null=True, on_delete=models.SET_NULL, related_name="foods",
                                      verbose_name="Категория")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлен")
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def __str__(self):
        return self.name

    def delete(self, *args):
        self.deleted = True
        self.save()

    def get_absolute_url(self):
        return reverse("dietcalc:food_view", kwargs={"pk": self.id})

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name"]