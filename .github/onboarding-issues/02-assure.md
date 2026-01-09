# Task 2: Write assurance tests for your dataset definition

Write _assurance tests_ for your dataset definition following the guide on [How to test your dataset definition](https://docs.opensafely.org/ehrql/how-to/test-dataset-definition/#how-to-test-your-dataset-definition).

1. **Create a test file** 
   - Start by creating a new file in the `analysis/` subdirectory with the same file name as the dataset definition you're testing but with the prefix `test_`. For example, if you're writing tests for `dm_reg_dataset.py`, the new test file should be named `test_dm_reg_dataset.py`.

2. **Import dataset and modules**
   - At the beginning of the new test file you need to import your `dataset` and the `date` function. Note that in this example `dm_reg_dataset` refers to the `analysis/dm_reg_dataset.py` file, you will have to change this to the dataset definition you want to test.

      ```py
      from datetime import date
      from dm_reg_dataset import dataset
      ```

3. **Define test data and expectations**
   - Now you can start defining test data for your assurance tests, see the [Data for test patients](https://docs.opensafely.org/ehrql/how-to/test-dataset-definition/#data-for-test-patients) section in the _How-to guide_. Here are some tips for writing assurance tests:
      - **Only specify data that is needed for your tests**: You only have to specify the data that you actually want to test, i.e., if you just want to test whether a patient is currently registered with a practice you only need to define the start and end date for the practice registration. You dont have to specify all the other columns from the [`practice_registrations`](https://docs.opensafely.org/ehrql/reference/schemas/tpp/#practice_registrations) table (e.g., `practice_pseudo_id` or `practice_stp`). Note that you always have to include an entry for each table that you're using in your dataset definition, regardless whether you want to specify test data for this patient or not, e.g., `"clinical_events": [{}],` in the example below.

     ```py
     test_data = {
         # Correctly not expected in population
         # No clinical events
         1: {
             "patients": {"date_of_birth": date(1950, 1, 1)},
             "practice_registrations": [
                 {
                     "start_date": date(2010, 1, 1),
                 },
             ],
             "clinical_events": [{}],
             "expected_in_population": False,
         },
      }
      ```

      - **Define simple test data**: I find it helpful to create _simple_ test patients that only test one isolated aspect of my dataset definition. This means that I end up with many tests patients, each testing a specific ehrQL query (e.g., a QOF exclusion rule or patient age calcualtion).
      - **Run assurance tests repeatendly**: Start with a simple test example and run the assurance tests repeatedly using the following command in your terminal. Adjust the file name as necessary.
      
      ```bash
      opensafely exec ehrql:v1 assure analysis/<name-of-test-for-dataset-definition>.py
      ```
      - **Start with writing failing tests**: Write tests expecting them to fail initially and then fix them. For example, if testing age calculation, specify an incorrect age in expected_columns to verify the test catches the error.

4. **Expand test coverage**
   - Add more test patients so that you are confident that the main ehrQL queries in your dataset definition are correct.

5. **Add tests to OpenSAFELY pipeline**
   - Add your test file to the `project.yaml` file so that the tests get exectuted every time you run your dataset definition. At the moment you have to inspect the log files to see the results of the assurance tests, e.g., `metadata/<name-of-your-generate_dataset-action.log`.