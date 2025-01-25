import logging
from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView

# Setup logger
logger = logging.getLogger(__name__)

class CustomerItemDropdownAPI(APIView):
    """
    API for retrieving customer item data using stored procedure `sp_dropdown_customeritem`.
    """

    def execute_sp(self):
        """
        Execute the stored procedure `sp_dropdown_customeritem` to retrieve customer item data.
        """
        try:
            with connection.cursor() as cursor:
                # Call the stored procedure without parameters
                cursor.callproc('sp_dropdown_customeritem')
                
                # Fetch all results
                columns = [col[0] for col in cursor.description]  # Get column names dynamically
                result = cursor.fetchall()

                # Format results into a list of dictionaries
                data = [dict(zip(columns, row)) for row in result]
                return {"customer_items": data}
        except Exception as e:
            logger.error(f"Error executing stored procedure: {str(e)}")
            return {"error": f"An error occurred: {str(e)}"}

    def get(self, request):
        """
        Handles GET requests to retrieve customer items.
        """
        # Execute the stored procedure
        result = self.execute_sp()

        # Handle errors and return the appropriate response
        if "error" in result:
            logger.error(f"Error executing stored procedure: {result['error']}")
            return JsonResponse({"error": result['error']}, status=500)

        return JsonResponse(result, safe=False, status=200)
