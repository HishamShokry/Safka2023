from django.contrib.auth.decorators import login_required
from affiliate.models import *
from affiliate.forms import *
from accounts.decorators import admin_required
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import get_list_or_404, render


# from affiliate.views import 



""" 
 Admin Panel
"""


@login_required()
@admin_required
def index(request):
    return render(request, "dashboard.html")


@login_required()
@admin_required
def dashboard(request):
    return render(request, "dashboard.html")


@login_required
@admin_required
def category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()  # This saves the new category to the database
    else:
        form = CategoryForm()
    # categories = Category.objects.all()
    return render(request, "pages/affilate/category.html", {"form": form})


@login_required
@admin_required
def list_of_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        variant_formset = ProductForm.product_variant_set(
            request.POST, request.FILES, instance=Product()
        )
        if form.is_valid() and variant_formset.is_valid():
            # Process form data, including the uploaded file
            product = form.save()
            variant_formset.instance = product
            variant_formset.save()
            return JsonResponse({"detail": "Product created successfully"})
        else:
            return JsonResponse({"detail": "Invalid form data"}, status=400)

    else:
        form = ProductForm()
        variant_formset = ProductForm.product_variant_set(instance=Product())
    return render(
        request,
        "pages/affilate/products_list.html",
        {"form": form, "variant_formset": variant_formset},
    )


@login_required
@admin_required
def products(request):
    products_list = Product.objects.all()
    paginator = Paginator(products_list, 12)  # Show 12 products per page

    page = request.GET.get("page")
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request, "pages/affilate/products.html", {"products": products})


@login_required
@admin_required
def product_detail(request, id):
    product = Product.objects.get(id=id)

    return render(request, "pages/affilate/product_detail.html", {"product": product})


@login_required
@admin_required
def shipping(request):
    if request.method == "POST":
        form = ShippingForm(request.POST)
        if form.is_valid():
            form.save()  # This saves the new category to the database
    else:
        form = ShippingForm()
    return render(request, "pages/affilate/shipping.html", {"form": form})


@login_required
@admin_required
def shipping_price(request):
    if request.method == "POST":
        form = ShippingPriceForm(request.POST)
        if form.is_valid():
            form.save()  # This saves the new category to the database
    else:
        form = ShippingPriceForm()
    return render(request, "pages/affilate/shippingPrice.html", {"form": form})


@login_required
@admin_required
def inventory(request):
    if request.method == "POST":
        form = InventoryForm(request.POST)
        if form.is_valid():
            form.save()  # This saves the new category to the database
    else:
        form = InventoryForm()
    return render(request, "pages/affilate/inventory.html", {"form": form})


@login_required
@admin_required
def orders(request):
    if request.method == "POST":
        form = OrderForm(request.POST, request.FILES, user=request.user)
        order_items = OrderForm.items(request.POST, request.FILES, instance=Product())
        if form.is_valid() and order_items.is_valid():
            # Process form data, including the uploaded file
            product = form.save()
            order_items.instance = product
            order_items.save()
            return JsonResponse({"detail": "Product created successfully"})

        else:
            return JsonResponse({"detail": "Invalid form data"}, status=400)
    else:
        form = OrderForm(user=request.user)
        order_items = OrderForm.items(instance=Product())
    return render(
        request,
        "pages/affilate/new_orders.html",
        { "form": form, "variant_formset": order_items},
    )


@login_required
@admin_required
def requests(request):
    if request.method == "POST":
        form = RequestFormِAdmin(request.POST, request.FILES)
        if form.is_valid():
            # Process form data, including the uploaded file
            request = form.save()
            return JsonResponse({"detail": "Product created successfully"})
        else:
            return JsonResponse({"detail": "Invalid form data"}, status=400)
    else:
        form = RequestFormِAdmin()
    return render(request, "pages/affilate/requests.html", {'form': form})


@login_required
@admin_required
def vendors_accounts(request):
    return render(request, "pages/affilate/vendors.html")


@login_required
@admin_required
def marketers_accounts(request):
    return render(request, "pages/affilate/marketers.html")


@login_required
@admin_required
def support(request):
    return render(request, "support.html")


@login_required
@admin_required
def profile(request):
    return render(request, "profile.html")

