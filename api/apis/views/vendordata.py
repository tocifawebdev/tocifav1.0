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
        # Mengambil data vendor/pelanggan
        results = self.execute_sp('READ', ['Vendor', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
        if isinstance(results, str):
            return JsonResponse({"error": results}, status=500)

        # Mapping hasil query ke dalam format JSON
        data = [
            {
                "id": row[0],
                "name": row[1],
                "address": row[2],
                "email": row[3],
                "phone": row[4],
                "bank_account": row[5],
                "add_time": row[6].strftime("%Y-%m-%d %H:%M:%S") if row[6] else None,
                "add_user": row[7],
                "upd_time": row[8].strftime("%Y-%m-%d %H:%M:%S") if row[8] else None,
                "upd_user": row[9],
            }
            for row in results
        ]
        return JsonResponse(data, safe=False)

    def post(self, request):
        # Menambahkan data vendor baru
        data = JSONParser().parse(request)
        params = [
            'Vendor', '',  # param_vporvs, update_vporvsID
            data.get("name", ""),
            "",  # param_npwp (kosong untuk vendor)
            data.get("address", ""),
            data.get("email", ""),
            data.get("phone", ""),
            data.get("bank_account", ""),
            '', '', '', '', '', '',  # Update fields kosong
            'yosephatigoran'  # param_adduser
        ]
        error = self.execute_sp('INSERT', params)
        if isinstance(error, str):
            return JsonResponse({"error": error}, status=500)
        return JsonResponse({"message": "Vendor created successfully"}, status=201)

    def put(self, request):
        # Mengupdate data vendor
        data = JSONParser().parse(request)
        params = [
            'Vendor',  # param_vporvs
            data.get("vendor_id", ""),  # update_vporvsID
            '',  '', '', '', '', '',  # param fields kosong
            data.get("name", ""),  # update_name
            '',  # update_npwp
            data.get("address", ""),  # update_address
            data.get("email", ""),  # update_email
            data.get("phone", ""),  # update_phone
            data.get("bank_account", ""),  # update_bank
            'yosephatigoran'  # param_adduser
        ]
        error = self.execute_sp('UPDATE', params)
        if isinstance(error, str):
            return JsonResponse({"error": error}, status=500)
        return JsonResponse({"message": "Vendor updated successfully"}, status=200)

    def delete(self, request):
        # Menghapus data vendor
        data = JSONParser().parse(request)
        params = [
            'Vendor',  # param_vporvs
            data.get("vendor_id", ""),  # update_vporvsID
            '', '', '', '', '', '', '', '', '', '', '', '',  # Semua param kosong
            'yosephatigoran'  # param_adduser
        ]
        error = self.execute_sp('DELETE', params)
        if isinstance(error, str):
            return JsonResponse({"error": error}, status=500)
        return JsonResponse({"message": "Vendor deleted successfully"}, status=200)