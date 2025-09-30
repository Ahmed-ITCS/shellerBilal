from django.db import models
from django.core.exceptions import ValidationError

# Global settings
class GlobalSettings(models.Model):
    opening_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_munji = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return "Global Settings"

    class Meta:
        verbose_name_plural = "Global Settings"


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
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    total_bags = models.PositiveIntegerField()
    buying_quantity_munji = models.DecimalField(max_digits=12, decimal_places=2)
    munji_price_per_unit = models.DecimalField(max_digits=12, decimal_places=2)
    total_munji_price = models.DecimalField(max_digits=12, decimal_places=2)  # your existing field
    total_munji_cost = models.DecimalField(max_digits=12, decimal_places=2, editable=False,null=True)  # new field
    payment_type = models.CharField(max_length=10)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Validate total_munji_price
        if self.total_munji_price != self.buying_quantity_munji * self.munji_price_per_unit:
            raise ValidationError("Total Munji Price must equal buying quantity * price per unit.")

        # Check if opening_balance is sufficient for cash purchases
        if self.payment_type == self.CASH:
            gs = GlobalSettings.objects.first()
            if gs and self.total_munji_price > gs.opening_balance:
                raise ValidationError("Insufficient opening balance for this purchase.")

    def save(self, *args, **kwargs):
        # Calculate total_munji_cost automatically
        self.total_munji_cost = self.buying_quantity_munji * self.munji_price_per_unit

        self.full_clean()
        super().save(*args, **kwargs)

        # Update global settings
        gs, _ = GlobalSettings.objects.get_or_create(id=1)
        gs.total_munji += self.buying_quantity_munji
        if self.payment_type == self.CASH:
            gs.opening_balance -= self.total_munji_price
        gs.save()

class Expense(models.Model):
    munji_purchase = models.ForeignKey(MunjiPurchase, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.amount}"


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
        if not gs or self.quantity_produced > gs.total_munji:
            raise ValidationError("Not enough Munji in global total.")

        # total_price = total_quality * rice_price_per_unit
        if self.total_price != self.total_quality * self.rice_price_per_unit:
            raise ValidationError("Total price must equal total quality * rice price per unit.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

        # Deduct used munji from global
        gs = GlobalSettings.objects.first()
        if gs:
            gs.total_munji -= self.quantity_produced
            gs.save()
