from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ValidationError

class LockLimitRekeningAPI(APIView):
    parser_classes = [JSONParser]

    def put(self, request, *args, **kwargs):
        """
        Handle lock or unlock operation for a bank account.
        """
        # Input dari request
        data = request.data
        lock_rek = data.get("lock_rek")  # "1" untuk lock, "0" untuk unlock
        rek_id = data.get("rek_id", "TCF0771")  # RekID bisa di-hardcode atau diambil dari request
        add_user = data.get("add_user", "01700551")  # Username default untuk testing

        # Validasi input
        if lock_rek not in ["0", "1"]:
            raise ValidationError({"lock_rek": "Must be '0' (unlock) or '1' (lock)"})
        if not rek_id:
            raise ValidationError({"rek_id": "rek_id is required"})
        if not add_user:
            raise ValidationError({"add_user": "add_user is required"})

        # Eksekusi stored procedure
        params = [lock_rek, rek_id, add_user]
        result = self.execute_procedure("sp_lockrek", params)
        return JsonResponse(result, safe=False)

    def get(self, request, *args, **kwargs):
        """
        Check lock status for a bank account.
        """
        rek_id = request.GET.get("rek_id", "TCF0771")  # Hardcode atau gunakan query parameter

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT LockRek FROM tocifa.tocifabank WHERE RekID = %s", [rek_id]
            )
            row = cursor.fetchone()

        if row is None:
            return JsonResponse({"error": f"Rekening with RekID '{rek_id}' not found"}, status=404)

        return JsonResponse({"rek_id": rek_id, "lock_rek": row[0]})

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
