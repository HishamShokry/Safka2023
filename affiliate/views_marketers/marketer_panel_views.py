from django.contrib.auth.decorators import login_required
from affiliate.models import *
from affiliate.forms import *
from accounts.decorators import marketer_required
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import get_list_or_404, render


""" 
 Marketer Panel
"""


@login_required()
@marketer_required
def marketer_index(request):
    return render(request, "marketers/dashboard.html")


@login_required()
@marketer_required
def marketer_dashboard(request):
    return render(request, "marketers/dashboard.html")


@login_required()
@marketer_required
def marketer_products(request):
    products_list = get_list_or_404(Product)
    paginator = Paginator(products_list, 12)  # Show 12 products per page

    page = request.GET.get("page")
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(
        request, "marketers/pages/affilate/products.html", {"products": products}
    )


@login_required()
@marketer_required
def marketer_product_detail(request, id):
    product = Product.objects.get(id=id)

    return render(
        request, "marketers/pages/affilate/product_detail.html", {"product": product}
    )


@login_required
@marketer_required
def marketer_orders(request):
    if request.method == "POST":
        form = OrderFormMarketer(request.POST, request.FILES)
        order_items = OrderFormMarketer.items(request.POST, request.FILES, instance=Product())
        if form.is_valid() and order_items.is_valid():
            # Process form data, including the uploaded file
            product = form.save()
            order_items.instance = product
            order_items.save()
            return JsonResponse({"detail": "Product created successfully"})

        else:
            return JsonResponse({"detail": "Invalid form data"}, status=400)
    else:
        form = OrderFormMarketer()
        order_items = OrderFormMarketer.items(instance=Product())
    return render(
        request,
        "marketers/pages/affilate/new_orders.html",
        { "form": form, "variant_formset": order_items},
    )




@login_required
@marketer_required
def marketer_requests(request):
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save()  # This saves the new category to the database
    else:
        form = RequestForm()
    return render(request, "marketers/pages/affilate/requests.html", { "form": form})



@login_required
@marketer_required
def marketer_support(request):
    return render(request, "marketers/support.html")


@login_required
@marketer_required
def marketer_profile(request):
    return render(request, "marketers/profile.html")






