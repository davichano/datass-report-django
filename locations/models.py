# locations/models.py
from django.db import models


class Province(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, null=True, blank=True, help_text="UBIGEO de la Provincia")

    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Provincias"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_centroid(self):
        """
        Calcula el centroide de todos los centros poblados en los distritos de esta provincia,
        basado en las coordenadas latitude_datass y longitude_datass.
        """
        # Obtener todos los centros poblados de los distritos de la provincia
        population_centers = PopulationCenter.objects.filter(
            district__province=self, latitude_datass__isnull=False, longitude_datass__isnull=False
        ).exclude(latitude_datass=0, longitude_datass=0)

        if not population_centers.exists():
            return None, None  # Si no hay centros poblados válidos, devolver None

        total_lat = 0
        total_lon = 0
        count = 0

        for center in population_centers:
            total_lat += float(center.latitude_datass)  # Convertir a float si es necesario
            total_lon += float(center.longitude_datass)  # Convertir a float si es necesario
            count += 1

        if count == 0:
            return None, None  # Si no hay centros poblados válidos, devolver None

        # Calcular el promedio de las coordenadas
        avg_lat = total_lat / count
        avg_lon = total_lon / count

        return avg_lat, avg_lon


class District(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, null=True, blank=True, help_text="UBIGEO del Distrito")
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name="districts")

    class Meta:
        verbose_name = "Distrito"
        verbose_name_plural = "Distritos"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_centroid(self):
        population_centers = self.population_centers.filter(
            latitude_datass__isnull=False,
            longitude_datass__isnull=False,
        ).exclude(latitude_datass=0, longitude_datass=0)

        if not population_centers:
            return None, None

        total_lat = 0
        total_lon = 0
        count = 0
        for center in population_centers:
            total_lat += float(center.latitude_datass)  # Convertir a float si es necesario
            total_lon += float(center.longitude_datass)  # Convertir a float si es necesario
            count += 1

        if count == 0:
            return None, None

        avg_lat = total_lat / count
        avg_lon = total_lon / count

        return avg_lat, avg_lon


class PopulationCenter(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(
        max_length=20, null=True, blank=True, help_text="UBIGEO del Centro Poblado", db_index=True
    )
    population_center_id_datass = models.CharField(max_length=50, help_text="ID de Centro Poblado en DATASS")
    survey_id = models.CharField(max_length=50, help_text="ID de Encuesta en DATASS", null=True, blank=True)
    latitude_inei = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Latitud en grados decimales según INEI",
    )
    longitude_inei = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Longitud en grados decimales según INEI",
    )
    latitude_datass = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Latitud en grados decimales según DATASS",
    )
    longitude_datass = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Longitud en grados decimales según DATASS",
    )
    district = models.ForeignKey(
        District, on_delete=models.CASCADE, related_name="population_centers", db_index=True
    )

    class Meta:
        verbose_name = "Centro Poblado"
        verbose_name_plural = "Centros Poblados"
        ordering = ["name"]
        unique_together = ("code", "district")

    def __str__(self):
        return self.name
