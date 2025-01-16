from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser


class RequestPOAPI(APIView):
    """
    API for handling CRUD operations using the sp_requestpo stored procedure.
    """

    def execute_sp(self, feature, params):
        """
        Execute the stored procedure `sp_requestpo` with given feature and params.
        """
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_requestpo', [feature, *params])
                if feature == 'READ':
                    # If the feature is READ, fetch all results
                    results = cursor.fetchall()
                    columns = [col[0] for col in cursor.description]
                    return [dict(zip(columns, row)) for row in results]
                return {"message": "Operation successful"}
        except Exception as e:
            return {"error": str(e)}

    def get(self, request):
        """
        Handles READ operation. Returns all PO records.
        """
        params = ["", "", "", "", "", "","", "", "", "", ""]
        result = self.execute_sp("READ", params)
        if "error" in result:
            return JsonResponse(result, status=500)
        return JsonResponse(result, safe=False)

    def post(self, request):
        """
        Handles INSERT operation to create a new PO record.
        """
        data = JSONParser().parse(request)
        params = [
            data.get("orderdate", ""),
            data.get("vendordata", ""),
            data.get("itemname", ""),
            data.get("itemdesc", ""),
            data.get("itemprice", ""),
            data.get("itemunit", ""),  # Tambahkan parameter itemunit
            data.get("itemqty", ""),
            data.get("paymentproof", ""),
            data.get("submitnotes", ""),
            "",  # PO ID is empty for INSERT
            '01700551'  # Admin ID (hardcoded for now)
        ]
        result = self.execute_sp("INSERT", params)
        if "error" in result:
            return JsonResponse(result, status=500)
        return JsonResponse(result, status=201)

    def delete(self, request):
        """
        Handles DELETE operation to delete a PO record.
        """
        data = JSONParser().parse(request)
        params = [
            "", "", "", "", "", "", "", "", "",
            data.get("poid", ""),
            '01700551'
        ]
        result = self.execute_sp("DELETE", params)
        if "error" in result:
            return JsonResponse(result, status=500)
        return JsonResponse(result, status=200)