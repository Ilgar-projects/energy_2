from django.db import models
from django.templatetags.static import static


class Product(models.Model):
    name = models.CharField("Название", max_length=120)
    flavor = models.CharField("Вкус", max_length=120)
    slug = models.SlugField("Slug", max_length=140, unique=True)
    price = models.DecimalField("Цена", max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField("Остаток", default=0)
    image = models.ImageField("Картинка", upload_to="products/", blank=True, null=True)
    sort_order = models.PositiveSmallIntegerField("Порядок", default=10)
    is_active = models.BooleanField("Активен", default=True)
    hero_product = models.BooleanField("Главный товар", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sort_order", "id"]
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"СТАРТ — {self.name}"

    @property
    def stock_label(self):
        if self.stock == 0:
            return "Нет в наличии"
        if self.stock <= 10:
            return f"Осталось {self.stock} шт."
        return f"В наличии {self.stock} шт."

    @property
    def status(self):
        if self.stock == 0:
            return "out"
        if self.stock <= 10:
            return "low"
        return "in"

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return static("store/img/placeholder-can.png")

    @property
    def theme(self):
        slug = (self.slug or "").lower()
        name = (self.name or "").lower()
        if "berry" in slug or "berry" in name or self.sort_order == 1:
            return "berry"
        if "citrus" in slug or "punch" in slug or self.sort_order == 2:
            return "gold"
        if "mint" in slug or "ice" in slug or self.sort_order == 3:
            return "cyan"
        if "mango" in slug or "storm" in slug or self.sort_order == 4:
            return "orange"
        return "berry"
