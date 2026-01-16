from datetime import date
from dm_reg_dataset_amy import dataset

# Rule 1: Pass to the next rule all patients from the specified population who meet both of the criteria below and reject the remaining patients.
# - Have a diabetes diagnosis in the patient record up to and including the achievement date.
# - Latest diabetes diagnosis is not followed by a diabetes resolved code.

# Rule 2: Reject patients passed to this rule who are aged under 17 years old on the achievement date. Select the remaining patients.

dm_code = "111552007"
dm_resolved_code = "315051004"

test_data = {
    # Not expected to due age < 17 : Rule 2
    1: {
        "patients": {"date_of_birth": date(2020, 1, 1)},
        "practice_registrations": [{
            "start_date": date(2020, 1,1), 
            "end_date": date(2026,1,1),  
            "practice_pseudo_id": 1234}],
        "clinical_events": [],
        "expected_in_population": False
    },
    # Not expected as clinical event is outside of range
    2: {
        "patients": {"date_of_birth": date(1960, 1, 1)},
        "practice_registrations": [{
            "start_date": date(2020, 1,1), 
            "end_date": date(2026,1,1),  
            "practice_pseudo_id": 1234}],
        "clinical_events": [
            {"date": date(2025, 1, 1), "snomedct_code": dm_code} 
        ],
        "expected_in_population": False
    },
    # Not expected as patient is not registered on the index date
    3: {
        "patients": {"date_of_birth": date(1960, 1, 1)},
        "practice_registrations": [{
            "start_date": date(2025, 1,1), 
            "end_date": date(2026,1,1),  
            "practice_pseudo_id": 1234}],
        "clinical_events": [
            {"date": date(2024, 1, 1), "snomedct_code": dm_code}
        ],
        "expected_in_population": False
    },
    # Not expected as most recent DM CE is resolved
    4: {
        "patients": {"date_of_birth": date(1960, 1, 1)},
        "practice_registrations": [{
            "start_date": date(2020, 1,1), 
            "end_date": date(2026,1,1),  
            "practice_pseudo_id": 1234}],
        "clinical_events": [
            {"date": date(2024, 1, 1), "snomedct_code": dm_code},
            {"date": date(2024, 2, 1), "snomedct_code": dm_resolved_code} 
        ],
        "expected_in_population": False,
    },
    # Expected as all rules are met - no resolved dm
    5: {
        "patients": {"date_of_birth": date(1960, 1, 1)},
        "practice_registrations": [{
            "start_date": date(2020, 1,1), 
            "end_date": date(2026,1,1),  
            "practice_pseudo_id": 1234}],
        "clinical_events": [
            {"date": date(2024, 1, 1), "snomedct_code": dm_code}
        ],
        "expected_in_population": True,
        "expected_columns": {
            "pat_age": 64,
            "dmlat_dat":  date(2024, 1, 1),
            "dmres_dat": None
        }
    },
    # Expected as all rules are met and most recent dm is resolved
    6: {
        "patients": {"date_of_birth": date(1960, 1, 1)},
        "practice_registrations": [{
            "start_date": date(2020, 1,1), 
            "end_date": date(2026,1,1),  
            "practice_pseudo_id": 1234}],
        "clinical_events": [
            {"date": date(2024, 1, 1), "snomedct_code": dm_code},
            {"date": date(2023, 1, 1), "snomedct_code": dm_resolved_code} 
        ],
        "expected_in_population": True,
        "expected_columns": {
            "pat_age": 64,
            "dmlat_dat":  date(2024, 1, 1),
            "dmres_dat": date(2023, 1, 1)
        }
    }
}