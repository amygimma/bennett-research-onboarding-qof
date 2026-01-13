from ehrql import codelist_from_csv

# Create codelists ----
dm_codelist = codelist_from_csv(
  "codelists/nhsd-primary-care-domain-refsets-dm_cod.csv"  ,
  column="code"
)

dmres_codelist = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-dmres_cod.csv",
    column="code"
)