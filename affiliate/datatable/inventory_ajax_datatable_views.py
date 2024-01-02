from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from ..models import Inventory
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
def inventory_api(request):
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
        inventories = Inventory.objects.filter(global_q_object)

        # Apply date range filter
        if start_date and end_date:
            inventories = inventories.filter(updated_at__range=[start_date, end_date])

        # Handle individual column searches
        extra_search = {}
        for key, value in request.GET.items():
            if key.startswith('extra_search[') and value:
                column_name = key[len('extra_search['):-1]  # Extract the column name from the key
                extra_search[f'{column_name}__icontains'] = value

        # Apply individual column filters
        if extra_search:
            inventories = inventories.filter(**extra_search)

        # Apply sorting
        order_column_index = int(request.GET.get('order[0][column]', 0))
        order_direction = request.GET.get('order[0][dir]', 'asc')

        # Map DataTables column index to your model fields
        order_columns = ['id', 'name', 'created_at', 'updated_at']  # Adjust as needed

        # Apply sorting
        order_column_name = order_columns[order_column_index]
        if order_direction == 'desc':
            order_column_name = f'-{order_column_name}'

        inventories = inventories.order_by(order_column_name)

        # Count total records after filtering
        total_records = inventories.count()

        # Apply pagination
        inventories = inventories[start:start + length]

        data = []
        for inventory in inventories:
            data.append({
                'id': inventory.id,
                'name': inventory.name,
                'created_at': inventory.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': inventory.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
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
def add_inventory(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('name')
            print(name)

            if not name:
                return JsonResponse({'success': False, 'error': 'Name is required'})

            # Check for duplicate inventory name
            if Inventory.objects.filter(name=name).exists():
                return JsonResponse({'success': False, 'error': 'المخزن بهذا الاسم موجودة بالفعل'})

            try:
                new_inventory = Inventory.objects.create(name=name)
                print(new_inventory)
                return JsonResponse({'success': True, 'id': new_inventory.id})
            except IntegrityError:
                # Handle the case where a concurrent request created the inventory with the same name
                return JsonResponse({'success': False, 'error': 'المخزن بهذا الاسم موجودة بالفعل'})

        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})



@login_required
@admin_required
def get_inventory(request, inventory_id):
    # Attempt to retrieve the Inventory instance or return a 404 response
    inventory = get_object_or_404(Inventory, id=inventory_id)

    # Create a dictionary containing the inventory details
    data = {
        'id': inventory.id,
        'name': inventory.name,
        'created_at': inventory.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': inventory.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
    }

    # Return the inventory details as a JSON response
    return JsonResponse(data)



@login_required
@admin_required
@require_POST
def delete_inventory(request, inventory_id):
    try:
        inventory = get_object_or_404(Inventory, id=inventory_id)
        inventory.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
@admin_required
@require_POST
def update_inventory(request):
    inventory_id = request.POST.get('id')
    updated_name = request.POST.get('name')
    print(inventory_id)

    try:
        inventory = Inventory.objects.get(id=inventory_id)
        print(inventory)
        inventory.name = updated_name
        inventory.save()
        return JsonResponse({'success': True})
    except Inventory.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Inventory not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})