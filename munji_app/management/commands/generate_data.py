from decimal import Decimal, ROUND_HALF_UP, getcontext
import random
from django.utils import timezone
from django.core.management.base import BaseCommand
from faker import Faker
from munji_app.models import Supplier, MunjiPurchase, RiceProduction

fake = Faker()
getcontext().prec = 28  # high precision to avoid float noise

def d2(val):
    return (Decimal(val)
            .quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

class Command(BaseCommand):
    help = "Generate random suppliers, munji purchases, and rice productions."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Generating data..."))

        for _ in range(10):
            supplier = Supplier.objects.create(name=fake.company())

            for _ in range(random.randint(2, 5)):
                qty = d2(random.uniform(10, 200))
                price = d2(random.uniform(50, 500))

                # Compute raw and quantize TWICE (defensive)
                raw_total = qty * price
                total_price = d2(raw_total)
                total_cost = d2(raw_total)

                # Force a 2-decimal string to kill any hidden tail
                total_price = Decimal(f"{total_price:.2f}")
                total_cost  = Decimal(f"{total_cost:.2f}")
                qty         = Decimal(f"{qty:.2f}")
                price       = Decimal(f"{price:.2f}")

                MunjiPurchase.objects.create(
                    supplier=supplier,
                    category=fake.word(),
                    total_bags=random.randint(10, 100),
                    buying_quantity_munji=qty,
                    munji_price_per_unit=price,
                    total_munji_price=total_price,
                    total_munji_cost=total_cost,
                    payment_type=random.choice(["Cash", "Credit"]),
                    created_at=timezone.now(),
                )

            for _ in range(random.randint(2, 5)):
                q_prod = d2(random.uniform(50, 500))
                rice_price = d2(random.uniform(50, 200))
                total_quality = d2(random.uniform(0.7, 0.95) * q_prod)
                total_price = d2(total_quality * rice_price)

                RiceProduction.objects.create(
                    quantity_produced=Decimal(f"{q_prod:.2f}"),
                    dryer_cost=Decimal(f"{d2(random.uniform(100, 500)):.2f}"),
                    factory_cost=Decimal(f"{d2(random.uniform(200, 1000)):.2f}"),
                    wastage=Decimal(f"{d2(random.uniform(0.01, 0.1)):.2f}"),
                    quality_of_rice=Decimal(f"{d2(random.uniform(0.7, 0.95)):.2f}"),
                    rice_price_per_unit=Decimal(f"{rice_price:.2f}"),
                    total_quality=Decimal(f"{total_quality:.2f}"),
                    total_price=Decimal(f"{total_price:.2f}"),
                    naku_price=Decimal(f"{d2(random.uniform(5, 20)):.2f}"),
                    naku_quantity=Decimal(f"{d2(random.uniform(10, 100)):.2f}"),
                    created_at=timezone.now(),
                )

        self.stdout.write(self.style.SUCCESS("✅ Data generation complete."))
