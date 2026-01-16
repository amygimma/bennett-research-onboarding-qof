# Create histograms of measures by group where applicable

library(dplyr)
library(purrr)
library(readr)
library(ggplot2)

output_plot_filepath <- file.path("output", "plots")
dir.create(here::here(output_plot_filepath))

df <- readr::read_csv(
    here::here("output", "unresolved_dm_measures.csv")
) %>% 
mutate(age_band = ifelse(is.na(age_band), "All", age_band))


df %>% 
    split(.$measure) %>%
    imap(~
        ggsave(
            filename = here::here(output_plot_filepath, paste0("histogram_", .y, ".png")),
            plot =  ggplot(.x, aes(x = interval_start, y = ratio, color = age_band, group = age_band)) +
                        geom_line() +
                        scale_x_date(breaks = "1 month", date_labels = "%b %Y") +
                        ylim(0,1) +
                        labs(
                            x = "Month",
                            y = "Ratio",
                            color = "Age group",
                            title = case_when(
                                .y == "unresolved_dm" ~ "Prevalence of unresolved diabetes melitis",
                                .y == "unresolved_dm_age" ~ "Prevalence of unresolved diabetes melitis by age group",
                                .y == "unresolved_dm_new" ~ "Ratio of new diabetes diagnoses"
                            )
                        )
        )
    )
    
