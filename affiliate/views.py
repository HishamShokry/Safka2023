from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db import transaction
from affiliate.forms import *
from .models import *
from django.shortcuts import get_list_or_404, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from accounts.decorators import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, F  # Import Q for complex queries
from .permissions import *

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import *
from rest_framework.decorators import action, api_view
from rest_framework import status
from rest_framework import generics, permissions

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
    products = Product.objects.all()
    return render(
        request,
        "pages/affilate/products_list.html",
        {"products": products, "form": form, "variant_formset": variant_formset},
    )


@login_required
@admin_required
def products(request):
    products_list = get_list_or_404(Product)
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
    order = Order.objects.all()
    return render(
        request,
        "pages/affilate/new_orders.html",
        {"order": order, "form": form, "variant_formset": order_items},
    )


@login_required
@admin_required
def requests(request):
    return render(request, "pages/affilate/requests.html")


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
    products = Product.objects.all()

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
    return render(request, "marketers/pages/affilate/orders.html")


@login_required
@marketer_required
def marketer_requests(request):
    return render(request, "marketers/pages/affilate/requests.html")


@login_required
@marketer_required
def marketer_support(request):
    return render(request, "marketers/support.html")


@login_required
@marketer_required
def marketer_profile(request):
    return render(request, "marketers/profile.html")


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
def vendor_category(request):
    return render(request, "vendors/pages/affilate/category.html")


@login_required
@vendor_required
def vendor_products(request):
    products = Product.objects.all()

    return render(
        request, "vendors/pages/affilate/products.html", {"products": products}
    )


@login_required
@vendor_required
def vendor_product_detail(request, id):
    product = Product.objects.get(id=id)

    return render(
        request, "vendors/pages/affilate/product_detail.html", {"product": product}
    )


@login_required
@vendor_required
def vendor_shipping(request):
    return render(request, "vendors/pages/affilate/shipping.html")


@login_required
@vendor_required
def vendor_inventory(request):
    return render(request, "vendors/pages/affilate/inventory.html")


@login_required
@vendor_required
def vendor_orders(request):
    return render(request, "vendors/pages/affilate/orders.html")


@login_required
@vendor_required
def vendor_requests(request):
    return render(request, "vendors/pages/affilate/requests.html")


@login_required
@vendor_required
def vendor_support(request):
    return render(request, "vendors/support.html")


@login_required
@vendor_required
def vendor_profile(request):
    return render(request, "vendors/profile.html")


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True, methods=["get"])
    def datatable_list(self, request, *args, **kwargs):
        try:
            draw = int(request.GET.get("draw", 1))
            start = int(request.GET.get("start", 0))
            length = int(request.GET.get("length", 10))
            global_search_value = request.GET.get("search[value]", "")
            start_date, end_date = request.GET.get("start_date", ""), request.GET.get(
                "end_date", ""
            )

            # Split the global search value into individual terms
            global_search_terms = global_search_value.split()

            # Start with an empty Q object to build the OR conditions for global search
            global_q_object = Q()

            # Build an OR condition for each term in the global search
            for term in global_search_terms:
                global_q_object |= Q(name__icontains=term)
                # Add other global search columns as needed

            # Filter data based on the constructed Q object for global search
            categories = self.queryset.filter(global_q_object)

            # Apply date range filter
            if start_date and end_date:
                categories = categories.filter(updated_at__range=[start_date, end_date])

            # Handle individual column searches
            extra_search = {}
            for key, value in request.GET.items():
                if key.startswith("extra_search[") and value:
                    column_name = key[
                        len("extra_search[") : -1
                    ]  # Extract the column name from the key
                    extra_search[f"{column_name}__icontains"] = value

            # Apply individual column filters
            if extra_search:
                categories = categories.filter(**extra_search)

            # Apply sorting
            order_column_index = int(request.GET.get("order[0][column]", 0))
            order_direction = request.GET.get("order[0][dir]", "asc")

            # Map DataTables column index to your model fields
            order_columns = [
                "id",
                "name",
                "created_at",
                "updated_at",
            ]  # Adjust as needed

            # Apply sorting
            order_column_name = order_columns[order_column_index]
            if order_direction == "desc":
                order_column_name = f"-{order_column_name}"

            categories = categories.order_by(order_column_name)

            # Count total records after filtering
            total_records = categories.count()

            # Apply pagination
            categories = categories[start : start + length]

            serializer = CategorySerializer(categories, many=True)

            response_data = {
                "draw": draw,
                "recordsTotal": total_records,
                "recordsFiltered": total_records,
                "data": serializer.data,
            }

            return Response(response_data)

        except Exception as e:
            # Handle exceptions, log the error, and return an appropriate response
            return Response({"error": str(e)})

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=201, headers=headers)

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop("partial", False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response(status=204)

    # def create(self, request, *args, **kwargs):
    #     try:
    #         if request.method == "POST":
    #             serializer = CategorySerializer(data=request.data)
    #             if serializer.is_valid():
    #                 # Check for duplicate category name
    #                 name = serializer.validated_data.get("name")
    #                 if Category.objects.filter(name=name).exists():
    #                     return Response(
    #                         {
    #                             "success": False,
    #                             "errors": serializer.errors,
    #                             "message": "Category with this name already exists",
    #                         },
    #                         status=status.HTTP_400_BAD_REQUEST,
    #                     )

    #                 serializer.save()
    #                 return Response(
    #                     {"success": True, "message": "Category created successfully"},
    #                     serializer.data,
    #                     status=status.HTTP_201_CREATED,
    #                 )

    #             else:
    #                 return Response(
    #                     {"success": False, "errors": serializer.errors},
    #                     status=status.HTTP_400_BAD_REQUEST,
    #                 )

    #         return Response(
    #             {"success": False, "error": "Invalid request method"},
    #             status=status.HTTP_405_METHOD_NOT_ALLOWED,
    #         )
    #     except Exception as e:
    #         return Response(
    #             {"success": False, "error": str(e)},
    #             status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         )


class InventoryViewSet(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True, methods=["get"])
    def datatable_list(self, request, *args, **kwargs):
        try:
            draw = int(request.GET.get("draw", 1))
            start = int(request.GET.get("start", 0))
            length = int(request.GET.get("length", 10))
            global_search_value = request.GET.get("search[value]", "")
            start_date, end_date = request.GET.get("start_date", ""), request.GET.get(
                "end_date", ""
            )

            # Split the global search value into individual terms
            global_search_terms = global_search_value.split()

            # Start with an empty Q object to build the OR conditions for global search
            global_q_object = Q()

            # Build an OR condition for each term in the global search
            for term in global_search_terms:
                global_q_object |= Q(name__icontains=term)
                # Add other global search columns as needed

            # Filter data based on the constructed Q object for global search
            inventories = self.queryset.filter(global_q_object)

            # Apply date range filter
            if start_date and end_date:
                inventories = inventories.filter(
                    updated_at__range=[start_date, end_date]
                )

            # Handle individual column searches
            extra_search = {}
            for key, value in request.GET.items():
                if key.startswith("extra_search[") and value:
                    column_name = key[
                        len("extra_search[") : -1
                    ]  # Extract the column name from the key
                    extra_search[f"{column_name}__icontains"] = value

            # Apply individual column filters
            if extra_search:
                inventories = inventories.filter(**extra_search)

            # Apply sorting
            order_column_index = int(request.GET.get("order[0][column]", 0))
            order_direction = request.GET.get("order[0][dir]", "asc")

            # Map DataTables column index to your model fields
            order_columns = [
                "id",
                "name",
                "created_at",
                "updated_at",
            ]  # Adjust as needed

            # Apply sorting
            order_column_name = order_columns[order_column_index]
            if order_direction == "desc":
                order_column_name = f"-{order_column_name}"

            inventories = inventories.order_by(order_column_name)

            # Count total records after filtering
            total_records = inventories.count()

            # Apply pagination
            inventories = inventories[start : start + length]

            serializer = InventorySerializer(inventories, many=True)

            response_data = {
                "draw": draw,
                "recordsTotal": total_records,
                "recordsFiltered": total_records,
                "data": serializer.data,
            }

            return Response(response_data)

        except Exception as e:
            # Handle exceptions, log the error, and return an appropriate response
            return Response({"error": str(e)})

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=201, headers=headers)

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop("partial", False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)

    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response(status=204)

    # def create(self, request, *args, **kwargs):
    #     try:
    #         if request.method == "POST":
    #             serializer = CategorySerializer(data=request.data)
    #             if serializer.is_valid():
    #                 # Check for duplicate category name
    #                 name = serializer.validated_data.get("name")
    #                 if Category.objects.filter(name=name).exists():
    #                     return Response(
    #                         {
    #                             "success": False,
    #                             "errors": serializer.errors,
    #                             "message": "Category with this name already exists",
    #                         },
    #                         status=status.HTTP_400_BAD_REQUEST,
    #                     )

    #                 serializer.save()
    #                 return Response(
    #                     {"success": True, "message": "Category created successfully"},
    #                     serializer.data,
    #                     status=status.HTTP_201_CREATED,
    #                 )

    #             else:
    #                 return Response(
    #                     {"success": False, "errors": serializer.errors},
    #                     status=status.HTTP_400_BAD_REQUEST,
    #                 )

    #         return Response(
    #             {"success": False, "error": "Invalid request method"},
    #             status=status.HTTP_405_METHOD_NOT_ALLOWED,
    #         )
    #     except Exception as e:
    #         return Response(
    #             {"success": False, "error": str(e)},
    #             status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         )


class ShippingCompanyViewSetAdmin(viewsets.ModelViewSet):
    queryset = ShippingCompany.objects.all()
    serializer_class = ShippingCompanySerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True, methods=["get"])
    def datatable_list(self, request, *args, **kwargs):
        try:
            draw = int(request.GET.get("draw", 1))
            start = int(request.GET.get("start", 0))
            length = int(request.GET.get("length", 10))
            global_search_value = request.GET.get("search[value]", "")
            start_date, end_date = request.GET.get("start_date", ""), request.GET.get(
                "end_date", ""
            )

            # Split the global search value into individual terms
            global_search_terms = global_search_value.split()

            # Start with an empty Q object to build the OR conditions for global search
            global_q_object = Q()

            # Build an OR condition for each term in the global search
            for term in global_search_terms:
                global_q_object |= Q(name__icontains=term)
                # Add other global search columns as needed

            # Filter data based on the constructed Q object for global search
            company = self.queryset.filter(global_q_object)

            # Apply date range filter
            if start_date and end_date:
                company = company.filter(updated_at__range=[start_date, end_date])

            # Handle individual column searches
            extra_search = {}
            for key, value in request.GET.items():
                if key.startswith("extra_search[") and value:
                    column_name = key[
                        len("extra_search[") : -1
                    ]  # Extract the column name from the key
                    extra_search[f"{column_name}__icontains"] = value

            # Apply individual column filters
            if extra_search:
                company = company.filter(**extra_search)

            # Apply sorting
            order_column_index = int(request.GET.get("order[0][column]", 0))
            order_direction = request.GET.get("order[0][dir]", "asc")

            # Map DataTables column index to your model fields
            order_columns = [
                "id",
                "name",
                "website",
                "created_at",
                "updated_at",
            ]  # Adjust as needed

            # Apply sorting
            order_column_name = order_columns[order_column_index]
            if order_direction == "desc":
                order_column_name = f"-{order_column_name}"

            company = company.order_by(order_column_name)

            # Count total records after filtering
            total_records = company.count()

            # Apply pagination
            company = company[start : start + length]

            serializer = ShippingCompanySerializer(company, many=True)

            response_data = {
                "draw": draw,
                "recordsTotal": total_records,
                "recordsFiltered": total_records,
                "data": serializer.data,
            }

            return Response(response_data)

        except Exception as e:
            # Handle exceptions, log the error, and return an appropriate response
            return Response({"error": str(e)})


class ShippingPriceViewSetAdmin(viewsets.ModelViewSet):
    queryset = ShippingPrice.objects.all()
    serializer_class = ShippingPriceSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True, methods=["get"])
    def datatable_list(self, request, *args, **kwargs):
        try:
            draw = int(request.GET.get("draw", 1))
            start = int(request.GET.get("start", 0))
            length = int(request.GET.get("length", 10))
            global_search_value = request.GET.get("search[value]", "")
            start_date, end_date = request.GET.get("start_date", ""), request.GET.get(
                "end_date", ""
            )

            # Split the global search value into individual terms
            global_search_terms = global_search_value.split()

            # Start with an empty Q object to build the OR conditions for global search
            global_q_object = Q()

            # Build an OR condition for each term in the global search
            for term in global_search_terms:
                global_q_object |= Q(governorate__name__icontains=term)
                # Add other global search columns as needed

            # Filter data based on the constructed Q object for global search
            company = self.queryset.filter(global_q_object)

            # Apply date range filter
            if start_date and end_date:
                company = company.filter(updated_at__range=[start_date, end_date])

            # Handle individual column searches
            extra_search = {}
            for key, value in request.GET.items():
                if key.startswith("extra_search[") and value:
                    column_name = key[
                        len("extra_search[") : -1
                    ]  # Extract the column name from the key
                    extra_search[f"{column_name}__icontains"] = value

            # Apply individual column filters
            if extra_search:
                company = company.filter(**extra_search)

            # Apply sorting
            order_column_index = int(request.GET.get("order[0][column]", 0))
            order_direction = request.GET.get("order[0][dir]", "asc")

            # Map DataTables column index to your model fields
            order_columns = [
                "id",
                "governorate",
                "price",
                "is_active",
                "created_at",
                "updated_at",
            ]  # Adjust as needed

            # Apply sorting
            order_column_name = order_columns[order_column_index]
            if order_direction == "desc":
                order_column_name = f"-{order_column_name}"

            company = company.order_by(order_column_name)

            # Count total records after filtering
            total_records = company.count()

            # Apply pagination
            company = company[start : start + length]

            serializer = ShippingPriceSerializer(company, many=True)

            response_data = {
                "draw": draw,
                "recordsTotal": total_records,
                "recordsFiltered": total_records,
                "data": serializer.data,
            }

            return Response(response_data)

        except Exception as e:
            # Handle exceptions, log the error, and return an appropriate response
            return Response({"error": str(e)})


class GovernorateViewSetAdmin(viewsets.ModelViewSet):
    queryset = Governorate.objects.all()
    serializer_class = GovernorateSerializer
    permission_classes = [permissions.IsAdminUser]


class ProductViewSetAdmin(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ["get", "post", "retrieve", "put", "patch"]

    @action(detail=True, methods=["get"])
    def datatable_list(self, request, *args, **kwargs):
        try:
            draw = int(request.GET.get("draw", 1))
            start = int(request.GET.get("start", 0))
            length = int(request.GET.get("length", 10))
            global_search_value = request.GET.get("search[value]", "")
            start_date, end_date = request.GET.get("start_date", ""), request.GET.get(
                "end_date", ""
            )

            # Split the global search value into individual terms
            global_search_terms = global_search_value.split()

            # Start with an empty Q object to build the OR conditions for global search
            global_q_object = Q()

            # Build an OR condition for each term in the global search
            for term in global_search_terms:
                global_q_object |= Q(barcode__iexact=term)
                # Add other global search columns as needed

            # Filter data based on the constructed Q object for global search
            products = self.queryset.filter(global_q_object)

            # Apply date range filter
            if start_date and end_date:
                products = products.filter(updated_at__range=[start_date, end_date])

            # Handle individual column searches
            extra_search = {}
            for key, value in request.GET.items():
                if key.startswith("extra_search[") and value:
                    column_name = key[
                        len("extra_search[") : -1
                    ]  # Extract the column name from the key
                    extra_search[f"{column_name}__icontains"] = value

            # Apply individual column filters
            if extra_search:
                products = products.filter(**extra_search)

            # Apply sorting
            order_column_index = int(request.GET.get("order[0][column]", 0))
            order_direction = request.GET.get("order[0][dir]", "asc")

            # Map DataTables column index to your model fields
            order_columns = [
                "id",
                "name",
                "purchase_price",
                "sale_price",
                "image",
                "product_variant_set",
                "description",
                "note",
                "media_url",
                "is_active",
                "access_type",
                "created_at",
                "updated_at",
                "inventory",
                "vendor",
                "category",
                "access_to",
                "barcode",
            ]  # Adjust as needed

            # Apply sorting
            order_column_name = order_columns[order_column_index]
            if order_direction == "desc":
                order_column_name = f"-{order_column_name}"

            products = products.order_by(order_column_name)

            # Count total records after filtering
            total_records = products.count()

            # Apply pagination
            products = products[start : start + length]

            serializer = ProductSerializer(products, many=True)

            response_data = {
                "draw": draw,
                "recordsTotal": total_records,
                "recordsFiltered": total_records,
                "data": serializer.data,
            }

            return Response(response_data)

        except Exception as e:
            # Handle exceptions, log the error, and return an appropriate response
            return Response({"error": str(e)})

    def create(self, request, *args, **kwargs):
        try:
            product_data = request.data
            variants_data = product_data.pop("product_variant_set", [])[
                0
            ]  # Extract variants data
            variants_data = json.loads(variants_data)

            # Validate and create product
            product_serializer = ProductSerializer(data=product_data)
            product_serializer.is_valid(raise_exception=True)
            product = product_serializer.save()
            # print(product.id)
            # Create variants associated with the product
            for variant_data in variants_data:
                variant_data[
                    "product"
                ] = product.id  # Link variant to the created product
                variant_serializer = ProductVariantSerializer(data=variant_data)
                variant_serializer.is_valid(raise_exception=True)
                variant_serializer.save()

            return Response(product_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Handle exceptions, log the error, and return an appropriate response
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # def update(self, request, *args, **kwargs):
    #     try:
    #         partial = kwargs.pop('partial', False)
    #         instance = self.get_object()

    #         # Create a mutable copy of the QueryDict
    #         product_data = QueryDict(request.data.urlencode(), mutable=True)
    #         variants_data = product_data.pop('product_variant_set', [])

    #         # Validate and update product
    #         product_serializer = ProductSerializer(instance, data=product_data, partial=partial)
    #         product_serializer.is_valid(raise_exception=True)
    #         updated_product = product_serializer.save()

    #         # Update or create variants associated with the product
    #         for variant_data in variants_data:
    #             variant_data['product'] = updated_product.id  # Link variant to the updated product
    #             variant_serializer = ProductVariantSerializer(data=variant_data)
    #             variant_serializer.is_valid(raise_exception=True)
    #             variant_serializer.save()

    #         return Response(product_serializer.data, status=status.HTTP_200_OK)

    #     except Exception as e:
    #         # Handle exceptions, log the error, and return an appropriate response
    #         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ProductVariantViewSetAdmin(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True, methods=["get"])
    def datatable_list(self, request, *args, **kwargs):
        try:
            draw = int(request.GET.get("draw", 1))
            start = int(request.GET.get("start", 0))
            length = int(request.GET.get("length", 10))
            global_search_value = request.GET.get("search[value]", "")
            start_date, end_date = request.GET.get("start_date", ""), request.GET.get(
                "end_date", ""
            )

            # Split the global search value into individual terms
            global_search_terms = global_search_value.split()

            # Start with an empty Q object to build the OR conditions for global search
            global_q_object = Q()

            # Build an OR condition for each term in the global search
            for term in global_search_terms:
                global_q_object |= Q(barcode__iexact=term)
                # Add other global search columns as needed

            # Filter data based on the constructed Q object for global search
            products = self.queryset.filter(global_q_object)

            # Apply date range filter
            if start_date and end_date:
                products = products.filter(updated_at__range=[start_date, end_date])

            # Handle individual column searches
            extra_search = {}
            for key, value in request.GET.items():
                if key.startswith("extra_search[") and value:
                    column_name = key[
                        len("extra_search[") : -1
                    ]  # Extract the column name from the key
                    extra_search[f"{column_name}__icontains"] = value

            # Apply individual column filters
            if extra_search:
                products = products.filter(**extra_search)

            # Apply sorting
            order_column_index = int(request.GET.get("order[0][column]", 0))
            order_direction = request.GET.get("order[0][dir]", "asc")

            # Map DataTables column index to your model fields
            order_columns = [
                "id",
                "name",
                "purchase_price",
                "sale_price",
                "image",
                "size",
                "description",
                "note",
                "media_url",
                "is_active",
                "access_type",
                "created_at",
                "updated_at",
                "inventory",
                "vendor",
                "category",
                "access_to",
                "barcode",
            ]  # Adjust as needed

            # Apply sorting
            order_column_name = order_columns[order_column_index]
            if order_direction == "desc":
                order_column_name = f"-{order_column_name}"

            products = products.order_by(order_column_name)

            # Count total records after filtering
            total_records = products.count()

            # Apply pagination
            products = products[start : start + length]

            serializer = ProductSerializer(products, many=True)

            response_data = {
                "draw": draw,
                "recordsTotal": total_records,
                "recordsFiltered": total_records,
                "data": serializer.data,
            }

            return Response(response_data)

        except Exception as e:
            # Handle exceptions, log the error, and return an appropriate response
            return Response({"error": str(e)})


class OrderViewSetAdmin(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True, methods=["get"])
    def datatable_list(self, request, *args, **kwargs):
        try:
            draw = int(request.GET.get("draw", 1))
            start = int(request.GET.get("start", 0))
            length = int(request.GET.get("length", 10))
            global_search_value = request.GET.get("search[value]", "")
            start_date, end_date = request.GET.get("start_date", ""), request.GET.get(
                "end_date", ""
            )

            # Split the global search value into individual terms
            global_search_terms = global_search_value.split()

            # Start with an empty Q object to build the OR conditions for global search
            global_q_object = Q()

            # Build an OR condition for each term in the global search
            for term in global_search_terms:
                global_q_object |= Q(barcode__iexact=term)
                # Add other global search columns as needed

            # Filter data based on the constructed Q object for global search
            products = self.queryset.filter(global_q_object)

            # Apply date range filter
            if start_date and end_date:
                products = products.filter(updated_at__range=[start_date, end_date])

            # Handle individual column searches
            extra_search = {}
            for key, value in request.GET.items():
                if key.startswith("extra_search[") and value:
                    column_name = key[
                        len("extra_search[") : -1
                    ]  # Extract the column name from the key
                    extra_search[f"{column_name}__icontains"] = value

            # Apply individual column filters
            if extra_search:
                products = products.filter(**extra_search)

            # Apply sorting
            order_column_index = int(request.GET.get("order[0][column]", 0))
            order_direction = request.GET.get("order[0][dir]", "asc")

            # Map DataTables column index to your model fields
            order_columns = [
                "id",
                "barcode",
                "status",
                "shiping_price",
                "commission",
                "total",
                "marketer",
                "governorate",
                "city",
                "shipping_company",
                "created_at",
                "updated_at",
            ]  # Adjust as needed
        
            # Apply sorting
            order_column_name = order_columns[order_column_index]
            if order_direction == "desc":
                order_column_name = f"-{order_column_name}"

            products = products.order_by(order_column_name)

            # Count total records after filtering
            total_records = products.count()

            # Apply pagination
            products = products[start : start + length]


            serializer = OrderSerializer(products, many=True)

            response_data = {
                "draw": draw,
                "recordsTotal": total_records,
                "recordsFiltered": total_records,
                "data": serializer.data,
            }

            return Response(response_data)

        except Exception as e:
            # Handle exceptions, log the error, and return an appropriate response
            return Response({"error": str(e)})

    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                order_data, variants_data = self.extract_data_from_request(request.data)

                # Validate and create order
                order_serializer = OrderSerializer(data=order_data)
                if not order_serializer.is_valid():
                    return Response(
                        {"error": order_serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                order = order_serializer.save()

                # Create variants associated with the order
                self.create_or_update_variants(order, variants_data)

                # Get shipping price
                order.shiping_price = self.get_shipping_price(order)
                # Calculate commission based on the formula
                order.commission = self.calculate_commission(order, variants_data)

                order.save(updated_by=request.user, action_type='تم اضافة طلب جديد')

                # Update the vendor's and admin's pending field with their profit
                self.update_vendor_and_admin_pending_ADD(order)

                

                # Update the marketer's pending field with the commission
                self.update_marketer_pending_ADD(order)

                # Update quantity for the corresponding ProductVariant(s)   
                self.update_product_variants_quantity_SUB(order)

                response_data = {
                    "order": order_serializer.data,
                    "variants": OrderItemSerializer(order.items.all(), many=True).data,
                }
                print(order_serializer.data)
                return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Log the detailed error message for debugging
            print(f"Error creating order: {str(e)}")
            # transaction.set_rollback(True)  # Rollback the transaction
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                order_id = kwargs.get("pk")
                order = get_object_or_404(Order, id=order_id)

                action_type = request.data.get("action_type")
                if action_type:
                    self.handle_action_type(order, action_type, request.user)
                    return Response(
                        {"order": OrderSerializer(order).data},
                        status=status.HTTP_200_OK,
                    )

                order_data, variants_data = self.extract_data_from_request(request.data)

                order_serializer = OrderSerializer(order, data=order_data)
                if not order_serializer.is_valid():
                    return Response(
                        {"error": order_serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                order_serializer = OrderSerializer(order, data=order_data)

                self.rollback_logic(order)
                order_serializer = OrderSerializer(order, data=order_data)

                print("=>" + str(order.marketer.PENDING))

                if order_serializer.is_valid():
                    updated_order = order_serializer.save()
                    self.create_or_update_variants(updated_order, variants_data)
                    updated_order.shiping_price = self.get_shipping_price(
                        updated_order
                    )
                    updated_order.commission = self.calculate_commission(
                        updated_order, variants_data
                    )
                    

                    # Create note for order history
                    note = ""
                    for item in variants_data:
                        # Fetching product details
                        product_id = item['product']
                        product = Product.objects.get(id=product_id)
                        product_barcode = product.barcode

                        # Quantity and variant details
                        quantity = item['quantity']
                        variant_id = item['variant']
                        variant = ProductVariant.objects.get(id=variant_id)

                        # Building the note with information about the ordered product
                        note += f"تم طلب منتج: {product_barcode}\n"
                        note += f"الكمية: {quantity}\n"
                        note += f"الخاصية: {variant}\n\n"

                    updated_order.save(updated_by=request.user, note=note)
                    self.update_vendor_and_admin_pending_ADD(updated_order)
                    self.update_marketer_pending_ADD(updated_order)
                    self.update_product_variants_quantity_SUB(updated_order)

                    response_data = {
                        "order": order_serializer.data,
                        "variants": OrderItemSerializer(
                            updated_order.items.all(), many=True
                        ).data,
                    }

                    return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def handle_action_type(self, order, action_type, user):
        # Handle action_type logic here
        order.update_click_counters(action_type, user)

    def extract_data_from_request(self, request_data):
        order_data = request_data.copy()
        variants_data_list = order_data.pop("product_variant_set", [])

        if not variants_data_list:
            return Response(
                {"error": "No variant data provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        variants_data = json.loads(variants_data_list[0])

        return order_data, variants_data

    def rollback_logic(self, order):
        # Implement your rollback logic here if needed
        self.update_vendor_and_admin_pending_SUB(order)
        self.update_product_variants_quantity_ADD(order)
        order.items.all().delete()
        self.update_marketer_pending_SUB(order)

    def update_vendor_and_admin_pending_SUB(self, order):
        admin_user = User.objects.filter(username="admin", is_superuser=True).first()

        for order_item in order.items.all():
            product = order_item.product
            vendor = product.vendor

            admin_user.PENDING -= (
                product.sale_price - product.purchase_price
            ) * order_item.quantity
            vendor.PENDING -= product.purchase_price * order_item.quantity
            vendor.save()
        admin_user.save()

    def update_vendor_and_admin_pending_ADD(self, order):
        admin_user = User.objects.filter(username="admin", is_superuser=True).first()

        for order_item in order.items.all():
            product = order_item.product
            vendor = product.vendor

            admin_user.PENDING += (
                product.sale_price - product.purchase_price
            ) * order_item.quantity
            vendor.PENDING += product.purchase_price * order_item.quantity
            vendor.save()
        admin_user.save()

    def update_marketer_pending_SUB(self, order):
        order.marketer.PENDING -= order.commission
        order.marketer.save()

    def update_marketer_pending_ADD(self, order):
        order.marketer.PENDING += order.commission
        order.marketer.save()

    def update_product_variants_quantity_ADD(self, order):
        for order_item in order.items.all():
            try:
                variant_id = order_item.variant.id
                ProductVariant.objects.filter(id=variant_id).update(
                    quantity=F("quantity") + order_item.quantity
                )
            except ProductVariant.DoesNotExist:
                pass

    def update_product_variants_quantity_SUB(self, order):
        for order_item in order.items.all():
            try:
                variant_id = order_item.variant.id
                ProductVariant.objects.filter(id=variant_id).update(
                    quantity=F("quantity") - order_item.quantity
                )
            except ProductVariant.DoesNotExist:
                pass

    def create_or_update_variants(self, order, variants_data):
        if variants_data:
            for variant_data in variants_data:
                variant_data["order"] = order.id
                variant_serializer = OrderItemSerializer(data=variant_data)
                if not variant_serializer.is_valid():
                    return Response(
                        {"error": variant_serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                variant_serializer.save()

    def get_shipping_price(self, order):
        try:
            shipping_price = ShippingPrice.objects.get(id=order.governorate.id)
            return shipping_price.price
        except ShippingPrice.DoesNotExist:
            return Response(
                {"error": "Shipping price not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def calculate_commission(self, order, variants_data):
        item_total_price = sum(int(item["total_item_price"]) for item in variants_data)
        return order.total - (order.shiping_price + item_total_price)

    def handle_order_status(request, order):
        order_items = order.items.all()

        def update_vendor_account(vendor, update):
            User.objects.filter(id=vendor.id).update(**update)

        def update_marketer_account(marketer, update):
            User.objects.filter(id=marketer.id).update(**update)

        def update_admin_account(update):
            User.objects.filter(username="admin", is_superuser=True).update(**update)

        def update_product_quantity(update, variant):
            variant_id = variant
            ProductVariant.objects.filter(id=variant_id).update(**update)
            # ProductVariant.objects.filter(id=variant_id).update(
            #     quantity=F("quantity") + qty
            # )

        # Handle each order status
        print(order.status, order.PREPARATION)

        if order.status == order.PREPARATION:
            for item in order_items:
                product = item.product
                vendor = product.vendor

                # Update vendor's account
                vendor_update = {
                    "PENDING": F("PENDING") - product.purchase_price * item.quantity,
                    "PREPARATION": F("PREPARATION")
                    + product.purchase_price * item.quantity,
                }
                update_vendor_account(vendor, vendor_update)

                # Update admin's account
                admin_profit = (
                    product.sale_price - product.purchase_price
                ) * item.quantity
                admin_update = {
                    "PENDING": F("PENDING") - admin_profit,
                    "PREPARATION": F("PREPARATION") + admin_profit,
                }
                update_admin_account(admin_update)

            # Update marketer's account
            marketer_update = {
                "PENDING": F("PENDING") - order.commission,
                "PREPARATION": F("PREPARATION") + order.commission,
            }
            update_marketer_account(order.marketer, marketer_update)

        elif order.status == order.SHIPPED:
            for item in order_items:
                product = item.product
                vendor = product.vendor

                # Update vendor's account
                vendor_update = {
                    "PREPARATION": F("PREPARATION")
                    - product.purchase_price * item.quantity,
                    "SHIPPED": F("SHIPPED") + product.purchase_price * item.quantity,
                }
                update_vendor_account(vendor, vendor_update)

                # Update admin's account
                admin_profit = (
                    product.sale_price - product.purchase_price
                ) * item.quantity
                admin_update = {
                    "PREPARATION": F("PREPARATION") - admin_profit,
                    "SHIPPED": F("SHIPPED") + admin_profit,
                }
                update_admin_account(admin_update)

            # Update marketer's account
            marketer_update = {
                "PREPARATION": F("PREPARATION") - order.commission,
                "SHIPPED": F("SHIPPED") + order.commission,
            }
            update_marketer_account(order.marketer, marketer_update)

        elif order.status == order.DELIVERED:
            for item in order_items:
                product = item.product
                vendor = product.vendor

                # Update vendor's account
                vendor_update = {
                    "SHIPPED": F("SHIPPED") - product.purchase_price * item.quantity,
                    "DELIVERED": F("DELIVERED")
                    + product.purchase_price * item.quantity,
                }
                update_vendor_account(vendor, vendor_update)

                # Update admin's account
                admin_profit = (
                    product.sale_price - product.purchase_price
                ) * item.quantity
                admin_update = {
                    "SHIPPED": F("SHIPPED") - admin_profit,
                    "DELIVERED": F("DELIVERED") + admin_profit,
                }
                update_admin_account(admin_update)

            # Update marketer's account
            marketer_update = {
                "SHIPPED": F("SHIPPED") - order.commission,
                "DELIVERED": F("DELIVERED") + order.commission,
            }
            update_marketer_account(order.marketer, marketer_update)

        elif order.status == order.CANCELED:
            for item in order_items:
                product = item.product
                vendor = product.vendor

                # Update vendor's account
                vendor_update = {
                    "PENDING": F("PENDING") - product.purchase_price * item.quantity,
                }
                update_vendor_account(vendor, vendor_update)

                # Update admin's account
                admin_profit = (
                    product.sale_price - product.purchase_price
                ) * item.quantity
                admin_update = {
                    "PENDING": F("PENDING") - admin_profit,
                }
                update_admin_account(admin_update)

                # Update product variant quantity
                variant_id = item.variant.id
                print(variant_id)
                product_update = {"quantity": F("quantity") + item.quantity}
                update_product_quantity(product_update, variant_id)

            # Update marketer's account
            marketer_update = {
                "PENDING": F("PENDING") - order.commission,
            }
            update_marketer_account(order.marketer, marketer_update)

        elif order.status == order.CANCELED_DURING_PREPARATION:
            for item in order_items:
                product = item.product
                vendor = product.vendor

                # Update vendor's account
                vendor_update = {
                    "PREPARATION": F("PREPARATION")
                    - product.purchase_price * item.quantity,
                }
                update_vendor_account(vendor, vendor_update)

                # Update admin's account
                admin_profit = (
                    product.sale_price - product.purchase_price
                ) * item.quantity
                admin_update = {
                    "PREPARATION": F("PREPARATION") - admin_profit,
                }
                update_admin_account(admin_update)

                # Update product variant quantity
                variant_id = item.variant.id
                print(variant_id)
                product_update = {"quantity": F("quantity") + item.quantity}
                update_product_quantity(product_update, variant_id)

            # Update marketer's account
            marketer_update = {
                "PREPARATION": F("PREPARATION") - order.commission,
            }
            update_marketer_account(order.marketer, marketer_update)

        elif order.status == order.RETURN_IN_PROGRESS:
            for item in order_items:
                product = item.product
                vendor = product.vendor

                # Update vendor's account
                vendor_update = {
                    "SHIPPED": F("SHIPPED") - product.purchase_price * item.quantity,
                }
                update_vendor_account(vendor, vendor_update)

                # Update admin's account
                admin_profit = (
                    product.sale_price - product.purchase_price
                ) * item.quantity
                admin_update = {
                    "SHIPPED": F("SHIPPED") - admin_profit,
                }
                update_admin_account(admin_update)

                
            # Update marketer's account
            marketer_update = {
                "SHIPPED": F("SHIPPED") - order.commission,
            }
            update_marketer_account(order.marketer, marketer_update)

        elif order.status == order.RETURNE_REQUESTS:
            for item in order_items:
                product = item.product
                vendor = product.vendor

                # Update vendor's account
                vendor_update = {
                    "DELIVERED": F("DELIVERED")
                    - product.purchase_price * item.quantity,
                }
                update_vendor_account(vendor, vendor_update)

                # Update admin's account
                admin_profit = (
                    product.sale_price - product.purchase_price
                ) * item.quantity
                admin_update = {
                    "DELIVERED": F("DELIVERED") - admin_profit,
                }
                update_admin_account(admin_update)

            # Update marketer's account
            marketer_update = {
                "DELIVERED": F("DELIVERED") - order.commission,
            }
            update_marketer_account(order.marketer, marketer_update)

            order.barcode_returned = order.barcode + "R"
            order.save()

        elif order.status == order.RETURNED:
            for item in order_items:
                # Update product variant quantity
                variant_id = item.variant.id
                print(variant_id)
                product_update = {"quantity": F("quantity") + item.quantity}
                update_product_quantity(product_update, variant_id)
           
        elif order.status == order.RETURNED_AFTER_DELIVERY:
            for item in order_items:
                # Update product variant quantity
                variant_id = item.variant.id
                print(variant_id)
                product_update = {"quantity": F("quantity") + item.quantity}
                update_product_quantity(product_update, variant_id)

           

        # elif order.status == 'shipped':
        #     for item in items:
        #         merchant = item['merchant']
        #         total_purchase_price = item['total_purchase_price']
        #         update_merchant_account(merchant, {'preparing': models.F('preparing') - total_purchase_price, 'shipped': models.F('shipped') + total_purchase_price})
        #     update_marketer_account(order.marketer, {'preparing': models.F('preparing') - order.commission, 'shipped': models.F('shipped') + order.commission})

        # elif order.status == 'skip':
        #     for item in items:
        #         merchant = item['merchant']
        #         total_purchase_price = item['total_purchase_price']
        #         update_merchant_account(merchant, {'shipped': models.F('shipped') - total_purchase_price})

        #     update_marketer_account(order.marketer, {'shipped': models.F('shipped') - order.commission})

        # elif order.status == 'returned1':
        #     for item in items:
        #         product_property_id = item['property']
        #         Product.objects.filter(properties__id=product_property_id).update(properties__value=models.F('properties__value') + item['qty'])

        # # Add similar logic for other order statuses...

        # elif order.status == 'returned2':
        #     for item in items:
        #         product_property_id = item['property']
        #         Product.objects.filter(properties__id=product_property_id).update(properties__value=models.F('properties__value') + item['qty'])

        # # Create a notification for the appropriate recipient
        # recipient_user = order.moderator if order.moderator else order.marketer
        # notification_content = f'The status of your order ({order.serial_number}) has changed to {order.status}'
        # create_notification(notification_content, recipient_user)

        return JsonResponse({"status": "success"})

    @action(detail=False, methods=["post"])
    def update_status(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                # Get the list of order IDs and new status from the request
                selected_order_ids = request.data.get("selected_order_ids", [])
                new_status = request.data.get("new_status")

                # Validate if at least one order is selected and new status is provided
                if not selected_order_ids:
                    return Response(
                        {"error": "No orders selected for status update."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if not new_status:
                    return Response(
                        {"error": "New status not provided."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Retrieve and update status for each selected order
                for order_id in selected_order_ids:
                    try:
                        order = Order.objects.get(pk=order_id)

                        # Validate the status transition
                        order.validate_status_transition(new_status)

                        # Update the order status
                        order.status = new_status
                        order.save(updated_by=request.user)
                        # Call the handle_order_status function to update vendor and marketer accounts
                        self.handle_order_status(order)

                    except Order.DoesNotExist:
                        # Log or handle the case where the order doesn't exist
                        pass

                return JsonResponse(
                    {"success": True, "message": f"تم تحديث حالة الطلب بنجاح إلى '{new_status}'."},
                    status=status.HTTP_200_OK,
                )

        except ValueError as ve:
            return JsonResponse({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Log the detailed error message for debugging
            print(f"Error updating order status: {str(e)}")
            return JsonResponse(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=["post"])
    def update_shipping_company(self, request, *args, **kwargs):
        # selected_order_ids = request.data.get("selected_order_ids", [])
        # print(selected_order_ids)
        # return JsonResponse({"key": "value"})
        try:
            with transaction.atomic():
                # Get the list of order IDs from the request
                selected_order_ids = request.data.get("selected_order_ids", [])
                shipping_company = request.data.get("shipping_company")

                # Validate if at least one order is selected
                if not selected_order_ids:
                    return Response(
                        {"error": "لم يتم تحديد أي طلبات لتحديث شركة الشحن."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if not shipping_company:
                    return Response(
                        {"error": "لم يتم تحديد شركة شحن للطلبات المحددة."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                print(shipping_company)
                # Retrieve and update shipping company for each selected order
                for order_id in selected_order_ids:
                    try:
                        order = Order.objects.get(pk=order_id)
                        # Update the shipping company (replace 'new_shipping_company' with your actual update logic)
                        updated_shipping_company = ShippingCompany.objects.get(
                            id=shipping_company
                        )

                        order.shipping_company = updated_shipping_company
                        order.save(updated_by=request.user)
                    except Order.DoesNotExist:
                        # Log or handle the case where the order doesn't exist
                        pass

                return Response(
                    {
                        "success": True,
                        "message": "تم تحديث شركة الشحن للطلبات المحددة.",
                    },
                    status=status.HTTP_200_OK,
                )

        except Exception as e:
            # Log the detailed error message for debugging
            print(f"Error updating shipping company: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        
    def retrieve(self, request, *args, **kwargs):
        # Assuming you have an 'Order' model
        orders = Order.objects.all()

        # Paginate the orders
        page = request.GET.get('page', 1)
        paginator = Paginator(orders, len(orders))  # Show 10 orders per page
        try:
            orders_page = paginator.page(page)
        except PageNotAnInteger:
            # If the page is not an integer, deliver the first page.
            orders_page = paginator.page(1)
        except EmptyPage:
            # If the page is out of range (e.g., 9999), deliver the last page of results.
            orders_page = paginator.page(paginator.num_pages)

        # Call the default retrieve method to get the instance
        instance = self.get_object()

        # Convert the instance to a serialized format using Django REST framework serializers
        serializer = self.get_serializer(instance)
        serialized_order = serializer.data

        # Get the next order's primary key
        next_order_pk = None
        prev_order_pk = None
        current_index = orders_page.index(instance)
        print(current_index)
        if current_index < orders_page.end_index() -1:
            next_order_pk = orders_page[current_index + 1].id

        if current_index > 0:
            prev_order_pk = orders_page[current_index - 1].id

        return Response({'order': serialized_order, 'next_order_pk': next_order_pk, 'prev_order_pk': prev_order_pk}, status=status.HTTP_200_OK)


class OrderItemViewSetAdmin(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=True, methods=["get"])
    def datatable_list(self, request, *args, **kwargs):
        try:
            draw = int(request.GET.get("draw", 1))
            start = int(request.GET.get("start", 0))
            length = int(request.GET.get("length", 10))
            global_search_value = request.GET.get("search[value]", "")
            start_date, end_date = request.GET.get("start_date", ""), request.GET.get(
                "end_date", ""
            )

            # Split the global search value into individual terms
            global_search_terms = global_search_value.split()

            # Start with an empty Q object to build the OR conditions for global search
            global_q_object = Q()

            # Build an OR condition for each term in the global search
            for term in global_search_terms:
                global_q_object |= Q(barcode__iexact=term)
                # Add other global search columns as needed

            # Filter data based on the constructed Q object for global search
            products = self.queryset.filter(global_q_object)

            # Apply date range filter
            if start_date and end_date:
                products = products.filter(updated_at__range=[start_date, end_date])

            # Handle individual column searches
            extra_search = {}
            for key, value in request.GET.items():
                if key.startswith("extra_search[") and value:
                    column_name = key[
                        len("extra_search[") : -1
                    ]  # Extract the column name from the key
                    extra_search[f"{column_name}__icontains"] = value

            # Apply individual column filters
            if extra_search:
                products = products.filter(**extra_search)

            # Apply sorting
            order_column_index = int(request.GET.get("order[0][column]", 0))
            order_direction = request.GET.get("order[0][dir]", "asc")

            # Map DataTables column index to your model fields
            order_columns = [
                "id",
                "name",
                "purchase_price",
                "sale_price",
                "image",
                "size",
                "description",
                "note",
                "media_url",
                "is_active",
                "access_type",
                "created_at",
                "updated_at",
                "inventory",
                "vendor",
                "category",
                "access_to",
                "barcode",
            ]  # Adjust as needed

            # Apply sorting
            order_column_name = order_columns[order_column_index]
            if order_direction == "desc":
                order_column_name = f"-{order_column_name}"

            products = products.order_by(order_column_name)

            # Count total records after filtering
            total_records = products.count()

            # Apply pagination
            products = products[start : start + length]

            serializer = OrderItemSerializer(products, many=True)

            response_data = {
                "draw": draw,
                "recordsTotal": total_records,
                "recordsFiltered": total_records,
                "data": serializer.data,
            }

            return Response(response_data)

        except Exception as e:
            # Handle exceptions, log the error, and return an appropriate response
            return Response({"error": str(e)})


def get_cities(request, governorate_id):
    cities = City.objects.filter(governorate_id=governorate_id)
    city_list = [{"id": city.id, "name": city.city_name_ar} for city in cities]
    return JsonResponse({"cities": city_list})


def get_variants(request, product_id):
    variants = ProductVariant.objects.filter(product_id=product_id)
    variant_list = [
        {
            "id": variant.id,
            "name": str(variant),
        }
        for variant in variants
    ]
    return JsonResponse({"variants": variant_list})


@require_GET
def product_search(request):
    term = request.GET.get("term", "")
    items_per_page = 10  # Adjust the number of items per page as needed

    if len(term) > 1:
        # Use icontains for a case-insensitive partial match
        products = Product.objects.filter(
            Q(name__icontains=term) | Q(barcode__iexact=term)
        ).values("id", "name", "sale_price")
    else:
        products = Product.objects.all().values("id", "name", "sale_price")

    # Paginate the products
    page = request.GET.get("page", 1)
    paginator = Paginator(products, items_per_page)

    try:
        paginated_products = paginator.page(page)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)

    # Transform products for JSON response
    transformed_products = [
        {"id": product["id"], "text": product["name"], "price": product["sale_price"]}
        for product in paginated_products
    ]

    return JsonResponse(
        {
            "results": transformed_products,
            "pagination": {
                "more": paginated_products.has_next(),
                "current_page": paginated_products.number,
                "total_pages": paginator.num_pages,
            },
        }
    )


@require_GET
def marketer_search(request):
    term = request.GET.get("term", "")
    items_per_page = 10  # Adjust the number of items per page as needed

    if len(term) > 1:
        # Use icontains for a case-insensitive partial match
        marketer = User.objects.filter(
            Q(email__icontains=term) & Q(is_marketer=True)
        ).values("id", "email")
    else:
        marketer = User.objects.filter(Q(is_marketer=True)).values("id", "email")

    # Paginate the marketer
    page = request.GET.get("page", 1)
    paginator = Paginator(marketer, items_per_page)

    try:
        paginated_marketer = paginator.page(page)
    except PageNotAnInteger:
        paginated_marketer = paginator.page(1)
    except EmptyPage:
        paginated_marketer = paginator.page(paginator.num_pages)

    # Transform marketer for JSON response
    transformed_marketer = [
        {"id": marketer["id"], "text": marketer["email"]}
        for marketer in paginated_marketer
    ]

    return JsonResponse(
        {
            "results": transformed_marketer,
            "pagination": {
                "more": paginated_marketer.has_next(),
                "current_page": paginated_marketer.number,
                "total_pages": paginator.num_pages,
            },
        }
    )


def get_product(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        # Additional logic if needed
        # For example, you might want to serialize the product data before returning it in the JSON response.
        product_data = {
            "id": product.id,
            "name": product.name,
            # Add more fields as needed
        }
        return JsonResponse({"product": product_data})
    except Exception as e:
        return JsonResponse({"error": str(e)})


def get_sale_price(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        sale_price = product.sale_price
        return JsonResponse({"sale_price": sale_price})
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)


def get_shipping_price(request, governorate_id):
    try:
        governorate = ShippingPrice.objects.get(id=governorate_id)
        shipping_price = governorate.price
        return JsonResponse({"shipping_price": shipping_price})
    except Product.DoesNotExist:
        return JsonResponse({"error": "Shipping_price not found"}, status=404)


@require_GET
def get_shipping_company(request):
    term = request.GET.get("term", "")
    items_per_page = 10  # Adjust the number of items per page as needed

    if len(term) > 1:
        # Use icontains for a case-insensitive partial match
        company = ShippingCompany.objects.filter(Q(name__icontains=term)).values(
            "id", "name"
        )
    else:
        company = ShippingCompany.objects.all().values("id", "name")

    # Paginate the company
    page = request.GET.get("page", 1)
    paginator = Paginator(company, items_per_page)

    try:
        paginated_company = paginator.page(page)
    except PageNotAnInteger:
        paginated_company = paginator.page(1)
    except EmptyPage:
        paginated_company = paginator.page(paginator.num_pages)

    # Transform company for JSON response
    transformed_company = [
        {"id": company["id"], "text": company["name"]} for company in paginated_company
    ]

    return JsonResponse(
        {
            "results": transformed_company,
            "pagination": {
                "more": paginated_company.has_next(),
                "current_page": paginated_company.number,
                "total_pages": paginator.num_pages,
            },
        }
    )
