# quotes/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Quotation, QuotationItem

class QuotationForm(forms.ModelForm):
    preferred_install_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        help_text="Optional preferred date"
    )

    class Meta:
        model = Quotation
        fields = [
            # Customer & site
            "customer_name", "customer_email", "reference_no",
            "site_address", "site_contact_name", "site_contact_phone", "preferred_install_date",
            # Charger & electrical
            "charger_type", "charger_power_kw", "phase", "mounting_type",
            "supply_type", "rcd_type", "cable_length_m",
            "civil_work", "interlock_removal", "earthing_required", "surge_protection",
            # Notes
            "notes",
        ]
        help_texts = {
            "charger_power_kw": "Common values: 7.4, 11, 22 for AC; 50+ for DC.",
            "cable_length_m": "Approximate cable/conduit run from supply to charger.",
        }

ItemFormSet = inlineformset_factory(
    Quotation, QuotationItem,
    fields=["description", "quantity", "unit_price"],
    extra=3, can_delete=True
)
class QuotationItemForm(forms.ModelForm):
    class Meta:
        model = QuotationItem
        fields = ["description", "quantity", "unit_price"]
        widgets = {
            "description": forms.TextInput(attrs={"placeholder": "e.g. Charger unit, installation labor"}),
            "quantity": forms.NumberInput(attrs={"min": 1}),
            "unit_price": forms.NumberInput(attrs={"step": "0.01"}),
        }
        help_texts = {
            "description": "Brief description of the item/service.",
            "quantity": "Number of units required.",
            "unit_price": "Price per unit in your local currency.",
        } 