from rest_framework import viewsets
from rest_framework.response import Response
from affiliate.serializers import *
from rest_framework.decorators import action, api_view
from rest_framework import status
from rest_framework import generics, permissions
from django.views.decorators.http import  require_GET

from django.http import JsonResponse
from django.db import transaction
from affiliate.models import *
from django.shortcuts import get_object_or_404
from django.views.decorators.http import  require_GET
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, F # Import Q for complex queries





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





class OrderViewSetMarketer(DataTableMixin, viewsets.ModelViewSet):
    # queryset = Order.objects.filter(marketer=marketer).select_related('marketer', 'city', 'governorate__governorate', 'shipping_company').prefetch_related('items', 'history_entries__updated_by')
    serializer_class = OrderSerializer
    # permission_classes = [permissions.IsAdminUser]
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
                "created_at",
                "updated_at",
            ] 
    
    def get_queryset(self):
        # Assuming you have access to the requesting user
        requesting_user = self.request.user

        # Get the marketer object for the requesting user
        marketer = get_object_or_404(User, email=requesting_user)
        queryset = Order.objects.filter(marketer=marketer).select_related('marketer', 'city', 'governorate__governorate', 'shipping_company').prefetch_related('items', 'history_entries__updated_by')

        return queryset

    


    @action(detail=True, methods=["get"])
    def datatable_list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return self.handle_datatables_request(queryset, self.serializer_class, self.order_columns, request)
    
    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                order_data, variants_data = self.extract_data_from_request(request.data)
                order_data.update({'marketer': request.user.id})
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
                order_data.update({'marketer': request.user.id})

                order_serializer = OrderSerializer(order, data=order_data)
                if not order_serializer.is_valid():
                    return Response(
                        {"error": order_serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                order_serializer = OrderSerializer(order, data=order_data)

                self.rollback_logic(order)
                order_serializer = OrderSerializer(order, data=order_data)


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
        item_total_price = sum(int(item["total_item_price"]) for item in variants_data)
        return order.total - (order.shiping_price + item_total_price)


    def retrieve(self, request, *args, **kwargs):
        # Assuming you have an 'Order' model
        try:
            # Call the default retrieve method to get the instance
            instance = self.get_object()
        except Http404:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Convert the instance to a serialized format using Django REST framework serializers
        serializer = self.get_serializer(instance)
        serialized_order = serializer.data

        # Get the IDs of the next and previous orders
        next_order_id = Order.objects.filter(id__gt=instance.id).order_by('id').values_list('id', flat=True).first()
        prev_order_id = Order.objects.filter(id__lt=instance.id).order_by('-id').values_list('id', flat=True).first()

        return Response({'order': serialized_order, 'next_order_pk': next_order_id, 'prev_order_pk': prev_order_id}, status=status.HTTP_200_OK)


class OrderItemViewSetMarketer(DataTableMixin, viewsets.ModelViewSet):
    queryset = OrderItem.objects.select_related('order', 'product').all()
    serializer_class = OrderItemSerializer
    # permission_classes = [permissions.IsAdminUser]




class RequestViewSetMarketer(DataTableMixin, viewsets.ModelViewSet):
    # queryset = Request.objects.all()
    serializer_class = RequestSerializer
    # permission_classes = [permissions.IsAdminUser]

    
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


    def get_queryset(self):
        # Assuming you have access to the requesting user
        requesting_user = self.request.user

        # Get the marketer object for the requesting user
        marketer = get_object_or_404(User, email=requesting_user)
        queryset = Request.objects.filter(user=marketer)

        return queryset
    
    @action(detail=True, methods=["get"])
    def datatable_list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return self.handle_datatables_request(queryset, self.serializer_class, self.order_columns, request)
  

    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                request_data = request.data.copy()
                request_data['user'] = request.user.id 
                serializer = self.serializer_class(data=request_data)

            if serializer.is_valid():
                # If the data is valid, save the instance and return a successful response
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(
                        {"error": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        except Exception as e:
            # Log the detailed error message for debugging
            print(f"Error creating order: {str(e)}")
            # transaction.set_rollback(True)  # Rollback the transaction
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
