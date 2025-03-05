from erddapy import ERDDAP
import pandas as pd
import matplotlib.pyplot as plt

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

e = ERDDAP(
    server="https://nwem.apl.washington.edu/erddap", 
    protocol="tabledap", 
    response="csvp")

e.dataset_id = "orca1_L1_profiles"
e.variables = [
    "sea_water_pressure",
    "time",
    "sea_water_temperature",
    "sea_water_practical_salinity"
]

# Otherwise it's too big and spins forever trying to grab all the data since. 1970.
e.constraints = {
    "time>": "2023-01-15T00:00:00Z",
    "time<": "2024-01-16T23:59:59Z",
    }

url = e.get_download_url(dataset_id="orca1_L1_profiles")

# it can't find the download link if I don't include these, and it also doesn't like it if I put them in the constraints instead. Hm.
# maybe I can do something with UTC time formatting in the constraints?
url = url.replace("<", "%3C")
url = url.replace(">", "%3E")
print(url)

df = pd.read_csv(url)
# print(df)

# print(df.columns)

df["time (UTC)"] = pd.to_datetime(df["time (UTC)"], format="%Y-%m-%dT%H:%M:%SZ")

# print(df)

# only the 13th
df_13 = df[df["time (UTC)"].dt.day == 13]

print(df_13)

df_13.plot(
    x='sea_water_temperature (degree_C)',
    y='sea_water_pressure (dbar)', 
    kind = 'scatter',
    c='sea_water_practical_salinity (PSU)',
    colormap="YlOrRd",
    )

# fig, ax = plt.subplots()
# ax.scatter(x=df_13['sea_water_temperature (degree_C)'], y=df_13['sea_water_pressure (dbar)'])
plt.show()

# print(df_13_avg)


# df = e.to_pandas()
# print(df)


