Noble 2019-2020

Includes:

* Soil

* Weather

* ERT

After been separately organized in a datetime table, the three are merged into a unique MultiIndex table.

**datetime** is hourly and it is used as index.

**weather** contains the data from the Noble weather station (ARD2), data provided by Mesonet.

Weather => ARD2 => station data

**Soil** contains soil information from the 6 soil sensors installed at the center of the ERT line.

Soil => sensors => sensor specific data

**ERT** contains the averages, standard deviations, min, and max for each of the specified regions of interest.

ERT => regions => avg, std, min, and max


# Analysis

How do the cultivars and their intervariability affect the soil response to the weather?

1. find a weather-soil model that correctly predict the data of the soil sensors from the weather data.
2. find an ERT-soil model that correctly predicts the resistivity from the data of the soil sensors.
3. use the ERT-soil model to upscale the soil data.
4. match weather and ERT to extract differences among cultivars and between the cultivars and bare soil.

# Measuring vs Estimating

Weather: we have standard weather data, but we are missing net radiation.
Anyway, net radiometers have significant errors and aren't really common.
Consequently, there is high interest in methods for estimating the net radiation.

## Possible models
Weather: see FAO Chapter 3, Metereological data

R_n = R_t * albedo

Soil: we have sensors for water content and temperature, and ERT resitivity, but we are missing soil heat flux.



