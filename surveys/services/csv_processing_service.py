# surveys/services/csv_processing_service.py
import pandas as pd
import logging
import io

from django.core.files.storage import default_storage
from django.db import transaction, IntegrityError
from django.utils import timezone

from locations.repositories.district_repository import DistrictRepository
from locations.repositories.population_center_repository import PopulationCenterRepository
from locations.repositories.province_repository import ProvinceRepository
from surveys.repositories.dataset_i_repository import DatasetIRepository
from surveys.repositories.dataset_ii_repository import DatasetIIRepository
from surveys.repositories.dataset_iii_repository import DatasetIIIRepository
from surveys.models import DatasetI, DatasetII, DatasetIII

logger = logging.getLogger(__name__)


class CSVProcessingService:
    @staticmethod
    def migration_exists(year, month):
        return (
            DatasetI.objects.filter(year=year, month=month).exists()
            or DatasetII.objects.filter(year=year, month=month).exists()
            or DatasetIII.objects.filter(year=year, month=month).exists()
        )

    @staticmethod
    def process_csv(file_path, year, month, dataset_type, chunk_size=500):
        if not (1 <= int(month) <= 12) or int(year) < 0:
            logger.error("El año o mes proporcionado son inválidos")
            raise ValueError("El año o mes proporcionado son inválidos")

        population_centers = PopulationCenterRepository.get_all()
        population_centers_dict = {pc.code: pc for pc in population_centers}

        logger.info(f"Cargados {len(population_centers)} PopulationCenters en memoria")

        # Mapeo de Dataset a Repositorio y Modelo
        dataset_config = {
            "ds_i": {
                "repository": DatasetIRepository,
                "model": DatasetI,
                "field_mapping": CSVProcessingService.get_dataset_i_mapping,
            },
            "ds_ii": {
                "repository": DatasetIIRepository,
                "model": DatasetII,
                "field_mapping": CSVProcessingService.get_dataset_ii_mapping,
            },
            "ds_iii": {
                "repository": DatasetIIIRepository,
                "model": DatasetIII,
                "field_mapping": CSVProcessingService.get_dataset_iii_mapping,
            },
        }

        if dataset_type not in dataset_config:
            raise ValueError(f"Tipo de dataset '{dataset_type}' no soportado")

        config = dataset_config[dataset_type]
        with default_storage.open(file_path, "rb") as file:
            file_data = io.BytesIO(file.read())

            for chunk in pd.read_csv(file_data, chunksize=chunk_size):
                instances = []
                for _, row in chunk.iterrows():
                    try:
                        # Extraer código del centro poblado
                        population_center_code, population_center_name = (
                            CSVProcessingService.get_population_center_info(row)
                        )

                        population_center = population_centers_dict.get(population_center_code)
                        if not population_center:
                            logger.info(
                                f"Population Center no encontrado, creando nuevo: {population_center_name}"
                            )
                            population_center = CSVProcessingService.create_new_population_center(row)
                            population_centers_dict[population_center_code] = population_center

                        instance = config["model"](
                            month=month,
                            year=year,
                            population_center=population_center,
                            **config["field_mapping"](row),
                        )
                        instances.append(instance)
                    except Exception as e:
                        logger.error(f"Error al procesar fila del CSV: {e}", exc_info=True)

                CSVProcessingService._bulk_save(config["repository"], instances)

    @staticmethod
    def get_population_center_info(row):
        """Extrae el código y nombre del centro poblado."""
        population_center_data = row["CentroPoblado_Nombre"].split(" - ", 1)
        population_center_code = population_center_data[0].strip()
        population_center_name = population_center_data[1].strip()
        return population_center_code, population_center_name

    @staticmethod
    def create_new_population_center(row):
        """Crea y guarda un nuevo centro poblado en la base de datos"""
        population_center = PopulationCenterRepository.get_by_code(0)
        population_center.code = row["CentroPoblado_Nombre"].split(" - ", 1)[0].strip()
        population_center.name = row["CentroPoblado_Nombre"].split(" - ", 1)[1].strip()
        population_center.population_center_id_datass = row.get("CentroPoblado_ID", 0)
        population_center.survey_id = row.get("Encuesta_ID", 0)
        population_center.latitude_datass = row.get("lat", 0)
        population_center.longitude_datass = row.get("lon", 0)

        # Asignar distrito y provincia
        district = DistrictRepository.get_by_name(row.get("Distrito_Nombre", ""))
        if district.id is None:
            logger.error(f"Distrito '{row.get('Distrito_Nombre', '')}' no encontrado, creando nuevo")
            province = ProvinceRepository.get_by_name(row.get("Provincia_Nombre", ""))
            if province.id is None:
                province.name = row.get("Provincia_Nombre", "")
                province = ProvinceRepository.save(province)
            district.name = row.get("Distrito_Nombre", "")
            district.province = province
            district = DistrictRepository.save(district)
        population_center.district = district
        return PopulationCenterRepository.save(population_center)

    @staticmethod
    def get_dataset_i_mapping(row):
        """Mapea las columnas del CSV al modelo DatasetI."""

        def safe_numeric(value):
            """Convierte el valor a numérico y reemplaza NaN con 0."""
            return pd.to_numeric(value, errors="coerce") if pd.notna(value) else 0

        def safe_str(value):
            """Convierte el valor a string si no es NaN y si es del tipo cadena"""
            return str(value).strip().lower() if isinstance(value, str) else str(value).lower()

        survey_last_modified = pd.to_datetime(row.get("FechaModificacion_Encuesta", ""), errors="coerce")
        if pd.isna(survey_last_modified) or survey_last_modified == pd.NaT:
            survey_last_modified = timezone.make_aware(pd.to_datetime("1900-01-01 00:00"))
        else:
            if survey_last_modified.tzinfo is None:
                try:
                    survey_last_modified = timezone.make_aware(survey_last_modified)
                except Exception as e:
                    logger.error(f"Error al aplicar zona horaria: {e}", exc_info=True)

        return {
            "survey_last_modified": survey_last_modified,
            "total_population": safe_numeric(row.get("p100_TotalPoblacion")),
            "inhabited_houses": safe_numeric(row.get("p100_ViviendasHabitadas")),
            "has_water_system": safe_str(row.get("p105_TieneSistemaAgua")).lower() == "si",
            "population_with_water": safe_numeric(row.get("p105c_NumeroPoblacionConAccesoServicio")),
            "total_houses_with_connection": safe_numeric(row.get("p105c_TotalViviendasConConexion")),
            "has_sanitation_system": safe_str(row.get("p107_CuentaSistemaDisposicionExcretas")).lower()
            == "si",
            "survey_type": row.get("Encuesta_Tipo", ""),
            "survey_completed": safe_str(row.get("Completado_Encuesta")).lower() == "si",
        }

    @staticmethod
    def get_dataset_ii_mapping(row):
        """Mapea las columnas del CSV al modelo DatasetII."""

        def safe_numeric(value):
            """Convierte el valor a numérico y reemplaza NaN con 0."""
            return pd.to_numeric(value, errors="coerce") if pd.notna(value) else 0

        def safe_str(value):
            """Convierte el valor a string si no es NaN y si es del tipo cadena"""
            return str(value).strip().lower() if isinstance(value, str) else str(value).lower()

        provider_last_modified = pd.to_datetime(row.get("FechaModificacion", ""), errors="coerce")
        if pd.isna(provider_last_modified) or provider_last_modified == pd.NaT:
            provider_last_modified = timezone.make_aware(pd.to_datetime("1900-01-01 00:00"))
        else:
            if provider_last_modified.tzinfo is None:
                try:
                    provider_last_modified = timezone.make_aware(provider_last_modified)
                except Exception as e:
                    logger.error(f"Error al aplicar zona horaria: {e}", exc_info=True)

        return {
            "provider_last_modified": provider_last_modified,
            "has_operator": safe_str(row.get("p206_PrestadorServicioAyS_OperadorGasfitero")).lower() == "si",
            "provider_name": row.get("Nombre_PrestadorServicio", ""),
            "incentive_payment_frequency": row.get(
                "p206a_TipoIncentivoPago_FrecuenciaConQueRecibeIncentivo", ""
            ),
            "average_operator_incentive": safe_numeric(row.get("p206a_TipoIncentivoPago_MontoPromedio")),
            "registered_associates": safe_numeric(
                row.get("p213_NumeroAsociadosInscritosEnPadronPrestadorServicio")
            ),
            "charges_family_fee": safe_str(row.get("p214_PrestadorServicioSaneamientoCobraCuotaFamiliar"))
            == "si",
            "family_fee_frequency": row.get("p215_CobroDeLaCuotaFamiliarPorElServicioAgua", ""),
            "average_family_fee": safe_numeric(row.get("p216_CuotaFamiliarPromedio")),
            "delinquent_associates": safe_numeric(row.get("p217_AsociadosMorososCuotaFamiliar")),
            "survey_module_completed": safe_str(row.get("Completado_EncuestaModulo")).lower() == "si",
            "has_residual_chlorine_register": safe_str(
                row.get("p207C1_PrestadorServicioAySTieneDocumentosDeGestion_RegistorCloroResidual")
            ).lower()
            == "si",
        }

    @staticmethod
    def get_dataset_iii_mapping(row):
        """Mapea las columnas del CSV al modelo DatasetIII."""

        def safe_str(value):
            """Convierte el valor a string si no es NaN y si es del tipo cadena"""
            return str(value).strip().lower() if isinstance(value, str) else str(value).lower()

        def safe_numeric(value):
            """Convierte el valor a numérico y reemplaza NaN con 0."""
            return pd.to_numeric(value, errors="coerce") if pd.notna(value) else 0

        system_last_modified = pd.to_datetime(row.get("FechaModificacion", ""), errors="coerce")
        if pd.isna(system_last_modified) or system_last_modified == pd.NaT:
            system_last_modified = timezone.make_aware(pd.to_datetime("1900-01-01 00:00"))

        else:
            if system_last_modified.tzinfo is None:
                try:
                    system_last_modified = timezone.make_aware(system_last_modified)
                except Exception as e:
                    logger.error(f"Error al aplicar zona horaria: {e}", exc_info=True)

        return {
            "system_last_modified": system_last_modified,
            "continuous_water_service": safe_str(row.get("p302_ServicioAguaContinuo24Horas")).lower() == "si",
            "has_chlorination_system": safe_str(row.get("p315_TieneSistemaCloracion")).lower() == "si",
            "chlorinates_water": safe_str(row.get("p315a_RealizaCloracionAgua")).lower() == "si",
            "served_population_with_connection": safe_numeric(row.get("p310_PoblacionAtendidaConexion")),
            "inhabited_houses_with_connection": safe_numeric(row.get("p310_ViviendasHabitadasConexion")),
            "water_system_type": safe_str(row.get("p334_TipoSistemaAguaCuenta")),
            "operational_state_annual": safe_str(
                row.get("p335C2_ComponenteSistemaGravedadSinTratamiento_EstadoOperativoAnualLineaConduccion")
            ),
        }

    @staticmethod
    def _bulk_save(repository, instances):
        if not instances:
            return

        try:
            with transaction.atomic():
                repository.bulk_create(instances)
                logger.info(f"{len(instances)} registros guardados correctamente")

        except IntegrityError as e:
            logger.error(f"Error de integridad al guardar datos: {e}", exc_info=True)
            raise
