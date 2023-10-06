import pandas as pd
path = "biourja-efzrr-y7i38ed9-input.csv"
data = pd.read_csv(path)

# Initial state forecasts for each zone
state_forecasts = {
    "E": 2800,
    "N": 1500,
    "S": 6500,
    "W": 2000
}

# Total forecast for the entire region
total_forecast = 12000

# Calculate the total forecast for all states
total_state_forecast = sum(state_forecasts.values())

# Calculate the total surplus/deficit
total_region_deficit = total_forecast - total_state_forecast
print(total_region_deficit)

# Redistribute the surplus/deficit proportionally to each state's forecast
for x in state_forecasts:
    state_forecasts[x] += (state_forecasts[x] / total_state_forecast) * total_region_deficit
    print(x, state_forecasts[x])

#new total state forecast after redistribution
total_state_forecast = sum(state_forecasts.values())
print(total_state_forecast)


#computing zonal wise forecasts
zone_capacity = data.groupby(data['Plant_Name'].str[0])['Forecast'].sum()
zone_capacity_dict = zone_capacity.to_dict()
print(zone_capacity_dict)
print(state_forecasts)


#computing surplus/deficit that needs to be assingned to each zone
zone_defsur = {key: state_forecasts[key] - zone_capacity_dict.get(key, 0) for key in state_forecasts}

#new column to have updated forecast values
data['new_forecast'] = data.apply(lambda row: row['Forecast'] + row['Forecast'] / zone_capacity_dict.get(row['Plant_Name'][0], 1) * zone_defsur.get(row['Plant_Name'][0], 0), axis=1)

data.to_csv('output.csv', index=False)