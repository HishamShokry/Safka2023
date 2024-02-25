from rest_framework import viewsets
from rest_framework.response import Response
from affiliate.serializers import *
from rest_framework.decorators import action, api_view
from rest_framework import status
from rest_framework import generics, permissions
from django.views.decorators.http import require_GET
from decimal import Decimal
from django_filters.rest_framework import DjangoFilterBackend

from django.http import JsonResponse
from django.db import transaction
from affiliate.models import *
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Case, When, F, Value, Count, IntegerField
from django.db.models import Case, When, F, Value
from django.utils.translation import gettext as _


class DataTableMixin:
    def handle_datatables_request(self, queryset, serializer_class, columns, request):
        try:
            draw = int(request.GET.get("draw", 1))
            start = int(request.GET.get("start", 0))
            length = int(request.GET.get("length", 10))
            global_search_value = request.GET.get("search[value]", "")
            start_date, end_date = request.GET.get("start_date", ""), request.GET.get(
                "end_date", ""
            )
            
            # Filter by status
            status_filter = request.GET.get("status", "")
            if status_filter and status_filter != "اجمالي عدد الطلبات":
                queryset = queryset.filter(status=status_filter)

            # Split the global search value into individual terms
            global_search_terms = global_search_value.split()

            # Start with an empty Q object to build the OR conditions for global search
            global_q_object = Q()

            # Build an OR condition for each term in the global search
            for term in global_search_terms:
                global_q_object |= Q(name__icontains=term)
                # Add other global search columns as needed

            # Filter data based on the constructed Q object for global search
            items = queryset.filter(global_q_object)

            # Apply date range filter
            if start_date and end_date:
                items = items.filter(updated_at__range=[start_date, end_date])

            # Handle individual column searches
            extra_search = {}
            for key, value in request.GET.items():
                if key.startswith("extra_search[") and value:
                    column_name = key[len("extra_search[") : -1]
                    extra_search[f"{column_name}__icontains"] = value

            # Apply individual column filters
            if extra_search:
                items = items.filter(**extra_search)

            # Apply sorting
            order_column_index = int(request.GET.get("order[0][column]", 0))
            order_direction = request.GET.get("order[0][dir]", "asc")

            # Map DataTables column index to your model fields
            order_columns = columns

            # Apply sorting
            order_column_name = order_columns[order_column_index]
            if order_direction == "desc":
                order_column_name = f"-{order_column_name}"

            items = items.order_by(order_column_name)

            # Count total records after filtering
            total_records = items.count()

            # Apply pagination
            items = items[start : start + length]

            serializer = serializer_class(items, many=True)

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


class CategoryViewSet(DataTableMixin, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]
    order_columns = [
        "id",
        "name",
        "created_at",
        "updated_at",
    ]

    @action(detail=True, methods=["get"])
    def datatable_list(self, request, *args, **kwargs):
        return self.handle_datatables_request(
            self.queryset, self.serializer_class, self.order_columns, request
        )


class InventoryViewSet(DataTableMixin, viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAdminUser]
    order_columns = [
        "id",
        "name",
        "created_at",
        "updated_at",
    ]

    @action(detail=True, methods=["get"])
    def datatable_list(self, request, *args, **kwargs):
        return self.handle_datatables_request(
            self.queryset, self.serializer_class, self.order_columns, request
        )


class ShippingCompanyViewSetAdmin(DataTableMixin, viewsets.ModelViewSet):
    queryset = ShippingCompany.objects.all()
    serializer_class = ShippingCompanySerializer
    permission_classes = [permissions.IsAdminUser]
    order_columns = [
        "id",
        "name",
        "website",
        "created_at",
        "updated_at",
    ]

    @action(detail=True, methods=["get"])
    def datatable_list(self, request, *args, **kwargs):
        return self.handle_datatables_request(
            self.queryset, self.serializer_class, self.order_columns, request
        )
        
    @action(detail=False, methods=["get"])
    def orders_count(self, request, *args, **kwargs):
        # Extracting data for the bar chart
        orders_count_data = ShippingCompany.objects.annotate(
            total_orders=Count('order'),
            delivered_orders=Count(Case(When(order__status=Order.DELIVERED, then=1), output_field=IntegerField())),
            return_requests_orders=Count(Case(When(order__status=Order.RETURNE_REQUESTS, then=1), output_field=IntegerField())),
        ).values('name', 'total_orders', 'delivered_orders', 'return_requests_orders')

        labels = [entry['name'] for entry in orders_count_data]
        total_orders_values = [entry['total_orders'] for entry in orders_count_data]
        delivered_orders_values = [entry['delivered_orders'] for entry in orders_count_data]
        return_requests_orders_values = [entry['return_requests_orders'] for entry in orders_count_data]

        # Calculate the total orders count
        total_orders_count = sum(total_orders_values)
        delivered_orders_count = sum(delivered_orders_values)
        return_requests_orders_count = sum(return_requests_orders_values)

        # Add total orders count as a label and value
        labels.append('اجمالي عدد الطلبات')
        total_orders_values.append(total_orders_count)
        delivered_orders_values.append(delivered_orders_count)
        return_requests_orders_values.append(return_requests_orders_count)

        bar_chart_data = {
            'labels': labels,
            'datasets': [
                {
                    'label': 'اجمالي عدد الطلبات',
                    'data': total_orders_values,
                    'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                    'borderColor': 'rgba(75, 192, 192, 1)',
                    'borderWidth': 1,
                },
                {
                    'label': 'طلبات تم التوصيل',
                    'data': delivered_orders_values,
                    'backgroundColor': 'rgba(0, 255, 0, 0.2)',  # Green color
                    'borderColor': 'rgba(0, 255, 0, 1)',  # Green color
                    'borderWidth': 1,
                },
                {
                    'label': 'طلبات استرجاع من العميل',
                    'data': return_requests_orders_values,
                    'backgroundColor': 'rgba(255, 0, 0, 0.2)',  # Red color
                    'borderColor': 'rgba(255, 0, 0, 1)',  # Red color
                    'borderWidth': 1,
                },
            ],
        }

        # Return the bar chart data in the response
        return Response({'bar_chart_data': bar_chart_data})


class ShippingPriceViewSetAdmin(DataTableMixin, viewsets.ModelViewSet):
    queryset = ShippingPrice.objects.all()
    serializer_class = ShippingPriceSerializer
    permission_classes = [permissions.IsAdminUser]
    order_columns = [
        "id",
        "governorate",
        "price",
        "is_active",
        "created_at",
        "updated_at",
    ]

    @action(detail=True, methods=["get"])
    def datatable_list(self, request, *args, **kwargs):
        return self.handle_datatables_request(
            self.queryset, self.serializer_class, self.order_columns, request
        )


class GovernorateViewSetAdmin(DataTableMixin, viewsets.ModelViewSet):
    queryset = Governorate.objects.all()
    serializer_class = GovernorateSerializer
    permission_classes = [permissions.IsAdminUser]


class ProductViewSetAdmin(DataTableMixin, viewsets.ModelViewSet):
    queryset = Product.objects.select_related(
        "inventory", "vendor", "category"
    ).prefetch_related(
        "product_variant_set__color", "product_variant_set__size", "access_to"
    )
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'sale_price']
    http_method_names = ["get", "post", "retrieve", "put", "patch"]
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
    ]

    @action(detail=True, methods=["get"])
    def datatable_list(self, request, *args, **kwargs):
        return self.handle_datatables_request(
            self.queryset, self.serializer_class, self.order_columns, request
        )

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
                variant_data["product"] = (
                    product.id
                )  # Link variant to the created product
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


class ProductVariantViewSetAdmin(DataTableMixin, viewsets.ModelViewSet):
    queryset = ProductVariant.objects.select_related(
        "product",
    )
    serializer_class = ProductVariantSerializer
    permission_classes = [permissions.IsAdminUser]


class OrderViewSetAdmin(DataTableMixin, viewsets.ModelViewSet):
    queryset = Order.objects.select_related(
        "marketer", "city", "governorate__governorate", "shipping_company"
    ).prefetch_related("items", "history_entries__updated_by")
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    permission_classes = [permissions.IsAdminUser]
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
    ]

    @action(detail=True, methods=["get"])
    def datatable_list(self, request, *args, **kwargs):
        return self.handle_datatables_request(
            self.queryset, self.serializer_class, self.order_columns, request
        )

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

                order.save(updated_by=request.user, action_type="تم اضافة طلب جديد")

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
                    updated_order.shiping_price = self.get_shipping_price(updated_order)
                    updated_order.commission = self.calculate_commission(
                        updated_order, variants_data
                    )

                    # Create note for order history
                    note = ""
                    for item in variants_data:
                        # Fetching product details
                        product_id = item["product"]
                        product = Product.objects.get(id=product_id)
                        product_barcode = product.barcode

                        # Quantity and variant details
                        quantity = item["quantity"]
                        variant_id = item["variant"]
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
        admin_user = User.objects.filter(username="system", is_superuser=True).first()

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
        admin_user = User.objects.filter(username="system", is_superuser=True).first()

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
        shipping_price = Decimal(order.shiping_price)
        total_item_price = sum(Decimal(item["total_item_price"]) for item in variants_data)
        order_total = Decimal(order.total)

        return order_total - (shipping_price + total_item_price)

        return order_total - (shipping_price + total_item_price)

    def handle_order_status(request, order):
    
        order_items = order.items.all()

        def update_vendor_account(vendor, update):
            User.objects.filter(id=vendor.id).update(**update)

        def update_marketer_account(marketer, update):
            User.objects.filter(id=marketer.id).update(**update)

        def update_admin_account(update):
            User.objects.filter(username="system", is_superuser=True).update(**update)

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

        return JsonResponse({"status": "success"})

    @action(detail=False, methods=["post"])
    def update_status(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                selected_order_ids = request.data.get("selected_order_ids", [])
                new_status = request.data.get("new_status")

                if not selected_order_ids:
                    return Response(
                        {"error": _("No orders selected for status update.")},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if not new_status:
                    return Response(
                        {"error": _("New status not provided.")},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                orders_to_update = Order.objects.filter(pk__in=selected_order_ids)

                # Validate status transition for all selected orders
                for order in orders_to_update:
                    order.validate_status_transition(new_status)

                # Perform bulk update for order statuses
                orders_to_update.update(status=new_status)

                # Call the handle_order_status function to update vendor and marketer accounts
                for order in orders_to_update:
                    self.handle_order_status(order)

                return Response(
                    {"success": True, "message": f"تم تحديث حالة الطلب بنجاح إلى '{new_status}'."},
                    status=status.HTTP_200_OK,
                )

        except Order.DoesNotExist as e:
            return Response({"error": _("Some orders do not exist.")}, status=status.HTTP_404_NOT_FOUND)

        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": _("Internal Server Error.")}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


    @action(detail=False, methods=["post"])
    def update_shipping_company(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                selected_order_ids = request.data.get("selected_order_ids", [])
                shipping_company_id = request.data.get("shipping_company")

                if not selected_order_ids:
                     return Response(
                        {"error": "لم يتم تحديد أي طلبات لتحديث شركة الشحن."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if not shipping_company_id:
                    return Response(
                        {"error": "لم يتم تحديد شركة شحن للطلبات المحددة."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Validate that the ShippingCompany exists
                updated_shipping_company = get_object_or_404(
                    ShippingCompany, id=shipping_company_id
                )

                # Retrieve all orders at once using bulk and update shipping_company
                orders_to_update = Order.objects.filter(pk__in=selected_order_ids)
                for order in orders_to_update:
                    order.shipping_company = updated_shipping_company
                    order.save(updated_by=request.user, action_type="تم تحديث شركة الشحن")

                Order.objects.bulk_update(orders_to_update, ['shipping_company'])

                return Response(
                    {
                        "success": True,
                        "message": "تم تحديث شركة الشحن للطلبات المحددة.",
                    },
                    status=status.HTTP_200_OK,
                )

        except ValidationError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Log the detailed error message for debugging
            return Response({"error": "Internal Server Error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        # Assuming you have an 'Order' model
        try:
            # Call the default retrieve method to get the instance
            instance = self.get_object()
        except Http404:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        # Convert the instance to a serialized format using Django REST framework serializers
        serializer = self.get_serializer(instance)
        serialized_order = serializer.data

        # Get the IDs of the next and previous orders
        next_order_id = (
            Order.objects.filter(id__gt=instance.id)
            .order_by("id")
            .values_list("id", flat=True)
            .first()
        )
        prev_order_id = (
            Order.objects.filter(id__lt=instance.id)
            .order_by("-id")
            .values_list("id", flat=True)
            .first()
        )

        return Response(
            {
                "order": serialized_order,
                "next_order_pk": next_order_id,
                "prev_order_pk": prev_order_id,
            },
            status=status.HTTP_200_OK,
        )

    
    @action(detail=False, methods=["get"])
    def filters(self, request, *args, **kwargs):

        # Extracting data for the bar chart
        status_data = Order.objects.values('status').annotate(order_count=Count('id'))
        labels = [entry['status'] for entry in status_data]
        values = [entry['order_count'] for entry in status_data]
        
        
        # Calculate the total orders count
        total_orders_count = sum(values)

        # Add total orders count as a label and value
        labels.append('اجمالي عدد الطلبات')
        values.append(total_orders_count)
        
        bar_chart_data = {
            'labels': labels,
            'values': values,
        }

         # Return the bar chart data in the response
        return Response({'bar_chart_data': bar_chart_data})

class OrderItemViewSetAdmin(DataTableMixin, viewsets.ModelViewSet):
    queryset = OrderItem.objects.select_related("order", "product").all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAdminUser]


class RequestViewSetAdmin(DataTableMixin, viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAdminUser]
    order_columns = [
        "id",
        "Amount",
        "Phone",
        "payment_method",
        "status",
        "note",
        "note",
        "created_at",
        "user",
    ]

    @action(detail=True, methods=["get"])
    def datatable_list(self, request, *args, **kwargs):
        return self.handle_datatables_request(
            self.queryset, self.serializer_class, self.order_columns, request
        )

    @action(detail=False, methods=["post"])
    def update_status(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                selected_request_id = request.data.get("selected_request_id", None)
                new_status = request.data.get("new_status")

                if not selected_request_id:
                    return Response(
                        {"error": _("No Request selected for status update.")},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if not new_status:
                    return Response(
                        {"error": _("New status not provided.")},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                request_to_update = Request.objects.get(pk=selected_request_id)
                # Perform update for request statuses
                if new_status == "تم الموافقة" and request_to_update.amount <= request_to_update.user.DELIVERED:
                    
                    request_to_update.user.DELIVERED -= request_to_update.amount
                    request_to_update.status = new_status
                    request_to_update.save()
                    request_to_update.user.save()

                    return Response(
                    {"success": True, "message": f"تم تحديث حالة طلب السحب بنجاح إلى '{new_status}'."},
                    status=status.HTTP_200_OK,
                )
                    
                elif new_status == "تم الرفض":
                    request_to_update.status = new_status
                    request_to_update.save()
                    return Response(
                        {"success": True, "message": f"تم تحديث حالة طلب السحب بنجاح إلى '{new_status}'."},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"error": True, "message": f"لا يوجد رصيد في الحساب كافي"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

        except Order.DoesNotExist as e:
            return Response({"error": _("Some orders do not exist.")}, status=status.HTTP_404_NOT_FOUND)

        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": _("Internal Server Error.")}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


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
