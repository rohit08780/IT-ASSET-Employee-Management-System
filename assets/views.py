from django.shortcuts import render
from .models import Asset

# Create your views here.
def asset_list(request):
    assets = Asset.objects.all().order_by("asset_tag")
    search_query = request.GET.get("q", "")
    category_filter = request.GET.get("category", "")
    status_filter = request.GET.get("status", "")

    if search_query:
        assets = assets.filter(
            asset_tag__icontains=search_query
        ) | assets.filter(
            asset_name__icontains=search_query
        ) | assets.filter(
            brand__icontains=search_query
        )

    if category_filter:
        assets = assets.filter(category=category_filter)

    if status_filter:
        assets = assets.filter(status=status_filter)


    context = {"assets": assets, "search_query": search_query, "category_filter": category_filter, "categories": Asset.CATEGORY_CHOICES, "status_filter": status_filter, "statuses": Asset.STATUS_CHOICES,}
    return render(request, "assets/asset_list.html", context)