from django.shortcuts import render, redirect
from .models import Asset
from .forms import AssetForm
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
def asset_list(request):
    assets = Asset.objects.all().order_by("asset_tag")
    sort_by = request.GET.get("sort", "asset_tag")
    allowed_sort_fields = [
        "asset_tag",
        "asset_name",
        "status",
    ]

    if sort_by not in allowed_sort_fields:
        sort_by = "asset_tag"

    assets = assets.order_by(sort_by)
    total_assets = Asset.objects.count()
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


    context = {"assets": assets, "search_query": search_query, "category_filter": category_filter, "categories": Asset.CATEGORY_CHOICES, "status_filter": status_filter, "statuses": Asset.STATUS_CHOICES, "total_assets": total_assets,}
    return render(request, "assets/asset_list.html", context)


def asset_create(request):
    if request.method == "POST":
        form = AssetForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("asset_list")
    else:
        form = AssetForm()

    return render(
        request,
        "assets/asset_form.html",
        {"form": form}
    )


def asset_edit(request, pk):
    asset = get_object_or_404(Asset, pk=pk)

    if request.method == "POST":
        form = AssetForm(request.POST, instance=asset)

        if form.is_valid():
            form.save()
            return redirect("asset_list")
    else:
        form = AssetForm(instance=asset)

    return render(
        request,
        "assets/asset_form.html",
        {"form": form}
    )

