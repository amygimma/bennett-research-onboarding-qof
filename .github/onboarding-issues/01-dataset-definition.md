# Task 1: Create a dataset defintion using the diabetes QOF rules

Diabetes register:  Patients aged at least 17 years old with an unresolved diabetes diagnosis

The rules for the all QOF registers and indicators are available [here](https://digital.nhs.uk/data-and-information/data-collections-and-data-sets/data-collections/quality-and-outcomes-framework-qof/business-rules/quality-and-outcomes-framework-qof-business-rules-v49-2024-25). The specific rules for each indicaror an in section 3.2.2.1 of each word document, e.g., `Diabetes_v49.0.docx` for Diabetes.

## Rule description or comments

- **Rule 1**: Pass to the next rule all patients from the specified population who meet both of the criteria below and reject the remaining patients.
  - Have a diabetes diagnosis in the patient record up to and including the achievement date.
  - Latest diabetes diagnosis is not followed by a diabetes resolved code.
- **Rule 2**: Reject patients passed to this rule who are aged under 17 years old on the achievement date. Select the remaining patients.

## Implementation details

Impletement the QOF Diabetes indicator (Version 49) for the NHS Financial Year 1st April 2023 to 31st March 2024.

Try to use the `opensafely exec` command introduced in the [Getting Started Tutorial](https://docs.opensafely.org/getting-started/tutorial/generate-a-first-dataset/) as much as possible to get used to an interative workflow. This will help to catch and resolve mistakes early. Some things will go wrong and you'll see some error messages. The how to guide on [Resolving ehrQL errors](https://docs.opensafely.org/ehrql/how-to/errors/) may help, if not just reach out on Slack.

1. First, you need to set some things up:
   - Create a [GitHub codespace](https://docs.opensafely.org/getting-started/tutorial/create-a-github-codespace/) for this repository. See also this how-to guide on [How to use GitHub Codespaces in your project](https://docs.opensafely.org/getting-started/how-to/use-github-codespaces-in-your-project/)
   - Add your own Git branch where you will work on this ticket (e.g., `<github-user-name>/<description-of-the-work>`).

2. Add the two codelist needed for the register (available at https://www.opencodelists.org/codelist/nhsd-primary-care-domain-refsets) to the `codelists/codelists.txt` file, e.g., `nhsd-primary-care-domain-refsets/dm_cod/20210127` for [DM_COD](https://www.opencodelists.org/codelist/nhsd-primary-care-domain-refsets/dm_cod/20210127/).
    - Run the following command in the terminal `opensafely codelists update`

3. Next, add a new file for your dataset definition to the analysis folder, e.g., `analysis/dm_reg_dataset_<your-name>.py`

4. Add each codelist to the dataset definition, see the [How to work with codelists](https://docs.opensafely.org/ehrql/how-to/codelists/) guide for more info.

5. Include everyone who had a practice registration on 31st March 2024 (this is slightly different to what the QOF rules actually say). Run `opensafely exec ehrql:v1 generate-dataset analysis/dm_reg_dataset_<your-name>.py` in the terminal every now and then to see if your code works.
   
   ```
   has_registration = practice_registrations.for_patient_on(index_date).exists_for_patient()
   ```

6. Add all variables needed for the register (`DM_REG`) to the file `analysis/dm_reg_dataset.py`. Again, run `opensafely exec ehrql:v1 generate-dataset analysis/dm_reg_dataset_<your-name>.py` in the terminal every now and then to see if your code works. For example:

    ```py
    # Field number: 6
    # DMLAT_DAT: Date of the most recent diabetes diagnosis up to and
    # including the achievement date.
    dataset.dmlat_dat = last_for_patient(prior_events, codelists.dm_cod).date
    ```

7. Define each clinical rule into ehrQL code. If there are multiple rules for your register, combine their logic. See the [Combining multiple inclusion criteria](https://docs.opensafely.org/ehrql/how-to/define-population/#combining-multiple-inclusion-criteria) section in our docs:
    ```py
    # DM REGISTER (DM_REG)
    # DM_REG rule 1:
    # Pass to the next rule all patients from the specified population who meet
    # both of the criteria below:  Have a diabetes diagnosis in the patient record
    # up to and including the achievement date. Latest diabetes diagnosis is not
    # followed by a diabetes resolved code.
    dm_reg_r1 = (dataset.dmres_dat < dataset.dmlat_dat) | (
        dataset.dmlat_dat.is_not_null() & dataset.dmres_dat.is_null()
    )
    ```

9. Add an action for your dataset definition to the `project.yaml` file, see [The project pipeline](https://docs.opensafely.org/actions-pipelines/) page in our docs for more

## Acceptance criteria

To complete this ticket:

- Add the codelists needed for `DM_REG`:
  - [ ] `DM_COD`
  - [ ] `DMRES_COD`
- All variables needed for `DM_REG` need to be added to the dataset definition:
  - [ ] `DMLAT_DAT`
  - [ ] `DMRES_DAT`
  - [ ] `PAT_AGE`
- Each rule in `DM_REG` is defined in the dataset definition:
  - [ ] `dm_reg_r1`
  - [ ] `dm_reg_r2`
- After adding all variables and rules: 
  - [ ] Add and action for the dataset definition to the [`project.yaml` file](https://docs.opensafely.org/getting-started/tutorial/generate-a-first-dataset/)