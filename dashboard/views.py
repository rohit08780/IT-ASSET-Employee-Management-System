
from django.shortcuts import render
from employees.models import Employee
from django.db.models import Count

# Create your views here.

def home(request):
	total_employees = Employee.objects.count()
	active_employees = Employee.objects.filter(is_active=True).count()
	inactive_employees = Employee.objects.filter(is_active=False).count()
	total_departments = (Employee.objects.values("department").distinct().count())
	department_counts = (Employee.objects.values("department").annotate(employee_count=Count("id")).order_by("department"))
	context = {"total_employees": total_employees, "active_employees": active_employees, "inactive_employees": inactive_employees, "total_departments": total_departments, "department_counts": department_counts,}
	return render(request, "dashboard/home.html", context)