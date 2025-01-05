from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

class VendorDataAPI(APIView):
    def execute_sp(self, feature, params):
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_supplymanagement', [feature, *params])
                if feature == 'READ':
                    return cursor.fetchall()
                return None
        except Exception as e:
            return str(e)

    def get(self, request):
        # READ data vendor
        results = self.execute_sp('READ', ['Vendor', '', '', '', '', '', '', '', '', '', '', '', ''])
        if isinstance(results, str):
            return JsonResponse({"error": results}, status=500)

        # Mapping hasil query ke dalam format JSON
        data = [
            {
                "id":           row[0],
                "name":         row[1],
                "address":      row[2],
                "phone":        row[3],
                "bank_account": row[4],
                "add_time":     row[5].strftime("%Y-%m-%d %H:%M:%S") if row[5] else None,
                "add_user":     row[6],
                "upd_time":     row[7].strftime("%Y-%m-%d %H:%M:%S") if row[7] else None,
                "upd_user":     row[8],
            }
            for row in results
        ]
        return JsonResponse(data, safe=False)

    def post(self, request):
        # INSERT data vendor
        data = JSONParser().parse(request)
        params = [
            'Vendor',
            data.get("name", ""),
            '',
            data.get("address", ""),
            data.get("phone", ""),
            data.get("bank_account", ""),
            '', '', '', '', '',
            '', 'yosephatigoran'
        ]
        error = self.execute_sp('INSERT', params)
        if isinstance(error, str):
            return JsonResponse({"error": error}, status=500)
        return JsonResponse({"message": "Vendor created successfully"}, status=201)

    def put(self, request):
        # UPDATE data vendor
        data = JSONParser().parse(request)
        params = [
            'Vendor',
            '', '', '', '', '',
            data.get("name", ""),
            '',
            data.get("address", ""),
            data.get("phone", ""),
            data.get("bank_account", ""),
            data.get("vendor_id", ""),
            'yosephatigoran'
        ]
        error = self.execute_sp('UPDATE', params)
        if isinstance(error, str):
            return JsonResponse({"error": error}, status=500)
        return JsonResponse({"message": "Vendor updated successfully"}, status=200)

    def delete(self, request):
        # DELETE data vendor
        data = JSONParser().parse(request)
        params = [
            'Vendor',
            '', '', '', '', '', '', '', '', '', '',
            data.get("vendor_id", ""),
            'yosephatigoran'
        ]
        error = self.execute_sp('DELETE', params)
        if isinstance(error, str):
            return JsonResponse({"error": error}, status=500)
        return JsonResponse({"message": "Vendor deleted successfully"}, status=200)