from decimal import Decimal, ROUND_HALF_UP
import random
from django.utils import timezone
from django.core.management.base import BaseCommand
from faker import Faker
from munji_app.models import Supplier, MunjiPurchase, RiceProduction

fake = Faker()

def d2(val):
    """Quantize to 2 decimal places (ROUND_HALF_UP)."""
    return Decimal(val).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

class Command(BaseCommand):
    help = "Generate random suppliers, munji purchases, and rice productions."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Generating data..."))
        for _ in range(10):  # number of suppliers
            supplier = Supplier.objects.create(
                name=fake.company(),
            )

            # ---- MunjiPurchase ----
            for _ in range(random.randint(2, 5)):
                buying_quantity_munji = d2(random.uniform(10, 200))
                munji_price_per_unit = d2(random.uniform(50, 500))
                total_munji_price = d2(buying_quantity_munji * munji_price_per_unit)
                total_munji_cost = d2(buying_quantity_munji * munji_price_per_unit)

                MunjiPurchase.objects.create(
                    supplier=supplier,
                    category=fake.word(),
                    total_bags=random.randint(10, 100),
                    buying_quantity_munji=buying_quantity_munji,
                    munji_price_per_unit=munji_price_per_unit,
                    total_munji_price=total_munji_price,
                    total_munji_cost=total_munji_cost,
                    payment_type=random.choice(["Cash", "Credit"]),
                    created_at=timezone.now(),
                )

            # ---- RiceProduction ----
            for _ in range(random.randint(2, 5)):
                quantity_produced = d2(random.uniform(50, 500))
                rice_price_per_unit = d2(random.uniform(50, 200))
                total_quality = d2(random.uniform(0.7, 0.95) * quantity_produced)
                total_price = d2(total_quality * rice_price_per_unit)

                RiceProduction.objects.create(
                    quantity_produced=quantity_produced,
                    dryer_cost=d2(random.uniform(100, 500)),
                    factory_cost=d2(random.uniform(200, 1000)),
                    wastage=d2(random.uniform(0.01, 0.1)),
                    quality_of_rice=d2(random.uniform(0.7, 0.95)),
                    rice_price_per_unit=rice_price_per_unit,
                    total_quality=total_quality,
                    total_price=total_price,
                    naku_price=d2(random.uniform(5, 20)),
                    naku_quantity=d2(random.uniform(10, 100)),
                    created_at=timezone.now(),
                )

        self.stdout.write(self.style.SUCCESS("✅ Data generation complete."))
