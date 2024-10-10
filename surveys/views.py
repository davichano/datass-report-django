# surveys/views.py
import os

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .serializers import CSVUploadSerializer
from .services.csv_processing_service import CSVProcessingService


class CSVUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CSVUploadSerializer(data=request.data)

        if serializer.is_valid():
            year = request.data.get("year")
            month = request.data.get("month")
            try:
                if not year or not month:
                    return Response(
                        {"error": "Se requiere año y mes para la migración"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if CSVProcessingService.migration_exists(year, month):
                    return Response(
                        {"error": f"Los datos para el año {year} y mes {month} ya fueron migrados."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                temp_dir = os.path.join(settings.MEDIA_ROOT, "temp")
                if not os.path.exists(temp_dir):
                    os.makedirs(temp_dir)

                # Obtener los archivos subidos
                ds_i_file = request.FILES.get("ds_i")
                ds_ii_file = request.FILES.get("ds_ii")
                ds_iii_file = request.FILES.get("ds_iii")

                if not ds_i_file or not ds_ii_file or not ds_iii_file:
                    return Response(
                        {"error": "Faltan uno o más archivos de dataset (ds_i, ds_ii, ds_iii)"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                try:
                    # Guardar los archivos temporalmente
                    ds_i_path = default_storage.save(f"temp/{ds_i_file.name}", ContentFile(ds_i_file.read()))
                    ds_ii_path = default_storage.save(
                        f"temp/{ds_ii_file.name}", ContentFile(ds_ii_file.read())
                    )
                    ds_iii_path = default_storage.save(
                        f"temp/{ds_iii_file.name}", ContentFile(ds_iii_file.read())
                    )
                    # Verificar que los archivos se hayan guardado correctamente
                    if not default_storage.exists(ds_i_path):
                        return Response(
                            {"error": f"No se pudo guardar el archivo {ds_i_file.name}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        )
                    if not default_storage.exists(ds_ii_path):
                        return Response(
                            {"error": f"No se pudo guardar el archivo {ds_ii_file.name}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        )
                    if not default_storage.exists(ds_iii_path):
                        return Response(
                            {"error": f"No se pudo guardar el archivo {ds_iii_file.name}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        )

                    print(f"Ruta de archivo ds_i: {ds_i_path}")
                    print(f"Ruta de archivo ds_ii: {ds_ii_path}")
                    print(f"Ruta de archivo ds_iii: {ds_iii_path}")

                    # Procesar los archivos CSV
                    CSVProcessingService.process_csv(ds_i_path, year, month, "ds_i")
                    CSVProcessingService.process_csv(ds_ii_path, year, month, "ds_ii")
                    CSVProcessingService.process_csv(ds_iii_path, year, month, "ds_iii")

                    return Response(
                        {"status": "Archivos procesados correctamente"}, status=status.HTTP_200_OK
                    )

                except Exception as e:
                    # Capturar cualquier error durante el procesamiento de los archivos CSV
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                finally:
                    print("Terminó todo")
                    if ds_i_path and default_storage.exists(ds_i_path):
                        default_storage.delete(ds_i_path)
                    if ds_ii_path and default_storage.exists(ds_ii_path):
                        default_storage.delete(ds_ii_path)
                    if ds_iii_path and default_storage.exists(ds_iii_path):
                        default_storage.delete(ds_iii_path)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Si la validación del serializer falla, retornar los errores
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
