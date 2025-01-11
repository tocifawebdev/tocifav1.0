import logging
from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView

# Setup logger
logger = logging.getLogger(__name__)

class VendorDropdownAPI(APIView):
    """
    API for retrieving vendor data using stored procedure `sp_dropdown_vendor`.
    """

    def execute_sp(self):
        """
        Execute the stored procedure `sp_dropdown_vendor` to retrieve vendor data.
        """
        try:
            with connection.cursor() as cursor:
                # Call the stored procedure
                cursor.callproc('sp_dropdown_vendor')
                # Fetch the result
                result = cursor.fetchall()
                if result:
                    # Format result into a list of vendor data
                    return {"Vendors": [row[0] for row in result]}
                return {"error": "No vendors found"}
        except Exception as e:
            logger.error(f"Error executing stored procedure: {str(e)}")
            return {"error": str(e)}

    def get(self, request):
        """
        Handles GET requests to retrieve vendor data.
        """
        # Execute the stored procedure
        result = self.execute_sp()

        # Return the result
        if "error" in result:
            logger.error(f"Error response: {result['error']}")
            return JsonResponse(result, status=404)
        logger.info("Successfully retrieved vendor data")
        return JsonResponse(result, status=200)
