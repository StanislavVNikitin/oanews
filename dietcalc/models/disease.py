__all__ = ['Disease']

from django.db import models

class Disease(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    acronym = models.CharField(max_length=5, verbose_name="Аббревиатура")
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def __str__(self):
        return self.name

    def delete(self, *args):
        self.deleted = True
        self.save()

    class Meta:
        verbose_name = "Болезнь"
        verbose_name_plural = "Болезни"
        ordering = ["name"]