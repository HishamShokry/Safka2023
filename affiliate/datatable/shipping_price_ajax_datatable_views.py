from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from ..models import ShippingPrice, Governorate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from accounts.decorators import admin_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, F
from datetime import datetime
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_POST


# Constants
DRAW_PARAM = "draw"
START_PARAM = "start"
LENGTH_PARAM = "length"
SEARCH_VALUE_PARAM = "search[value]"
EXTRA_SEARCH_PREFIX = "extra_search["
START_DATE_PARAM = "start_date"  # Add this constant for consistency
END_DATE_PARAM = "end_date"  # Add this constant for consistency


@login_required
@admin_required
def shipping_price_api(request):
    try:
        draw = int(request.GET.get(DRAW_PARAM, 1))
        start = int(request.GET.get(START_PARAM, 0))
        length = int(request.GET.get(LENGTH_PARAM, 10))
        global_search_value = request.GET.get(SEARCH_VALUE_PARAM, "")
        start_date, end_date = request.GET.get("start_date", ""), request.GET.get(
            "end_date", ""
        )

        # Split the global search value into individual terms
        global_search_terms = global_search_value.split()

        # Start with an empty Q object to build the OR conditions for global search
        global_q_object = Q()

        # Build an OR condition for each term in the global search
        # Build an OR condition for each term in the global search
        for term in global_search_terms:
            global_q_object |= Q(governorate__governorate_name_ar__icontains=term)
            global_q_object |= Q(price__icontains=term)

        # Filter data based on the constructed Q object for global search
        shipping_price = ShippingPrice.objects.filter(global_q_object)

        # Apply date range filter
        if start_date and end_date:
            shipping_price = shipping_price.filter(
                updated_at__range=[start_date, end_date]
            )

        # Handle individual column searches
        extra_search = {}
        for key, value in request.GET.items():
            if key.startswith("extra_search[") and value:
                column_name = key[
                    len("extra_search[") : -1
                ]  # Extract the column name from the key
                # Check if the column corresponds to a ForeignKey relationship
                if column_name == "governorate":
                    # Use the related model's field for filtering
                    extra_search[
                        f"{column_name}__governorate_name_ar__icontains"
                    ] = value
                else:
                    # For other columns, use icontains as usual
                    extra_search[f"{column_name}__icontains"] = value

        # Apply individual column filters
        if extra_search:
            shipping_price = shipping_price.filter(**extra_search)

        # Apply sorting
        order_column_index = int(request.GET.get("order[0][column]", 0))
        order_direction = request.GET.get("order[0][dir]", "asc")

        # Map DataTables column index to your model fields
        order_columns = [
            "id",
            "governorate",
            "price",
            "created_at",
            "updated_at",
        ]  # Adjust as needed

        # Apply sorting
        order_column_name = order_columns[order_column_index]
        if order_direction == "desc":
            order_column_name = f"-{order_column_name}"

        shipping_price = shipping_price.order_by(order_column_name)

        # Count total records after filtering
        total_records = shipping_price.count()

        # Apply pagination
        shipping_price = shipping_price[start : start + length]

        data = []
        for shipping_price in shipping_price:
            data.append(
                {
                    "id": shipping_price.id,
                    "governorate": shipping_price.governorate.governorate_name_ar,
                    "price": shipping_price.price,
                    "created_at": shipping_price.created_at.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "updated_at": shipping_price.updated_at.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                }
            )

        response_data = {
            "draw": draw,
            "recordsTotal": total_records,
            "recordsFiltered": total_records,
            "data": data,
        }

        return JsonResponse(response_data, safe=False)

    except Exception as e:
        # Handle exceptions, log the error, and return an appropriate response
        return JsonResponse({"error": str(e)})


@login_required
@admin_required
def add_shipping_price(request):
    try:
        if request.method == "POST":
            governorate_id = request.POST.get("governorate")
            price = request.POST.get("price")

            if not governorate_id or not price:
                return JsonResponse(
                    {"success": False, "error": "مطلوب كل من المحافظة والسعر"}
                )

            # Retrieve the Governorate instance, case-insensitive search
            governorate = get_object_or_404(Governorate, id=governorate_id)

            # Check for duplicate shipping_price for the given governorate
            if ShippingPrice.objects.filter(governorate=governorate).exists():
                return JsonResponse(
                    {"success": False, "error": "سعر الشحن لهذه المحافظة موجود بالفعل"}
                )

            try:
                # Create a new ShippingPrice instance
                new_shipping_price = ShippingPrice.objects.create(
                    governorate=governorate, price=price
                )
                return JsonResponse({"success": True, "id": new_shipping_price.id})
            except IntegrityError:
                # Handle the case where a concurrent request created the shipping_price with the same name
                return JsonResponse(
                    {"success": False, "error": "Error creating shipping price"}
                )
        return JsonResponse({"success": False, "error": "Invalid request method"})
    except Governorate.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "No Governorate matches the given query"}
        )
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@login_required
@admin_required
def get_shipping_price(request, shipping_price_id):
    # Attempt to retrieve the ShippingPrice instance or return a 404 response
    shipping_price = get_object_or_404(ShippingPrice, id=shipping_price_id)

    # Create a dictionary containing the shipping_price details
    data = {
        "id": shipping_price.id,
        "ShippingGovernorate": shipping_price.governorate.governorate_name_ar,
        "ShippingPrice": shipping_price.price,
        "created_at": shipping_price.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": shipping_price.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
    }

    # Return the shipping_price details as a JSON response
    return JsonResponse(data)


@login_required
@admin_required
@require_POST
def delete_shipping_price(request, shipping_price_id):
    try:
        shipping_price = get_object_or_404(ShippingPrice, id=shipping_price_id)
        shipping_price.delete()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@login_required
@admin_required
@require_POST
def update_shipping_price(request):
    shipping_price_id = request.POST.get("id")
    # updated_governorate = request.POST.get("name")
    updated_price = request.POST.get("updated_price")

    try:
        shipping_price = ShippingPrice.objects.get(id=shipping_price_id)
        shipping_price.price = updated_price

        shipping_price.save()
        return JsonResponse({"success": True})
    except ShippingPrice.DoesNotExist:
        return JsonResponse({"success": False, "error": "ShippingPrice not found"})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@require_GET
def search_governorates(request):
    try:
        search_term = request.GET.get("q", "")

        # Exclude Governorates with a corresponding entry in ShippingPrice
        governorates_without_price = Governorate.objects.exclude(
            shippingprice__isnull=False
        )

        # Perform a case-insensitive search on the Governorate model
        results = governorates_without_price.filter(governorate_name_ar__icontains=search_term)

        # Paginate the results
        page = request.GET.get("page", 1)
        paginator = Paginator(results, 10)  # Show 10 results per page
        try:
            current_results = paginator.page(page)
        except PageNotAnInteger:
            current_results = paginator.page(1)
        except EmptyPage:
            current_results = paginator.page(paginator.num_pages)

        # Format the paginated results as needed by Select2
        data = [
            {"id": gov.id, "text": gov.governorate_name_ar} for gov in current_results
        ]

        return JsonResponse(
            {
                "results": data,
                "pagination": {
                    "more": current_results.has_next(),
                },
            }
        )
    except Exception as e:
        return JsonResponse({"error": str(e)})
