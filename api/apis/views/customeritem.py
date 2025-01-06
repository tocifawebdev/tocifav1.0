from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

class CustomerItemAPI(APIView):
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        """
        Handle INSERT operation for customeritem
        """
        data = request.data
        param_feature = "INSERT"
        params = [
            param_feature,                # Operation type
            data.get("itemname"),         # Item Name
            data.get("unit"),             # Unit
            "", "",                       # Fields not used for INSERT
            "",                           # Item ID (empty for INSERT)
            '01700551'                    # User who adds the item
        ]
        result = self.execute_procedure("sp_customeritem", params)
        return JsonResponse(result, safe=False)

    def put(self, request, *args, **kwargs):
        """
        Handle UPDATE operation for customeritem
        """
        data = request.data
        param_feature = "UPDATE"
        params = [
            param_feature,                # Operation type
            "", "",                       # Fields not used for UPDATE
            data.get("update_itemname"),  # Updated Item Name
            data.get("update_unit"),      # Updated Unit
            data.get("itemid"),           # Item ID to update
            '01700551'                    # User who updates the item
        ]
        result = self.execute_procedure("sp_customeritem", params)
        return JsonResponse(result, safe=False)

    def delete(self, request, *args, **kwargs):
        """
        Handle DELETE operation for customeritem
        """
        data = request.data
        param_feature = "DELETE"
        params = [
            param_feature,                # Operation type
            "", "", "", "",               # Fields not used for DELETE
            data.get("itemid"),           # Item ID to delete
            '01700551'                    # User who deletes the item
        ]
        result = self.execute_procedure("sp_customeritem", params)
        return JsonResponse(result, safe=False)

    def get(self, request, *args, **kwargs):
        """
        Handle READ operation for customeritem
        """
        param_feature = "READ"
        params = [param_feature] + ["" for _ in range(6)]  # Remaining parameters are empty
        result = self.execute_procedure("sp_customeritem", params)
        return JsonResponse(result, safe=False)

    def execute_procedure(self, procedure_name, params):
        """
        Helper method to execute a stored procedure
        """
        with connection.cursor() as cursor:
            param_placeholders = ", ".join(["%s"] * len(params))  # Placeholder for params
            cursor.callproc(procedure_name, params)              # Execute stored procedure
            if cursor.description:                               # If data is returned
                columns = [col[0] for col in cursor.description]
                result = [dict(zip(columns, row)) for row in cursor.fetchall()]
            else:                                                # For non-SELECT operations
                result = {"message": "Operation completed successfully"}
        return result
