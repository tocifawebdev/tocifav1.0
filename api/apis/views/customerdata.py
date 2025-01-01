from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser


class CustomerDataAPI(APIView):
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
        # Mengambil data pelanggan
        results = self.execute_sp('READ', ['Pelanggan', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
        if isinstance(results, str):
            return JsonResponse({"error": results}, status=500)

        # Mapping hasil query ke dalam format JSON
        data = [
            {
                "id": row[0],
                "name": row[1],
                "npwp": row[2],
                "address": row[3],
                "email": row[4],
                "phone": row[5],
                "bank_account": row[6],
                "add_time": row[7].strftime("%Y-%m-%d %H:%M:%S") if row[7] else None,
                "add_user": row[8],
                "upd_time": row[9].strftime("%Y-%m-%d %H:%M:%S") if row[9] else None,
                "upd_user": row[10],
            }
            for row in results
        ]
        return JsonResponse(data, safe=False)

    def post(self, request):
        # Menambahkan data pelanggan baru
        data = JSONParser().parse(request)
        params = [
            'Pelanggan', '',  # param_vporvs, update_vporvsID
            data.get("name", ""),
            data.get("npwp", ""),
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
        return JsonResponse({"message": "Customer created successfully"}, status=201)

    def put(self, request):
        # Mengupdate data pelanggan
        data = JSONParser().parse(request)
        params = [
            'Pelanggan',  # param_vporvs
            data.get("customer_id", ""),  # update_vporvsID
            '',  '', '', '', '', '',  # param fields kosong
            data.get("name", ""),  # update_name
            data.get("npwp", ""),  # update_npwp
            data.get("address", ""),  # update_address
            data.get("email", ""),  # update_email
            data.get("phone", ""),  # update_phone
            data.get("bank_account", ""),  # update_bank
            'yosephatigoran'  # param_adduser
        ]
        error = self.execute_sp('UPDATE', params)
        if isinstance(error, str):
            return JsonResponse({"error": error}, status=500)
        return JsonResponse({"message": "Customer updated successfully"}, status=200)

    def delete(self, request):
        # Menghapus data pelanggan
        data = JSONParser().parse(request)
        params = [
            'Pelanggan',  # param_vporvs
            data.get("customer_id", ""),  # update_vporvsID
            '', '', '', '', '', '', '', '', '', '', '', '',  # Semua param kosong
            'yosephatigoran'  # param_adduser
        ]
        error = self.execute_sp('DELETE', params)
        if isinstance(error, str):
            return JsonResponse({"error": error}, status=500)
        return JsonResponse({"message": "Customer deleted successfully"}, status=200)