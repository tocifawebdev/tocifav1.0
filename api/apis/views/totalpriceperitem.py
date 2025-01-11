import logging
from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

# Setup logger
logger = logging.getLogger(__name__)

class TotalPricePerItemAPI(APIView):
    """
    API for calculating total price per item using stored procedure `sp_gettotalprice`.
    """

    def execute_sp(self, param_itemprice, param_itemqty):
        """
        Execute the stored procedure `sp_gettotalprice` with the given parameters.
        """
        try:
            with connection.cursor() as cursor:
                # Call the stored procedure
                cursor.callproc('sp_gettotalprice', [param_itemprice, param_itemqty])
                # Fetch the result
                result = cursor.fetchall()
                if result:
                    return {"TotalPricePerItem": float(result[0][0])}
                return {"error": "Unable to calculate total price"}
        except Exception as e:
            logger.error(f"Error executing stored procedure: {str(e)}")
            return {"error": str(e)}

    def post(self, request):
        """
        Handles POST requests to calculate total price per item.
        """
        # Parse request data
        data = JSONParser().parse(request)

        # Validate required parameters
        param_itemprice = data.get("itemprice")
        param_itemqty = data.get("itemqty")

        if not param_itemprice or not param_itemqty:
            logger.error("Missing required parameters 'itemprice' or 'itemqty'")
            return JsonResponse({"error": "Missing required parameters 'itemprice' or 'itemqty'"}, status=400)

        # Log received parameters
        logger.info(f"Received parameters: itemprice = {param_itemprice}, itemqty = {param_itemqty}")

        # Execute the stored procedure
        result = self.execute_sp(param_itemprice, param_itemqty)

        # Return the result
        if "error" in result:
            logger.error(f"Error response: {result['error']}")
            return JsonResponse(result, status=500)
        logger.info(f"Successfully calculated total price: {result['TotalPricePerItem']}")
        return JsonResponse(result, status=200)
