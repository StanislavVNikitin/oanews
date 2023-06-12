__all__ = ['UserDiet', 'Diet']

from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify

# Create your models here.
from authapp.models import CustomUser

class UserDiet(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    gender = models.CharField(max_length=1, choices=CustomUser.GENGER_CHOICES, blank=True, verbose_name="Пол")
    age = models.PositiveSmallIntegerField(verbose_name="Возраст")
    weight = models.DecimalField(max_digits=4, decimal_places=1, verbose_name='Вес')
    height = models.PositiveSmallIntegerField(blank=True, verbose_name="Рост")
    disease = models.ForeignKey('Disease', null=True, on_delete=models.SET_NULL, related_name="disease",
                                verbose_name="Заболевание")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="userdiets",
                             verbose_name="Пользователь")
    slug = models.SlugField(null=False, editable=False, verbose_name="Url диеты", unique=True)
    is_published = models.BooleanField(default=False, verbose_name='Видин всем')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлен")
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def __str__(self):
        return self.name

    def delete(self, *args):
        self.deleted = True
        self.save()

    def get_absolute_url(self):
        return reverse("dietcalc:diet_view", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Пользовательская диета"
        verbose_name_plural = "Пользовательские диеты"
        ordering = ["-created_at"]


class Diet(models.Model):
    user_diet = models.ForeignKey('UserDiet', on_delete=models.CASCADE, related_name="diets",
                                  verbose_name="Пользовательская диета")
    food = models.ForeignKey('Food', on_delete=models.CASCADE, related_name="diets", verbose_name="Продукт")
    count = models.PositiveSmallIntegerField(verbose_name="Количество")


    class Meta:
        verbose_name = "Диета"
        verbose_name_plural = "Диеты"
        unique_together = ('user_diet', 'food')


