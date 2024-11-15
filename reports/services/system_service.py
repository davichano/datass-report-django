from surveys.repositories.dataset_iii_repository import DatasetIIIRepository


class SystemService:

    @staticmethod
    def get_systems_resume():
        last_ds_i_record = DatasetIIIRepository.get_last_year_month()
        last_year = last_ds_i_record.year if last_ds_i_record else None
        last_month = last_ds_i_record.month if last_ds_i_record else None
        if last_year is None or last_month is None:
            return None
        systems_resume_by_province = DatasetIIIRepository.get_systems_resume(last_year, last_month)
        total_by_state = DatasetIIIRepository.get_total_by_state(last_year, last_month)
        total_by_type = DatasetIIIRepository.get_total_by_type(last_year, last_month)
        return {
            "systems_resume": systems_resume_by_province,
            "states_resume": total_by_state,
            "types_resume": total_by_type,
        }
