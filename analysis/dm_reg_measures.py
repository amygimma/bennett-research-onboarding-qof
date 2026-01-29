from ehrql import INTERVAL, case, create_measures, months, when, show
from ehrql.tables.core import clinical_events, patients, practice_registrations
from codelists import dm_codelist, dmres_codelist


start_financial_year = "2022-04-01"
end_financial_year = "2024-03-31"

# establish patient is registered
has_registration_spanning_interval = (
    practice_registrations
    .spanning(INTERVAL.start_date, INTERVAL.end_date)
    .exists_for_patient()
)

# identify patients over 17 and are alive
is_17_or_over_by_interval_start = (
    patients.age_on(INTERVAL.start_date) >= 17
)

is_alive_during_interval = patients.is_alive_on(INTERVAL.end_date)

# identify clinical events by the end of the interval date to capture ALL patients with unresolved dm
prev_clin_events_by_interval_end = (
    clinical_events.where(clinical_events.date <= INTERVAL.end_date)
)

# identify latest DM dx
latest_dm_date = (
    prev_clin_events_by_interval_end
    .where(prev_clin_events_by_interval_end.snomedct_code.is_in(dm_codelist))
    .sort_by(prev_clin_events_by_interval_end.date)
    .last_for_patient()
    .date
)

# identify latest dm resolution
latest_dmres_date = (
    prev_clin_events_by_interval_end
    .where(clinical_events.snomedct_code.is_in(dmres_codelist))
    .sort_by(clinical_events.date)
    .last_for_patient()
    .date
)


# rule 1
patients_with_unresolved_dm = (
    latest_dm_date.is_not_null() & (
        latest_dmres_date.is_null() | (latest_dmres_date < latest_dm_date)
    )
 )

# rule 2
patients_eligible = is_alive_during_interval & is_17_or_over_by_interval_start & has_registration_spanning_interval

# rule 1 and 2
eligible_patients_with_unresolved_dm = patients_with_unresolved_dm & patients_eligible



# Age groups
patients.age = patients.age_on(INTERVAL.start_date)
patients.age_band = case(
    when(patients.age < 20).then("0-19"),
    when(patients.age < 40).then("20-39"),
    when(patients.age < 60).then("40-59"),
    when(patients.age < 80).then("60-79"),
    when(patients.age >= 80).then("80+"),
    otherwise="missing",
)


# Set up measures object ----
measures = create_measures()

measures.configure_dummy_data(population_size=1000)

# Disable disclosure control in case its needed for this demo.
# Values will neither be suppressed nor rounded.
measures.configure_disclosure_control(enabled=False)

# Define unresolved dm measure ----
measures.define_measure(
    name = "unresolved_dm",
    numerator = eligible_patients_with_unresolved_dm,
    denominator = patients_eligible,
    intervals = months(24).starting_on(start_financial_year)
)

# Define unresolved dm measure by age ----
measures.define_measure(
    name = "unresolved_dm_age",
    numerator = eligible_patients_with_unresolved_dm,
    denominator = patients_eligible,
    group_by = { "age_band": patients.age_band },
    intervals = months(24).starting_on(start_financial_year)
)
