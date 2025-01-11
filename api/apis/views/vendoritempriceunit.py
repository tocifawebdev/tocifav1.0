import logging
from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView

# Setup logger
logger = logging.getLogger(__name__)

class VendorItemPriceUnitAPI(APIView):
    """
    API for retrieving vendor item price and unit using stored procedure `sp_getvendoritem_priceunit`.
    """

    def execute_sp(self, param_vendoritemdata):
        """
        Execute the stored procedure `sp_getvendoritem_priceunit` with the given parameter.
        """
        try:
            with connection.cursor() as cursor:
                # Call the stored procedure
                cursor.callproc('sp_getvendoritem_priceunit', [param_vendoritemdata])
                # Fetch the result
                result = cursor.fetchall()
                if result:
                    # Assuming the stored procedure returns only one row
                    return {"Price": result[0][0], "Unit": result[0][1]}
                return {"error": "Vendor item not found"}
        except Exception as e:
            logger.error(f"Error executing stored procedure: {str(e)}")
            return {"error": str(e)}

    def get(self, request):
        """
        Handles GET requests to retrieve vendor item price and unit.
        """
        # Retrieve 'vendoritemdata' parameter from the query string
        vendoritemdata = request.GET.get("vendoritemdata")
        if not vendoritemdata:
            logger.error("Missing required parameter 'vendoritemdata'")
            return JsonResponse({"error": "Missing required parameter 'vendoritemdata'"}, status=400)

        # Log the received parameter
        logger.info(f"Received parameter: vendoritemdata = {vendoritemdata}")

        # Execute the stored procedure and retrieve results
        result = self.execute_sp(vendoritemdata)

        # Return the result
        if "error" in result:
            logger.error(f"Error response: {result['error']}")
            return JsonResponse(result, status=404)
        logger.info(f"Successfully retrieved data for vendor item: {vendoritemdata}")
        return JsonResponse(result, status=200)
