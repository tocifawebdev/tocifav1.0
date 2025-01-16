import logging
from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView

# Setup logger
logger = logging.getLogger(__name__)

class VendorDropdownAPI(APIView):
    """
    API for retrieving vendor data using stored procedure `sp_dropdown_vendor_for_requestpo`.
    """

    def execute_sp(self, param_vendordata):
        """
        Execute the stored procedure `sp_dropdown_vendor_for_requestpo` to retrieve vendor data.
        """
        try:
            with connection.cursor() as cursor:
                # Call the stored procedure with the given parameter
                cursor.callproc('sp_dropdown_vendor_for_requestpo', [param_vendordata])
                # Fetch the results
                columns = [col[0] for col in cursor.description]  # Get column names dynamically
                result = cursor.fetchall()

                # If results are found, format them into a structured response
                if result:
                    data = [dict(zip(columns, row)) for row in result]
                    return {"vendors": data}
                return {"error": "No vendor data found."}

        except Exception as e:
            logger.error(f"Error executing stored procedure: {str(e)}")
            return {"error": f"An error occurred: {str(e)}"}

    def get(self, request):
        """
        Handles GET requests to retrieve vendor data.
        """
        # Get the 'vendordata' parameter from the request
        param_vendordata = request.GET.get('vendordata', '')

        # Log the received parameter
        logger.info(f"Received parameter: vendordata = {param_vendordata}")

        # Execute the stored procedure
        result = self.execute_sp(param_vendordata)

        # Return the result
        if "error" in result:
            logger.error(f"Error response: {result['error']}")
            return JsonResponse(result, status=404)

        logger.info("Successfully retrieved vendor data.")
        return JsonResponse(result, safe=False, status=200)