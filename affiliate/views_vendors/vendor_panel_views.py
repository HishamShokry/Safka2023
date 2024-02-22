from django.contrib.auth.decorators import login_required
from affiliate.models import *
from affiliate.forms import *
from accounts.decorators import vendor_required
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404



""" 
 Vendor Panel
"""


@login_required()
@vendor_required
def vendor_index(request):
    return render(request, "vendors/dashboard.html")


@login_required()
@vendor_required
def vendor_dashboard(request):
    return render(request, "vendors/dashboard.html")



@login_required
@vendor_required
def vendor_products(request):
    products_list = Product.objects.filter(vendor=request.user)
    
    paginator = Paginator(products_list, 12)  # Show 12 products per page

    page = request.GET.get("page")
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)


    return render(
        request, "vendors/pages/affilate/products.html", {"products": products}
    )


@login_required
@vendor_required
def vendor_product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    # Check if the currently authenticated user is the owner of the product
    if request.user == product.vendor:
        return render(
            request, "vendors/pages/affilate/product_detail.html", {"product": product}
        )
    else:
        # You can handle unauthorized access in a way that fits your application
        # For example, you may redirect the user or show an error message
                raise Http404("Product not found or you do not have permission to view it.")




@login_required
@vendor_required
def vendor_orders(request):
    return render(
        request,
        "vendors/pages/affilate/new_orders.html",
    )

@login_required
@vendor_required
def vendor_requests(request):
    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save()  # This saves the new category to the database
    else:
        form = RequestForm()
    return render(request, "vendors/pages/affilate/requests.html", {'form': form})


@login_required
@vendor_required
def vendor_support(request):
    return render(request, "vendors/support.html")


@login_required
@vendor_required
def vendor_profile(request):
    return render(request, "vendors/profile.html")
