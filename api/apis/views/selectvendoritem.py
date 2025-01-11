import logging
from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView

# Setup logger
logger = logging.getLogger(__name__)

class VendorItemDropdownAPI(APIView):
    """
    API for retrieving vendor item data using stored procedure `sp_dropdown_vendoritem_by_vendor`.
    """

    def execute_sp(self, param_vendordata):
        """
        Execute the stored procedure `sp_dropdown_vendoritem_by_vendor` with the given parameter.
        """
        try:
            with connection.cursor() as cursor:
                # Call the stored procedure
                cursor.callproc('sp_dropdown_vendoritem_by_vendor', [param_vendordata])
                # Fetch the result
                result = cursor.fetchall()
                if result:
                    # Format result into a list of vendor item data
                    return {"VendorItems": [row[0] for row in result]}
                return {"error": "No vendor items found for the given vendor"}
        except Exception as e:
            logger.error(f"Error executing stored procedure: {str(e)}")
            return {"error": str(e)}

    def get(self, request):
        """
        Handles GET requests to retrieve vendor items based on vendor data.
        """
        # Retrieve 'vendordata' parameter from the query string
        vendordata = request.GET.get("vendordata")
        if not vendordata:
            logger.error("Missing required parameter 'vendordata'")
            return JsonResponse({"error": "Missing required parameter 'vendordata'"}, status=400)

        # Log the received parameter
        logger.info(f"Received parameter: vendordata = {vendordata}")

        # Execute the stored procedure
        result = self.execute_sp(vendordata)

        # Return the result
        if "error" in result:
            logger.error(f"Error response: {result['error']}")
            return JsonResponse(result, status=404)
        logger.info(f"Successfully retrieved vendor items for vendor: {vendordata}")
        return JsonResponse(result, status=200)
