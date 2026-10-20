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
			"date_of_joining": forms.DateInput(attrs={"type": "date"}),
		}
