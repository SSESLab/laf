import json
import sys
import csv
import numpy
import warnings
import pandas as pd


warnings.simplefilter('ignore', numpy.RankWarning)

# Group holes indexes in consecutive groups
#  ==================================================================================================================== #
def group_consecutives(vals):
    run = []
    result = [run]
    expect = None
    for v in vals:
        if (v == expect) or (expect is None):
            run.append(v)
        else:
            run = [v]
            result.append(run)
        expect = v + 1
    return result

# Break Date into year, month, day...
#  ==================================================================================================================== #
def date_break(Date):
    year = []
    month = []
    day = []
    hh = []
    mm = []
    for i in range(0, len(Date)):
        zz = Date[i]
        year.append(int(zz[0:4]))
        month.append(int(zz[5:7]))
        day.append(int(zz[8:10]))
        hh.append(int(zz[11:13]))
        mm.append(int(zz[14:16]))

    return year, month, day, hh, mm
#  ==================================================================================================================== #


def create_date_range_from_year_no_tz(year):
    vector_date_range = pd.date_range(start=str(year) + '-01-01 00:00', end=str(year) + '-12-31 23:00', freq='H')         #This is the right one
    return vector_date_range

def create_date_range_from_year(year, time_zone):
    if abs(float(time_zone)) > 9:
        start_date = str(year) + '0101' + str(int(abs(float(time_zone)))) + '00'
        end_date = str(int(year) + 1) + '0101' + str(int(abs(float(time_zone)))) + '00'
    else:
        start_date = str(year) + '01010' + str(int(abs(float(time_zone)))) + '00'
        end_date = str(int(year)+1) + '01010' + str(int(abs(float(time_zone)))) + '00'
    return start_date, end_date




def hourlydata(Variable, Date, month_days, delta_holes_threshold, TimeZone):


    [year, month, day, hh, mm] = date_break(Date)

    # check if there is any NoneType. If any, write down the index
    #  ==================================================================================================================== #
    none_index = []
    for i in range(0, len(year)):
       if Variable[i] == None:
           none_index.append(i)


    # Pass from 5min to 1h steps
    # ==================================================================================================================== #
    k = 0
    t = 1
    variable_h = []
    if 0 in none_index:
        variable_h.append(0)
    else:
        variable_h.append(Variable[0])
    HH = []
    HH.append(hh[0])
    D = []
    D.append(day[0])
    M = []
    M.append(month[0])
    for i in range(1, len(mm)):
        if i in none_index:
            nothing = 1
        elif hh[i] == hh[i-1]:
            variable_h[k] = variable_h[k] + Variable[i]
            t = t + 1
        else:
            HH.append(hh[i])
            D.append(day[i])
            M.append(month[i])
            variable_h.append(Variable[i])
            variable_h[k] = variable_h[k]/t
            t = 1
            k = k + 1
    variable_h[k] = variable_h[k] / t



    # create date/time vectors to compare
    #  ==================================================================================================================== #
    Y_check = []
    M_check = []
    D_check = []
    HH_check = []
    MM_check = []
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Year shifted
    if TimeZone <= 0:
        for i in range(-1 * TimeZone, month_days * 24):
            Y_check.append(year[0])
        for i in range(0, -1 * TimeZone):  # The last hour of the month go to the next month
            Y_check.append(year[0]+1)
    else:
        for i in range(-TimeZone, 0):
            Y_check.append(year[0]-1)
        for i in range(0, month_days * 24 - TimeZone):
            Y_check.append(year[0])
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Month shifted
    if TimeZone <= 0:
        for i in range(-1*TimeZone, month_days * 24):
            M_check.append(month[0])
        for i in range(0, -1*TimeZone): #The last hour of the month go to the next month
            if month[0] + 1 < 13:
                m = month[0] + 1
            else:
                m = 1
            M_check.append(m)
    else:
        for i in range(-TimeZone, 0):
            if month[0] > 1:
                m = month[0] - 1
            else:
                m = 12
            M_check.append(m)
        for i in range(0, month_days * 24 - TimeZone):
            M_check.append(month[0])
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Days
    if TimeZone <= 0:
        for g in range(-1 * TimeZone, 24):
            D_check.append(1)
        for i in range(2, month_days + 1):
            for g in range(0, 24):
                D_check.append(i)
        for g in range(0, -1*TimeZone):
            D_check.append(1)
    else:
        for g in range(-TimeZone, 0):
            p = month[0]
            if p == 1 or p == 2 or p == 4 or p == 6 or p == 8 or p == 9 or p == 11:
                D_check.append(31)
            elif p == 3:
                D_check.append(28)
            else:
                D_check.append(30)
        for i in range(1, month_days):
            for g in range(0, 24):
                D_check.append(i)
        for i in range(0, -TimeZone):
            D_check.append(month_days)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Hours
    if TimeZone <= 0:
        for i in range(- TimeZone, 24):
            HH_check.append(i)
        for j in range(1, month_days):
            for i in range(0, 24):
                HH_check.append(i)
        for i in range(0, - TimeZone):
            HH_check.append(i)
    else:
        for i in range(24 + TimeZone, 24):
            HH_check.append(i)
        for j in range(1, month_days):
            for i in range(0, 24):
                HH_check.append(i)
        for i in range(0, 24 + TimeZone):
            HH_check.append(i)
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Minutes
    for i in range(0, month_days * 24):
        MM_check.append(00)


    # #

    # Check where the holes are
    #  ==================================================================================================================== #
    Weather = []
    indexes = []
    k = 0
    for i in range(0, len(HH_check)):
        if k >= len(M):
            break
        elif int(M_check[i]) == int(M[k]) and int(D_check[i]) == int(D[k]) and int(HH_check[i]) == int(HH[k]):
            Weather.append(variable_h[k])
            k = k + 1
        else:
            Weather.append(99999)
            indexes.append(i)



    # If the holes are at the end of the vector (Like in HOL in February 2015)
    #  ==================================================================================================================== #
    Delta_h = len(HH_check) - len(Weather)
    threshold = len(Weather)
    for i in range(0, Delta_h):
        Weather.append(99999)
        indexes.append(i + threshold)


    groups = group_consecutives(indexes)

    max_length =0
    for i in range(0, len(groups)):
        new_max_length = len(groups[i])
        if new_max_length > max_length:
            max_length = new_max_length

    if max_length > delta_holes_threshold:
        nothing = 1
    else:
        if len(groups[0]) > 0:
            for i in range(0, len(groups)):
                ind = groups[i]
                ind_min = ind[0] - 1
                ind_max = ind[len(ind) - 1] + 1
                l_ind = len(ind)
                if ind_max > len(Weather) - 1:
                    delta_ind = 0
                else:
                    delta_ind = (Weather[ind_max] - Weather[ind_min]) / (l_ind + 1)
                for j in range(0, l_ind):
                    Weather[ind[j]] = Weather[ind[j]-1] + delta_ind


    return Weather, max_length










