import logging
from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

# Setup logger
logger = logging.getLogger(__name__)

class UpdateRequestPOAPI(APIView):
    """
    API for updating Request PO data using stored procedure `sp_updatepo`.
    """

    def execute_sp(self, params):
        """
        Execute the stored procedure `sp_updatepo` with the given parameters.
        """
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_updatepo', params)
                return {"message": "Operation successful"}
        except Exception as e:
            logger.error(f"Error executing stored procedure: {str(e)}")
            return {"error": str(e)}

    def put(self, request):
        """
        Handles PUT requests to update Request PO data.
        """
        # Parse request data
        data = JSONParser().parse(request)
        logger.info(f"Received data: {data}")

        # Validate required parameter 'poid'
        poid = data.get("poid", "")
        if not poid:
            logger.error("Missing required parameter 'poid'")
            return JsonResponse({"error": "Missing required parameter 'poid'"}, status=400)

        # Collect parameters
        params = [
            data.get("paymentproof", ""),    # param_paymentproof
            data.get("paymentstatus", ""),   # param_paymentstatus
            data.get("verifstatus", ""),     # param_verifstatus
            data.get("verifnotes", ""),      # param_verifnotes
            poid,                            # param_POid
            '01700551'          # param_adduser
        ]

        # Execute the stored procedure
        result = self.execute_sp(params)

        # Handle result
        if "error" in result:
            logger.error(f"Error response: {result['error']}")
            return JsonResponse(result, status=500)
        logger.info("Request PO updated successfully")
        return JsonResponse(result, status=200)
