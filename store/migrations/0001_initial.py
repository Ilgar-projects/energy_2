from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, verbose_name="Название")),
                ("flavor", models.CharField(max_length=120, verbose_name="Вкус")),
                ("slug", models.SlugField(max_length=140, unique=True, verbose_name="Slug")),
                ("price", models.DecimalField(decimal_places=2, max_digits=8, verbose_name="Цена")),
                ("stock", models.PositiveIntegerField(default=0, verbose_name="Остаток")),
                ("image", models.ImageField(blank=True, null=True, upload_to="products/", verbose_name="Картинка")),
                ("sort_order", models.PositiveSmallIntegerField(default=10, verbose_name="Порядок")),
                ("is_active", models.BooleanField(default=True, verbose_name="Активен")),
                ("hero_product", models.BooleanField(default=False, verbose_name="Главный товар")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "Товар",
                "verbose_name_plural": "Товары",
                "ordering": ["sort_order", "id"],
            },
        ),
    ]
