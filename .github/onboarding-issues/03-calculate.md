# Task 3: calculate monthly prevalence

## Objective

Using the `measures` framework, calculate the monthly prevalence trends for a QOF register of your choice (e.g., the Diabetes register or the register you selected for your first GitHub issue) during the NHS Financial Year 2023/24.

## Background 

Have a look at our paper on the [Impact of COVID-19 on recorded blood pressure screening and hypertension management in England: An analysis of monthly changes in Quality and Outcomes Framework indicators in OpenSAFELY](https://www.medrxiv.org/content/10.1101/2023.07.20.23292883v2). The subsection _Implementation of QOF business rules in analytic code_ in the Methods section outlines the approach. Note that this was implemented using [Cohort Extractor](https://docs.opensafely.org/type-one-opt-outs/#1-cohort-extractor), the predecessor to ehrQL.

## Implementation details

Follow the explanation on [Using the measures framework](https://docs.opensafely.org/ehrql/explanation/measures/) from our documentation. Here are some implementation notes:

1. **Create a new branch** 
   - Name your branch simething like `<github-user-name>/add-dm017-measures`

2. **Create a new measures file** 
   - In the `analysis` subdirectory, create new Python file for your measures definition e.g., `analysis/dm_reg_measures.py`

3. **Define numerator and denominator rules**
   - Write the rules similar to those you would write for a dataset definition, but the key difference that you will use the placeholders `INTERVAL.start_date` and `INTERVAL.end_date` (see more [here](https://docs.opensafely.org/ehrql/explanation/measures/#the-interval-placeholder)) instead of `index_date`. For example, to calculate patient age at the end of every montly interval:


      ```py
      # Field number: 4
      # PAT_AGE: The age of the patient in full years at the achievement date.
      dataset.pat_age = patients.age_on(INTERVAL.end_date)
      ```
   
      or to select the appropriate clinical events for every interval:

      ```py
      selected_events = clinical_events.where(
          clinical_events.date.is_on_or_before(INTERVAL.end_date)
      )

      dmlat_dat = (
           selected_events.where(selected_events.snomedct_code.is_in(dm_cod))
          .sort_by(selected_events.date)
          .last_for_patient()
          .date
      )
      ```

4. **Define your measures**
   - Think what would be good variables for `dm017_numerator` and `dm017_denominator`
   
      ```py
      measures.define_measure(
          name="dm017",
          numerator=dm017_numerator,
          denominator=dm017_denominator,
          intervals=months(12).starting_on("2023-04-01"),
      )
      ```

5. **Test your code using `opensafely exec`**
   - Periodically run the following command in your terminal to check if you code works `opensafely exec ehrql:v1 generate-measures analysis/dm_reg_measures.py`

6. **Add breakdown variables** 
   - Think about what breakdown variables would be useful for QOF. You can check our paper to see what we did previously. Add the breakdown variables to your measures definition using the `group_by` argument (see [Grouping by multiple features](https://docs.opensafely.org/ehrql/explanation/measures/#grouping-by-multiple-features)), for example:
      ```py
      measures.define_measure(
          name="dm017",
          numerator=dm017_numerator,
          denominator=dm017_denominator,
          group_by={
              "sex": patients.sex
          },
          intervals=months(12).starting_on("2023-04-01"),
      )
      ```

7. **Update the `project.yaml` file**
   - Add an action for generating measures. Note that the generate-measures command is similar to generate-dataset, with a few differences (e.g., `generate-measures` does not have a `--test-data-file` argument):

      ```yaml
     generate_dm017_measures:
       run: > 
         ehrql:v1 generate-measures analysis/measures_definition_dm017.py
         --output output/dm/dm017_measures.csv
       outputs:
         moderately_sensitive:
           measure: output/dm/dm017_measures.csv
      ```
