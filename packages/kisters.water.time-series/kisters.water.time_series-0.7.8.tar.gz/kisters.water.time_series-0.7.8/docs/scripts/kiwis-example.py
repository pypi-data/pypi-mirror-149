from datetime import datetime

import matplotlib.pyplot as plt

from kisters.water.time_series.kiwis import KiWISStore

# Initialize KiWISStore object with url to location
kiwis = KiWISStore("http://kiwis.kisters.de/KiWIS2/KiWIS")

# Get time series list by path filter
ts_list = kiwis.get_by_filter("123/*/Precip/MMonth.Total")

# Get time series by path
ts = kiwis.get_by_path("DWD/07367/Precip/CmdTotal.1h")

# We can access timeseries metadata as a dict using the metadata attribute
ts_metadata_dict = ts.metadata
# ts_metadata_dict looks like this:
# {
#     "from": datetime.datetime(
#         2007, 12, 1, 0, 0, tzinfo=tzoffset(None, 3600)
#     ),
#     "to": datetime.datetime(
#         2018, 7, 16, 23, 0, tzinfo=tzoffset(None, 3600)
#     ),
#     "tsPath": "DWD/07367/Precip/CmdTotal.1h",
#     "shortName": "CmdTotal.1h",
#     "id": 7411042,
#     "name": "0 Stundenwerte",
#     "dataCoverageFrom": datetime.datetime(
#         2007, 12, 1, 0, 0, tzinfo=tzoffset(None, 3600)
#     ),
#     "dataCoverageUntil": datetime.datetime(
#         2018, 7, 16, 23, 0, tzinfo=tzoffset(None, 3600)
#     ),
# }

# Access the time series data in the form of pandas DataFrame
df = ts.read_data_frame(datetime(2017, 1, 1), ts.coverage_until)

# Plot the data
plt.figure(figsize=(15, 5))
df["Value"].plot(label=ts.name, figsize=(15, 5))
df["Value"].resample("D").sum().plot(label="Daily sum", figsize=(15, 5))
plt.legend(loc=2)
plt.show()
