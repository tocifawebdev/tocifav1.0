from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

class VendorItemAPI(APIView):
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        """
        Handle INSERT operation for vendoritem
        """
        data = request.data
        param_feature = "INSERT"
        params = [
            param_feature,
            data.get("vendordata"),
            data.get("itemname"),
            data.get("price"),
            data.get("unit"),
            "", "", "", "",
            "", 'tocifausermanagement'
        ]
        result = self.execute_procedure("sp_vendoritem", params)
        return JsonResponse(result, safe=False)

    def put(self, request, *args, **kwargs):
        """
        Handle UPDATE operation for vendoritem
        """
        data = request.data
        param_feature = "UPDATE"
        params = [
            param_feature,
            "", "", "", "",
            data.get("update_vendordata"),
            data.get("update_itemname"),
            data.get("update_price"),
            data.get("update_unit"),
            data.get("itemid"),
            'tocifausermanagement'
        ]
        result = self.execute_procedure("sp_vendoritem", params)
        return JsonResponse(result, safe=False)

    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE operation for vendoritem
        """
        data = request.data
        param_feature = "DELETE"
        params = [
            param_feature,
            "", "", "", "",
            "", "", "", "",
            data.get("itemid"),
            'tocifausermanagement'
        ]
        result = self.execute_procedure("sp_vendoritem", params)
        return JsonResponse(result, safe=False)

    def get(self, request, *args, **kwargs):
        """
        Handle READ operation for vendoritem
        """
        param_feature = "READ"
        params = [param_feature] + ["" for _ in range(10)]
        result = self.execute_procedure("sp_vendoritem", params)
        return JsonResponse(result, safe=False)

    def execute_procedure(self, procedure_name, params):
        """
        Helper method to execute a stored procedure
        """
        with connection.cursor() as cursor:
            param_placeholders = ", ".join(["%s"] * len(params))
            cursor.callproc(procedure_name, params)
            if cursor.description:
                columns = [col[0] for col in cursor.description]
                result = [dict(zip(columns, row)) for row in cursor.fetchall()]
            else:
                result = {"message": "Operation completed successfully"}
        return result
