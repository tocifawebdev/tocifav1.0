from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser


class MoneyManagementAPI(APIView):
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        """
        Handle INSERT operation for bank data
        """
        data = request.data
        param_feature = "INSERT"
        params = [
            param_feature,                  # Operation type
            data.get("bankname"),           # Nama Bank
            data.get("rekname"),            # Nama Rekening
            data.get("norek"),              # Nomor Rekening
            data.get("nominrek"),           # Nominal Rekening
            data.get("lim_min_nominrek"),   # Limit Minimal Nominal Rekening
            "", "", "", "", "",             # Update fields kosong untuk INSERT
            "",                             # RekID kosong untuk INSERT
            data.get("adduser")             # User yang menambahkan
        ]
        result = self.execute_procedure("sp_tocifabank", params)
        return JsonResponse(result, safe=False)

    def put(self, request, *args, **kwargs):
        """
        Handle UPDATE operation for bank data
        """
        data = request.data
        param_feature = "UPDATE"
        params = [
            param_feature,                  # Operation type
            "", "", "", "", "",             # Fields kosong untuk UPDATE
            data.get("update_bankname"),    # Nama Bank yang diupdate
            data.get("update_rekname"),     # Nama Rekening yang diupdate
            data.get("update_norek"),       # Nomor Rekening yang diupdate
            data.get("update_nominrek"),    # Nominal Rekening yang diupdate
            data.get("update_lim_min_nominrek"),  # Limit Minimal Nominal Rekening yang diupdate
            data.get("rekid"),              # RekID yang akan diupdate
            data.get("adduser")             # User yang memperbarui
        ]
        result = self.execute_procedure("sp_tocifabank", params)
        return JsonResponse(result, safe=False)

    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE operation for bank data
        """
        data = request.data
        param_feature = "DELETE"
        params = [
            param_feature,                  # Operation type
            "", "", "", "", "", "", "", "", "", "",  # Fields kosong untuk DELETE
            data.get("rekid"),              # RekID yang akan dihapus
            data.get("adduser")             # User yang menghapus
        ]
        result = self.execute_procedure("sp_tocifabank", params)
        return JsonResponse(result, safe=False)

    def get(self, request, *args, **kwargs):
        """
        Handle READ operation for bank data
        """
        param_feature = "READ"
        params = [param_feature] + ["" for _ in range(12)]  # Semua parameter kosong kecuali fitur
        result = self.execute_procedure("sp_tocifabank", params)
        return JsonResponse(result, safe=False)

    def execute_procedure(self, procedure_name, params):
        """
        Helper method to execute a stored procedure
        """
        with connection.cursor() as cursor:
            cursor.callproc(procedure_name, params)
            if cursor.description:  # Jika ada data yang dikembalikan
                columns = [col[0] for col in cursor.description]
                result = [dict(zip(columns, row)) for row in cursor.fetchall()]
            else:  # Untuk operasi non-SELECT
                result = {"message": "Operation completed successfully"}
        return result
