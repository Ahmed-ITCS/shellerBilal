import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from faker import Faker
from munji_app.models import GlobalSettings, Supplier, MunjiPurchase, Expense, RiceProduction

class Command(BaseCommand):
    help = 'Generates random data for all models in munji_app'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Generating random data...'))
        fake = Faker()

        # Clear existing data (optional, for fresh data generation)
        GlobalSettings.objects.all().delete()
        Supplier.objects.all().delete()
        MunjiPurchase.objects.all().delete()
        Expense.objects.all().delete()
        RiceProduction.objects.all().delete()

        # 1. GlobalSettings
        global_settings, created = GlobalSettings.objects.get_or_create(
            id=1,
            defaults={
                'opening_balance': Decimal(random.uniform(10000, 100000)),
                'total_munji': Decimal(random.uniform(1000, 5000))
            }
        )
        self.stdout.write(self.style.SUCCESS(f'Created/Updated GlobalSettings: {global_settings}'))

        # 2. Suppliers
        suppliers = []
        for _ in range(5):
            supplier = Supplier.objects.create(name=fake.company())
            suppliers.append(supplier)
            self.stdout.write(self.style.SUCCESS(f'Created Supplier: {supplier.name}'))

        # 3. MunjiPurchases
        munji_purchases = []
        for _ in range(10):
            supplier = random.choice(suppliers)
            buying_quantity_munji = Decimal(random.uniform(100, 1000)).quantize(Decimal('0.01'))
            munji_price_per_unit = Decimal(random.uniform(10, 50)).quantize(Decimal('0.01'))
            total_munji_price = buying_quantity_munji * munji_price_per_unit
            payment_type = random.choice([MunjiPurchase.CASH, MunjiPurchase.CREDIT])

            try:
                munji_purchase = MunjiPurchase.objects.create(
                    supplier=supplier,
                    category=fake.word(),
                    total_bags=random.randint(10, 100),
                    buying_quantity_munji=buying_quantity_munji,
                    munji_price_per_unit=munji_price_per_unit,
                    total_munji_price=total_munji_price,
                    payment_type=payment_type
                )
                munji_purchases.append(munji_purchase)
                self.stdout.write(self.style.SUCCESS(f'Created MunjiPurchase: {munji_purchase.category} from {supplier.name}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating MunjiPurchase: {e}'))

        # 4. Expenses
        for _ in range(15):
            if munji_purchases:
                munji_purchase = random.choice(munji_purchases)
                expense = Expense.objects.create(
                    munji_purchase=munji_purchase,
                    title=fake.sentence(nb_words=3),
                    amount=Decimal(random.uniform(5, 200)).quantize(Decimal('0.01'))
                )
                self.stdout.write(self.style.SUCCESS(f'Created Expense: {expense.title} for {munji_purchase.category}'))

        # 5. RiceProduction
        for _ in range(7):
            quantity_produced = Decimal(random.uniform(50, 500)).quantize(Decimal('0.01'))
            rice_price_per_unit = Decimal(random.uniform(20, 80)).quantize(Decimal('0.01'))
            total_quality = Decimal(random.uniform(quantity_produced * Decimal('0.8'), quantity_produced)).quantize(Decimal('0.01'))
            total_price = total_quality * rice_price_per_unit

            try:
                rice_production = RiceProduction.objects.create(
                    quantity_produced=quantity_produced,
                    dryer_cost=Decimal(random.uniform(100, 500)).quantize(Decimal('0.01')),
                    factory_cost=Decimal(random.uniform(200, 1000)).quantize(Decimal('0.01')),
                    wastage=Decimal(random.uniform(0.01, 0.1)).quantize(Decimal('0.01')),
                    quality_of_rice=Decimal(random.uniform(0.7, 0.95)).quantize(Decimal('0.01')),
                    rice_price_per_unit=rice_price_per_unit,
                    total_quality=total_quality,
                    total_price=total_price,
                    naku_price=Decimal(random.uniform(5, 20)).quantize(Decimal('0.01')),
                    naku_quantity=Decimal(random.uniform(10, 100)).quantize(Decimal('0.01'))
                )
                self.stdout.write(self.style.SUCCESS(f'Created RiceProduction: {rice_production.quantity_produced}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating RiceProduction: {e}'))

        self.stdout.write(self.style.SUCCESS('Random data generation complete.'))