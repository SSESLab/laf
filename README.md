#LAF
The Localized AMY File converter is a tool to download, modify and customize weather data for building energy simulations.
http://energysystems.mech.utah.edu/laf

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
SOFTWARE ARCHITECTURE:

The software is composed of three separate modules: the TMY3 module, the MesoWest module and the EPW module. Each module is independent and can be used individually, with no dependence on the others.

- TMY3 Module

	A Google Maps interface shows all the available stations in USA and Canada providing .epw files. The user can choose the 		preferred urban location, click on the closest station and directly download the .epw file in a location chose by the user.
	The stations shown come from a list available on http://climate.onebuilding.org. It provides coordinates and a web link to 		download the TMY3 file for each available location. CWEC files for Canadian urban areas are also included.


- MesoWest Module

	Similarly to the previous module, the user will choose the geographic coordinates to download data accordingly. The use can select 	the desired location by moving the marker on the map. On the map, the active MesoWest stations in the selected radius in the selected 	year are shown.
	The user will select a radius (5 miles by default) to scan MesoWest stations, which can be extended up to 30 miles. Clicking on 	update map, after the radius and the marker location are changed, will cause a new group of MesoWest stations to be displayed. 
	Clicking on each station, the user can inspect the name of the station, its coordinates, the corresponding Network ID and the 		available weather variables and their associated period of record.
	Multiple meteorological networks are available to download data from. With the MesoWest API it is possible to use a flag to 		specify the networks to use. Each network has specific features and can capture specific variables, but a station or network might 	be biased due to its location, sensor accuracy, sensor reliability or sensor drift. As shown by Tyndall et al., some networks are 	more reliable than others. The NWS (National Weather Service) network "consists of professional grade equipment", while the CWOP 	(Citizen Weather Observer Program) network "frequently relies on lower-grade sensors sited on residences". On top of that, it is 	not possible to know the condition of a station located in private houses; the stations's surroundings or any possible bias effects 	are not known. However, in some cases the quality of the data of CWOP is comparable to NWS data.
	CWOP stations can be highly unreliable, but they also have the advantage of being the most diffuse network in many urban areas. 	The current software was created to provide customized micro-climate urban weather data to run building energy simulations. For 	this reason, the user has the option to choose what networks to include for each selected variable. The CWOP network is available, 	along with the NWS network, RAWS (Remote Automated Weather Stations), the MW (MesoWest) network and other networks listed in the 	window accessed through the Network" button. Each network could potentially be more reliable for certain variables rather than 		others in a given location; it is up to the user to select the most appropriate list of networks for each selected variable.
	The user is cautioned to consider the possible biases of the CWOP data, as well as any bias effect of any given network}.
	Moreover, playing with the marker and the radius, it is possible to check what variables are available in each station, what 		network provides the variables and what is the correspondent period of records. The user can select the desired year accordingly.
	If more than one year is selected, the output file will contain a linear average of the data for each selected year.
	It is important to understand the implications when selecting multiple years. The TMY3 data were constructed by taking into 		account multiple years, generally 20 to 30. For each month, a representative month (among the years considered) was selected that 	had behavior representing as closely as possible the average weather behavior in the selected month over the years considered. The 	selected month, though, is not a linear average of all the variables over the selected time range. It actually corresponds to a 	particular set of data from a specific month from a specific weather station for each urban area, typically in the closest airport	.
	
	The plot reports daily average data for each day of the year. The average dry bulb temperature from the airport is smoothed out 	with respect to the TMY3 data. The latter  maintains more of the inherent temperature fluctuations since the data employed belong 	to real historical months. The averaged airport data, because of the arithmetic mean procedure, do not show the fluctuations visible 	in the TMY3 data. Even though on average the data might show the same temperature trend, in terms of subsequent building energy 	consumption, the local different temperature fluctuations could play a major role. 
	In the literature it is possible to find examples of linear averages of weather data from multiple years. Nevertheless, if the 		weather data are used to perform building energy simulations, the user is advised not to directly employ averaged data over a 		multi-year period.
	When the "Download from MesoWest" function is called, multiple iterative loops are nested in it. The first loop is over the 		selected variables. Then, for each variable, the second loop goes through each selected year. Finally, for each variable and each 	year, the third loop goes through each identified station in the radius specified by the user starting from the chosen location.
	Before executing the last loop, the MesoWest API is called to get the number of available stations (for the specific year and 		variable) and their distance from the user's location.
	
	Inside is the third loop, as shown in Fig. \ref{mw_fc}.b. The MesoWest API is called again to download the data for each station, 	each year and each variable. A full explanation of the MesoWest API is provided on their website.
	The data downloaded from MesoWest have a time step of 5 minutes and may have some missing time steps randomly distributed in a 		whole year period.
	In order to account for this, the function "5min-to-1h" is called. The function groups the data into hourly time steps, averaging 	the available 5-min data in the same hour. Subsequently, it locates where the missing time steps are and applies a linear 		interpolation to fill the gaps. If the missing data comprise more than 20 consecutive time steps, the quality of the data is 		considered to be too low and the data are not taken into account.

	At the end of the third loop, each yearly vector for each station is averaged. The data from all the considered stations are first 	interpolated linearly according to the latitude only, then according to the longitude only, and finally the two interpolated values	 are averaged. This means that the values in each station are weighted on their distance from the location chosen by the user; the 	stations closer to the chosen location influence the final interpolated value more than the further stations. It is the user's 		responsibility to consider how far from the chosen location the available stations are, and to judge their representativeness 		based on the local geography. If they are far away, the data probably will not reliably represent the weather in the selected 		location.
	If only one station is available, the data from that station is assumed to be representative of the weather in the selected 		location.

	Leaving the second loop, then, each yearly vector has been averaged over the total year-range declared by the user.
	This procedure has been repeated for each selected variable. Finally, a .csv file is output and saved in the path declared by the 	user. 
	The .csv file contains as many columns as the number of declared variables. Each column is formed by a 1 line header, reporting 	the name of the variable, and 8760 values, corresponding to the total amount of hours in a one year period.



- EPW Module

	Similarly to the previous modules, the user must indicate the location of multiple files to perform the requested task. This 		module is independent from the previous two, but the files output from those two modules can be directly employed to create a 		customized .epw file with this module.
	Initially the TMY3 file to be modified is required. Once the user selects it, they may visualize it.
	As mentioned by Bhandari et al., "The minimum weather data parameters necessary for whole building simulations accuracy are: dry 	bulb temperature; wet bulb temperature and/or relative humidity, global, direct normal and diffuse solar radiation (only two 		variables are required to represent solar radiation); wind speed and wind direction (for natural ventilation and infiltration)". 	This is confirmed by other authors as well, although sometimes the relevant variables are reduced to dry bulb temperature, relative 	humidity and wind speed or to dry bulb temperature and relative humidity only.
	The customized .epw file for a specific location in an urban area will be created starting from the TMY3 file relative to the same 	urban area. Only the columns corresponding to 6 weather variables are currently available for customization: dry bulb temperature, 	relative humidity, wind speed, wind direction, atmospheric pressure, and dew point temperature. The rest of the variables are assumed 	to be homogeneous throughout the same urban environment. 
	Although solar irradiation has been reported to be important for the accuracy of building simulations, the availability of solar 	radiation data is limited. Additionally it is reasonable to assume the distribution of incoming radiation is more likely to be 		homogeneous in the same urban area compared with, e.g., temperature. Atmospheric pressure and dew point temperature have been 		taken into account in order to respect the proper psychrometric relationships with dry bulb temperature and relative humidity.
	The TMY3 file provides solar irradiation values assuming no shading effects or reflections on the considered building by the 		surrounding urban canopy. If the user is trying to generate a site-specific weather file that would involve alteration of solar 	irradiation, it is necessary to include these effects directly in the building energy simulation software.
	For example, in EnergyPlus it is possible to create virtual surfaces around the building model in order to simulate the shading 	effect of surrounding buildings or trees.
	The header of the TMY3 file is also read by the module and can be customized by the user black to indicate the geographical 		details of the location of the new weather data.
	Next, the user is requested to input a .csv file containing the weather variables to be substituted in the original TMY3 file, and 	to indicate what each column corresponds to. 
	The .csv file will contain as many columns as the number of selected variables. Each column contains one line for the header with 	the name of the variable and 8760 values for each variable.
	After indicating the path to save the customized weather file, the user may launch the function "Print .epw file".
	This function accepts the selected TMY3 file as input, substitutes the header with the one defined by the user, substitutes the 	TMY3 columns corresponding to the variable selected by the user with the new data provided by the user, and saves the new .epw 		file in the path indicated by the user. 
	It is important to emphasize that the psychrometric relationships are preserved. Dry bulb temperature, relative humidity, dew 		point temperature and pressure are correlated in LAF, so that if any of these four variables is customized by the user, it will be 	used to calculate the corresponding non-customized psychrometric variable or variables.
	The generated file has been tested with BEM simulations and can} be used to run simulations with EnergyPlus. Using the appropriate 	converter, it is also possible to convert the created .epw file into eQUEST and DOE-2 BIN weather files. 










