from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

class LoginAPI(APIView):
    def execute_sp(self, userid, password):
        """
        Menjalankan Stored Procedure sp_login untuk memverifikasi login.
        """
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_login', [userid, password])
                result = cursor.fetchall()
                return result
        except Exception as e:
            return str(e)

    def post(self, request):
        """
        Endpoint untuk login user.
        """
        data = JSONParser().parse(request)
        userid = data.get("userid", "")
        password = data.get("password", "")

        # Validasi input
        if not userid or not password:
            return JsonResponse(
                {"error": "UserID and Password are required."}, status=400
            )

        # Menjalankan stored procedure
        results = self.execute_sp(userid, password)
        if isinstance(results, str):
            return JsonResponse({"error": results}, status=500)

        # Jika tidak ada data yang dikembalikan, berarti login gagal
        if not results:
            return JsonResponse({"error": "Invalid UserID or Password."}, status=401)

        # Jika login berhasil, kirimkan data user
        user_data = {
            "userid": results[0][0],       # UserID
            "user_level": results[0][1],  # UserLevel
            "username": results[0][2],    # Username
            "email": results[0][4],       # Email
        }
        return JsonResponse({"message": "Login successful.", "user": user_data}, status=200)