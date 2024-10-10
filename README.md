# DATASS Viewer - Backend

This solution displays DATASS reports on a web interface. Reports are fetched from an external API and shown in tables
and charts, coordinated with the Regional Housing and Sanitation Directorate of the Regional Government of Cajamarca,
Peru, and the GAC of the Ministry of Housing. Users can filter reports by date and export them to a CSV file.

### Demo site link coming soon here

## Table of Contents

- [Overview](#overview)
    - [Requirement](#requirement)
    - [Screenshots](#screenshots)
    - [Data Models](#data-models)
        - [DatasetI (Water and Sanitation Services Access)](#dataseti-water-and-sanitation-services-access)
        - [DatasetII (Service Providers)](#datasetii-service-providers)
        - [DatasetIII (Water Systems)](#datasetiii-water-systems)
- [My Process](#my-process)
    - [Built With](#built-with)
    - [Project Setup](#project-setup)
    - [Continuous Development](#continuous-development)
    - [Useful Resources](#useful-resources)
- [Author](#author)
- [Acknowledgements](#acknowledgements)

## Overview

### Requirement

Consume an external API and display reports on a web interface. Details will be updated soon.

### Screenshots

Coming soon

### Data Models

This project processes data from the `ds_i`, `ds_ii`, `ds_iii` datasets. Below is the mapping of original dataset
columns to Django model fields.

#### DatasetI (Water and Sanitation Services Access)

| Original Column                          | Model Field                    | Description                               |
|------------------------------------------|--------------------------------|-------------------------------------------|
| `CentroPoblado_Nombre`                   | `population_center`            | Associated population center              |
| `FechaModificacion_Encuesta`             | `survey_last_modified`         | Survey last modification date             |
| `p100_TotalPoblacion`                    | `total_population`             | Total population of the population center |
| `p100_ViviendasHabitadas`                | `inhabited_houses`             | Number of inhabited houses                |
| `p105_TieneSistemaAgua`                  | `has_water_system`             | If there is a water system                |
| `p105c_NumeroPoblacionConAccesoServicio` | `population_with_water`        | Population with access to water           |
| `p105c_TotalViviendasConConexion`        | `total_houses_with_connection` | Houses connected to the water system      |
| `p107_CuentaSistemaDisposicionExcretas`  | `has_sanitation_system`        | If there is a sanitation system           |
| `Encuesta_Tipo`                          | `survey_type`                  | Survey type                               |
| `Completado_Encuesta`                    | `survey_completed`             | If the survey was completed               |

#### DatasetII (Service Providers)

| Original Column                                                             | Model Field                      | Description                        |
|-----------------------------------------------------------------------------|----------------------------------|------------------------------------|
| `Nombre_PrestadorServicio`                                                  | `provider_name`                  | Provider organization name         |
| `FechaModificacion`                                                         | `provider_last_modified`         | Provider last modification date    |
| `p206_PrestadorServicioAyS_OperadorGasfitero`                               | `has_operator`                   | If the provider has an operator    |
| `p206a_TipoIncentivoPago_FrecuenciaConQueRecibeIncentivo`                   | `incentive_payment_frequency`    | Incentive payment frequency        |
| `p206a_TipoIncentivoPago_MontoPromedio`                                     | `average_operator_incentive`     | Average incentive amount           |
| `p213_NumeroAsociadosInscritosEnPadronPrestadorServicio`                    | `registered_associates`          | Registered associates              |
| `p214_PrestadorServicioSaneamientoCobraCuotaFamiliar`                       | `charges_family_fee`             | If charges a family fee            |
| `p215_CobroDeLaCuotaFamiliarPorElServicioAgua`                              | `family_fee_frequency`           | Family fee frequency               |
| `p216_CuotaFamiliarPromedio`                                                | `average_family_fee`             | Average family fee                 |
| `p217_AsociadosMorososCuotaFamiliar`                                        | `delinquent_associates`          | Delinquent associates              |
| `Completado_EncuestaModulo`                                                 | `survey_module_completed`        | If the survey module was completed |
| `p207C1_PrestadorServicioAySTieneDocumentosDeGestion_RegistorCloroResidual` | `has_residual_chlorine_register` | If has residual chlorine register  |

#### DatasetIII (Water Systems)

| Original Column                                                                      | Model Field                         | Description                                   |
|--------------------------------------------------------------------------------------|-------------------------------------|-----------------------------------------------|
| `FechaModificacion`                                                                  | `system_last_modified`              | Water system last modification date           |
| `p302_ServicioAguaContinuo24Horas`                                                   | `continuous_water_service`          | If there is continuous water service 24 hours |
| `p315_TieneSistemaCloracion`                                                         | `has_chlorination_system`           | If there is a chlorination system             |
| `p315a_RealizaCloracionAgua`                                                         | `chlorinates_water`                 | If chlorinates water                          |
| `p310_PoblacionAtendidaConexion`                                                     | `served_population_with_connection` | Population served with connection             |
| `p310_ViviendasHabitadasConexion`                                                    | `inhabited_houses_with_connection`  | Inhabited houses with connection              |
| `p334_TipoSistemaAguaCuenta`                                                         | `water_system_type`                 | Water system type                             |
| `p335C2_ComponenteSistemaGravedadSinTratamiento_EstadoOperativoAnualLineaConduccion` | `operational_state_annual`          | Annual operational state                      |

## My Process

### Built With

- Django
- Python

### Project Setup

- black
- flake8
- pre-commit

### Continuous Development

- [x] Create the project.

### Useful Resources

## Author

- GitHub - [David Paredes Abanto](https://github.com/davichano)

## Acknowledgements

Thanks to the Ministry of Housing team for the opportunity to work on this project and the Fondo Social Mi Vivienda
Cajamarca team.
