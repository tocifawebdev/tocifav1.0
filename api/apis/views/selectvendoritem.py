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
        Execute the stored procedure `sp_dropdown_vendoritem_by_vendor` to retrieve vendor item data.
        """
        try:
            with connection.cursor() as cursor:
                # Call the stored procedure with the given parameter
                cursor.callproc('sp_dropdown_vendoritem_by_vendor', [param_vendordata])
                # Fetch all results
                columns = [col[0] for col in cursor.description]  # Get column names dynamically
                result = cursor.fetchall()

                # Format results into a list of dictionaries
                data = [dict(zip(columns, row)) for row in result]
                return {"vendor_items": data}
        except Exception as e:
            logger.error(f"Error executing stored procedure: {str(e)}")
            return {"error": f"An error occurred: {str(e)}"}

    def get(self, request):
        param_vendordata = request.GET.get('vendordata', '').strip()

        # Jika parameter kosong, log peringatan
        if not param_vendordata:
            logger.warning("Parameter 'vendordata' is empty. Returning all items.")
        
        result = self.execute_sp(param_vendordata)

        # Jika terjadi error, tangani dengan respons JSON
        if "error" in result:
            logger.error(f"Error executing stored procedure: {result['error']}")
            return JsonResponse({"error": result['error']}, status=500)

        return JsonResponse(result, safe=False, status=200)