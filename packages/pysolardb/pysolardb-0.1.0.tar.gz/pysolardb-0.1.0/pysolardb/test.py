from SolarDB import SolarDB
import matplotlib.pyplot as plt
from datetime import datetime as dt
import logging

if __name__=="__main__":
    solar = SolarDB()
    solar.setloggerLevel(logging.WARNING)
    
    print(solar.getSensors(sites=["vacoas"])[0])
    print(solar.getAllSites()[-1])
    print(solar.getAllTypes()[1])

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

    # plot the average global irradiance per week for the last 2 y

    plt.plot(dates, values)
plt.legend(labels=sensors)
plt.show()


alias= ['saintlouisjeanjoly']
dtype = ['GHI']
sensors = solar.getSensors(types=dtype, sites=alias)
bounds = []
for sensor in sensors:
    bound = solar.getBounds(sites=alias, types=dtype, sensors=[sensor])
    bounds.append(sensor + "= start: " + bound.get(alias[0]).get(sensor).get("start") \
                         + " | stop: " + bound.get(alias[0]).get(sensor).get("stop"))
print("\n".join(bounds))
print(solar.getCampaigns(territory="Mauritius"))

print(solar.getInstruments())

print(solar.getMeasures())

print(solar.getModels())