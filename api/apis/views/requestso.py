from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser


class RequestSOAPI(APIView):
    """
    API for handling CRUD operations using the sp_requestso stored procedure.
    """

    def execute_sp(self, feature, params):
        """
        Execute the stored procedure `sp_requestso` with given feature and params.
        """
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_requestso', [feature, *params])
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
        Handles READ operation. Returns all SO records.
        """
        params = ["", "", "", "", "", "", "", "", "", "", "", ""]
        result = self.execute_sp("READ", params)
        if "error" in result:
            return JsonResponse(result, status=500)
        return JsonResponse(result, safe=False)

    def post(self, request):
        """
        Handles INSERT operation to create a new SO record.
        """
        data = JSONParser().parse(request)  # Parse JSON request
        params = [
            data.get("orderdate", ""),  # Purchase date
            data.get("customerdata", ""),  # Customer data
            data.get("itemname", ""),  # Concatenated item names
            data.get("itemdesc", ""),  # Concatenated item descriptions
            data.get("itemprice", ""),  # Concatenated item prices
            data.get("itemunit", ""),  # Concatenated item units
            data.get("itemqty", ""),  # Concatenated item quantities
            data.get("itemaddprice", ""),  # Additional price
            data.get("ppn", ""),  # Tax percentage
            data.get("submitnotes", ""),  # Submission notes
            "",  # SO ID (empty for insert)
            '01700551',  # Admin ID (hardcoded for now)
        ]
        result = self.execute_sp("INSERT", params)  # Call stored procedure
        if "error" in result:
            return JsonResponse(result, status=500)
        return JsonResponse(result, status=201)

    def delete(self, request):
        """
        Handles DELETE operation to delete an SO record.
        """
        data = JSONParser().parse(request)
        params = [
            "", "", "", "", "", "", "", "", "", "",
            data.get("soid", ""),
            '01700551'
        ]
        result = self.execute_sp("DELETE", params)
        if "error" in result:
            return JsonResponse(result, status=500)
        return JsonResponse(result, status=200)
