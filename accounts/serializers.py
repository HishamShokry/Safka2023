import json
import re
from rest_framework import serializers
from .models import *
from django.contrib.auth.decorators import login_required
from accounts.decorators import *


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'is_active', 'date_joined', 'mobile_number', 'PENDING', 'PREPARATION', 'SHIPPED', 'DELIVERED']


