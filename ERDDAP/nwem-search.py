from erddapy import ERDDAP
e = ERDDAP(
    server="https://nwem.apl.washington.edu/erddap", 
    protocol="tabledap", 
    response="csv")

# these lines fix the SSL: CERTIFICATE_VERIFY_FAILED error I was getting on linux, not sure how safe they are in general
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Search the NWEM for all the datasets that include aggregate sea water pressure
url = e.get_search_url(search_for="sea_water_pressure_qc_agg", response="csv")
print(url)

# That URL returns a CSV, so we can directly read it with pandas
import pandas as pd
df = pd.read_csv(url)
print(df["Dataset ID"])
# df

# take a look at index 6 - Twanoh
twanoh = df.loc[6]
print(twanoh)

# its tabledap url can also be accessed directly
print(twanoh["tabledap"])


# now that I know the dataset ID, I can use it to extract data from our original ERDDAP object
e.dataset_id = "orca1_L1_profiles"
e.variables = [
    "sea_water_pressure",
    "time",
    # "sea_water_electrical_conductivity (S/m)",
    # "sea_water_temperature_qc_agg",
    # "sea_water_practical_salinity_qc_agg"
]

e.constraints = {
    "time>=": "2023-01-13T00:00:00Z",
    "time<=": "2024-01-16T23:59:59Z",}

url = e.get_download_url(dataset_id="orca1_L1_profiles")
print(url)

df = pd.read_csv("https://nwem.apl.washington.edu/erddap/tabledap/orca1_L1_profiles.csv?sea_water_pressure,time&time%3E=1673568000.0&time%3C=1705449599.0")

print(df)

# we can also directly the metadata of one of the datasets
info_url = e.get_info_url(dataset_id="orca1_L1_profiles")
print(info_url)
metadata = pd.read_csv(info_url)
metadata[0:10]

metadata["Variable Name"].unique()