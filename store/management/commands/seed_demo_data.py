from django.conf import settings
from django.core.management.base import BaseCommand

from store.models import Product


class Command(BaseCommand):
    help = "Создаёт демо-товары для локального запуска"

    def handle(self, *args, **options):
        demo_products = [
            {
                "slug": "neon-berry",
                "name": "NEON BERRY",
                "flavor": "Клубника + малина",
                "price": 200,
                "stock": 107,
                "image": "products/neon_berry.png",
                "sort_order": 1,
                "hero_product": True,
            },
            {
                "slug": "citrus-punch",
                "name": "CITRUS PUNCH",
                "flavor": "Цитрус + лайм",
                "price": 210,
                "stock": 64,
                "image": "products/citrus_punch.png",
                "sort_order": 2,
                "hero_product": False,
            },
            {
                "slug": "ice-mint",
                "name": "ICE MINT",
                "flavor": "Ледяная мята + лимон",
                "price": 220,
                "stock": 92,
                "image": "products/ice_mint.png",
                "sort_order": 3,
                "hero_product": False,
            },
            {
                "slug": "mango-storm",
                "name": "MANGO STORM",
                "flavor": "Манго + маракуйя",
                "price": 215,
                "stock": 48,
                "image": "products/mango_storm.png",
                "sort_order": 4,
                "hero_product": False,
            },
        ]

        created_count = 0
        for item in demo_products:
            product, created = Product.objects.get_or_create(
                slug=item["slug"],
                defaults={
                    "name": item["name"],
                    "flavor": item["flavor"],
                    "price": item["price"],
                    "stock": item["stock"],
                    "sort_order": item["sort_order"],
                    "hero_product": item["hero_product"],
                    "is_active": True,
                },
            )
            if created:
                image_path = settings.MEDIA_ROOT / item["image"]
                if image_path.exists():
                    product.image = item["image"]
                    product.save(update_fields=["image"])
                created_count += 1

        if created_count:
            self.stdout.write(self.style.SUCCESS(f"Создано демо-товаров: {created_count}."))
        else:
            self.stdout.write("Демо-товары уже существуют. Изменения пользователя сохранены.")
