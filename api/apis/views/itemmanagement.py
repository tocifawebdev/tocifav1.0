from django.http import JsonResponse, HttpResponse
from django.db import connection
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
import openpyxl
# import openpyxl
from io import BytesIO


class ItemManagementAPI(APIView):
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        """
        Insert data into tables using `sp_check_insert_table`.
        """
        data = request.data
        params = [
            data.get("param_kategori"),  # BARANG MASUK / BARANG KELUAR
            data.get("param_itemname"),  # Item names separated by "|"
            data.get("param_itemqty"),   # Item quantities separated by "|"
            data.get("param_notes"),     # Notes separated by "|"
            data.get("param_date"),      # Input date (YYYY-MM-DD)
            '01700551'                   # Example User ID
        ]

        # Validasi parameter
        if not all(params):
            return JsonResponse({"error": "All parameters are required."}, status=400)

        if params[0] not in ["BARANG MASUK", "BARANG KELUAR"]:
            return JsonResponse({"error": "Invalid 'param_kategori'. Must be 'BARANG MASUK' or 'BARANG KELUAR'."}, status=400)

        # Eksekusi stored procedure
        result = self.execute_procedure("sp_check_insert_table", params)
        return JsonResponse(result, safe=False)

    def get(self, request, *args, **kwargs):
        """
        Fetch data for both BARANG MASUK and BARANG KELUAR directly without parameters.
        """
        try:
            # Fetch data for BARANG MASUK
            barang_masuk_data = self.execute_procedure("sp_list_table", ["BARANG MASUK", ""])
            
            # Fetch data for BARANG KELUAR
            barang_keluar_data = self.execute_procedure("sp_list_table", ["BARANG KELUAR", ""])

            # Combine results
            data = {
                "BARANG MASUK": barang_masuk_data,
                "BARANG KELUAR": barang_keluar_data
            }

            return JsonResponse(data, safe=False)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
        
        

    def execute_procedure(self, procedure_name, params):
        """
        Execute a stored procedure with parameters.
        """
        try:
            with connection.cursor() as cursor:
                cursor.callproc(procedure_name, params)
                if cursor.description:
                    columns = [col[0] for col in cursor.description]
                    result = [dict(zip(columns, row)) for row in cursor.fetchall()]
                else:
                    result = {"message": f"Stored Procedure '{procedure_name}' executed successfully."}
            return result
        except Exception as e:
            return {"error": str(e)}

def handle_download_template(request, category):
    """
    Generate and download an Excel template for the selected category.
    """
    try:
        # Validasi kategori
        if category not in ["BARANG MASUK", "BARANG KELUAR"]:
            return JsonResponse({"error": "Invalid category."}, status=400)

        # Buat workbook Excel
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = category
        ws.append(["ItemName", "ItemQty", "Notes"])  # Header

        # Simpan workbook ke dalam BytesIO
        output = BytesIO()
        wb.save(output)
        output.seek(0)

        # Respons file Excel
        response = HttpResponse(
            output.getvalue(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = f'attachment; filename="Template_{category}.xlsx"'
        return response

    except Exception as e:
        print(f"Error generating template: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)