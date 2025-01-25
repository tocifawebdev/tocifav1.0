import logging
from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView

# Setup logger
logger = logging.getLogger(__name__)

class CustomerItemPriceUnitAPI(APIView):
    """
    API for retrieving customer item unit using stored procedure `sp_getcustomeritem_unit`.
    """

    def execute_sp(self, param_customeritemdata):
        """
        Execute the stored procedure `sp_getcustomeritem_unit` with the given parameter.
        """
        try:
            with connection.cursor() as cursor:
                # Call the stored procedure
                cursor.callproc('sp_getcustomeritem_unit', [param_customeritemdata])
                # Fetch the result
                result = cursor.fetchall()
                if result:
                    # Assuming the stored procedure returns only one row
                    return {"Unit": result[0][0]}
                return {"error": "Customer item not found"}
        except Exception as e:
            logger.error(f"Error executing stored procedure: {str(e)}")
            return {"error": str(e)}

    def get(self, request):
        """
        Handles GET requests to retrieve customer item unit.
        """
        # Retrieve 'customeritemdata' parameter from the query string
        customeritemdata = request.GET.get("customeritemdata")
        if not customeritemdata:
            logger.error("Missing required parameter 'customeritemdata'")
            return JsonResponse({"error": "Missing required parameter 'customeritemdata'"}, status=400)

        # Log the received parameter
        logger.info(f"Received parameter: customeritemdata = {customeritemdata}")

        # Execute the stored procedure and retrieve results
        result = self.execute_sp(customeritemdata)

        # Return the result
        if "error" in result:
            logger.error(f"Error response: {result['error']}")
            return JsonResponse(result, status=404)
        logger.info(f"Successfully retrieved data for customer item: {customeritemdata}")
        return JsonResponse(result, status=200)
