from django.db import models
from employees.models import Employee

# Create your models here.
class Asset(models.Model):
    CATEGORY_CHOICES = [("Laptop", "Laptop"),
                        ("Desktop", "Desktop"),
                        ("Monitor", "Monitor"),
                        ("Keyboard", "Keyboard"),
                        ("Mouse", "Mouse"),
                        ("Printer", "Printer"),
                        ("Other", "Other"),
                        ]

    STATUS_CHOICES = [
        ("Available", "Available"),
        ("Assigned", "Assigned"),
        ("Under Repair", "Under Repair"),
        ("Retired", "Retired"),
    ]

    asset_tag = models.CharField(max_length=30, unique=True)
    asset_name = models.CharField(max_length=100)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES,)
    brand = models.CharField(max_length=100, blank=True)
    serial_number = models.CharField(max_length=100, unique=True, null=True,blank=True)
    purchase_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Available",)
    assigned_to = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_assets"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.asset_tag} - {self.asset_name}"