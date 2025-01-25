import logging
from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView

# Setup logger
logger = logging.getLogger(__name__)

class CustomerDropdownAPI(APIView):
    """
    API for retrieving customer data using stored procedure `sp_dropdown_customer_for_requestso`.
    """

    def execute_sp(self, param_customerdata):
        """
        Execute the stored procedure `sp_dropdown_customer_for_requestso` to retrieve customer data.
        """
        try:
            with connection.cursor() as cursor:
                # Call the stored procedure with the given parameter
                cursor.callproc('sp_dropdown_customer_for_requestso', [param_customerdata])
                
                # Fetch all results
                columns = [col[0] for col in cursor.description]  # Get column names dynamically
                result = cursor.fetchall()

                # Format results into a list of dictionaries
                if result:
                    data = [dict(zip(columns, row)) for row in result]
                    return {"customers": data}
                return {"error": "No customer data found."}

        except Exception as e:
            logger.error(f"Error executing stored procedure: {str(e)}")
            return {"error": f"An error occurred: {str(e)}"}

    def get(self, request):
        """
        Handles GET requests to retrieve customer data.
        """
        # Get the 'customerdata' parameter from the request
        param_customerdata = request.GET.get('customerdata', '').strip()

        # Log the received parameter
        logger.info(f"Received parameter: customerdata = {param_customerdata}")

        # Execute the stored procedure
        result = self.execute_sp(param_customerdata)

        # Handle errors and return the appropriate response
        if "error" in result:
            logger.error(f"Error response: {result['error']}")
            return JsonResponse(result, status=404)

        logger.info("Successfully retrieved customer data.")
        return JsonResponse(result, safe=False, status=200)
