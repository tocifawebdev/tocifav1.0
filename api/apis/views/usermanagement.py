from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

class UserManagementAPI(APIView):
    def execute_sp(self, feature, params):
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_usermanagement', [feature, *params])
                if feature == 'READ':
                    return cursor.fetchall()
        except Exception as e:
            return str(e)

    def get(self, request):
        results = self.execute_sp('READ', ['', '', '', '', '', '', '', '', ''])
        if isinstance(results, str):
            return JsonResponse({"error": results}, status=500)

        data = [
            {
                "id": row[0],
                "user_level": row[1],
                "username": row[2],
                "email": row[3],
                "password": row[4],
                "add_time": row[5].strftime("%Y-%m-%d %H:%M:%S") if row[5] else None,
                "add_user": row[6],
                "upd_time": row[7].strftime("%Y-%m-%d %H:%M:%S") if row[7] else None,
                "upd_user": row[8],
            }
            for row in results
        ]
        return JsonResponse(data, safe=False)

    def post(self, request):
        data = JSONParser().parse(request)
        params = [
            data.get("user_level", ""),
            data.get("username", ""),
            data.get("password", ""),
            data.get("email", ""),
            '', '', '', '',
            'yosephatigoran'
        ]
        error = self.execute_sp('INSERT', params)
        if isinstance(error, str):
            return JsonResponse({"error": error}, status=500)
        return JsonResponse({"message": "User created successfully"}, status=201)

    def put(self, request):
        data = JSONParser().parse(request)
        params = [
            '', 'budimanasdasd', '',
            '', data.get("user_level", ""),
            data.get("username", ""), data.get("password", ""),
            data.get("email", ""), 'yosephatigoran'
        ]
        error = self.execute_sp('UPDATE', params)
        if isinstance(error, str):
            return JsonResponse({"error": error}, status=500)
        return JsonResponse({"message": "User updated successfully"}, status=200)

    def delete(self, request):
        data = JSONParser().parse(request)
        params = [
            '', 'budimanasdasd', '', '',
            '', '', '', '',
            'yosephatigoran'
        ]
        error = self.execute_sp('DELETE', params)
        if isinstance(error, str):
            return JsonResponse({"error": error}, status=500)
        return JsonResponse({"message": "User deleted successfully"}, status=200)