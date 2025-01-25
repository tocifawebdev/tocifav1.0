import logging
from django.http import JsonResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

logger = logging.getLogger(__name__)

class UpdateRequestSOAPI(APIView):
    """
    API for updating Request SO data using stored procedure `sp_updateso`.
    """

    def execute_sp(self, params):
        """
        Execute the stored procedure `sp_updateso` with the given parameters.
        """
        try:
            with connection.cursor() as cursor:
                cursor.callproc('sp_updateso', params)
                return {"message": "Operation successful"}
        except Exception as e:
            logger.error(f"Error executing stored procedure: {str(e)}")
            return {"error": str(e)}

    def put(self, request):
        """
        Handles PUT requests to update Request SO data.
        """
        data = JSONParser().parse(request)
        logger.info(f"Received data: {data}")

        soid = data.get("soid", "")
        if not soid:
            return JsonResponse({"error": "Missing required parameter 'soid'"}, status=400)

        params = [
            data.get("paymentproof", ""),    # param_paymentproof
            data.get("paymentstatus", ""),   # param_paymentstatus
            data.get("verifstatus", ""),     # param_verifstatus
            data.get("verifnotes", ""),      # param_verifnotes
            soid,                            # param_SOid
            '01700551'                       # param_adduser (hardcoded for example)
        ]

        result = self.execute_sp(params)

        if "error" in result:
            return JsonResponse(result, status=500)
        return JsonResponse(result, status=200)
