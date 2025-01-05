from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView

class ListVendorAPI(APIView):
    """
    API untuk mendapatkan daftar vendor sebagai dropdown
    """
    def get(self, request, *args, **kwargs):
        """
        Handle fetching dropdown data for vendor
        """
        try:
            with connection.cursor() as cursor:
                cursor.callproc("sp_dropdown_vendor")
                columns = [col[0] for col in cursor.description]
                result = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return JsonResponse(result, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
