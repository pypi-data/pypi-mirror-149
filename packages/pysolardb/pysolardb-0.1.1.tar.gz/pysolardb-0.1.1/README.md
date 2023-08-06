# pySolarDB

Python library to access LE2P solar database SolarDB

Source code accessible via the github repository: [pySolarDB](https://github.com/LE2P/pySolarDB)

## Installation

Using pip3

```python
pip3 install pysolardb
```

__Suggestion__: You will need a token to allow data access.

In the following, we  will use an instance of the `SolarDB` class as an example.

```python
from pysolardb.SolarDB import SolarDB
solar=SolarDB()
```

You can disable part of the messages by setting a new logging level for the SolarDB object:

```python
import logging

solar.setloggerLevel(logging.WARNING)
# using and integer
solar.setloggerLevel(10)
```

Keep in mind that the requests will sometimes result in empty answers. `solar.setLoggerLevel(20)` will help find such cases.

## Utils methods: Register, Login, Status and Logout

__Note__: You can configure the '~/.bashrc' file in your home directory to allow the library to automatically recover and use your authentication token.

In the `~/.bashrc` file:

```python
export SolarDBToken=YOUR_AUTHENTICATION_TOKEN
```

### Register

If you do not already possess a token, use the `register` method to receive a new one by email:

```python
solar.register(email="YOUR_EMAIL_ADDRESS")
```

### Login

Assuming you did not configure your '~/.bashrc' file, logged out or just received your token, you will need to use the `login` method before being able to access the solar data:

```python
solar.login(token="YOUR_AUTHENTICATION_TOKEN")
```

### Status

The `status` method verifies if the user is still logged in SolarDB.

```python
solar.status()
```
 __Remark__: This method becomes obsolete for logging levels higher than INFO.

### Logout

The `logout` method disables the access to SolarDB data.

```python
solar.logout()
```

## Recovering the sites, types and sensors list

### Sites recovery

The `getAllSites` method returns a list of strings containing all the alias sites present in SolarDB.

```python
solar.getAllSites()
```

### Types recovery

The `getAllTypes` method returns a list of strings containing all the data types present in SolarDB.

```python
solar.getAllTypes()
```

### Sensors recovery

The `getSensors` method returns a list of strings containing the sensor IDs extracted from SolarDB. To narrow down the sensors, use the following parameters:
- sites : list[str] (optional)
- types : list[str] (optional)

```python
solar.getSensors()
# search the diffuse and global irradiance sensors at Le Port Mairie
solar.getSensors(sites=["leportmairie"], types=["DHI","GHI"])
```

## Data collection

__Note__: The following data recovery methods will return empty dictionaries unless they recieve at least one site, type and/or sensor ID as parameters.

### Raw data recovery

The `getData` method recovers all the data associated to a list of alias sites, types and/or sensor IDs. It takes at least one of the following parameters:
- sites : list[string]
- types : list[string]
- sensors : list[string]
- start : string (optional)
- stop : string (optional)
- aggrFn : string (optional)
- aggrEvery : string (optional)

```python
# get the global irradiance values from Vacaos and Plaine Des Palmistes Parc National taking the average value for each day over the last 2 months
data = solar.getData(sites=["plaineparcnational","vacoas"], types=["GHI"], start="-2y", aggrFn="mean", aggrEvery="1w")
```

The data we just collected can then be used to plot the evolution of the global irradiance:

```python
import matplotlib.pyplot as plt
from datetime import datetime as dt

alias = ["plaineparcnational","vacoas"]
dtype = ["GHI"]
data = solar.getData(sites=alias, types=dtype, start="-2y", aggrFn="mean", aggrEvery="1d")

# extract the dates and values for Vacoas from the 'data' dictionary
sensors = solar.getSensors(sites=["plaineparcnational"], types=["GHI"])

plt.figure()
for sensor in sensors:
    dates = data["plaineparcnational"][sensor]["dates"]
    values = data["plaineparcnational"][sensor]["values"]

    # put the dates to a datetime format
    dates = [dt.strptime(date, "%Y-%m-%dT%H:%M:%SZ") for date in dates]

    # plot the average global irradiance per day for the last 2 years

    plt.plot(dates, values)
plt.legend(labels=sensors)
plt.show()
```

### Get the sensors' active period for specific sites

The `getBounds` method returns a dictionary containing the active time period per sensor per site. it takes at least one of the following the parameters:
- sites : list[string] (optional)
- types : list[string] (optional)
- sensors : list[string] (optional)

```python
# get the temporal bounds of each sensor at Saint Louis Lycée Jean Joly
alias= ['saintlouisjeanjoly']
dtype = ['GHI']
sensors = solar.getSensors(types=dtype, sites=alias)
bounds = []
for sensor in sensors:
    bound = solar.getBounds(sites=alias, types=dtype, sensors=[sensor])
    bounds.append(sensor + "= start: " + bound.get(alias[0]).get(sensor).get("start") \
                         + " | stop: " + bound.get(alias[0]).get(sensor).get("stop"))
print("\n".join(bounds))
```

## Metadata recovery

### Recover the campaigns' metadata

the `getCampaigns` method is used to recover the metadata associated with the different campaigns of the IOS-Net project in a dictionary. You can use the following parameters:
- id : string (optional)
- name : string (optional)
- territory : string (optional)
- alias : string (optional)

```python
solar.getCampaigns()
# get the campaigns' metadata for Mauritius
solar.getCampaigns(territory="Mauritius")
```

### Extract the instruments' metadata

The `getInstruments` method recovers the metadata associated to the instruments used by the IOS-Net project. It takes the following parameters:
- id : string (optional)
- name : string (optional)
- label : string (optional)
- serial : string (optional)

```python
solar.getInstruments()
```

### Get the measures' metadata

The `getMeasures` method recovers the metadata that is associated with the different types of measures. You can use the parameters:
- id : string (optional)
- name : string (optional)
- dtype : string (optional)
- nested : boolean (optional)

```python
solar.getMeasures()
# get the metadat for UV measures
solar.getMeasures(type="UVAB")
```

### Recover the models' metadata

The `getModels` method recovers the metadata associated to the sensor types. You can use these parameters :
- id : string (optional)
- name : string (optional)
- dtype : string (optional)

```python
solar.getModels()
```
