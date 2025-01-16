from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser


class MoneyManagementAPI(APIView):
    parser_classes = [JSONParser]

    def put(self, request, *args, **kwargs):
        """
        Handle UPDATE operation for bank data
        """
        data = request.data
        param_feature = "UPDATE"
        params = [
            param_feature,                  
            data.get("update_bankname"),    
            data.get("update_rekname"),     
            data.get("update_norek"),       
            data.get("update_nominrek"),    
            data.get("rekid"),              
            '01700551'             
        ]
        result = self.execute_procedure("sp_moneymanagement", params)
        return JsonResponse(result, safe=False)

    def get(self, request, *args, **kwargs):
        """
        Handle READ operation for bank data
        """
        param_feature = "READ"
        params = [param_feature, "", "", "", "", "", ""] 
        result = self.execute_procedure("sp_moneymanagement", params)
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