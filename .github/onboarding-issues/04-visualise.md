# Task 4: Visualise your results

Write a [scripted action](https://docs.opensafely.org/actions-scripts/) in R or Python to visualise the monthly trends of the QOF register you picked.

1. **Decide _where_ to work on this issue**
   - You could keep working on the branch you used for #12 or create a new branch, e.g., `<github-user-name>/visualise-dm017-measures`

2. **Create a new file** 
   - In the `analysis` subdirectory, create new R or Python file for your scripted action e.g., `analysis/visualise_measures.R`

3. **Load the output form the `generate-measures` action**
   - For example in R:

      ```R
      # Load data
      df_measures <- readr::read_csv(
        here::here("output", "dm", "dm017_measures.csv")
      )
      ```

4. **Develop your code interactively and that it works in the OpenSAFELY R/Python environments**
   - Write code to visualise the monthly trends in the QOF register you picked. In our recent [QOF paper](https://www.medrxiv.org/content/10.1101/2023.07.20.23292883v2.full-text) we chose to visualise the trends like [this](https://www.medrxiv.org/content/medrxiv/early/2023/07/31/2023.07.20.23292883/F1.large.jpg), see panel B for the Hypertension register.
   - You can use your local R or Python environment, but there may be some differences in the versions of the packages. This will sometimes lead to errors and it is usually best to test your code in the same environments that we have available in OpenSAFELY. You can read more on our R, Python, and STATA packages [here](https://docs.opensafely.org/requesting-libraries/).
   - You can launch the R or Python environment and develop your code interactively, for example you can launch an R console with the exact environment we have in OpenSAFELY using:
    
     ```bash
     opensafely exec r R
     ```
    
     or for `ipython`:


     ```bash
     opensafely exec python ipython
     ```

   - For more details see our documentation on how to [How to use the OpenSAFELY command-line interface](https://docs.opensafely.org/opensafely-cli/#exec-interactive-development
)

5. **Update the `project.yaml` file**

   - Add an action for visualising the measures. Note that this scripted action depends on the `generate-measures` you wrote for #12 and that you have to use `needs`
   - You would need to use `python:latests analysis/visualise_measures.py` if you want to use Python for this task

      ```yaml
      visualise_dm017_measures:
       run: > 
         r:latests analysis/visualise_measures.R
         --output output/dm/dm017_measures.png
       needs: [generate_dm017_measures]
       outputs:
         moderately_sensitive:
           measure: output/dm/dm017_measures.png
      ```