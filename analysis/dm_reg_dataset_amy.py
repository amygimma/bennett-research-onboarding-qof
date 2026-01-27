from ehrql import create_dataset, show
from ehrql.tables.core import patients, practice_registrations, clinical_events, medications

# Import codelists defined in analysis/codelists.py
from codelists import dm_codelist, dmres_codelist

index_date = "2024-03-31"

# Create data objects to assess eligibility against rules ----

# establish patient is registered
has_registration = (
    practice_registrations
    .exists_for_patient_on(index_date)
)

# identify patients over 17 and are alive
is_17_or_over = (
    patients.age_on(index_date) >= 17
)

is_alive = patients.is_alive_on(index_date)

# identify clinical events prior to index date
prev_clin_events = (
    clinical_events.where(clinical_events.date <= index_date)
)

# identify latest DM dx
latest_dm_date = (
    prev_clin_events
    .where(prev_clin_events.snomedct_code.is_in(dm_codelist))
    .sort_by(prev_clin_events.date)
    .last_for_patient()
    .date
)

# identify latest dm resolution
latest_dmres_date = (
    prev_clin_events
    .where(clinical_events.snomedct_code.is_in(dmres_codelist))
    .sort_by(clinical_events.date)
    .last_for_patient()
    .date
)

# Define rules ----

# Rule 1: Pass to the next rule all patients from the specified population who meet both of the criteria below and reject the remaining patients.
# - Have a diabetes diagnosis in the patient record up to and including the achievement date.
# - Latest diabetes diagnosis is not followed by a diabetes resolved code.

# Rule 2: Reject patients passed to this rule who are aged under 17 years old on the achievement date. Select the remaining patients.

# rule 1
dm_reg_r1 = (
    latest_dm_date.is_not_null() & (
        latest_dmres_date.is_null() | (latest_dmres_date < latest_dm_date)
    )
 )

# rule 2
dm_reg_r2 = is_alive & is_17_or_over & has_registration

# Create dataset ---- 
dataset = create_dataset()
dataset.define_population(dm_reg_r1 & dm_reg_r2)

# define dataset columns
dataset.dmlat_dat = latest_dm_date
dataset.dmres_dat = latest_dmres_date
dataset.pat_age = patients.age_on(index_date)
