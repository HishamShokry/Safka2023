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

            serializer = serializer_class(items, many=True, context={'request': request})

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



class OrderViewSetVendor(DataTableMixin, viewsets.ModelViewSet):
    serializer_class = OrderSerializerVendor
    # permission_classes = [permissions.IsAdminUser]
    order_columns = [
                "id",
                "barcode",
                "status",
                "shiping_price",
                "governorate",
                "city",
                "updated_at"
            ] 
    http_method_names = ['get']

    def get_queryset(self):
        # Assuming you have access to the requesting user
        requesting_user = self.request.user
        # Get the marketer object for the requesting user
        vendor = get_object_or_404(User, email=requesting_user)
        queryset = Order.objects.filter(items__product__vendor=vendor).select_related('marketer', 'city', 'governorate__governorate', 'shipping_company').prefetch_related('items', 'history_entries__updated_by')
        return queryset

    


    @action(detail=True, methods=["get"])
    def datatable_list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return self.handle_datatables_request(queryset, self.serializer_class, self.order_columns, request)
    


    # def retrieve(self, request, *args, **kwargs):
    #     # Assuming you have an 'Order' model
    #     try:
    #         # Call the default retrieve method to get the instance
    #         instance = self.get_object()
    #     except Http404:
    #         return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    #     # Convert the instance to a serialized format using Django REST framework serializers
    #     serializer = self.get_serializer(instance)
    #     serialized_order = serializer.data

    #     # Get the IDs of the next and previous orders
    #     next_order_id = Order.objects.filter(id__gt=instance.id).order_by('id').values_list('id', flat=True).first()
    #     prev_order_id = Order.objects.filter(id__lt=instance.id).order_by('-id').values_list('id', flat=True).first()

    #     return Response({'order': serialized_order, 'next_order_pk': next_order_id, 'prev_order_pk': prev_order_id}, status=status.HTTP_200_OK)


class OrderItemViewSetVendor(DataTableMixin, viewsets.ModelViewSet):
    queryset = OrderItem.objects.select_related('order', 'product').all()
    serializer_class = OrderItemSerializer
    # permission_classes = [permissions.IsAdminUser]




class RequestViewSetVendor(DataTableMixin, viewsets.ModelViewSet):
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
        vendor = get_object_or_404(User, email=requesting_user)
        queryset = Request.objects.filter(user=vendor)

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
