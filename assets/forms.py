
from django import forms
from .models import Asset


class AssetForm(forms.ModelForm):

    class Meta:
        model = Asset
        fields = [
            "asset_tag",
            "asset_name",
            "category",
            "brand",
            "serial_number",
            "purchase_date",
            "status",
        ]

        widgets = {
            "purchase_date": forms.DateInput(
                attrs={"type": "date"}
            ),
        }
