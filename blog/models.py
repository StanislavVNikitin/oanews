from django.db import models
from django.urls import reverse, reverse_lazy
from bs4 import BeautifulSoup

class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, verbose_name="Url категории", unique=True)
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:category", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["title"]


class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название")
    slug = models.SlugField(max_length=50, verbose_name="Url тэга", unique=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:tag", kwargs={"slug": self.slug})

    def delete(self, *args):
        self.deleted = True
        self.save()

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"
        ordering = ["title"]


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название новости")
    slug = models.SlugField(max_length=255, verbose_name="Url новости", unique=True)
    author = models.CharField(max_length=100, verbose_name="Автор")
    content = models.TextField(blank=True, verbose_name="Текст новости")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Опубликовано")
    photo = models.ImageField(upload_to="photo/%Y/%m/%d/", blank=True, verbose_name="Картинка")
    views = models.IntegerField(default=0, verbose_name="Количество просмотров")
    category = models.ForeignKey("Category", on_delete=models.PROTECT, related_name="posts", verbose_name="Категория")
    tags = models.ManyToManyField("Tag", blank=True, related_name="posts", verbose_name="Тэг")
    deleted = models.BooleanField(default=False, verbose_name='Удалено')

    def __str__(self):
        return self.title

    def delete(self, *args):
        self.deleted = True
        self.save()

    def get_absolute_url(self):
        return reverse("blog:post", kwargs={"slug": self.slug})

    def get_content_no_html(self):
        soup = BeautifulSoup(self.content, 'html.parser')
        return soup.get_text()

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ["-created_at"]
