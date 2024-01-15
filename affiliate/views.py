from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from affiliate.forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from accounts.decorators import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q  # Import Q for complex queries
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
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        variant_formset = ProductForm.product_variant_set(request.POST, request.FILES, instance=Product())
        if form.is_valid() and variant_formset.is_valid():
            # Process form data, including the uploaded file
            product = form.save()
            variant_formset.instance = product
            variant_formset.save()
            return JsonResponse({'detail': 'Product created successfully'})
        else:
            return JsonResponse({'detail': 'Invalid form data'}, status=400)

    else:
        form = ProductForm()
        variant_formset = ProductForm.product_variant_set(instance=Product())  
    products = Product.objects.all()
    return render(request, "pages/affilate/products_list.html", {"products": products,  'form': form, 'variant_formset': variant_formset})


@login_required
@admin_required
def products(request):
    
    products = Product.objects.all()

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
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        order_items = OrderForm.items(request.POST, request.FILES, instance=Product())
        if form.is_valid() and order_items.is_valid():
            # Process form data, including the uploaded file
            product = form.save()
            order_items.instance = product
            order_items.save()
            return JsonResponse({'detail': 'Product created successfully'})
            
        else:
            return JsonResponse({'detail': 'Invalid form data'}, status=400)
    else:
        form = OrderForm()
        order_items = OrderForm.items(instance=Product())  
    order = Order.objects.all()
    return render(request, "pages/affilate/new_orders.html", {"order": order,  'form': form, 'variant_formset': order_items})


@login_required
@admin_required
def requests(request):
    return render(request, "pages/affilate/requests.html")


@login_required
@admin_required
def vendors_accounts(request):
    return render(request, "pages/affilate/vendors_accounts.html")


@login_required
@admin_required
def marketers_accounts(request):
    return render(request, "pages/affilate/marketers_accounts.html")


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
    http_method_names = ['get','post','retrieve','put','patch']

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
                'product_variant_set',
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
            variants_data = product_data.pop('product_variant_set', [])[0]  # Extract variants data
            variants_data = json.loads(variants_data)

            # Validate and create product
            product_serializer = ProductSerializer(data=product_data)
            product_serializer.is_valid(raise_exception=True)
            product = product_serializer.save()
            # print(product.id)
            # Create variants associated with the product
            for variant_data in variants_data:
                variant_data['product'] = product.id  # Link variant to the created product
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
        print(request.data)
        try:
            product_data = request.data
            variants_data = product_data.pop('product_variant_set', [])[0]  # Extract variants data
            variants_data = json.loads(variants_data)
            print(request.data)
            # Validate and create product
            product_serializer = OrderSerializer(data=product_data)
            product_serializer.is_valid(raise_exception=True)
            product = product_serializer.save()
            # print(product.id)
            # Create variants associated with the product
            for variant_data in variants_data:
                variant_data['product'] = product.id  # Link variant to the created product
                variant_serializer = OrderItemSerializer(data=variant_data)
                variant_serializer.is_valid(raise_exception=True)
                variant_serializer.save()

            return Response(product_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Handle exceptions, log the error, and return an appropriate response
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        



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
    variant_list = [{"id": variant.id, "name": str(variant),} for variant in variants]
    return JsonResponse({"variants": variant_list})



@require_GET
def product_search(request):
    term = request.GET.get('term', '')
    items_per_page = 10  # Adjust the number of items per page as needed

    if len(term) > 1:
        # Use icontains for a case-insensitive partial match
        products = Product.objects.filter(
            Q(name__icontains=term) | Q(barcode__iexact=term)
        ).values('id', 'name', 'sale_price')
    else:
        products = Product.objects.all().values('id', 'name', 'sale_price')
    
    # Paginate the products
    page = request.GET.get('page', 1)
    paginator = Paginator(products, items_per_page)

    try:
        paginated_products = paginator.page(page)
    except PageNotAnInteger:
        paginated_products = paginator.page(1)
    except EmptyPage:
        paginated_products = paginator.page(paginator.num_pages)

    # Transform products for JSON response
    transformed_products = [
        {'id': product['id'], 'text': product['name'], 'price': product['sale_price']}
        for product in paginated_products
    ]

    return JsonResponse({
        'results': transformed_products,
        'pagination': {
            'more': paginated_products.has_next(),
            'current_page': paginated_products.number,
            'total_pages': paginator.num_pages,
        }
    })



def get_sale_price(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        sale_price = product.sale_price  # Assuming 'sale_price' is a field in your Product model
        return JsonResponse({'sale_price': sale_price})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)