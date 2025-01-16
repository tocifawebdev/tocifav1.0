import logging
from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView

# Setup logger
logger = logging.getLogger(__name__)

class DateTimeAPI(APIView):
    """
    API for retrieving the current date and time using stored procedure `sp_getdatetime`.
    """

    def execute_sp(self):
        """
        Execute the stored procedure `sp_getdatetime` to retrieve the current date and time.
        """
        try:
            with connection.cursor() as cursor:
                # Call the stored procedure
                cursor.callproc('sp_getdatetime')
                # Fetch the result
                result = cursor.fetchall()
                if result:
                    return {"CurrentDateTime": result[0][0].strftime("%Y-%m-%d %H:%M:%S")}
                return {"error": "Unable to fetch current date and time"}
        except Exception as e:
            logger.error(f"Error executing stored procedure: {str(e)}")
            return {"error": str(e)}

    def get(self, request):
        """
        Handles GET requests to retrieve the current date and time.
        """
        # Execute the stored procedure
        result = self.execute_sp()

        # Return the result
        if "error" in result:
            logger.error(f"Error response: {result['error']}")
            return JsonResponse(result, status=500)
        logger.info(f"Successfully retrieved current date and time: {result['CurrentDateTime']}")
        return JsonResponse(result, status=200)