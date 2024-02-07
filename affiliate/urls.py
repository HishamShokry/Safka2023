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
from rest_framework.routers import DefaultRouter
from accounts.views import VendorViewSet, MarketerViewSet


router = DefaultRouter()

router.register(r"vendors_api", VendorViewSet, basename="vendor")
router.register(r"marketers_api", MarketerViewSet, basename="marketer")

router.register(r"requests_api", views.RequestViewSetAdmin, basename="requests")


router.register(r"categories_api", views.CategoryViewSet, basename="category")
router.register(r"inventory_api", views.InventoryViewSet, basename="inventory")
router.register(
    r"ShippingCompany_api",
    views.ShippingCompanyViewSetAdmin,
    basename="shippingcompany",
)
router.register(
    r"ShippingPrice_api", views.ShippingPriceViewSetAdmin, basename="shippingprice"
)
router.register(
    r"GovernoratePrice_api", views.GovernorateViewSetAdmin, basename="Governorate"
)
router.register(r"products_api", views.ProductViewSetAdmin, basename="products")
router.register(
    r"product_variant_api", views.ProductVariantViewSetAdmin, basename="product_variant"
)
router.register(r"order_api", views.OrderViewSetAdmin, basename="order")
router.register(r"order_item_api", views.OrderItemViewSetAdmin, basename="order_item")

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("category", views.category, name="category"),
    path("products", views.products, name="products"),
    path("list_of_product", views.list_of_product, name="list_of_product"),
    path("products/<int:id>", views.product_detail, name="product_detail"),
    path("shipping", views.shipping, name="shipping"),
    path("price_shipping", views.shipping_price, name="price_shipping"),
    path("inventory", views.inventory, name="inventory"),
    path("orders", views.orders, name="orders"),
    path("requests", views.requests, name="requests"),
    path("vendors_accounts", views.vendors_accounts, name="vendors_accounts"),
    path("marketers_accounts", views.marketers_accounts, name="marketers_accounts"),
    path("support", views.support, name="support"),
    path("profile", views.profile, name="profile"),
    # marketer
    path("marketer/", views.marketer_dashboard, name="marketer_dashboard"),
    path("marketer/dashboard", views.marketer_dashboard, name="marketer_dashboard"),
    path("marketer/products", views.marketer_products, name="marketer_products"),
    path(
        "marketer/products/<int:id>",
        views.marketer_product_detail,
        name="marketer_product_detail",
    ),
    path("marketer/orders", views.marketer_orders, name="marketer_orders"),
    path("marketer/requests", views.marketer_requests, name="marketer_requests"),
    path("marketer/support", views.marketer_support, name="marketer_support"),
    path("marketer/profile", views.marketer_profile, name="marketer_profile"),
    # vendor
    path("vendor/", views.vendor_dashboard, name="vendor_dashboard"),
    path("vendor/dashboard", views.vendor_dashboard, name="vendor_dashboard"),
    path("vendor/products", views.vendor_products, name="vendor_products"),
    path(
        "vendor/products/<int:id>",
        views.vendor_product_detail,
        name="vendor_product_detail",
    ),
    path("vendor/orders", views.vendor_orders, name="vendor_orders"),
    path("vendor/requests", views.vendor_requests, name="vendor_requests"),
    path("vendor/support", views.vendor_support, name="vendor_support"),
    path("vendor/profile", views.vendor_profile, name="vendor_profile"),
    path("api/", include(router.urls)),
    path("get-cities/<int:governorate_id>/", views.get_cities, name="get_cities"),
    path("get-product/<int:product_id>/", views.get_product, name="get_product"),
    path("get-variants/<int:product_id>/", views.get_variants, name="get_variants"),
    path("product/search/", views.product_search, name="product_search"),
    path("marketer/search/", views.marketer_search, name="marketer_search"),
    path("company/search/", views.get_shipping_company, name="get_shipping_company"),
    path("get_sale_price/<int:product_id>/", views.get_sale_price, name="get_sale_price"),
    path("get_shipping_price/<int:governorate_id>/", views.get_shipping_price, name="get_shipping_price"),
]
