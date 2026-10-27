
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
            "assigned_to",
        ]

        widgets = {
            "purchase_date": forms.DateInput(
                attrs={"type": "date"}
            ),
        }

    def clean(self):
        cleaned_data = super().clean()

        status = cleaned_data.get("status")
        assigned_to = cleaned_data.get("assigned_to")

        if status == "Assigned" and not assigned_to:
            self.add_error(
                "assigned_to",
                "Please select an employee when asset status is Assigned."
            )

        return cleaned_data
