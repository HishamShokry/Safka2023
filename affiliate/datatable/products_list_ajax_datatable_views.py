from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from ..models import Product
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
def products_list_api(request):
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
            global_q_object |= Q(name__icontains=term)
            global_q_object |= Q(id__icontains=term)

        # Filter data based on the constructed Q object for global search
        products_list = Product.objects.filter(global_q_object)

        # Apply date range filter
        if start_date and end_date:
            products_list = products_list.filter(
                updated_at__range=[start_date, end_date]
            )

        # Handle individual column searches
        extra_search = {}
        for key, value in request.GET.items():
            if key.startswith("extra_search[") and value:
                column_name = key[
                    len("extra_search[") : -1
                ]  # Extract the column name from the key
                if column_name == "governorate":
                    # Use the related model's field for filtering
                    extra_search[f"{column_name}__governorate_name_ar__icontains"] = value
                elif column_name == "vendor":
                    # Use the related model's field for filtering
                    extra_search[f"{column_name}__email__icontains"] = value
                elif column_name == "category":
                    # Use the related model's field for filtering
                    extra_search[f"{column_name}__name__icontains"] = value
                # Add other ForeignKey relationships as needed
                elif column_name == "inventory":
                    # Use the related model's field for filtering
                    extra_search[f"{column_name}__name__icontains"] = value
                # Add other ForeignKey relationships as needed
                else:
                    # For other columns, use icontains as usual
                    extra_search[f"{column_name}__icontains"] = value

        # Apply individual column filters
        if extra_search:
            products_list = products_list.filter(**extra_search)

        # Apply sorting
        order_column_index = int(request.GET.get("order[0][column]", 0))
        order_direction = request.GET.get("order[0][dir]", "asc")

        # Map DataTables column index to your model fields
        order_columns = [
            "id",
            "name",
            "category",
            "vendor",
            "inventory",
            "purchase_price",
            "sale_price",
            "description",
            "note",
            "media_url",
            "is_active",
            "access_type",
            "access_to",
            "created_at",
            "updated_at",
        ]  # Adjust as needed

        # Apply sorting
        order_column_name = order_columns[order_column_index]
        if order_direction == "desc":
            order_column_name = f"-{order_column_name}"

        products_list = products_list.order_by(order_column_name)

        # Count total records after filtering
        total_records = products_list.count()

        # Apply pagination
        products_list = products_list[start : start + length]

        data = []
        for products_list in products_list:
            data.append(
                {
                    "id": products_list.id,
                    "name": products_list.name,
                    "category": products_list.category.name,
                    "vendor": products_list.vendor.email,
                    "inventory": products_list.inventory.name,
                    "sale_price": products_list.sale_price,
                    "purchase_price": products_list.purchase_price,
                    "description": products_list.description,
                    "note": products_list.note,
                    "image": products_list.image.url,
                    "media_url": products_list.media_url,
                    "is_active": products_list.is_active,
                    "access_type": products_list.access_type,
                    "access_to": ", ".join(
                        user.email for user in products_list.access_to.all()
                    ),
                    "created_at": products_list.created_at.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "updated_at": products_list.updated_at.strftime(
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
def add_products_list(request):
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

            # Check for duplicate products_list for the given governorate
            if ShippingPrice.objects.filter(governorate=governorate).exists():
                return JsonResponse(
                    {"success": False, "error": "سعر الشحن لهذه المحافظة موجود بالفعل"}
                )

            try:
                # Create a new ShippingPrice instance
                new_products_list = ShippingPrice.objects.create(
                    governorate=governorate, price=price
                )
                return JsonResponse({"success": True, "id": new_products_list.id})
            except IntegrityError:
                # Handle the case where a concurrent request created the products_list with the same name
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
def get_products_list(request, products_list_id):
    # Attempt to retrieve the ShippingPrice instance or return a 404 response
    products_list = get_object_or_404(ShippingPrice, id=products_list_id)

    # Create a dictionary containing the products_list details
    data = {
        "id": products_list.id,
        "ShippingGovernorate": products_list.governorate.governorate_name_ar,
        "ShippingPrice": products_list.price,
        "created_at": products_list.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": products_list.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
    }

    # Return the products_list details as a JSON response
    return JsonResponse(data)


@login_required
@admin_required
@require_POST
def delete_products_list(request, products_list_id):
    try:
        products_list = get_object_or_404(ShippingPrice, id=products_list_id)
        products_list.delete()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@login_required
@admin_required
@require_POST
def update_products_list(request):
    products_list_id = request.POST.get("id")
    # updated_governorate = request.POST.get("name")
    updated_price = request.POST.get("updated_price")

    try:
        products_list = ShippingPrice.objects.get(id=products_list_id)
        products_list.price = updated_price

        products_list.save()
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
        results = governorates_without_price.filter(
            governorate_name_ar__icontains=search_term
        )

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
