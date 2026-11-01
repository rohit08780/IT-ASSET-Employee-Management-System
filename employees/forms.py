
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

        # Phone number is optional
        if not phone:
            return phone

        # Must contain exactly 10 digits
        if not phone.isdigit() or len(phone) != 10:
            raise forms.ValidationError(
                "Enter a valid 10-digit mobile number."
            )

        # Indian mobile number must start with 6, 7, 8, or 9
        if phone[0] not in "6789":
            raise forms.ValidationError(
                "Mobile number must start with 6, 7, 8, or 9."
            )

        return phone
