# quotes/models.py
from django.db import models
from django.utils import timezone

class Quotation(models.Model):
    # --- Existing fields ---
    customer_name  = models.CharField(max_length=200)
    customer_email = models.EmailField(blank=True)
    reference_no   = models.CharField(max_length=50, blank=True)
    notes          = models.TextField(blank=True)
    created_at     = models.DateTimeField(default=timezone.now)

    # --- EV charger fields ---
    CHARGER_TYPE_CHOICES = [
        ("ac", "AC Charger"),
        ("dc", "DC Fast Charger"),
    ]
    PHASE_CHOICES = [
        ("single", "Single-phase"),
        ("three", "Three-phase"),
    ]
    MOUNTING_CHOICES = [
        ("wall", "Wall-mounted"),
        ("pedestal", "Pedestal/Stand"),
    ]
    SUPPLY_TYPE_CHOICES = [
        ("existing", "Use existing supply"),
        ("new_circuit", "New dedicated circuit"),
        ("upgrade", "Supply upgrade required"),
    ]
    RCD_TYPE_CHOICES = [
        ("type_a", "Type A"),
        ("type_b", "Type B"),
        ("rcbo", "RCBO"),
        ("other", "Other/Consult"),
    ]

    charger_type = models.CharField(max_length=10, choices=CHARGER_TYPE_CHOICES, default="ac")
    charger_power_kw = models.DecimalField(max_digits=5, decimal_places=2, default=7.00, help_text="e.g. 7.4, 11, 22, 50")
    phase = models.CharField(max_length=10, choices=PHASE_CHOICES, default="single")
    mounting_type = models.CharField(max_length=10, choices=MOUNTING_CHOICES, default="wall")

    civil_work = models.BooleanField(default=False, help_text="Trenching, core drilling, base/stand, etc.")
    interlock_removal = models.BooleanField(default=False, help_text="Remove/adjust interlock if present")
    earthing_required = models.BooleanField(default=True)
    surge_protection = models.BooleanField(default=True)

    supply_type = models.CharField(max_length=20, choices=SUPPLY_TYPE_CHOICES, default="existing")
    rcd_type = models.CharField(max_length=10, choices=RCD_TYPE_CHOICES, default="type_a")
    cable_length_m = models.DecimalField(max_digits=6, decimal_places=2, default=10.00, help_text="Approximate run in meters")

    site_address = models.CharField(max_length=255, blank=True)
    site_contact_name = models.CharField(max_length=200, blank=True)
    site_contact_phone = models.CharField(max_length=50, blank=True)
    preferred_install_date = models.DateField(null=True, blank=True)

    @property
    def subtotal(self):
        return sum(item.line_total for item in self.items.all())

    def __str__(self):
        return f"Quotation #{self.pk} • {self.customer_name}"


class QuotationItem(models.Model):
    quotation   = models.ForeignKey(Quotation, related_name="items", on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    quantity    = models.PositiveIntegerField(default=1)
    unit_price  = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def line_total(self):
        return self.quantity * self.unit_price
