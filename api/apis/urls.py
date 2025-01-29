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
from .views.moneymanagement import MoneyManagementAPI, SummaryPOSOAPI
from .views.locklimitrekening import LockLimitRekeningAPI
from .views.requestpo import RequestPOAPI
from .views.updaterequestpo import UpdateRequestPOAPI
from .views.vendoritempriceunit import VendorItemPriceUnitAPI
from .views.datetime import DateTimeAPI
from .views.selectvendoritem import VendorItemDropdownAPI
from .views.selectvendor import VendorDropdownAPI
from .views.itemmanagement import ItemManagementAPI
from .views.itemmanagement import handle_download_template 
from .views.requestso import RequestSOAPI
from .views.updaterequestso import UpdateRequestSOAPI
from .views.selectcustomer import CustomerDropdownAPI
from .views.selectcustomeritem import CustomerItemDropdownAPI
from .views.customeritempriceunit import CustomerItemPriceUnitAPI

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

    # Summary PO SO Endpoints API
    path('summary_po_so/', SummaryPOSOAPI.as_view(), name='summary-po-so'),

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

    # Item IN/OUT Management Endpoints API
    path('itemmanagement/', ItemManagementAPI.as_view(), name='item_management'),

    # Item Donwload IN/OUT dpoints API
    path('itemmanagement/template/<str:category>/', handle_download_template, name='handle_download_template'),

     # RequestPO Endpoints API
    path('requestso/', RequestSOAPI.as_view(), name='requst_So'),

     # Update RequestPO Endpoints API
    path('updaterequestso/', UpdateRequestSOAPI.as_view(), name='update_requst_so'),

    # Select Vendor Item Endpoints API
    path('selectcustomer/', CustomerDropdownAPI.as_view(), name='select_customer'),

     # Select Vendor Item Endpoints API
    path('selectcustomeritem/', CustomerItemDropdownAPI.as_view(), name='select_customer_item'),

     # Select Vendor Endpoints AP
    path('customeritempriceunit/', CustomerItemPriceUnitAPI.as_view(), name='customer_item_price_unit'),

    # Token Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]