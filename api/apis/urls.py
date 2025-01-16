from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views.usermanagement import UserManagementAPI
from .views.vendordata import VendorDataAPI
from .views.customerdata import CustomerDataAPI
from .views.login import LoginAPI
from .views.vendoritem import VendorItemAPI
from .views.listvendor import ListVendorAPI
from .views.customeritem import CustomerItemAPI
from .views.moneymanagement import MoneyManagementAPI
from .views.locklimitrekening import LockLimitRekeningAPI
from .views.requestpo import RequestPOAPI
from .views.updaterequestpo import UpdateRequestPOAPI
from .views.vendoritempriceunit import VendorItemPriceUnitAPI
from .views.datetime import DateTimeAPI
from .views.selectvendoritem import VendorItemDropdownAPI
from .views.selectvendor import VendorDropdownAPI
from django.http import HttpResponse


# Home view function
def home_view(request):
    """
    Home view to provide an API overview or welcome message.
    """
    return HttpResponse("Development Server, add path in URL to see JSON Data")


urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls, name='admin'),

    # Home
    path('', home_view, name='home'),

    # Login Endpoints API
    path('login/', LoginAPI.as_view(), name='login'),

    # User Management Endpoints API
    path('usermanagement/', UserManagementAPI.as_view(), name='user_management'),

    # Vendor Data Endpoints API
    path('vendordata/', VendorDataAPI.as_view(), name='vendor_data'),

    # Customer Data Endpoints API
    path('customerdata/', CustomerDataAPI.as_view(), name='customer_data'),

    # Barang Vendor Endpoints API
    path('vendoritem/', VendorItemAPI.as_view(), name='vendor_item'),

    # List Vendor Endpoints API
    path('listvendor/', ListVendorAPI.as_view(), name='list_vendor'),

    # Barang Customer Endpoints API
    path('customeritem/', CustomerItemAPI.as_view(), name='customer_item'),

    # Money Management Endpoints API
    path('moneymanagement/', MoneyManagementAPI.as_view(), name='money_management'),

    # Lock Limit Rekening Endpoints API
    path('locklimitrekening/', LockLimitRekeningAPI.as_view(), name='lock_limit_rekening'),

    # RequestPO Endpoints API
    path('requestpo/', RequestPOAPI.as_view(), name='requst_po'),

    # Update RequestPO Endpoints API
    path('updaterequestpo/', UpdateRequestPOAPI.as_view(), name='update_requst_po'),

    # Vendor Item Price Unit Endpoints API
    path('vendoritempriceunit/', VendorItemPriceUnitAPI.as_view(), name='vendor_item_price_unit'),

    # Date Time Endpoints API
    path('datetime/', DateTimeAPI.as_view(), name='date_time'),

    # Select Vendor Item Endpoints API
    path('selectvendoritem/', VendorItemDropdownAPI.as_view(), name='select_vendor_item'),

    # Select Vendor Endpoints API
    path('selectvendor/', VendorDropdownAPI.as_view(), name='select_vendor'),


    # Token Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
