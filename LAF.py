#
import datetime
import math
import time
from psychropy import *
import urllib
#
from PyQt5 import QtWebChannel
from PyQt5.QtWidgets import *
#
from GUI_about import *
from GUI_custom_page import *
from GUI_latlonpage import *
from GUI_mainPage import *
from GUI_Networks import *
from GUI_tmy3 import *
from GUI_mw_api_gui import *
from GUI_ack import *
from GUI_license import *
#
from Locations import *
from mw_stations_list import *



# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Global Variables
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
global lat, long, DS, City, State, Country, elev, wmosn, comm1, tz, refy, lat_mw, long_mw, lat_tmy3, long_tmy3
lat = '0'
long = '0'
DS = '-Not Set-'
City = '-Not Set-'
State = '-Not Set-'
Country = 'USA'
elev = '0'
wmosn = '0'
comm1 = '-'
tz = '0'
lat_mw = 40.767367
long_mw = -111.848007
lat_tmy3 = 40.767367
long_tmy3 = -111.848007


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Text2Vector
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def t2v(text):
    line = []
    i = 0
    while i < len(text):
        if text[i].isdigit():
            numb = 0
            while text[i].isdigit():
                numb = numb * 10 + int(text[i])
                i = i + 1
                if i > len(text) - 1:
                    break
            line.append(numb)
        else:
            i = i + 1
    return line


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Read TMY3 file
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def read_tmy3(tmy3_name):
    if len(tmy3_name) is 0:
        nothing = 1
    else:
        ############################
        # Read TMY3 header
        ############################
        f = open(tmy3_name)
        global header
        header = []
        for i in range(0, 8):
            line = f.readline()
            header.append(line)
        f.close()

        f2 = open(tmy3_name, 'rt')
        first_line = next(csv.reader(f2))
        for i in range(0, 4):
            next(csv.reader(f2))
        comm_line = next(csv.reader(f2))
        f2.close()
        #
        global lat, long, DS, City, State, Country, elev, wmosn, comm1, tz, refy
        lat = first_line[6]
        long = first_line[7]
        DS = 'LAF'
        City = first_line[1]
        State = first_line[2]
        Country = first_line[3]
        elev = first_line[9]
        wmosn = first_line[5]
        comm1 = comm_line[1]
        tz = first_line[8]
        ############################
        # Read TMY3 data
        ############################
        data = read_datafile(tmy3_name, 8)
        global Y, M, D, HH, MM, Tdb, Tdew, RH, Patm, ExHorRad, ExDirNormRad, HorIR, GHRad, DNRad, DHRad, GHIll, DNIll, DHIll
        global HorIR, GHRad, GHIll, DNIll, DHIll, ZenLum, Wdir, Wspeed, TotSkyCover, OpSkyCover, Visib, CeilH, PrecWater
        global AerOptDepth, SnowDepth, DSLS, Albedo, LiqPrecDepth, LiqPrecQuant

        Y = data[:, 0]
        M = data[:, 1]
        D = data[:, 2]
        HH = data[:, 3]
        MM = data[:, 4]
        Tdb = data[:, 6]
        Tdew = data[:, 7]
        RH = data[:, 8]
        Patm = data[:, 9]
        ExHorRad = data[:, 10]
        ExDirNormRad = data[:, 11]
        HorIR = data[:, 12]
        GHRad = data[:, 13]
        DNRad = data[:, 14]
        DHRad = data[:, 15]
        GHIll = data[:, 16]
        DNIll = data[:, 17]
        DHIll = data[:, 18]
        ZenLum = data[:, 19]
        Wdir = data[:, 20]
        Wspeed = data[:, 21]
        TotSkyCover = data[:, 22]
        OpSkyCover = data[:, 23]
        Visib = data[:, 24]
        CeilH = data[:, 25]
        PresWeathObs = data[:, 26]
        PresWeathCodes = data[:, 27]
        PrecWater = data[:, 28]
        AerOptDepth = data[:, 29]
        SnowDepth = data[:, 30]
        DSLS = data[:, 31]
        Albedo = data[:, 32]
        LiqPrecDepth = data[:, 33]
        LiqPrecQuant = data[:, 34]
        ############################
        # Date/Time vector
        ############################
        global DateTime
        DateTime = []
        for i in range(0, 8760):
            dt = str(int(Y[i])) + '/' + str(int(M[i])) + '/' + str(int(D[i])) + ' - ' + str(int(HH[i])) + ':' + str(int(MM[i])) + ':00'
            DateTime.append(dt)
        ############################
        return 0
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Read CSV file
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def read_csv(csv_name, var):
    ############################
    # CSV file reading
    ############################
    # Cases:
    # 0)  Tdb + Tdew + RH = 0
    # 1)  Tdb + Tdew = RH
    # 2)  Tdb + RH = Tdew
    # 3)  Tdew + RH = Tdb
    # 4)  Tdb ---RHtmy3--> Tdew
    # 5)  RH ---Tdbtmy3--> Tdew
    # 6)  Tdew ---Tdbtmy3--> RH

    #
    data2 = read_datafile(csv_name, 1)
    # try:
    #     data2 = read_datafile(csv_name, 1)
    # except (TypeError, ValueError):
    #     QMessageBox.warning(None, 'Wrong Format', "Check out the CSV file you input, there is something wrong with it.")


    global Tdb, Tdew, RH, Patm, Wdir, Wspeed
    #
    try:
        numb_columns = len(data2[0, :])
    except (IndexError):
        numb_columns = 1
    else:
        nothing = 1

    if len(var) > numb_columns:
        flag_columns = 33
    # CASE 0
    elif 2 and 3 and 4 in var:
        flag_columns = 0
        if len(var) > 1:
            for i in range(0, len(var)):
                if var[i] == 1:
                    Patm = data2[:,i]
                elif var[i] == 2:
                    RH = data2[:,i]
                elif var[i] == 3:
                    Tdew = data2[:,i]
                elif var[i] == 4:
                    Tdb = data2[:,i]
                elif var[i] == 5:
                    Wspeed = data2[:,i]
                elif var[i] == 6:
                    Wdir = data2[:,i]
        else:
            if var[0] == 1:
                Patm = data2
            elif var[0] == 2:
                RH = data2
            elif var[0] == 3:
                Tdew = data2
            elif var[0] == 4:
                Tdb = data2
            elif var[0] == 5:
                Wspeed = data2
            elif var[0] == 6:
                Wdir = data2
    # CASE 1
    elif 3 and 4 in var:
        flag_columns = 0
        if len(var) > 1:
            for i in range(0, len(var)):
                if var[i] == 1:
                    Patm = data2[:, i]
                elif var[i] == 2:
                    RH = data2[:, i]
                elif var[i] == 3:
                    Tdew = data2[:, i]
                elif var[i] == 4:
                    Tdb = data2[:, i]
                elif var[i] == 5:
                    Wspeed = data2[:, i]
                elif var[i] == 6:
                    Wdir = data2[:, i]
        else:
            if var[0] == 1:
                Patm = data2
            elif var[0] == 2:
                RH = data2
            elif var[0] == 3:
                Tdew = data2
            elif var[0] == 4:
                Tdb = data2
            elif var[0] == 5:
                Wspeed = data2
            elif var[0] == 6:
                Wdir = data2
        for i in range(0, 8760):
            RH[i] = (psych(Patm[i], 'Tdb', Tdb[i], 'DP', Tdew[i], 'RH', 'SI'))*100
    # CASE 2
    elif 2 and 4 in var:
        flag_columns = 0
        if len(var) > 1:
            for i in range(0, len(var)):
                if var[i] == 1:
                    Patm = data2[:, i]
                elif var[i] == 2:
                    RH = data2[:, i]
                elif var[i] == 3:
                    Tdew = data2[:, i]
                elif var[i] == 4:
                    Tdb = data2[:, i]
                elif var[i] == 5:
                    Wspeed = data2[:, i]
                elif var[i] == 6:
                    Wdir = data2[:, i]
        else:
            if var[0] == 1:
                Patm = data2
            elif var[0] == 2:
                RH = data2
            elif var[0] == 3:
                Tdew = data2
            elif var[0] == 4:
                Tdb = data2
            elif var[0] == 5:
                Wspeed = data2
            elif var[0] == 6:
                Wdir = data2
        for i in range(0, 8760):
            Tdew[i] = psych(Patm[i], 'Tdb', Tdb[i], 'RH', RH[i] / 100, 'DP', 'SI')
    # CASE 3
    elif 2 and 3 in var:
        flag_columns = 0
        if len(var) > 1:
            for i in range(0, len(var)):
                if var[i] == 1:
                    Patm = data2[:, i]
                elif var[i] == 2:
                    RH = data2[:, i]
                elif var[i] == 3:
                    Tdew = data2[:, i]
                elif var[i] == 4:
                    Tdb = data2[:, i]
                elif var[i] == 5:
                    Wspeed = data2[:, i]
                elif var[i] == 6:
                    Wdir = data2[:, i]
        else:
            if var[0] == 1:
                Patm = data2
            elif var[0] == 2:
                RH = data2
            elif var[0] == 3:
                Tdew = data2
            elif var[0] == 4:
                Tdb = data2
            elif var[0] == 5:
                Wspeed = data2
            elif var[0] == 6:
                Wdir = data2
        for i in range(0, 8760):
            Tdb[i] = psych(Patm[i], 'DP', Tdew[i], 'RH', RH[i] / 100, 'DP', 'SI')
    # CASE 4
    elif 4 in var:
        flag_columns = 0
        if len(var) > 1:
            for i in range(0, len(var)):
                if var[i] == 1:
                    Patm = data2[:, i]
                elif var[i] == 2:
                    RH = data2[:, i]
                elif var[i] == 3:
                    Tdew = data2[:, i]
                elif var[i] == 4:
                    Tdb = data2[:, i]
                elif var[i] == 5:
                    Wspeed = data2[:, i]
                elif var[i] == 6:
                    Wdir = data2[:, i]
        else:
            if var[0] == 1:
                Patm = data2
            elif var[0] == 2:
                RH = data2
            elif var[0] == 3:
                Tdew = data2
            elif var[0] == 4:
                Tdb = data2
            elif var[0] == 5:
                Wspeed = data2
            elif var[0] == 6:
                Wdir = data2
        for i in range(0, 8760):
            Tdew[i] = psych(Patm[i], 'Tdb', Tdb[i], 'RH', RH[i] / 100, 'DP', 'SI')
    # CASE 5
    elif 2 in var:
        flag_columns = 0
        if len(var) > 1:
            for i in range(0, len(var)):
                if var[i] == 1:
                    Patm = data2[:, i]
                elif var[i] == 2:
                    RH = data2[:, i]
                elif var[i] == 3:
                    Tdew = data2[:, i]
                elif var[i] == 4:
                    Tdb = data2[:, i]
                elif var[i] == 5:
                    Wspeed = data2[:, i]
                elif var[i] == 6:
                    Wdir = data2[:, i]
        else:
            if var[0] == 1:
                Patm = data2
            elif var[0] == 2:
                RH = data2
            elif var[0] == 3:
                Tdew = data2
            elif var[0] == 4:
                Tdb = data2
            elif var[0] == 5:
                Wspeed = data2
            elif var[0] == 6:
                Wdir = data2
        for i in range(0, 8760):
            Tdew[i] = psych(Patm[i], 'Tdb', Tdb[i], 'RH', RH[i] / 100, 'DP', 'SI')
    # CASE 6
    elif 3 in var:
        flag_columns = 0
        if len(var) > 1:
            for i in range(0, len(var)):
                if var[i] == 1:
                    Patm = data2[:, i]
                elif var[i] == 2:
                    RH = data2[:, i]
                elif var[i] == 3:
                    Tdew = data2[:, i]
                elif var[i] == 4:
                    Tdb = data2[:, i]
                elif var[i] == 5:
                    Wspeed = data2[:, i]
                elif var[i] == 6:
                    Wdir = data2[:, i]
        else:
            if var[0] == 1:
                Patm = data2
            elif var[0] == 2:
                RH = data2
            elif var[0] == 3:
                Tdew = data2
            elif var[0] == 4:
                Tdb = data2
            elif var[0] == 5:
                Wspeed = data2
            elif var[0] == 6:
                Wdir = data2
        for i in range(0, 8760):
            RH[i] = (psych(Patm[i], 'Tdb', Tdb[i], 'DP', Tdew[i], 'RH', 'SI'))*100

    return flag_columns

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Write new EPW file
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def write_epw(save_path):
    OPFILE = save_path + '.epw'
    ofile = open(OPFILE, "w", newline='')
    line1 = 'LOCATION,' + City + ',' + State + ',' + Country + ',customized weather file,' + str(wmosn) + ',' +\
            str(lat) + ',' + str(long) + ',' + str(tz) + ',' + str(elev) + '\n'
    ofile.write(line1)
    ofile.write(header[1])
    ofile.write(header[2])
    ofile.write(header[3])
    ofile.write(header[4])
    ofile.write('COMMENTS 1,' + str(comm1) + '\n')
    ofile.write(header[6])
    ofile.write('DATA PERIODS,1,1,Data,Sunday, 1/ 1,12/31\n')
    #
    writer = csv.writer(ofile, delimiter=',')
    #
    for i in range(0, 8760):
        row = [int(Y[i]), int(M[i]), int(D[i]), int(HH[i]), int(MM[i]), DS, Tdb[i], Tdew[i], RH[i], Patm[i],
               ExHorRad[i],
               ExDirNormRad[i], HorIR[i], GHRad[i], DNRad[i], DHRad[i], GHIll[i], DNIll[i], DHIll[i], HorIR[i],
               GHRad[i],
               GHIll[i], DNIll[i], DHIll[i], ZenLum[i], Wdir[i], Wspeed[i], TotSkyCover[i], OpSkyCover[i],
               Visib[i],
               CeilH[i],
               PrecWater[i], AerOptDepth[i], SnowDepth[i], DSLS[i], Albedo[i], LiqPrecDepth[i], LiqPrecQuant[i]]
        writer.writerow(row)
    ofile.close()
    return 0
#
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Read TMY3 file 2
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def tmy3_reader_select(tmy3_name, csv_name, var, save_path):
    OPFILE = save_path
    ############################
    # Read TMY3 header
    ############################
    f = open(tmy3_name)
    header = []
    for i in range(0, 8):
        line = f.readline()
        header.append(line)
    f.close()
    ############################
    # Read TMY3 data
    ############################
    data = read_datafile(tmy3_name, 8)
    # #
    global Y, M, D, HH, MM, Tdb, Tdew, RH, Patm, ExHorRad, ExDirNormRad, HorIR, GHRad, DNRad, DHRad, GHIll, DNIll, DHIll
    global HorIR, GHRad, GHIll, DNIll, DHIll, ZenLum, Wdir, Wspeed, TotSkyCover, OpSkyCover, Visib, CeilH, PrecWater
    global AerOptDepth, SnowDepth, DSLS, Albedo, LiqPrecDepth, LiqPrecQuant

    Y = data[:, 0]
    M = data[:, 1]
    D = data[:, 2]
    HH = data[:, 3]
    MM = data[:, 4]
    Tdb = data[:, 6]
    Tdew = data[:, 7]
    RH = data[:, 8]
    Patm = data[:, 9]
    ExHorRad = data[:, 10]
    ExDirNormRad = data[:, 11]
    HorIR = data[:, 12]
    GHRad = data[:, 13]
    DNRad = data[:, 14]
    DHRad = data[:, 15]
    GHIll = data[:, 16]
    DNIll = data[:, 17]
    DHIll = data[:, 18]
    ZenLum = data[:, 19]
    Wdir = data[:, 20]
    Wspeed = data[:, 21]
    TotSkyCover = data[:, 22]
    OpSkyCover = data[:, 23]
    Visib = data[:, 24]
    CeilH = data[:, 25]
    PresWeathObs = data[:, 26]
    PresWeathCodes = data[:, 27]
    PrecWater = data[:, 28]
    AerOptDepth = data[:, 29]
    SnowDepth = data[:, 30]
    DSLS = data[:, 31]
    Albedo = data[:, 32]
    LiqPrecDepth = data[:, 33]
    LiqPrecQuant = data[:, 34]
    ############################
    # CSV file reading
    ############################
    data2 = read_datafile(csv_name, 1)
    #
    flag = 0
    for i in range(0, len(var)-1):
        if var == 1:
            Patm = data2[:, i]
        elif var[i] == 2:
            RH = data2[:, i]
        elif var[i] == 3:
            Tdew = data2[:, i]
        elif var[i] == 4:
            Tdb = data2[:, i]
        elif var[i] == 5:
            Wspeed = data2[:, i]
        elif var[i] == 6:
            Wdir = data2[:, i]
    ############################
    # Date/Time vector
    ############################
    global DateTime
    DateTime = []
    for i in range(0, 8760):
        dt = str(int(Y[i])) + '/' + str(int(M[i])) + '/' + str(int(D[i])) + ' - ' + str(int(HH[i])) + ':' + str(int(MM[i])) + ':00'
        DateTime.append(dt)
    ############################
    ofile = open(OPFILE, "w")
    line1 = 'LOCATION,' + City + ',' + State + ',' + Country + ',customized weather file,' + str(wmosn) + ',' +\
            str(lat) + ',' + str(long) + ',' + str(tz) + ',' + str(elev) + '\n'
    ofile.write(line1)
    ofile.write(header[1])
    ofile.write(header[2])
    ofile.write(header[3])
    ofile.write(header[4])
    ofile.write('COMMENTS 1,' + str(comm1) + '\n')
    ofile.write(header[6])
    ofile.write('DATA PERIODS,1,1,Data,Sunday, 1/ 1,12/31\n')
    #
    writer = csv.writer(ofile, delimiter=',')
    #
    for i in range(0, 8760):
        row = [int(Y[i]), int(M[i]), int(D[i]), int(HH[i]), int(MM[i]), DS, Tdb[i], Tdew[i], RH[i], Patm[i],
               ExHorRad[i],
               ExDirNormRad[i], HorIR[i], GHRad[i], DNRad[i], DHRad[i], GHIll[i], DNIll[i], DHIll[i], HorIR[i],
               GHRad[i],
               GHIll[i], DNIll[i], DHIll[i], ZenLum[i], Wdir[i], Wspeed[i], TotSkyCover[i], OpSkyCover[i],
               Visib[i],
               CeilH[i],
               PrecWater[i], AerOptDepth[i], SnowDepth[i], DSLS[i], Albedo[i], LiqPrecDepth[i], LiqPrecQuant[i]]
        writer.writerow(row)
    ofile.close()
    return 0
#
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Read file
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def read_datafile(file_name, skiplines):
    data = numpy.genfromtxt(file_name, delimiter=',', skip_header=skiplines)
    return data
#

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Main Page
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class MainPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mainpage = Ui_mainpage()  # The name of my top level object is MainWindow
        self.mainpage.setupUi(self)
        self.mainpage.custom_button.clicked.connect(self.open_custom)
        self.mainpage.mesowest.clicked.connect(self.open_mesowest)
        self.mainpage.About_label.mousePressEvent = self.open_about
        self.mainpage.tmy3_button.clicked.connect(self.open_tmy3)

    def open_custom(self):
        self.custom = CustomEPW()
        self.custom.show()

    def open_tmy3(self):
        try:
            urllib.request.urlopen('http://google.com')
            self.tmy3page = tmy3_page()
            self.tmy3page.show()
        except:
            QMessageBox.warning(self, 'No Internet connection',
                                "Check your Internet connection!\nI need to access the web to show you the TMY3 locations.")


    def open_mesowest(self):
        try:
            urllib.request.urlopen('http://google.com')
            self.mw = MW_Download()
            self.mw.show()
        except:
            QMessageBox.warning(self, 'No Internet connection',
                                "Check your Internet connection!\nI need to access the web to show you the MesoWest locations.")

    def open_about(self, event):
        self.about_page = About()
        self.about_page.show()

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# TMY3 - MAP
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def _downloadRequested(item):  # QWebEngineDownloadItem
    # self.license_page.textBrowser.setOpenExternalLinks(True)
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    #
    global pathsave_custom
    pathsave_custom = QFileDialog.getSaveFileName(None, "Select destination folder and file name", "", "Zip file (*.zip)",
                                          options=options)[0]
    print('downloading to', item.path())
    item.setPath(pathsave_custom + '.zip')
    print('downloading to', item.path())
    print(item)
    print(type(item))
    item.accept()
    save_path = item.path()

class tmy3_page(QMainWindow):
    def __init__(self):
        super().__init__()
        self.map_tmy3 = Ui_tmy3page()
        self.map_tmy3.setupUi(self)
        self.map_tmy3.html_code.loadFinished.connect(self.onLoad)
        self.map_tmy3.html_code.setHtml('''
               <!DOCTYPE html>
        <html>
        <head>
        <meta name="viewport" content="initial-scale=1.0, user-scalable=yes" />
        <style type="text/css">
          html { height: 100% }
          body { height: 100%; margin: 0px; padding: 0px }
          #map_canvas { height: 100% }
        </style>
        <script type="text/javascript"
          src="http://maps.google.com/maps/api/js?sensor=false">
        </script>
        <script type="text/javascript">
        var map;
        function initialize() {
            var latlng = new google.maps.LatLng(40.767367, -111.848007);
            var myOptions = {
                            zoom: 8,
                            center: latlng,
                            mapTypeId: google.maps.MapTypeId.ROADMAP
                            };
             map = new google.maps.Map(document.getElementById("map_canvas"),
                                       myOptions);
         }

        function addMarker(lat, lon, city, url) {
            var newmarker = new google.maps.Marker({
                position: new google.maps.LatLng(lat, lon),
                map: map,
                title: city
            });

            newmarker['infowindow'] = new google.maps.InfoWindow({
                    content: url
                });

            google.maps.event.addListener(newmarker, 'click', function() {
                this['infowindow'].open(map, this);
            });
        }

        </script>
        </head>
        <body onload="initialize();">
            <div id="map_canvas" style="width:100%; height:100%"></div>
        </body>
        </html>
        ''')
        self.map_tmy3.html_code.page().profile().downloadRequested.connect(_downloadRequested)

    def onLoad(self):
        QtCore.QTimer.singleShot(1000, self.save_fun)

    def save_fun(self):
        state = locations_col(1)
        cities = locations_col(2)
        type = locations_col(3)
        latitudes = locations_col(4)
        longitudes = locations_col(5)
        links = locations_col(6)
        names = []
        address = []
        for i in range(0, len(state)):
            names.append(cities[i] + ",  " + state[i])
            print(links[i])
            address.append('<div id="content">' +
                           '<div id="siteNotice">' +
                           '</div>' +
                           '<h1 id="firstHeading" class="firstHeading">' + names[i] + '</h1>' +
                           '<div id="bodyContent">' +
                           '<p> Type: ' + type[i] + '</p>' +
                           '<p> Latitude: ' + str(latitudes[i]) + '</p>' +
                           '<p> Longitude: ' + str(longitudes[i]) + '</p>' +
                           '<p><a href="' + links[i] + '">' +
                           'Download</a> ' +
                           '.</p>' +
                           '</div>' +
                           '</div>')
            argument = "addMarker(" + str(latitudes[i]) + "," + str(longitudes[i]) + ",'" + names[i] + "','" + \
                       address[i] + "')"
            self.map_tmy3.html_code.page().runJavaScript(argument)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# MesoWest
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class MW_Download(QMainWindow):
    def __init__(self):
        super().__init__()
        global year_start
        year_start = 2015
        self.latitude_marker = 40.767367
        self.longitude_marker = -111.848007
        self.radius = 5
        self.mwapi = Ui_mw_page()  # The name of my top level object is MainWindow
        self.mwapi.setupUi(self)
        channel = QtWebChannel.QWebChannel(self.mwapi.html_code.page())
        self.mwapi.html_code.page().setWebChannel(channel)
        channel.registerObject("jshelper", self)
        self.mwapi.html_code.setHtml('''

<html>
<head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=yes"/>
    <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
    <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
    <!--<script type="text/javascript" src="useless.js"></script>-->
    <script type="text/javascript">




        var jshelper;

new QWebChannel(qt.webChannelTransport, function (channel) {
    jshelper = channel.objects.jshelper;
});


function geocodePosition(pos) {
    geocoder.geocode({
        latLng: pos
    }, function (responses) {
        if (responses && responses.length > 0) {
            updateMarkerAddress(responses[0].formatted_address);
        } else {
            updateMarkerAddress('Cannot determine address at this location.');
        }
    });
}


function updateMarkerStatus(str) {
    document.getElementById('markerStatus').innerHTML = str;
}

function updateMarkerPosition(latLng) {
    document.getElementById('info').innerHTML = [
        latLng.lat(),
        latLng.lng()
    ].join(', ');
}


function updateMarkerAddress(str) {
    document.getElementById('address').innerHTML = str;
}


var geocoder = new google.maps.Geocoder();
var map;


var goldStar = {
    path: 'M 125,5 155,90 245,90 175,145 200,230 125,180 50,230 75,145 5,90 95,90 z',
    fillColor: 'yellow',
    fillOpacity: 0.8,
    scale: 0.1,
    strokeColor: 'gold',
    strokeWeight: 1
};


function addMarker(lat, lon, city, url) {
    var newmarker = new google.maps.Marker({
        position: new google.maps.LatLng(lat, lon),
        icon: goldStar,
        map: map,
        title: city
    });
    newmarker['infowindow'] = new google.maps.InfoWindow({
        content: url
    });
    google.maps.event.addListener(newmarker, 'click', function () {
        this['infowindow'].open(map, this);
    });
}


function initialize(lat_init, long_init) {
    var latLng = new google.maps.LatLng(lat_init, long_init);
// function initialize() {
//     var latLng = new google.maps.LatLng(40.767367, -111.848007);
    // create as a global variable
    map = new google.maps.Map(document.getElementById('mapCanvas'), {
        zoom: 11,
        center: latLng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    });
    var marker = new google.maps.Marker({
        position: latLng,
        title: 'Point A',
        map: map,
        draggable: true
    });

    // Update current position info.
    updateMarkerPosition(latLng);
    geocodePosition(latLng);

    // Add dragging event listeners.
    google.maps.event.addListener(marker, 'dragstart', function () {
        updateMarkerAddress('Dragging...');
    });

    google.maps.event.addListener(marker, 'drag', function () {
        updateMarkerStatus('Dragging...');
        updateMarkerPosition(marker.getPosition());
        jshelper.markerMoved(marker.position.lat(), marker.position.lng());
    });

    google.maps.event.addListener(marker, 'dragend', function () {
        updateMarkerStatus('Drag ended');
        geocodePosition(marker.getPosition());
    });

//  return latLng
}


// Onload handler to fire off the app.
// google.maps.event.addDomListener(window, 'load', initialize);


    </script>


</head>
<body>
<style>
    #mapCanvas {
        width: 102%;
        height: 102%;
        float: left;
        /*margin-left: -7px;*/
        /*margin-right: -10px;*/
        /*margin-top: -7px;*/
        /*margin-bottom: -10px;*/
    }
    /*#infoPanel {*/
        /*float: left;*/
        /*margin-left: 20px;*/
    /*}*/
    /*#infoPanel div {*/
        /*margin-bottom: 10px;*/
    /*}*/
</style>

<span style="font-size: small; color: black; font-family: verdana; "></span>
<div id="mapCanvas"></div>
<div id="infoPanel">
    <span style="font-size: small; color: black; font-family: verdana; "></span>
    <!-- <b>Marker status:</b> -->
    <div id="markerStatus"><i>Click and drag the marker.</i></div>
    <!--<span style="font-size: small; color: black; font-family: verdana; "></span>-->
    <!--<b>Current position:</b>-->
    <div id="info"></div>
    <!--<b>Closest matching address:</b>-->
    <!--<div id="address"></div>-->
</div>
</body>
</html>






        ''')

        self.mwapi.rad_scan.valueChanged[str].connect(self.rad_fun)
        self.mwapi.html_code.loadFinished.connect(self.onLoad)
        self.mwapi.update_map.clicked.connect(self.add_stars)
        self.mwapi.html_code.page().profile().downloadRequested.connect(_downloadRequested)
        self.mwapi.year_mw.valueChanged[str].connect(self.y_start)
        self.mwapi.year_mw_2.valueChanged[str].connect(self.y_end)
        self.mwapi.download_button.clicked.connect(self.download_mw)
        self.mwapi.networks.clicked.connect(self.nw_info)

    @QtCore.pyqtSlot(float, float)
    def markerMoved(self, lat_marker, lng_marker):
        global latitude_marker, longitude_marker
        self.latitude_marker = lat_marker
        self.longitude_marker = lng_marker
        self.mwapi.le_lat.setText(str(self.latitude_marker))
        self.mwapi.le_long.setText(str(self.longitude_marker))
        print(self.latitude_marker)
        print(self.longitude_marker)

    def rad_fun(self, text):
        global rad_mw
        self.radius = float(text)
        rad_mw = self.radius
        print(rad_mw)
        if rad_mw > 10:
            Area_rad_mw = math.pi * rad_mw ** 2
            message_rad = 'Be aware you are scanning an area of ' + str(
                float("{0:.2f}".format(Area_rad_mw))) + ' squared miles, you may want to reduce the radius'
            QMessageBox.warning(None, 'Large Radius', message_rad)


    def nw_info(self):
        self.nw_class = NW()
        self.nw_class.show()

    def onLoad(self):
        QtCore.QTimer.singleShot(1000, self.add_stars)

    def add_stars(self):
        print(self.latitude_marker, self.latitude_marker)
        argument_init = "initialize('" + str(self.latitude_marker) + "','" + str(self.longitude_marker) + "')"
        self.mwapi.html_code.page().runJavaScript(argument_init)
        date1 = year_start * 100000000 + 1 * 1000000 + 1 * 10000
        date2 = year_start * 100000000 + 1 * 1000000 + 2 * 10000 + 100
        names = []
        address = []
        [lat_station, long_station, name_st, distance, network, POR, SensVars] = show_mw_stats(self.latitude_marker, self.longitude_marker, self.radius, str(date1), str(date2))
        if not long_station:
            nothing = 1
        else:
            for i in range(0, len(long_station)):
                address.append('<div id="content">' +
                               '<div id="siteNotice">' +
                               '</div>' +
                               '<h1 id="firstHeading" class="firstHeading">' + name_st[i] + '</h1>' +
                               '<div id="bodyContent">' +
                               '<p> Latitude: ' + str(lat_station[i]) + '</p>' +
                               '<p> Longitude: ' + str(long_station[i]) + '</p>' +
                               '<p> Distance from marker: ' + str(distance[i]) + ' miles</p>' +
                               '<p> Network ID: ' + str(network[i]) + '</p>' +
                               '<p> Period of Record -> ' + str(POR[i]) + '</p>' +
                               '<p> Sensor Variables: ' + str(SensVars[i]) + '</p>' +
                               '</div>' +
                               '</div>')
                argument = "addMarker(" + str(lat_station[i]) + "," + str(long_station[i]) + ",'" + name_st[i] + "','" + \
                           address[i] + "')"
                self.mwapi.html_code.page().runJavaScript(argument)


    def y_start(self, text):
        global year_start
        year_start = int(text)

    def y_end(self, text):
        global year_end
        year_end = int(text)

    def path_fun(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        #
        global path_mw
        path_mw = QFileDialog.getSaveFileName(self, "Select destination folder and file name", "", "CSV files (*.csv)", options=options)[0]

    def Date(self):
        now = datetime.datetime.now()
        ThisYear = int(now.year)
        if 'year_start' in globals():
            nothing = 1
        else:
            global year_start
            year_start = 2015
        if 'year_end' in globals():
            nothing = 1
        else:
            global year_end
            year_end = 2015
        Delta = ThisYear - int(year_end)
        if Delta > 0:
            if year_start > year_end:
                QMessageBox.warning(self, 'Wrong Year', "Wait, we can't go back in time yet yet!\n Correct the years to simulate")
            else:
                self.flag_date = 3
        else:
            QMessageBox.warning(self, 'Wrong Year', "Wait, we can't forecast the future yet!\n Chose another year")

    def check_fun(self, inp):
        if inp == "Atmospheric pressure [Pa]":
            return 1
        elif inp == "Relative humidity [%]":
            return 2
        elif inp == "Dewpoint Temperature [°C]":
            return 3
        elif inp == "Dry Bulb Temperature [°C]":
            return 4
        elif inp == "Wind speed [m/s]":
            return 5
        elif inp == "Wind Direction [Deg]":
            return 6
        else:
            return 99

    def variable_list(self):
        variables_mw = []
        list_nw = []
        check_nw = 0
        if self.mwapi.checkBox1.isChecked():
            variables_mw.append(self.check_fun(self.mwapi.option1.currentText()))
            netw1 = t2v(self.mwapi.lineEdit_1.text())
            list_nw.append(netw1)
            if not netw1:
                check_nw = 1
        if self.mwapi.checkBox2.isChecked():
            variables_mw.append(self.check_fun(self.mwapi.option2.currentText()))
            netw2 = t2v(self.mwapi.lineEdit_2.text())
            list_nw.append(netw2)
            if not netw2:
                check_nw = 1
        if self.mwapi.checkBox3.isChecked():
            variables_mw.append(self.check_fun(self.mwapi.option3.currentText()))
            netw3 = t2v(self.mwapi.lineEdit_3.text())
            list_nw.append(netw3)
            if not netw3:
                check_nw = 1
        if self.mwapi.checkBox4.isChecked():
            variables_mw.append(self.check_fun(self.mwapi.option4.currentText()))
            netw4 = t2v(self.mwapi.lineEdit_4.text())
            list_nw.append(netw4)
            if not netw4:
                check_nw = 1
        if self.mwapi.checkBox5.isChecked():
            variables_mw.append(self.check_fun(self.mwapi.option5.currentText()))
            netw5 = t2v(self.mwapi.lineEdit_5.text())
            list_nw.append(netw5)
            if not netw5:
                check_nw = 1
        if self.mwapi.checkBox6.isChecked():
            variables_mw.append(self.check_fun(self.mwapi.option6.currentText()))
            netw6 = t2v(self.mwapi.lineEdit_6.text())
            list_nw.append(netw6)
            if not netw6:
                check_nw = 1
        return variables_mw, list_nw, check_nw

    def download_mw(self):
        t = time.time()
        #
        [variables_mw, list_nw, check_nw] = self.variable_list()
        #
        print('list_nw')
        print(list_nw)
        print('variables_mw')
        print(variables_mw)
        #
        self.flag_date = 0
        self.Date()
        if 99 in variables_mw:
            QMessageBox.warning(self, 'No Variable Selected', "One or more columns have been selected but no variable has been chosen")
        else:
            if self.flag_date == 3:
                if 'rad_mw' in globals():
                    nothing = 1
                else:
                    global rad_mw
                    rad_mw = 5
                years_data_empty = 0
                global variable_flag, nw
                TotalYearlyVariables = []
                variable_names = []
                for i in range(0, len(variables_mw)):
                    if variables_mw[i] == 1:
                        variable_flag = 'pressure'
                    elif variables_mw[i] == 2:
                        variable_flag = 'relative_humidity'
                    elif variables_mw[i] == 3:
                        variable_flag = 'dew_point_temperature'
                    elif variables_mw[i] == 4:
                        variable_flag = 'air_temp'
                    elif variables_mw[i] == 5:
                        variable_flag = 'wind_speed'
                    elif variables_mw[i] == 6:
                        variable_flag = 'wind_direction'
                    (YearlyVariable_final, years_data_empty) = MesoWest_fun(self.latitude_marker, self.longitude_marker, rad_mw, variable_flag, year_start, year_end, list_nw[i])
                    if years_data_empty == 5:
                        break
                    else:
                        TotalYearlyVariables.append(YearlyVariable_final)
                        variable_names.append(variable_flag)
                #
                print('len variables_mw')
                print(len(variables_mw))
                if not variables_mw:
                    QMessageBox.warning(None, 'No Variables Selected', "If you don't tell me what variables to download, I don't know what to do!")
                elif years_data_empty == 3:
                    QMessageBox.warning(None, 'No Stations', 'There are no stations with the selected variable in this radius. Try to change location or to increase the radius')
                else:
                    try:
                        check_matrix(TotalYearlyVariables)
                    except (IndexError):
                        QMessageBox.warning(None, 'No Stations', 'There are no stations with the selected variable in this radius. Try to change location or to increase the radius')
                    else:
                        self.path_fun()
                        if not path_mw:
                            nothing = 0
                        else:
                            mw_csv_fun(TotalYearlyVariables, variable_names, path_mw)
                            print('Hurray!')
                            elapsed = time.time() - t
                            print(elapsed)


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Network Page
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class NW(QMainWindow):
    def __init__(self):
        super().__init__()
        self.nw_page = Ui_nw()
        self.nw_page.setupUi(self)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Custom Weather File
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class CustomEPW(QMainWindow):
    def __init__(self):
        super().__init__()
        self.custompage = Ui_custompage()
        self.custompage.setupUi(self)
        #
        self.custompage.custom_csv.clicked.connect(self.SelectCustomCSV)
        self.custompage.custom_tmy3.clicked.connect(self.SelectTMY3)
        self.custompage.printepw_custom.clicked.connect(self.print_select)
        self.custompage.save_custom.clicked.connect(self.SaveIn_custom)
        self.custompage.visualize_tmy3.clicked.connect(self.VisualizeTMY3)
        self.custompage.checkbox_latlon.setChecked(False)
        self.custompage.checkbox_latlon.toggled.connect(self.open_wsinfo)

    def open_wsinfo(self):
        if self.custompage.checkbox_latlon.isChecked() == True:
            self.latlon_class = LatLon()
            self.latlon_class.show()

    def showpath(self, value):
        sender = self.sender()
        if sender.text() == 'Select TMY3 file':
            self.custompage.linetmy3.setText(value)
        elif sender.text() == 'Select CSV file':
            self.custompage.linecsv.setText(value)
        elif sender.text() == 'Save in':
            self.custompage.linesave.setText(value)
        elif sender.text() == 'Save in:':
            self.custompage.line_savein_custom.setText(value)

    def VisualizeTMY3(self):
       if 'pathTMY3' in globals():
            if len(pathTMY3) is 0:
                QMessageBox.warning(self, 'TMY3 file', "No TMY3 file has been selected!\n Please select one.")
            else:
                self.table_class = TablePage()
                self.table_class.show()
       else:
            QMessageBox.warning(self, 'No TMY3', "Wait, you need to select a TMY3 file first!")


    def SelectTMY3(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        global pathTMY3
        pathTMY3 = QFileDialog.getOpenFileName(self, caption='Select TMY3 file', filter='TMY3 files (*.epw)')[0]
        try:
            read_tmy3(pathTMY3)
        except (ValueError, RuntimeError, TypeError, NameError, KeyError, StopIteration):
            QMessageBox.warning(self, 'Wrong TMY3 file', "This is not a correct TMY3 file.\n Re-try with another file.")

    def SelectCustomCSV(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        global pathCustomCSV
        pathCustomCSV = QFileDialog.getOpenFileName(self, "Select CSV file", "", "CSV files (*.csv)", options=options)[0]
        #


    def SaveIn_custom(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        #
        global pathsave_custom
        pathsave_custom = QFileDialog.getSaveFileName(self, "Select destination folder and file name", "", ".epw", options=options)[0]
        self.showpath(pathsave_custom + '.epw')

    def check_fun(self, inp):
        if inp == "Atmospheric pressure [Pa]":
            return 1
        elif inp == "Relative humidity [%]":
            return 2
        elif inp == "Dewpoint Temperature [°C]":
            return 3
        elif inp == "Dry Bulb Temperature [°C]":
            return 4
        elif inp == "Wind speed [m/s]":
            return 5
        elif inp == "Wind Direction [Deg]":
            return 6
        else:
            return 99

    def print_select(self):
        sender = self.sender()

        global variables
        variables = []
        if self.custompage.checkBox1.isChecked():
            variables.append(self.check_fun(self.custompage.option1.currentText()))
        if self.custompage.checkBox2.isChecked():
            variables.append(self.check_fun(self.custompage.option2.currentText()))
        if self.custompage.checkBox3.isChecked():
            variables.append(self.check_fun(self.custompage.option3.currentText()))
        if self.custompage.checkBox4.isChecked():
            variables.append(self.check_fun(self.custompage.option4.currentText()))
        if self.custompage.checkBox5.isChecked():
            variables.append(self.check_fun(self.custompage.option5.currentText()))
        if self.custompage.checkBox6.isChecked():
            variables.append(self.check_fun(self.custompage.option6.currentText()))
        #

        if 'pathTMY3' in globals() and 'pathCustomCSV' in globals() and 'pathsave_custom' in globals():
            if 99 in variables:
                QMessageBox.warning(self, 'EPW creation',
                                    "One or more columns have been selected but no variable has been chosen")
            elif len(pathTMY3) is 0:
                QMessageBox.warning(self, 'No TMY3', "Wait, you need to select a TMY3 file first!")
            elif len(pathCustomCSV) is 0:
                QMessageBox.warning(self, 'No CSV', "Wait, you need to select a CSV file first!")
            elif len(pathsave_custom) is 0:
                QMessageBox.warning(self, 'No destination path', "Wait, you need to select a destination path first!")
            else:
                try:
                    flag_columns = read_csv(pathCustomCSV, variables)
                except (UnboundLocalError, ValueError):
                    QMessageBox.warning(self, 'Format Error',
                                        "Check out the CSV file you input, there is something wrong with it.")
                else:
                    if flag_columns > 0:
                        QMessageBox.warning(self, 'CSV file error',
                                            "Wait! You selected too many variables! Your CSV file contains less columns than what you selected.")
                    else:
                        try:
                            write_epw(pathsave_custom)
                        except (PermissionError):
                            QMessageBox.warning(self, 'Permission Error', "Sorry, we got a permission error. Try to save the file somewhere else.")
                        except (IndexError):
                            QMessageBox.warning(self, 'Index Error',
                                            "Sorry, we got a IndexError error.\nTry to check the CSV file you input.\nIt might contain data for less than 365 days.")
                        except (ValueError):
                            QMessageBox.warning(self, 'ValueError', "Sorry, we got a ValueError.")
                        except (RuntimeError):
                            QMessageBox.warning(self, 'RuntimeError', "Sorry, we got a RuntimeError.")
                        except (TypeError):
                            QMessageBox.warning(self, 'TypeError', "Sorry, we got a TypeError.")
                        except (NameError):
                            QMessageBox.warning(self, 'NameError', "Sorry, we got a NameError.")
                        except (FileNotFoundError):
                            QMessageBox.warning(self, 'FileNotFoundError',
                                                "Sorry, we got a FileNotFoundError error. Try to save the file somewhere else.")
                        else:
                            buttonReply = QMessageBox.question(self, 'EPW creation', "A new EPW file has been created. \nDo you want to visualize it?",
                                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                            if buttonReply == QMessageBox.Yes:
                                self.table_class = TablePage()
                                self.table_class.show()
                            self.show()



        #
        elif 'pathTMY3' in globals() and 'pathCustomCSV' in globals():
            QMessageBox.warning(self, 'Save in', "No path to save the .epw file has been selected!")
        elif 'pathTMY3' in globals() and 'pathsave_custom' in globals():
            QMessageBox.warning(self, 'No CSV file', "No custom weather data (.csv file) have been selected!")
        elif 'pathCustomCSV' in globals() and 'pathsave_custom' in globals():
            QMessageBox.warning(self, 'No TMY3 file', "No TMY3 file has been selected!")
        #
        elif 'pathTMY3' in globals():
            QMessageBox.warning(self, 'Missing files', "No .csv file and saving path have been selected!")
        elif 'pathCustomCSV' in globals():
            QMessageBox.warning(self, 'Missing files', "No TMY3 file and saving path have been selected!")
        elif 'pathsave_custom' in globals():
            QMessageBox.warning(self, 'Missing files', "No TMY3 and .csv files have been selected!")
        else:
            QMessageBox.warning(self, 'Missing files', "No TMY3, .csv files and saving path have been selected!")

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# LatLon Page
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class LatLon(QMainWindow):
    def __init__(self):
        super().__init__()
        self.latlon_page = Ui_latlonpage()
        self.latlon_page.setupUi(self)
        global lat_new, long_new, DS_new, City_new, State_new, Country_new, elev_new, wmosn_new, comm1_new, tz_new
        lat_new = lat
        long_new = long
        City_new = City
        State_new = State
        Country_new = Country
        DS_new = DS
        elev_new = elev
        wmosn_new = wmosn
        comm1_new = comm1
        tz_new = tz
        # connect buttons
        self.latlon_page.line_lat.setText(lat)
        self.latlon_page.line_long.setText(long)
        self.latlon_page.line_city.setText(City)
        self.latlon_page.line_state.setText(State)
        self.latlon_page.line_country.setText(Country)
        self.latlon_page.line_SDS.setText(DS)
        self.latlon_page.line_tz.setText(tz)
        self.latlon_page.line_elevation.setText(elev)
        self.latlon_page.line_comm1.setText(comm1)
        self.latlon_page.line_WMOSN.setText(wmosn)
        #
        self.latlon_page.Save.clicked.connect(self.save_fun)
        self.latlon_page.Cancel.clicked.connect(self.cancel_fun)
        #
        self.latlon_page.line_lat.textChanged[str].connect(self.latitude)
        self.latlon_page.line_long.textChanged[str].connect(self.longitude)
        self.latlon_page.line_SDS.textChanged[str].connect(self.datasource)
        self.latlon_page.line_city.textChanged[str].connect(self.city_fun)
        self.latlon_page.line_state.textChanged[str].connect(self.state_fun)
        self.latlon_page.line_country.textChanged[str].connect(self.country_fun)
        self.latlon_page.line_WMOSN.textChanged[str].connect(self.wmosn_fun)
        self.latlon_page.line_elevation.textChanged[str].connect(self.elevation_fun)
        self.latlon_page.line_tz.textChanged[str].connect(self.tz_fun)
        self.latlon_page.line_comm1.textChanged[str].connect(self.comm1_fun)

    def latitude(self, text):
        global lat_new
        lat_new = text
    def longitude(self, text):
        global long_new
        long_new = text
    def city_fun(self, text):
        global City_new
        City_new = text
    def state_fun(self, text):
        global State_new
        State_new = text
    def country_fun(self, text):
        global Country_new
        Country_new = text
    def datasource(self, text):
        global DS_new
        DS_new = text
    def elevation_fun(self, text):
        global elev_new
        elev_new = text
    def wmosn_fun(self, text):
        global wmosn_new
        wmosn_new = text
    def comm1_fun(self, text):
        global comm1_new
        comm1_new = text
    def tz_fun(self, text):
        global tz_new
        tz_new = text
    def save_fun(self):
        global lat, long, DS, City, State, Country, elev, wmosn, comm1, tz
        lat = lat_new
        long = long_new
        City = City_new
        State = State_new
        Country = Country_new
        DS = DS_new
        elev = elev_new
        wmosn = wmosn_new
        comm1 = comm1_new
        tz = tz_new
        self.close()
    def cancel_fun(self):
        self.close()

# # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# # Table Page
# # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class TablePage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tabpage = Tab()
        self.tabpage.setupUi(self)
#
class Tab(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 900)
        MainWindow.setMaximumSize(QtCore.QSize(900, 900))
        MainWindow.setMinimumSize(QtCore.QSize(900, 900))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 900, 901))
        self.tableWidget.setMouseTracking(False)
        self.tableWidget.setAutoScroll(True)
        self.tableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.AnyKeyPressed | QtWidgets.QAbstractItemView.DoubleClicked | QtWidgets.QAbstractItemView.EditKeyPressed | QtWidgets.QAbstractItemView.SelectedClicked)
        self.tableWidget.setDragEnabled(True)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectColumns)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(9)
        self.tableWidget.setRowCount(8760)
        # Vertical Header
        for i in range(0, 8760):
            item = QtWidgets.QTableWidgetItem()
            font = QtGui.QFont()
            font.setPointSize(15)
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
            self.tableWidget.setVerticalHeaderItem(i, item)
        # Horizontal Header
        for i in range(0, 9):
            item = QtWidgets.QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            font = QtGui.QFont()
            font.setPointSize(15)
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
            self.tableWidget.setHorizontalHeaderItem(i, item)
        # Filling the cells
        for i in range(0, 8760):
            for j in range(0, 9):
                item = QtWidgets.QTableWidgetItem()
                self.tableWidget.setItem(i, j, item)
        #
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(False)
        self.tableWidget.verticalHeader().setVisible(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setSortIndicatorShown(False)
        self.tableWidget.verticalHeader().setStretchLastSection(False)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    #
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tableWidget.setSortingEnabled(False)
        #
        for i in range(0, 8760):
            item = self.tableWidget.verticalHeaderItem(i)
            item.setText(_translate("MainWindow", str(DateTime[i])))
        #
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", 'Dry Bulb\nTemperature\n[ºC]'))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", 'Dewpoint\nTemperature\n[ºC]'))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", 'Relative\nHumidity\n[%]'))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", 'Atmospheric\nPressure\n[Pa]'))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", 'Wind\nDirection\n[Deg]'))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", 'Wind\nSpeed\n[m/s]'))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", 'Global\nSolar\n[Wh/m2]'))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", 'Normal\nSolar\n[Wh/m2]'))
        item = self.tableWidget.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", 'Diffuse\nSolar\n[Wh/m2]'))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        #
        self.tableWidget.resizeColumnsToContents()
        for i in range(0, 8760):
            item = self.tableWidget.item(i, 0)
            item.setText(_translate("MainWindow", str(Tdb[i])))
            item = self.tableWidget.item(i, 1)
            item.setText(_translate("MainWindow", str(Tdew[i])))
            item = self.tableWidget.item(i, 2)
            item.setText(_translate("MainWindow", str(RH[i])))
            item = self.tableWidget.item(i, 3)
            item.setText(_translate("MainWindow", str(Patm[i])))
            item = self.tableWidget.item(i, 4)
            item.setText(_translate("MainWindow", str(Wdir[i])))
            item = self.tableWidget.item(i, 5)
            item.setText(_translate("MainWindow", str(Wspeed[i])))
            item = self.tableWidget.item(i, 6)
            item.setText(_translate("MainWindow", str(GHRad[i])))
            item = self.tableWidget.item(i, 7)
            item.setText(_translate("MainWindow", str(DNRad[i])))
            item = self.tableWidget.item(i, 8)
            item.setText(_translate("MainWindow", str(DHRad[i])))
        #
        self.tableWidget.setSortingEnabled(__sortingEnabled)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# About Page
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class About(QMainWindow):
    def __init__(self):
        super().__init__()
        self.about_page = Ui_about()
        self.about_page.setupUi(self)
        self.about_page.link_web.setOpenExternalLinks(True)
        self.about_page.acknow.mousePressEvent = self.ack_fun
        self.about_page.license.mousePressEvent = self.license_fun
        self.about_page.label_7.setOpenExternalLinks(True)

    def ack_fun(self, event):
        self.ack_page = Ack()
        self.ack_page.show()

    def license_fun(self, event):
        self.license_page = License()
        self.license_page.show()

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Acknowledgments Page
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class Ack(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ack_page = Ui_ack()
        self.ack_page.setupUi(self)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# License Page
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
class License(QMainWindow):
    def __init__(self):
        super().__init__()
        self.license_page = Ui_license()
        self.license_page.setupUi(self)
        self.license_page.textBrowser.setOpenExternalLinks(True)



#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainPage()
    ex.show()
    sys.exit(app.exec_())