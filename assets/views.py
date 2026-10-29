from django.shortcuts import render, redirect
from .models import Asset, AssetHistory
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
            asset = form.save()

            AssetHistory.objects.create(
                asset=asset,
                action="Created",
                details=f"Asset {asset.asset_tag} was created."
            )
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
        old_asset_tag = asset.asset_tag
        old_asset_name = asset.asset_name
        old_brand = asset.brand
        old_status = asset.status
        old_assigned_to = asset.assigned_to

        form = AssetForm(request.POST, instance=asset)

        if form.is_valid():
            asset = form.save()
            changes = []

            if old_asset_tag != asset.asset_tag:
                changes.append(
                    f"Asset Tag: {old_asset_tag} -> {asset.asset_tag}"
                )

            if old_asset_name != asset.asset_name:
                changes.append(
                    f"Asset Name: {old_asset_name} -> {asset.asset_name}"
                )

            if old_brand != asset.brand:
                changes.append(
                    f"Brand: {old_brand} -> {asset.brand}"
                )

            if old_status != asset.status:
                changes.append(
                    f"Status: {old_status} -> {asset.status}"
                )

            if old_assigned_to != asset.assigned_to:
                old_employee = (
                    str(old_assigned_to)
                    if old_assigned_to else "Unassigned"
                )
                new_employee = (
                    str(asset.assigned_to)
                    if asset.assigned_to else "Unassigned"
                )

                changes.append(
                    f"Assigned To: {old_employee} -> {new_employee}"
                )

            if changes:
                AssetHistory.objects.create(
                    asset=asset,
                    action="Updated",
                    details="; ".join(changes)
                )

            return redirect("asset_list")
    else:
        form = AssetForm(instance=asset)

    return render(
        request,
        "assets/asset_form.html",
        {"form": form}
    )


def asset_delete(request, pk):
    asset = get_object_or_404(Asset, pk=pk)

    if request.method == "POST":
        asset_tag = asset.asset_tag
        asset_name = asset.asset_name
        AssetHistory.objects.create(
            asset = asset,
            action="Deleted",
            details=f"Asset {asset_tag} - {asset_name} was deleted."
        )
        asset.delete()
        return redirect("asset_list")

    return render(
        request,
        "assets/asset_confirm_delete.html",
        {"asset": asset}
    )


def asset_detail(request, pk):
    asset = get_object_or_404(Asset, pk=pk)
    history = asset.history.order_by("-changed_at")

    return render(
        request,
        "assets/asset_detail.html",
        {"asset": asset, "history": history,}
    )
