from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee
from .forms import EmployeeForm
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.

def employee_list(request):
	query = request.GET.get("q","")
	selected_department = request.GET.get("department", "")
	selected_status = request.GET.get("status", "")

	employees = Employee.objects.all().order_by("employee_id")

	if query:
		employees = employees.filter(
			Q(employee_id__icontains=query)|
			Q(first_name__icontains=query)|
			Q(last_name__icontains=query)|
			Q(email__icontains=query)|
			Q(department__icontains=query)|
			Q(designation__icontains=query)
		)

	if selected_department:
		employees = employees.filter(department=selected_department)
	departments = Employee.objects.order_by("department").values_list("department", flat=True).distinct()

	if selected_status == "active":
		employees = employees.filter(is_active=True)
	elif selected_status == "inactive":
		employees = employees.filter(is_active=False)

	paginator = Paginator(employees,5)
	page_number = request.GET.get("page")
	page_obj = paginator.get_page(page_number)

	return render(
		request,
		"employees/employee_list.html",
		{"employees": page_obj, "query": query, "departments": departments, "selected_department": selected_department, "selected_status": selected_status, "page_obj": page_obj,}
	)

def employee_create(request):
	if request.method == "POST":
		form = EmployeeForm(request.POST)

		if form.is_valid():
			form.save()
			return redirect("employee_list")

	else:
		form = EmployeeForm()

	return render(
		request,
		"employees/employee_form.html",
		{"form": form}
	)


def employee_update(request, pk):
	employee = Employee.objects.get(pk=pk)

	if request.method == "POST":
		form = EmployeeForm(request.POST, instance=employee)

		if form.is_valid():
			form.save()
			return redirect("employee_list")

	else:
		form = EmployeeForm(instance=employee)

	return render(
		request, "employees/employee_form.html",{"form": form}
	)

def employee_delete(request,pk):
	employee = get_object_or_404(Employee, pk=pk)

	if request.method == "POST":
		employee.delete()
		return redirect("employee_list")
	
	return render(
		request, "employees/employee_confirm_delete.html", {"employee": employee}
	)

def employee_detail(request,pk):
	employee = get_object_or_404(Employee, pk=pk)

	return render(request, "employees/employee_detail.html", {"employee":employee})
