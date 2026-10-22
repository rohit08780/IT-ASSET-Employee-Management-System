
from django import forms
from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = [
            "employee_id",
            "first_name",
            "last_name",
            "email",
            "department",
            "designation",
            "phone",
            "date_of_joining",
            "is_active",
        ]

        widgets = {
            "date_of_joining": forms.DateInput(
                attrs={"type": "date"}
            ),
        }

    def clean_employee_id(self):
        employee_id = self.cleaned_data["employee_id"].strip()

        existing = Employee.objects.filter(
            employee_id__iexact=employee_id
        )

        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)

        if existing.exists():
            raise forms.ValidationError(
                "This Employee ID already exists."
            )

        return employee_id

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        existing = Employee.objects.filter(
            email__iexact=email
        )

        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)

        if existing.exists():
            raise forms.ValidationError(
                "This email address is already registered."
            )

        return email

    def clean_phone(self):
        phone = self.cleaned_data.get("phone", "").strip()

        if phone and not phone.replace("+", "").isdigit():
            raise forms.ValidationError(
                "Enter a valid phone number using digits and an optional +."
            )

        if phone.count("+") > 1 or (
            "+" in phone and not phone.startswith("+")
        ):
            raise forms.ValidationError(
                "The + sign is allowed only at the beginning."
            )

        return phone
