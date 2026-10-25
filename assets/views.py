from django.shortcuts import render
from .models import Asset

# Create your views here.
def asset_list(request):
    assets = Asset.objects.all().order_by("asset_tag")

    context = {"assets": assets,}
    return render(request, "assets/asset_list.html", context)