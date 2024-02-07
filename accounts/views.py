from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth import authenticate, login ,logout
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import *
from rest_framework.decorators import action, api_view
from rest_framework import status
from rest_framework import generics, permissions
from django.db.models import Q, F  # Import Q for complex queries



def index(request):
    return render(request, 'index.html')

def signupMarketer(request):
    msg = None
    if request.method == 'POST':
        form = SignUpFormMarketer(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_marketer = True
            user.save()
            msg = 'User Created'
            return redirect('signin')
        else:
            msg = 'Form is not Valid!'
    else:
        form = SignUpFormMarketer()
    return render(request, 'signupMarketer.html', {'form': form, 'msg': msg})



def signupVendor(request):
    msg = None
    if request.method == 'POST':
        form = SignUpFormVendor(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_vendor = True
            user.save()
            msg = 'User Created'
            return redirect('signin')
        else:
            msg = 'Form is not Valid!'
    else:
        form = SignUpFormVendor()
    return render(request, 'signupVendor.html', {'form': form, 'msg': msg})


def signin(request):
    form = SignInForm
    msg = None
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = authenticate(username=email, password=password)
            if user is not None:    
                login(request, user)
                if user.is_admin:
                    return redirect('dashboard')
                elif user.is_vendor:
                    return redirect('vendor_dashboard')
                elif user.is_marketer:
                    return redirect('marketer_dashboard')
                else:
                    return redirect('dashboard')
        else:
            msg = 'البريد الاكتروني او كلمة السر غير صحيحة'
    
    return render(request, 'signin.html', {'form': form, 'msg': msg})


@login_required
def user_logout(request):
    logout(request)
    return redirect('index')



class VendorViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_vendor=True)
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ['get']

    # def get(self, request, *args, **kwargs):
    #         queryset = User.objects.filter(is_vendor=True)
    #         serializer = AccountSerializer(queryset, many=True)
    #         return Response(serializer.data)
    
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
                global_q_object |= Q(username__icontains=term)
                # Add other global search columns as needed

            # Filter data based on the constructed Q object for global search
            vednors = self.queryset.filter(global_q_object)

            # Apply date range filter
            if start_date and end_date:
                vednors = vednors.filter(date_joined__range=[start_date, end_date])

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
                vednors = vednors.filter(**extra_search)

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

            vednors = vednors.order_by(order_column_name)

            # Count total records after filtering
            total_records = vednors.count()

            # Apply pagination
            vednors = vednors[start : start + length]

            serializer = AccountSerializer(vednors, many=True)

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





class MarketerViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_marketer=True)
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAdminUser]
    http_method_names = ['get']

    # def get(self, request, *args, **kwargs):
    #         queryset = User.objects.filter(is_vendor=True)
    #         serializer = AccountSerializer(queryset, many=True)
    #         return Response(serializer.data)
    
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
                global_q_object |= Q(username__icontains=term)
                # Add other global search columns as needed

            # Filter data based on the constructed Q object for global search
            vednors = self.queryset.filter(global_q_object)

            # Apply date range filter
            if start_date and end_date:
                vednors = vednors.filter(date_joined__range=[start_date, end_date])

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
                vednors = vednors.filter(**extra_search)

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

            vednors = vednors.order_by(order_column_name)

            # Count total records after filtering
            total_records = vednors.count()

            # Apply pagination
            vednors = vednors[start : start + length]

            serializer = AccountSerializer(vednors, many=True)

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
