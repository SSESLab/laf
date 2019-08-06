# LAF
The Localized AMY File creator is a tool to download, modify and customize weather data for building energy simulations.
http://energysystems.mech.utah.edu/laf

New! Read the paper (open access): https://doi.org/10.1016/j.softx.2019.100299


# Usage
- MAC OSX: 
	It doesn’t require any installation or any prerequisite, just download the application from the website.
	
- WINDOWS:
	It doesn’t require any installation or any prerequisite, just download the application from the website.

- SOURCE CODE:

	If you prefer to use the code though a Python compiler directly, you need:
	
			- python 3.5 or 3.6:
				You can download it directly from: http://python.org/downloads/
				
			- PyQt5:
				On MacOSX, Windows, Linux just type “pip install pyqt5”
				
			- Numpy: 
				On MacOSX and Linux just type “pip install numpy”
				On Windows download the appropriate version of “Numpy+MKL” from here:
				http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
				Then install the package as “pip install numpy….wheel” from the directory where the file was downloaded.
				
			- Scipy: 
				On MacOSX and Linux just type “pip install scipy”
				On Windows download the appropriate version of “SciPy” from here: 
				http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy
				Then install the package as “pip install scipy….wheel” from the directory where the file was downloaded.
	
	Once all the dependencies are installed, it is just necessary to run “python LAF.py” from the directory where LAF.py is.



######################################################################################
USER MANUAL:

Three modules compose LAF: TMY3 module, MesoWest module, and EPW module.


- TMY3 Module

	This modules allows the user to download all the TMY3 and CWEC files available for the US and Canada.
	The user chan select a location and directly download the correspondent weather file.
	The available stations are retrieved from http://climate.onebuilding.org.


- MesoWest Module

	This modules allow the user to download data from the MesoWest database. It provides weather data from more than 9000 weather 		stations in thr US.
	The user is again asked to choose a location using Google Maps. The user can select a radius and a year. The stations from the 		MesoWest database will be shown on the map accordingly.
	The radius is 5 miles by default and can be extended up to 30 miles.
	The user can update the stations to be shown on the map clicking on "update map".
	
	Clicking on each station, the user can check out the details of the selcted stations. Specifically, the user can check the 		coordinates, the station network ID, the available weather variables measured in the selected station and the corresponding period 	of record.
	Multiple meteorological networks are available to retrieve data. The user can select some networks, to be chosen in the list 		associated with the button "Networks". If no network ID is selected next to each variable, all networks are selected.
	Each network can have pros and cons, it can be biased on some variables and reliable on some others. The user is supposed to 		select the networks responsibly. 
	
	Clicking on "Download from MesoWest", the data from MesoWest are downloaded and processed.
	The data are separately dowloaded for each month in the selected year, for each month, for each available station in the selected 	radius. The values for the selected variable from each available station are averaged to calculated the value of the selected 		variable in the pin position selected by the user. A weighted average is applied: the closer a station is to the location selected 	by the user, the more the value from that locaton will influence the final value.
	If one station only is available, the data from that station will be used for the location selected by the user.

	The data downloaded from MesoWest have a timestep of 5 minutes and my contain some missing steps. for this reason the data are 		proceesed before being averaged. They are transformed from 5-min timesteps to 1h-timesteps, averaging the data in 1h periods. If 	whole 1h-timestep chunck of data are missing, they are filled with a linear interpolation between the previous and the next data 	timestep. If more than 20 consecutive tiestep are missing, the quality of the data is considered too low and no data are 		downloaded.

	The data are therefore saved in a location decided by the user. They are in .csv format and contain 8761 rows: 1 row contains the 	title of the column and 8760 rows contain the data for all the hours of the year.
	
	
- EPW Module

	This module is indipendent from the previous 2 modules, but the data downloaded from the previous modules can be directly employed 	here.
	A TMY3 file is requested to be input and can be therefore visualized. Of course, the TMY3 file to be selected is supposed to be 	the one relative  
	Then, the user can customize the header of the future output EPW file.

	The user is therefore requested to select the .csv file that contains the weather variables to be customized in the TMY3 file.
	6 variables are available to be customized in the TMY3 file: dry bulb temperature, relative humidity, wind speed, wind direction, 	atmospheric pressure, and dew point temperature. The other variables in the TMY3 file are assumed to be homogeneous over the same 	city.
	Dry bulb temperature, dew point temperature and atmospheric pressure are either provided by the user or calculated by this module 	in order to respect psychrometric relationships.
	The selected .csv file is supposed to contain only 1 line for the header, as for the files putput by the previous module.

	The user can therefore print the customized EPW file and save it in the chosen location.
	The generated files have been tested with EnergyPlus simulations. They can be converted with the apposite tool in order to be used 	for eQUEST simulations.


