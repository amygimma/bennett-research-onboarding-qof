from ehrql import codelist_from_csv, create_dataset, show
from ehrql.tables.core import patients, practice_registrations, clinical_events, medications

index_date = "2024-03-31"

# Create codelists ----
dm_codelist = codelist_from_csv(
  "codelists/nhsd-primary-care-domain-refsets-dm_cod.csv"  ,
  column="code"
)

dmres_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-dmres_cod.csv",
    column="code"
)

# Create data to assess eligibility against rules ----

# establish patient is registered
has_registration = (
    practice_registrations
    .for_patient_on(index_date)
    .exists_for_patient()
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
latest_dm = (
    prev_clin_events
    # Q: why do both prev_clin_events and clinical events work?
    .where(prev_clin_events.snomedct_code.is_in(dm_codelist))
    .sort_by(prev_clin_events.date)
    # Q. What are the object class and attributes after last_for_patient?
    .last_for_patient()
    .date
)

# identify latest dm resolution
latest_dmres = (
    prev_clin_events
    # Q: why do both prev_clin_events and clinical events work?
    .where(clinical_events.snomedct_code.is_in(dmres_codelist))
    .sort_by(clinical_events.date)
    .last_for_patient()
    .date
)

# Define rules ----

dm_reg_r1 = (
    latest_dm.is_not_null() & (
        latest_dmres.is_null() | (latest_dmres < latest_dm)
    )
 )

dm_reg_r2 = is_alive & is_17_or_over

# Create dataset ---- 
dataset = create_dataset()
dataset.define_population(dm_reg_r1 & dm_reg_r2)

# define dataset columns
dataset.dmlat_dat = latest_dm
dataset.dmres_dat = latest_dmres
dataset.pat_age = patients.age_on(index_date)

# show(dataset)



# Code for more questions
# # dm_dx = (
# #     clinical_events
# #     .snomedct_code
# #     .is_in(dm_codelist)
# #     .exists_for_patient()
# # )

# latest_dm_dx= (
#     clinical_events
#     .where(
#         (clinical_events.date <= index_date) 
#         & ((clinical_events.snomedct_code.is_in(dm_codelist))
#         | clinical_events.snomedct_code.is_in(dmres_codelist))
#         )
#     .sort_by(clinical_events.date)
#     .last_for_patient()
#     .where(clinical_events.snomedct_code.is_in(dm_codelist))
    
# )

# current_dm_dx = latest_dm_dx

# show(latest_dm_dx)

# latest_unres_dm_dx_date = (
#     clinical_events.where(
#         clinical_events.date
#         clinical_events.date.is_on_or_before(index_date)
#     )
#     .except_where(clinical_events.snomedct_code.is_in(dmres_codelist))  
# )

# show(dm_dx)
# dataset = create_dataset()
# dataset.sex = patients.sex

# dataset.define_population(
#     has_registration 
#     & is_17_or_over
#     & is_alive
# )
    

# show(
#     dataset
# )