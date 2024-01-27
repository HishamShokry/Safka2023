from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from ..models import ShippingCompany
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from accounts.decorators import admin_required
from django.core.paginator import Paginator
from django.db.models import Q, F
from datetime import datetime
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_POST



# Constants
DRAW_PARAM = 'draw'
START_PARAM = 'start'
LENGTH_PARAM = 'length'
SEARCH_VALUE_PARAM = 'search[value]'
EXTRA_SEARCH_PREFIX = 'extra_search['
START_DATE_PARAM = 'start_date'  # Add this constant for consistency
END_DATE_PARAM = 'end_date'  # Add this constant for consistency


@login_required
@admin_required
def shipping_api(request):
    try:
        draw = int(request.GET.get(DRAW_PARAM, 1))
        start = int(request.GET.get(START_PARAM, 0))
        length = int(request.GET.get(LENGTH_PARAM, 10))
        global_search_value = request.GET.get(SEARCH_VALUE_PARAM, '')
        start_date, end_date = request.GET.get('start_date', ''), request.GET.get('end_date', '')

        # Split the global search value into individual terms
        global_search_terms = global_search_value.split()

        # Start with an empty Q object to build the OR conditions for global search
        global_q_object = Q()

        # Build an OR condition for each term in the global search
        for term in global_search_terms:
            global_q_object |= Q(name__icontains=term)
            # Add other global search columns as needed

        # Filter data based on the constructed Q object for global search
        shippingCompanies = ShippingCompany.objects.filter(global_q_object)

        # Apply date range filter
        if start_date and end_date:
            shippingCompanies = shippingCompanies.filter(updated_at__range=[start_date, end_date])

        # Handle individual column searches
        extra_search = {}
        for key, value in request.GET.items():
            if key.startswith('extra_search[') and value:
                column_name = key[len('extra_search['):-1]  # Extract the column name from the key
                extra_search[f'{column_name}__icontains'] = value

        # Apply individual column filters
        if extra_search:
            shippingCompanies = shippingCompanies.filter(**extra_search)

        # Apply sorting
        order_column_index = int(request.GET.get('order[0][column]', 0))
        order_direction = request.GET.get('order[0][dir]', 'asc')

        # Map DataTables column index to your model fields
        order_columns = ['id', 'name', 'website', 'created_at', 'updated_at']  # Adjust as needed

        # Apply sorting
        order_column_name = order_columns[order_column_index]
        if order_direction == 'desc':
            order_column_name = f'-{order_column_name}'

        shippingCompanies = shippingCompanies.order_by(order_column_name)

        # Count total records after filtering
        total_records = shippingCompanies.count()

        # Apply pagination
        shippingCompanies = shippingCompanies[start:start + length]

        data = []
        for shipping in shippingCompanies:
            data.append({
                'id': shipping.id,
                'name': shipping.name,
                'website': shipping.website,
                'created_at': shipping.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': shipping.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            })

        response_data = {
            'draw': draw,
            'recordsTotal': total_records,
            'recordsFiltered': total_records,
            'data': data,
        }

        return JsonResponse(response_data, safe=False)

    except Exception as e:
        # Handle exceptions, log the error, and return an appropriate response
        return JsonResponse({'error': str(e)})


@login_required
@admin_required
def add_shipping(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('name')
            website = request.POST.get('website')
            print(name)

            if not name:
                return JsonResponse({'success': False, 'error': 'Name is required'})

            # Check for duplicate shipping name
            if ShippingCompany.objects.filter(name=name).exists():
                return JsonResponse({'success': False, 'error': 'شركة شحن بهذا الاسم موجودة بالفعل'})

            try:
                new_shipping = ShippingCompany.objects.create(name=name, website=website)
                print(new_shipping)
                return JsonResponse({'success': True, 'id': new_shipping.id})
            except IntegrityError:
                # Handle the case where a concurrent request created the shipping with the same name
                return JsonResponse({'success': False, 'error': 'شركة شحن بهذا الاسم موجودة بالفعل'})

        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})



@login_required
@admin_required
def get_shipping(request, shipping_id):
    # Attempt to retrieve the ShippingCompany instance or return a 404 response
    shipping = get_object_or_404(ShippingCompany, id=shipping_id)

    # Create a dictionary containing the shipping details
    data = {
        'id': shipping.id,
        'name': shipping.name,
        'website': shipping.website,
        'created_at': shipping.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': shipping.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
    }

    # Return the shipping details as a JSON response
    return JsonResponse(data)



@login_required
@admin_required
@require_POST
def delete_shipping(request, shipping_id):
    try:
        shipping = get_object_or_404(ShippingCompany, id=shipping_id)
        shipping.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@admin_required
@require_POST
def update_shipping(request):
    shipping_id = request.POST.get('id')
    updated_name = request.POST.get('name')
    updated_website = request.POST.get('website')

    try:
        shipping = ShippingCompany.objects.get(id=shipping_id)
        print(shipping)
        shipping.name = updated_name
        shipping.website = updated_website

        shipping.save()
        return JsonResponse({'success': True})
    except ShippingCompany.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'ShippingCompany not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})