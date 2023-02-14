from django import template

from blog.models import Category

register = template.Library()


@register.inclusion_tag("blog/menu_tpl.html")
def show_menu(menu_class="menu"):
    categoies = Category.objects.all()
    return {"categories": categoies, "menu_class": menu_class}
