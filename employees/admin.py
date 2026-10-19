from django.contrib import admin
from .models import Employee
# Register your models here.

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
	list_display = (
		"employee_id",
		"first_name",
		"last_name",
		"department",
		"designation",
		"is_active",
	)

	search_fields = (
		"employee_id",
		"first_name",
		"last_name",
		"email",
	)

	list_filter = ("department", "is_active")