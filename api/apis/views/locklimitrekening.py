from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ValidationError

class LockLimitRekeningAPI(APIView):
    parser_classes = [JSONParser]

    def put(self, request, *args, **kwargs):
        """
        Handle lock or unlock operation for a bank account using sp_lockrek.
        """
        rek_id = "TCF0771"  
        data = request.data
        lock_rek = data.get("lock_rek")  # "1" untuk lock, "0" untuk unlock
        add_user = data.get("add_user")  # User yang melakukan operasi

        # Validasi input
        if lock_rek not in ["0", "1"]:
            raise ValidationError({"lock_rek": "Must be '0' (unlock) or '1' (lock)"})
        if not add_user:
            raise ValidationError({"add_user": "add_user is required"})

        # Eksekusi stored procedure
        params = [lock_rek, rek_id, add_user]
        result = self.execute_procedure("sp_lockrek", params)

        # Validasi hasil prosedur
        if isinstance(result, list) and result and "Message" in result[0]:
            return JsonResponse({"error": result[0]["Message"]}, status=400)

        return JsonResponse(result, safe=False)

    def get(self, request, *args, **kwargs):
        """
        Check lock status for the hardcoded RekID.
        """
        # Hardcode RekID
        rek_id = "TCF0771"

        # Query untuk mengambil status LockReck
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT LockReck FROM tocifa.tocifabank WHERE ReckID = %s", [rek_id]
            )
            row = cursor.fetchone()

        # Jika RekID tidak ditemukan
        if row is None:
            return JsonResponse({"error": f"Rekening with RekID '{rek_id}' not found"}, status=404)

        # Kembalikan status LockReck
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
            else:  # non-SELECT
                result = {"message": "Operation completed successfully"}
        return result