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
