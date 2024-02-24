from django.contrib.auth.decorators import login_required
from affiliate.models import *
from django.db.models import Count, Q
from affiliate.forms import *
from accounts.decorators import admin_required
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import get_list_or_404, render
from datetime import datetime, timedelta
from accounts.models import User



# from affiliate.views import 



""" 
 Admin Panel
"""


@login_required()
@admin_required
def index(request):
    return render(request, "dashboard.html")


def dashboard(request):
    # Calculate counts for today, this week, this month, and total
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    # Orders counts
    orders_today = Order.objects.filter(created_at__date=today).count()
    orders_this_week = Order.objects.filter(created_at__date__gte=start_of_week).count()
    orders_this_month = Order.objects.filter(created_at__date__gte=start_of_month).count()
    total_orders = Order.objects.all().count()

    # Users counts
    total_users = User.objects.all().count()


    # Products counts
    total_products = Product.objects.all().count()


    # Top Marketers
    top_marketers = User.objects.filter(is_marketer=True).values('email').annotate(
        order_count=Count('marketer_orders')
    ).order_by(
        '-order_count'
    )[:10]


    top_marketers_this_week = User.objects.filter(is_marketer=True).values('email').annotate(
        order_count=Count('marketer_orders', filter=Q(marketer_orders__created_at__gte=start_of_week))
    ).order_by(
        '-order_count'
    )[:10]


    top_marketers_this_month = User.objects.filter(is_marketer=True).values('email').annotate(
        order_count=Count('marketer_orders', filter=Q(marketer_orders__created_at__gte=start_of_month))
    ).order_by(
        '-order_count'
    )[:10]






    data_points = Order.objects.values_list('created_at__month').annotate(count=Count('id')).order_by('created_at__month')
    arabic_month_names = [
    'يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو',
    'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر'
    ]

    
    labels = [f'{arabic_month_names[point[0] - 1]}' for point in data_points]
    values = [point[1] for point in data_points]

    sales_chart = {
        'labels': labels,
        'values': values,
    }


    governorate_data = (
        ShippingPrice.objects.annotate(order_count=Count('order'))
        .values('governorate__governorate_name_ar', 'order_count')
    )

    # Extracting labels and values for the chart
    governorate_labels = [entry['governorate__governorate_name_ar'] for entry in governorate_data]
    governorate_values = [entry['order_count'] for entry in governorate_data]


    governorate_chart = {
            'labels': governorate_labels,
            'values': governorate_values,
        }

    print(governorate_chart)

    context = {
        'orders_today': orders_today,
        'orders_this_week': orders_this_week,
        'orders_this_month': orders_this_month,
        'total_orders': total_orders,
        'total_users': total_users,
        'total_products': total_products,
        'top_marketers': top_marketers,
        'top_marketers_this_week': top_marketers_this_week,
        'top_marketers_this_month': top_marketers_this_month,
        'sales_chart': sales_chart,
        'governorate_chart': governorate_chart,
    }

    return render(request, "dashboard.html", context)

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

