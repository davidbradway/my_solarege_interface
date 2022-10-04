import os
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from solaredge_interface.api.SolarEdgeAPI import SolarEdgeAPI 

site_id = os.environ.get('SOLAREDGE_SITEID')
api = SolarEdgeAPI(api_key=os.environ.get('SOLAREDGE_API_KEY'), datetime_response=True, pandas_response=True) 


def print_current_power_flow():
    response = api.get_site_current_power_flow(site_id)
    grid = response.data['siteCurrentPowerFlow']['GRID']['currentPower']
    load = response.data['siteCurrentPowerFlow']['LOAD']['currentPower']
    pv = response.data['siteCurrentPowerFlow']['PV']['currentPower']
    unit = response.data['siteCurrentPowerFlow']['unit']
    print(f"{pv = }, {load = }, {grid = } {unit}\n")
    if pv > load:
        print(f"pv -> (load + grid)")
    else:
        print(f"(pv + grid) -> load")


def get_daily_results():
    response = api.get_site_data_period(site_id)
    startDate = response.data['dataPeriod']['startDate']
    endDate = response.data['dataPeriod']['endDate']
    start_day = startDate.strftime("%Y-%m-%d")
    end_day = endDate.strftime("%Y-%m-%d")
    response = api.get_site_energy(site_id, start_day, end_day)

    return response

def main():
    response = get_daily_results()
    df = response.pandas
    df = df.set_index('energy.values.date')
    df = df.sort_index()
    df[df['energy.values.value'] > 70000] = np.nan
    df = df.fillna(method="ffill")
    # df.head()

    monthly = df.groupby(df.index.month)['energy.values.value'].sum()
    print(monthly)

    # ax = monthly.plot()
    # plt.show()


if __name__ == '__main__':
    main()
