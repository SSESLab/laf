import urllib.parse
import urllib.request
import urllib.error
#
from mesowest_api import *



global token, base_url, geo_criteria, station, start, end, endpoint
global latitude_marker, longitude_marker
token = 'ca01203d0c9746cd998ee8d0007fdf07'
base_url = 'http://api.mesowest.net/v2/'
geo_criteria = ['stid', 'state', 'country', 'county', 'radius', 'bbox', 'cwa', 'nwsfirezone', 'gacc', 'subgacc']
# start = '201401010000'
# end = '201401010100'

endpoint = 'stations/timeseries'


# ==================================================================================================================== #
def api_fun(**kwargs):
    kwargs['start'] = date1
    kwargs['end'] = date2
    kwargs['token'] = token
    kwargs['radius'] = radius_
    qsp = urllib.parse.urlencode(kwargs, doseq=True)
    resp = urllib.request.urlopen(base_url + endpoint + '?' + qsp).read()
    #
    response = json.loads(resp.decode('utf-8'))
    return response

# ==================================================================================================================== #
def show_mw_stats(lat_inp, long_inp, rad_inp, date1_inp, date2_inp):
    # *****************
    lat = lat_inp
    long = long_inp
    rad = rad_inp
    # *****************
    global radius_, date1, date2
    date1 = date1_inp
    date2 = date2_inp
    radius_ = [lat, long, rad]
    allstationdata = api_fun()
    num_stat = allstationdata['SUMMARY']['NUMBER_OF_OBJECTS']

    if num_stat is 0:  # this means there are no data available for this month, so the year cannot be completed
        flag_numb_stations = 3
        return [], [], [], [], [], [], []
        # break
    else:
        Stations_Vars = []
        code_station = []
        lat_station = []
        long_station = []
        name_st = []
        distance = []
        network = []
        POR = []
        SensVars = []
        # print(len(lat_station))
        for i in range(0, num_stat):
            if allstationdata['STATION'][i]['STATUS'] == 'ACTIVE':
                lat_station.append(allstationdata['STATION'][i]['LATITUDE'])
                long_station.append(allstationdata['STATION'][i]['LONGITUDE'])
                name_st.append(allstationdata['STATION'][i]['NAME'])
                distance.append(allstationdata['STATION'][i]['DISTANCE'])
                network.append(allstationdata['STATION'][i]['MNET_ID'])
                period_of_record = allstationdata['STATION'][i]['PERIOD_OF_RECORD']
                # print(period_of_record['start'])
                # print(period_of_record['end'])
                por_assemble = 'Start: ' + period_of_record['start'] + ' - End: ' + period_of_record['end']
                #
                # try:
                #     por_assemble = 'Start: ' + period_of_record['start'] + ' - End: ' + period_of_record['end']
                # except (TypeError):
                #     print('wrong date format')
                # else:
                #     por_assemble = 'Start: NaN - End: NaN'
                POR.append(por_assemble)
                # POR.append('ciao')
                variables = list(allstationdata['STATION'][i]['SENSOR_VARIABLES'])
                var_str = variables[0]
                for j in range(1, len(variables)):
                    var_str = (var_str + ', ' + variables[j])
                SensVars.append(var_str)
        return lat_station, long_station, name_st, distance, network, POR, SensVars


