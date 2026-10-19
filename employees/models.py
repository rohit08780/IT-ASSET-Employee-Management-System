from django.db import models


# Create your models here.
class Employee(models.Model):
	employee_id = models.CharField(max_length=20,unique=True)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.EmailField(unique=True)
	department = models.CharField(max_length=100)
	designation = models.CharField(max_length=100)
	phone = models.CharField(max_length=15,blank=True)
	date_of_joining = models.DateField()
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.employee_id} - {self.first_name} {self.last_name}"