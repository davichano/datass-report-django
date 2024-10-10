# surveys/models.py
from django.db import models


class DatasetI(models.Model):
    month = models.PositiveSmallIntegerField(help_text="Mes de la data (1-12)")
    year = models.PositiveIntegerField(help_text="Año de la data")
    population_center = models.ForeignKey(
        "locations.PopulationCenter", on_delete=models.CASCADE, related_name="dataset_i_records"
    )

    survey_last_modified = models.DateTimeField(help_text="Última fecha de modificación de la encuesta")
    total_population = models.PositiveIntegerField(
        help_text="Población total del centro poblado", null=True, blank=True
    )
    inhabited_houses = models.PositiveIntegerField(
        help_text="Número de viviendas habitadas", null=True, blank=True
    )
    has_water_system = models.BooleanField(help_text="Tiene sistema de agua", default=False)
    population_with_water = models.PositiveIntegerField(
        help_text="Número de personas con acceso al servicio de agua", null=True, blank=True
    )
    total_houses_with_connection = models.PositiveIntegerField(
        help_text="Total viviendas con conexión al sistema de agua", null=True, blank=True
    )
    has_sanitation_system = models.BooleanField(
        help_text="Cuenta con sistema de disposición de excretas", default=False
    )
    survey_type = models.CharField(max_length=50, help_text="Tipo de encuesta", null=True, blank=True)
    survey_completed = models.BooleanField(help_text="Encuesta completada", default=False)

    class Meta:
        verbose_name = "Dataset I"
        verbose_name_plural = "Datasets I"
        ordering = ["-year", "-month"]
        constraints = [
            models.UniqueConstraint(fields=["month", "year", "population_center"], name="unique_dataset_i")
        ]

    def __str__(self):
        return f"Acceso a Servicios de Agua - {self.month}/{self.year} - {self.population_center.name}"


class DatasetII(models.Model):
    month = models.PositiveSmallIntegerField(help_text="Mes de la data (1-12)")
    year = models.PositiveIntegerField(help_text="Año de la data")
    provider_name = models.CharField(max_length=255, help_text="Nombre del prestador de servicio")
    population_center = models.ForeignKey(
        "locations.PopulationCenter", on_delete=models.CASCADE, related_name="dataset_ii_records"
    )
    provider_last_modified = models.DateTimeField(help_text="Última fecha de modificación")
    has_operator = models.BooleanField(help_text="Prestador de servicio tiene operador", default=False)
    incentive_payment_frequency = models.CharField(
        max_length=50, help_text="Frecuencia de pago de incentivo", null=True, blank=True
    )
    average_operator_incentive = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Monto promedio del incentivo pagado al operador",
        null=True,
        blank=True,
    )
    registered_associates = models.PositiveIntegerField(
        help_text="Número de asociados inscritos en padrón", null=True, blank=True
    )
    charges_family_fee = models.BooleanField(help_text="Prestador cobra cuota familiar", default=False)
    family_fee_frequency = models.CharField(
        max_length=50, help_text="Frecuencia de la cuota familiar", null=True, blank=True
    )
    average_family_fee = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Cuota familiar promedio", null=True, blank=True
    )
    delinquent_associates = models.PositiveIntegerField(
        help_text="Número de asociados morosos", null=True, blank=True
    )
    survey_module_completed = models.BooleanField(help_text="Encuesta del módulo completada", default=False)
    has_residual_chlorine_register = models.BooleanField(
        help_text="Prestador tiene registro de cloro residual", default=False
    )

    class Meta:
        verbose_name = "Dataset II"
        verbose_name_plural = "Datasets II"
        ordering = ["-year", "-month"]

    def __str__(self):
        return f"Proveedor de Servicio - {self.month}/{self.year} - {self.population_center.name}"


class DatasetIII(models.Model):
    month = models.PositiveSmallIntegerField(help_text="Mes de la data (1-12)")
    year = models.PositiveIntegerField(help_text="Año de la data")
    population_center = models.ForeignKey(
        "locations.PopulationCenter", on_delete=models.CASCADE, related_name="dataset_iii_records"
    )
    system_last_modified = models.DateTimeField(help_text="Última fecha de modificación")
    continuous_water_service = models.BooleanField(
        help_text="Servicio de agua continuo 24 horas", default=False
    )
    has_chlorination_system = models.BooleanField(help_text="Tiene sistema de cloración", default=False)
    chlorinates_water = models.BooleanField(help_text="Realiza cloración del agua", default=False)
    served_population_with_connection = models.PositiveIntegerField(
        help_text="Población atendida con conexión", null=True, blank=True
    )
    inhabited_houses_with_connection = models.PositiveIntegerField(
        help_text="Viviendas habitadas con conexión", null=True, blank=True
    )
    water_system_type = models.CharField(
        max_length=255, help_text="Tipo de sistema de agua", null=True, blank=True
    )
    operational_state_annual = models.CharField(
        max_length=255,
        help_text="Estado operativo anual de la línea de conducción",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Dataset III"
        verbose_name_plural = "Datasets III"
        ordering = ["-year", "-month"]

    def __str__(self):
        return f"Sistemas de Agua - {self.month}/{self.year} - {self.population_center.name}"
