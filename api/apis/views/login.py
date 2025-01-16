from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from collections import namedtuple

class LoginAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = JSONParser().parse(request)
        userid = data.get("userid")
        password = data.get("password")

        if not userid or not password:
            return JsonResponse({"detail": "UserID and Password are required"}, status=400)

        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_login', [userid, password])
                result = cursor.fetchall()

            if not result:
                return JsonResponse({"detail": "Invalid credentials"}, status=401)

            user = result[0]
            user_data = {
                "UserID": user[0],
                "UserLevel": user[1],
                "Username": user[2],
                "Password": user[3],
                "Email": user[4],
            }

            # Create user SimpleJWT to get generate token
            User = namedtuple('User', ['id'])
            dummy_user = User(id=user_data["UserID"])

            # Generate JWT token
            refresh = RefreshToken.for_user(dummy_user)
            access_token = str(refresh.access_token)

            response_data = {
                "UserID": user_data["UserID"],
                "UserLevel": user_data["UserLevel"],
                "Username": user_data["Username"],
                "Email": user_data["Email"],
                "token": access_token,
                "refresh_token": str(refresh),
            }
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({"detail": str(e)}, status=500)