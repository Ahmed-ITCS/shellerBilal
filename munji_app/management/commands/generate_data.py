import random
from decimal import Decimal, ROUND_HALF_UP
from django.core.management.base import BaseCommand
from faker import Faker
from munji_app.models import GlobalSettings, Supplier, MunjiPurchase, Expense, RiceProduction


def d2(val: float) -> Decimal:
    """Return Decimal rounded to 2 places (half up)."""
    return Decimal(val).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class Command(BaseCommand):
    help = "Generates random data for all models in munji_app"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Generating random data..."))
        fake = Faker()

        # Clear existing data
        GlobalSettings.objects.all().delete()
        Supplier.objects.all().delete()
        MunjiPurchase.objects.all().delete()
        Expense.objects.all().delete()
        RiceProduction.objects.all().delete()

        # 1. GlobalSettings
        global_settings, _ = GlobalSettings.objects.get_or_create(
            id=1,
            defaults={
                "opening_balance": d2(random.uniform(10_000, 100_000)),
                "total_munji": d2(random.uniform(1_000, 5_000)),
            },
        )
        self.stdout.write(
            self.style.SUCCESS(f"Created/Updated GlobalSettings: {global_settings}")
        )

        # 2. Suppliers
        suppliers = []
        for _ in range(5):
            supplier = Supplier.objects.create(name=fake.company())
            suppliers.append(supplier)
            self.stdout.write(self.style.SUCCESS(f"Created Supplier: {supplier.name}"))

        # 3. MunjiPurchases
        munji_purchases = []
        for _ in range(10):
            supplier = random.choice(suppliers)
            buying_quantity_munji = d2(random.uniform(100, 1000))
            munji_price_per_unit = d2(random.uniform(10, 50))
            total_munji_price = d2(buying_quantity_munji * munji_price_per_unit)
            payment_type = random.choice([MunjiPurchase.CASH, MunjiPurchase.CREDIT])

            try:
                mp = MunjiPurchase.objects.create(
                    supplier=supplier,
                    category=fake.word(),
                    total_bags=random.randint(10, 100),
                    buying_quantity_munji=buying_quantity_munji,
                    munji_price_per_unit=munji_price_per_unit,
                    total_munji_price=total_munji_price,
                    payment_type=payment_type,
                )
                munji_purchases.append(mp)
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created MunjiPurchase: {mp.category} from {supplier.name}"
                    )
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating MunjiPurchase: {e}"))

        # 4. Expenses
        for _ in range(15):
            if munji_purchases:
                mp = random.choice(munji_purchases)
                expense = Expense.objects.create(
                    munji_purchase=mp,
                    title=fake.sentence(nb_words=3),
                    amount=d2(random.uniform(5, 200)),
                )
                self.stdout.write(
                    self.style.SUCCESS(f"Created Expense: {expense.title} for {mp.category}")
                )

        # 5. RiceProduction
        for _ in range(7):
            quantity_produced = d2(random.uniform(50, 500))
            rice_price_per_unit = d2(random.uniform(20, 80))

            # random.uniform needs floats, so cast Decimals to float
            low = float(quantity_produced * Decimal("0.8"))
            high = float(quantity_produced)
            total_quality = d2(random.uniform(low, high))
            total_price = d2(total_quality * rice_price_per_unit)

            try:
                rp = RiceProduction.objects.create(
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
                )
                self.stdout.write(
                    self.style.SUCCESS(f"Created RiceProduction: {rp.quantity_produced}")
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating RiceProduction: {e}"))

        self.stdout.write(self.style.SUCCESS("Random data generation complete."))
