"""
URL configuration for safka project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from .datatable import (
    category_ajax_datatable_views,
    inventory_ajax_datatable_views,
    shipping_ajax_datatable_views,
    shipping_price_ajax_datatable_views,
    products_list_ajax_datatable_views,
)
from . import views
from .views_admin import admin_panel_views, admin_api_views
from .views_marketers import marketer_panel_views
from .views_vendors import vendor_panel_views

from rest_framework.routers import DefaultRouter
from accounts.views import VendorViewSet, MarketerViewSet


router = DefaultRouter()

router.register(r"vendors_api", VendorViewSet, basename="vendor")
router.register(r"marketers_api", MarketerViewSet, basename="marketer")

router.register(r"requests_api", admin_api_views.RequestViewSetAdmin, basename="requests")


router.register(r"categories_api", admin_api_views.CategoryViewSet, basename="category")
router.register(r"inventory_api", admin_api_views.InventoryViewSet, basename="inventory")
router.register(
    r"ShippingCompany_api",
    admin_api_views.ShippingCompanyViewSetAdmin,
    basename="shippingcompany",
)
router.register(
    r"ShippingPrice_api", admin_api_views.ShippingPriceViewSetAdmin, basename="shippingprice"
)
router.register(
    r"GovernoratePrice_api", admin_api_views.GovernorateViewSetAdmin, basename="Governorate"
)
router.register(r"products_api", admin_api_views.ProductViewSetAdmin, basename="products")
router.register(
    r"product_variant_api", admin_api_views.ProductVariantViewSetAdmin, basename="product_variant"
)
router.register(r"order_api", admin_api_views.OrderViewSetAdmin, basename="order")
router.register(r"order_item_api", admin_api_views.OrderItemViewSetAdmin, basename="order_item")

urlpatterns = [
    path("", admin_panel_views.dashboard, name="dashboard"),
    path("dashboard", admin_panel_views.dashboard, name="dashboard"),
    path("category", admin_panel_views.category, name="category"),
    path("products", admin_panel_views.products, name="products"),
    path("list_of_product", admin_panel_views.list_of_product, name="list_of_product"),
    path("products/<int:id>", admin_panel_views.product_detail, name="product_detail"),
    path("shipping", admin_panel_views.shipping, name="shipping"),
    path("price_shipping", admin_panel_views.shipping_price, name="price_shipping"),
    path("inventory", admin_panel_views.inventory, name="inventory"),
    path("orders", admin_panel_views.orders, name="orders"),
    path("requests", admin_panel_views.requests, name="requests"),
    path("vendors_accounts", admin_panel_views.vendors_accounts, name="vendors_accounts"),
    path("marketers_accounts", admin_panel_views.marketers_accounts, name="marketers_accounts"),
    path("support", admin_panel_views.support, name="support"),
    path("profile", admin_panel_views.profile, name="profile"),
    
    
    
    # marketer
    path("marketer/", marketer_panel_views.marketer_dashboard, name="marketer_dashboard"),
    path("marketer/dashboard", marketer_panel_views.marketer_dashboard, name="marketer_dashboard"),
    path("marketer/products", marketer_panel_views.marketer_products, name="marketer_products"),
    path(
        "marketer/products/<int:id>",
        marketer_panel_views.marketer_product_detail,
        name="marketer_product_detail",
    ),
    path("marketer/orders", marketer_panel_views.marketer_orders, name="marketer_orders"),
    path("marketer/requests", marketer_panel_views.marketer_requests, name="marketer_requests"),
    path("marketer/support", marketer_panel_views.marketer_support, name="marketer_support"),
    path("marketer/profile", marketer_panel_views.marketer_profile, name="marketer_profile"),
    
    
    
    # vendor
    path("vendor/", vendor_panel_views.vendor_dashboard, name="vendor_dashboard"),
    path("vendor/dashboard", vendor_panel_views.vendor_dashboard, name="vendor_dashboard"),
    path("vendor/products", vendor_panel_views.vendor_products, name="vendor_products"),
    path(
        "vendor/products/<int:id>",
        vendor_panel_views.vendor_product_detail,
        name="vendor_product_detail",
    ),
    path("vendor/orders", vendor_panel_views.vendor_orders, name="vendor_orders"),
    path("vendor/requests", vendor_panel_views.vendor_requests, name="vendor_requests"),
    path("vendor/support", vendor_panel_views.vendor_support, name="vendor_support"),
    path("vendor/profile", vendor_panel_views.vendor_profile, name="vendor_profile"),







    path("api/", include(router.urls)),
    path("get-cities/<int:governorate_id>/", admin_api_views.get_cities, name="get_cities"),
    path("get-product/<int:product_id>/", admin_api_views.get_product, name="get_product"),
    path("get-variants/<int:product_id>/", admin_api_views.get_variants, name="get_variants"),
    path("product/search/", admin_api_views.product_search, name="product_search"),
    path("marketer/search/", admin_api_views.marketer_search, name="marketer_search"),
    path("company/search/", admin_api_views.get_shipping_company, name="get_shipping_company"),
    path("get_sale_price/<int:product_id>/", admin_api_views.get_sale_price, name="get_sale_price"),
    path("get_shipping_price/<int:governorate_id>/", admin_api_views.get_shipping_price, name="get_shipping_price"),
]
