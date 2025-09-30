from decimal import Decimal, ROUND_HALF_UP
import random
from django.utils import timezone
from django.core.management.base import BaseCommand
from faker import Faker
from munji_app.models import Supplier, MunjiPurchase, RiceProduction, GlobalSettings, Category

fake = Faker()
def d2(x): return Decimal(x).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

class Command(BaseCommand):
    help = "Generate random data safely"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Generating data..."))

        # Ensure GlobalSettings exists with large balance
        gs, _ = GlobalSettings.objects.get_or_create(id=1,
                                                     defaults={'opening_balance': Decimal('999999.99'),
                                                               'total_munji': Decimal('0.00')})

        # Create default categories if they don't exist
        default_categories = ["Paddy", "Wheat", "Corn", "Rice"]
        for cat_name in default_categories:
            Category.objects.get_or_create(name=cat_name)

        suppliers = []
        munji_purchases = []
        rice_productions = []

        for _ in range(10):
            s = Supplier(name=fake.company())
            suppliers.append(s)

        Supplier.objects.bulk_create(suppliers)

        # Get all categories for random assignment
        all_categories = list(Category.objects.all())

        for s in Supplier.objects.all():
            for _ in range(random.randint(2, 5)):
                qty   = d2(random.uniform(10, 200))
                price = d2(random.uniform(50, 500))
                total = d2(qty * price)

                munji_purchases.append(MunjiPurchase(
                    supplier=s,
                    category=random.choice(all_categories),
                    total_bags=random.randint(10, 100),
                    buying_quantity_munji=qty,
                    munji_price_per_unit=price,
                    total_munji_price=total,
                    total_munji_cost=total,
                    payment_type=random.choice(["Cash", "Credit"]),
                    created_at=timezone.now()
                ))

            for _ in range(random.randint(2, 5)):
                qprod = d2(random.uniform(50, 500))
                rice_price = d2(random.uniform(50, 200))
                total_quality = d2(float(qprod) * random.uniform(0.7, 0.95))
                total_price = d2(total_quality * rice_price)

                rice_productions.append(RiceProduction(
                    quantity_produced=qprod,
                    dryer_cost=d2(random.uniform(100, 500)),
                    factory_cost=d2(random.uniform(200, 1000)),
                    wastage=d2(random.uniform(0.01, 0.1)),
                    quality_of_rice=d2(random.uniform(0.7, 0.95)),
                    rice_price_per_unit=rice_price,
                    total_quality=total_quality,
                    total_price=total_price,
                    naku_price=d2(random.uniform(5, 20)),
                    naku_quantity=d2(random.uniform(10, 100)),
                    created_at=timezone.now()
                ))

        MunjiPurchase.objects.bulk_create(munji_purchases)
        RiceProduction.objects.bulk_create(rice_productions)

        self.stdout.write(self.style.SUCCESS("✅ Data generation complete (bulk inserted)."))
