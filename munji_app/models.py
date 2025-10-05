from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal, ROUND_HALF_UP

class GlobalSettings(models.Model):
    opening_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cash_in_hand = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_munji = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if not self.pk and GlobalSettings.objects.exists():
            raise ValidationError("Only one GlobalSettings instance is allowed.")
        return super().save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj

    def __str__(self):
        return "Global Settings"

    # --- ACCOUNTING RULES ---
    def add_capital(self, amount):
        """When capital is added, it increases opening balance."""
        self.opening_balance += amount
        self.save()

    def add_cash(self, amount):
        """
        When cash is injected:
        - Increase cash_in_hand
        - Decrease capital (opening_balance)
        """
        if self.opening_balance < amount:
            raise ValidationError("Not enough capital to convert to cash.")
        self.cash_in_hand += amount
        self.opening_balance -= amount
        self.save()

    def deduct_purchase(self, amount, munji_qty):
        """
        When a purchase is made:
        - Decrease cash_in_hand (if Cash payment)
        - Increase total_munji
        """
        if self.cash_in_hand < amount:
            raise ValidationError("Not enough cash in hand for this purchase.")

        self.cash_in_hand -= amount
        self.total_munji += munji_qty
        self.save()

    def deduct_expense(self, amount):
        """Deduct expense from cash in hand."""
        if self.cash_in_hand < amount:
            raise ValidationError("Not enough cash in hand to record expense.")
        self.cash_in_hand -= amount
        self.save()

    def deduct_miscellaneous(self, amount):
        """Deduct miscellaneous cost from cash in hand."""
        if self.cash_in_hand < amount:
            raise ValidationError("Not enough cash in hand to cover miscellaneous cost.")
        self.cash_in_hand -= amount
        self.save()

# Supplier / Buying source
class Supplier(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


# Category
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


# Munji Purchase
class MunjiPurchase(models.Model):
    CASH = "Cash"
    CREDIT = "Credit"
    PAYMENT_CHOICES = [
        (CASH, "Cash"),
        (CREDIT, "Credit"),
    ]

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE,null=True,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True,blank=True)
    total_bags = models.PositiveIntegerField()
    buying_quantity_munji = models.DecimalField(max_digits=12, decimal_places=2)
    munji_price_per_unit = models.DecimalField(max_digits=12, decimal_places=2)
    total_munji_price = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    total_munji_cost = models.DecimalField(max_digits=12, decimal_places=2, editable=False, null=True)
    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Check if opening_balance is sufficient for cash purchases
        if self.payment_type == self.CASH:
            gs = GlobalSettings.objects.first()
            if gs and self.total_munji_price > gs.opening_balance:
                raise ValidationError({"payment_type": "Insufficient opening balance for this purchase."})

    def save(self, *args, **kwargs):
        self.total_munji_price = (
            (self.buying_quantity_munji * self.munji_price_per_unit)
            .quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        )
        self.total_munji_cost = self.total_munji_price

        try:
            self.full_clean()
            super().save(*args, **kwargs)

            gs = GlobalSettings.get_instance()

            if self.payment_type == self.CASH:
                gs.deduct_purchase(self.total_munji_price, self.buying_quantity_munji)
            else:
                # Credit purchase → still increase munji, but no cash deduction
                gs.total_munji += self.buying_quantity_munji
                gs.save()

        except ValidationError as e:
            raise ValidationError(e)
        


class Expense(models.Model):
    munji_purchase = models.ForeignKey(MunjiPurchase, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        gs = GlobalSettings.get_instance()
        try:
            gs.deduct_expense(self.amount)
        except ValidationError as e:
            self.delete()  # rollback if invalid
            raise e

# Rice Production
class RiceProduction(models.Model):
    quantity_produced = models.DecimalField(max_digits=12, decimal_places=2)
    dryer_cost = models.DecimalField(max_digits=12, decimal_places=2)
    factory_cost = models.DecimalField(max_digits=12, decimal_places=2)
    wastage = models.DecimalField(max_digits=12, decimal_places=2)
    quality_of_rice = models.DecimalField(max_digits=12, decimal_places=2)
    rice_price_per_unit = models.DecimalField(max_digits=12, decimal_places=2)
    total_quality = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    naku_price = models.DecimalField(max_digits=12, decimal_places=2)
    naku_quantity = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        gs = GlobalSettings.objects.first()
        if not gs:
            raise ValidationError({"__all__": "Global settings not found."})
        if self.quantity_produced > gs.total_munji:
            raise ValidationError({"quantity_produced": "Not enough Munji in global total."})

        # total_price = total_quality * rice_price_per_unit
        if self.total_price != self.total_quality * self.rice_price_per_unit:
            raise ValidationError({"total_price": "Total price must equal total quality * rice price per unit."})

    def save(self, *args, **kwargs):
        try:
            self.full_clean()
            super().save(*args, **kwargs)

            # Deduct used munji from global
            gs = GlobalSettings.objects.first()
            if gs:
                gs.total_munji -= self.quantity_produced
                gs.save()
        except ValidationError as e:
            raise ValidationError(e)


class MiscellaneousCost(models.Model):
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        gs = GlobalSettings.get_instance()
        try:
            gs.deduct_miscellaneous(self.amount)
        except ValidationError as e:
            self.delete()  # rollback if invalid
            raise e