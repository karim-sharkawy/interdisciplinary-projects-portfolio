# Calibration Demo

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
# %matplotlib inline

truth = np.array([0.00,  1.00,  2.00,  3.00,  4.00,  5.00,  \
                  6.00,  7.00,  8.00,  9.00,  10.00, 11.00, \
                  12.00, 13.00, 14.00, 15.00, 16.00, 17.00, \
                  18.00, 19.00, 20.00])
test  = np.array([1.76,  1.73,  3.77,  3.82,  5.69,  6.12,  \
                  6.75,  8.87,  8.95,  11.17, 10.30, 12.77, \
                  13.20, 14.68, 14.75, 17.19, 18.95, 18.38, \
                  20.45, 21.66, 20.87])

fig = plt.figure(figsize = (8, 8))
ax = plt.subplot(1, 1, 1)
plt.plot(truth, test, '.', color = 'darkred', markersize = 20, label = 'Measurements')
plt.plot(truth, truth, '--', color = 'darkgray', label = '1:1 line')
plt.xlabel('Truth: Chamber temperature (deg C)')
plt.ylabel('Test: Thermometer reading (deg C)')
plt.xlim(0,20)
plt.ylim(0,20)
plt.grid()
plt.title('Thermometer chamber test results')
h = plt.legend()

fig = plt.figure(figsize = (8, 8))
ax = plt.subplot(1, 1, 1)
plt.plot(truth, test, '.', color = 'darkred', markersize = 20, label = 'Measurements')
plt.plot(truth, truth, '--', color = 'darkgray', label = '1:1 line')
for n in range(len(truth)):
    plt.plot([n, n], [test[n], truth[n]], 'orange')
plt.xlabel('Truth: Chamber temperature (deg C)')
plt.ylabel('Test: Thermometer reading (deg C)')
plt.xlim(0,20)
plt.ylim(0,20)
plt.grid()
plt.title('Thermometer chamber test results')
plt.text(5.0, 12.5, r'Error $\varepsilon_{i}$', color ='orange', fontsize = 20)
plt.legend()

error = test - truth
print('Error = ', error, 'deg C') # print error values to the screen

N = len(test) # Should be 21
print('N = ', N)

bias = (1 / N) * np.sum(error)
print('Bias = ', bias, 'deg C')

fig = plt.figure(figsize = (8, 8))
ax = plt.subplot(1, 1, 1)
plt.plot(truth, test, '.', color = 'darkred', markerfacecolor = 'None', markersize = 20, \
         label = 'Measurements', alpha = 0.3) # 'alpha' controls transparency
for n in range(len(truth)):
    plt.plot([n, n], [test[n], test[n]-bias], 'magenta', alpha = 0.3)
plt.plot(truth, test - bias, '.', color = 'darkblue', markersize = 20, label = 'Measurements - bias')
plt.plot(truth, truth, '--', color = 'darkgray', label = '1:1 line')
plt.xlabel('Truth: Chamber temperature (deg C)')
plt.ylabel('Test: Thermometer reading (deg C)')
plt.xlim(0,20)
plt.ylim(0,20)
plt.grid()
plt.title('Thermometer chamber test results')
h = plt.legend()

uncertainty = np.sqrt( (1 / (N - 1)) * np.sum((error - bias) ** 2.) )
print('Uncertainty = ', uncertainty, ' deg C')

hist = plt.hist(error - bias, bins = np.arange(-1.5, 1.75, 0.25), density = True)
plt.xlabel('Bias-subtracted error')
plt.ylabel('Probability')
plt.title('Error histogram')
plt.grid()

bins = np.arange(-1.5, 1.75, 0.25)
hist = plt.hist(error - bias, bins = bins, density = True)
plt.xlabel('Bias-subtracted error')
plt.ylabel('Probability')
plt.title('Error histogram')
plt.grid()
plt.plot(hist[1], stats.norm.pdf(bins, 0, uncertainty), color = 'pink', linewidth = 5)

bins = np.arange(-1.5, 1.75, 0.25)
hist = plt.hist(uncertainty * np.random.randn(20000), bins = bins, density = True)
plt.xlabel('Bias-subtracted error')
plt.ylabel('Probability')
plt.title('Error histogram (20,000 realizations)')
plt.grid()
plt.plot(hist[1], stats.norm.pdf(bins, 0, uncertainty), color = 'pink', linewidth = 5)

"""# METER Station Plot"""

# Commented out IPython magic to ensure Python compatibility.
from metpy.io import parse_metar_to_dataframe
from metpy.plots import add_metpy_logo, current_weather, sky_cover, StationPlot
import matplotlib.pyplot as plt
# %matplotlib inline

# Because raw METARs can be quite long, let's store one to a string variable.
myMETAR = "KLAF 201154Z 13006KT 2 1/2SM +RA BR FEW015 BKN029 OVC039 21/20 A2998 RMK AO2 SLP148 P0005 60016 70016 T02060200 10222 20206 56008 $"
data = parse_metar_to_dataframe(myMETAR, year = 2021, month = 9)
data # Print out the contents of the DataFrame

def draw_station_plot(data):
    """
    Draws a station plot from a Dataframe.

    Inputs:

        data: An Pandas Dataframe produced from metpy.io.parse_metar_into_dataframe().

    Outputs:

        A station plot floating on a small canvas.

    """
    # First, I have to create a figure and axis for the station plot to be drawn on.
    fig = plt.figure(figsize=(3, 3)) # make a 3-inch by 3-inch canvas
    ax = fig.add_subplot(1, 1, 1) # Make an axis called "ax" on the figure canvas

    # The following creates an instance of a StationPlot class at coordinates (0,0) on the canvas.

    # Note: The actual station plot is not drawn until we use a couple of additional commands, below this one.
    # You can comment out each block to see what each one does.
    stationplot = StationPlot(ax, 0, 0, fontsize = 24)

    # Plot the temperature and dew point to the upper and lower left, respectively, of
    # the center point. Each one uses a different color.
    stationplot.plot_parameter('NW', data['air_temperature'].values, color='darkblue')
    stationplot.plot_parameter('SW', data['dew_point_temperature'].values,
                               color='darkgreen')
    # A more complex example uses a custom formatter to control how the sea-level pressure
    # values are plotted. This uses the standard trailing 3-digits of the pressure value
    # in tenths of millibars.
    stationplot.plot_parameter('NE', data['air_pressure_at_sea_level'].values,
                               formatter=lambda v: format(10 * v, '.0f')[-3:])

    # Plot the cloud cover symbols in the center location. This uses the codes made above and
    # uses the `sky_cover` mapper to convert these values to font codes for the
    # weather symbol font.
    stationplot.plot_symbol('C', data['cloud_coverage'].values, sky_cover)
    # Same this time, but plot current weather to the left of center, using the
    # `current_weather` mapper to convert symbols to the right glyphs.
    stationplot.plot_symbol('W', data['current_wx1_symbol'].values, current_weather)

    # Add wind barbs
    stationplot.plot_barb(data['eastward_wind'].values, data['northward_wind'].values)

    # Also plot the actual text of the station id. Instead of cardinal directions,
    # plot further out by specifying a location of 2 increments in x and 0 in y.
    stationplot.plot_text((2, 0), data['station_id'].values)

    # These last lines remove the axes and ticks.
    #ax.spines['top'].set_visible(False)
    #ax.spines['right'].set_visible(False)
    #ax.spines['bottom'].set_visible(False)
    #ax.spines['left'].set_visible(False)
    ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])

draw_station_plot(data)

myMETAR2 = "" # Paste your METAR in between the quotation marks!

# Note: If your METAR is historical, you will need to change the year and month!
data2 = parse_metar_to_dataframe(myMETAR2, year = 2021, month = 9)
data2 # Print out the contents of the DataFrame

draw_station_plot(data2)

from siphon.catalog import TDSCatalog
cat = TDSCatalog("http://thredds-test.unidata.ucar.edu/thredds/catalog/noaaport/text/metar/")

ds = cat.datasets[-18]  # The number in front of the minus sign means "XX hours ago"
# Note that I decrement by a few hours, just to make sure the METAR text file is reasonably complete
ds # Print the name of the file to be downloaded
ds.download()

from metpy.io import parse_metar_file

df = parse_metar_file(ds)
df  # Print out the contents of the DataFrame to the screen

df = df.dropna(subset = ['air_temperature', 'dew_point_temperature',
                         'air_pressure_at_sea_level', 'cloud_coverage',
                         'current_wx1_symbol'], how = 'any')
df

import cartopy.crs as ccrs
#import cartopy.feature as cfeature

# Set up the map projection
proj = ccrs.LambertConformal(central_longitude=-95, central_latitude=35,
                             standard_parallels=[35])

# Use the Cartopy map projection to transform station locations to the map and
# then refine the number of stations plotted by setting a 300km radius
point_locs = proj.transform_points(ccrs.PlateCarree(), df['longitude'].values,
                                   df['latitude'].values)

# This DataFrame has way too many stations to plot all of them.
# The number of stations plotted will be reduced using reduce_point_density.
from metpy.calc import reduce_point_density
from metpy.units import units
df = df[reduce_point_density(point_locs, 300. * units.km)]
df

# Change the DPI of the resulting figure. Higher DPI drastically improves the
# look of the text rendering.
plt.rcParams['savefig.dpi'] = 255

# Create the figure and an axes set to the projection.
fig = plt.figure(figsize=(20, 10))
add_metpy_logo(fig, 1100, 300, size='large')
ax = fig.add_subplot(1, 1, 1, projection=proj)

# Set plot bounds (latitude and longitude)
ax.set_extent([-118, -73, 23, 50], crs=ccrs.PlateCarree())

# Add some various map elements to the plot to make it recognizable.
# Note: These features require "fetching" from an external site.
# Commands may fail if you don't have write permissions.
#ax.add_feature(cfeature.LAND)
#ax.add_feature(cfeature.OCEAN)
#ax.add_feature(cfeature.LAKES)
#ax.add_feature(cfeature.COASTLINE)
#ax.add_feature(cfeature.STATES)
#ax.add_feature(cfeature.BORDERS)
# Trust me, these look really nice when they work.

# Because the downloadable shapefiles are not working,
# let's use a static one I've already installed on Scholar for you.
from cartopy.io.shapereader import BasicReader
countries = BasicReader('/depot/eapsdept/apps/eaps227-2021/gis/ne_110m_admin_0_countries.shp')
states = BasicReader('/depot/eapsdept/apps/eaps227-2021/gis/ne_110m_admin_1_states_provinces_lines.shp')

ax.add_geometries(countries.geometries(), ccrs.PlateCarree(), facecolor = 'none', edgecolor = 'black', lw = 2)
ax.add_geometries(states.geometries(), ccrs.PlateCarree(), facecolor = 'none', edgecolor = 'gray')

# Start the station plot by specifying the axes to draw on, as well as the
# lon/lat of the stations (with transform). We also change the fontsize to 12 pt.
stationplot = StationPlot(ax, df['longitude'].values, df['latitude'].values,
                          clip_on=True, transform=ccrs.PlateCarree(), fontsize=12)

# Plot the temperature and dew point to the upper and lower left, respectively, of
# the center point. Each one uses a different color.
stationplot.plot_parameter('NW', df['air_temperature'].values, color='darkblue')
stationplot.plot_parameter('SW', df['dew_point_temperature'].values,
                           color='darkgreen')

# A more complex example uses a custom formatter to control how the sea-level pressure
# values are plotted. This uses the standard trailing 3-digits of the pressure value
# in tenths of millibars.
stationplot.plot_parameter('NE', df['air_pressure_at_sea_level'].values,
                           formatter=lambda v: format(10 * v, '.0f')[-3:])

# Plot the cloud cover symbols in the center location. This uses the codes made above and
# uses the `sky_cover` mapper to convert these values to font codes for the
# weather symbol font.
stationplot.plot_symbol('C', df['cloud_coverage'].values, sky_cover)

# Same this time, but plot current weather to the left of center, using the
# `current_weather` mapper to convert symbols to the right glyphs.
stationplot.plot_symbol('W', df['current_wx1_symbol'].values, current_weather)

# Add wind barbs
stationplot.plot_barb(df['eastward_wind'].values, df['northward_wind'].values)

# Also plot the actual text of the station id. Instead of cardinal directions,
# plot further out by specifying a location of 2 increments in x and 0 in y.
stationplot.plot_text((2, 0), df['station_id'].values)

plt.title(df['date_time'][0])


plt.show()

"""# SKEWT & Hodograph"""

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import pandas as pd
# Huzzah! MetPy already has pre-defined Hodograph and Skew-T classes!
from metpy.plots import add_metpy_logo, Hodograph, SkewT
from metpy.units import units
import metpy.calc as mpcalc

sounding = pd.read_csv('2021-10-11_1239.sharppy_mod.txt', skiprows = [0, 1, 2, 3, 4, 5],
                       names = ["Pressure", "Height", "Temperature", "Dewpoint", "Wind Direction", "Wind Speed"],
                      skipfooter = 1, engine = 'python')
sounding  # Print out the contents of the variable 'sounding' to the screen

p = sounding['Pressure'].values * units('hectopascal')
z = sounding['Height'].values * units('meters')
t = sounding['Temperature'].values * units('degC')
d = sounding['Dewpoint'].values * units('degC')

fig = plt.figure(figsize = (10, 10)) # Create a 10 inch-by-10 inch figure object.
add_metpy_logo(fig, 115, 100) # Acknowledge the nice MetPy team who made this package.
skew = SkewT(fig, rotation=45)

# Add the relevant special lines
skew.plot_dry_adiabats() # Light red
skew.plot_moist_adiabats() # Light blue
skew.plot_mixing_lines() # Light green
# Plot a zero degree isotherm
skew.ax.axvline(0, color='cyan', linestyle='--', linewidth=1.5)

### PLOT THE SOUNDING ###
skew.plot(p, t, 'darkred')
skew.plot(p, d, 'darkblue')
### END SOUNDING PLOTTING ###

plt.title('Purdue Sounding, 11 October 2021 1745 UTC')
plt.xlabel('Temperature (deg C)')
plt.ylabel('Pressure (hPa)')
plt.savefig('skew1.png')
plt.show()

parcel_prof = mpcalc.parcel_profile(p, t[0], d[0]).to('degC')
parcel_prof # Print out the contents of the variable 'parcel_prof' to the screen

cape, cin = mpcalc.cape_cin(p, t, d, parcel_prof)
lcl = mpcalc.lcl(p[0], t[0], d[0]) # This is LCL based on the surface parcel.
lfc = mpcalc.lfc(p, t, d, parcel_prof, which = 'most_cape')
el = mpcalc.el(p, t, d, parcel_prof, which = 'most_cape')

print('CAPE = ', cape)
print('CIN = ', cin)
print('LCL = ', lcl)
print('LFC = ', lfc)
print('EL', el)

fig = plt.figure(figsize = (10, 10)) # Create a 10 inch-by-10 inch figure object.
add_metpy_logo(fig, 115, 100)
skew = SkewT(fig, rotation=45)

# Add the relevant special lines
skew.plot_dry_adiabats() # Light red
skew.plot_moist_adiabats() # Light blue
skew.plot_mixing_lines() # Light green
# Plot a zero degree isotherm
skew.ax.axvline(0, color='cyan', linestyle='--', linewidth=1.5)

# Plot the data using normal plotting functions, in this case using
# log scaling in Y, as dictated by the typical meteorological plot.
skew.plot(p, t, 'darkred')
skew.plot(p, d, 'darkblue')
### NEW STUFF ###
# Plot parcel profile
skew.plot(p, parcel_prof, 'black')
# Shade areas of CAPE and CIN
skew.shade_cin(p, t, parcel_prof, d) # Light blue shading
skew.shade_cape(p, t, parcel_prof) # Light red shading
### END OF NEW STUFF ###

plt.title('Purdue Sounding, 11 October 2021 1745 UTC')
plt.xlabel('Temperature (deg C)')
plt.ylabel('Pressure (hPa)')
plt.savefig('skew2.png')
plt.show()

wd = sounding['Wind Direction'].values * units('degrees')
ws = sounding['Wind Speed'].values * units('knots')

u, v = mpcalc.wind_components(ws, wd)
plt.plot(u, v)
# Create a basic plot just to ensure that the values look sane.
plt.show()

fig = plt.figure()
hodo = Hodograph(component_range=80.)
hodo.add_grid(increment=20)
hodo.plot(u, v)   # Plain hodograph
plt.xlabel('East-west wind (kts)')
plt.ylabel('North-south wind (kts)')
plt.title('Purdue Hodograph, 11 October 2021 1745 UTC')
plt.savefig('hodo1.png')
plt.show()

fig = plt.figure()
hodo = Hodograph(component_range=80.)
hodo.add_grid(increment=20)
hodo.plot_colormapped(u, v, z)  # Plot a line colored by altitude
plt.xlabel('East-west wind (kts)')
plt.ylabel('North-south wind (kts)')
plt.title('Purdue Hodograph, 11 October 2021 1745 UTC')
plt.savefig('hodo2.png')
plt.show()

fig = plt.figure()
hodo = Hodograph(component_range=80.)
hodo.add_grid(increment=20)
hodo.plot_colormapped(u[::25], v[::25], z[::25])  # Plot a line colored by altitude
plt.xlabel('East-west wind (kts)')
plt.ylabel('North-south wind (kts)')
plt.title('Purdue Hodograph, 11 October 2021 1745 UTC')
plt.savefig('hodo3.png')
plt.show()

fig = plt.figure(figsize = (10, 10)) # Create a 10 inch-by-10 inch figure object.
add_metpy_logo(fig, 115, 100)
skew = SkewT(fig, rotation=45)

# Add the relevant special lines
skew.plot_dry_adiabats() # Light red
skew.plot_moist_adiabats() # Light blue
skew.plot_mixing_lines() # Light green
# Plot a zero degree isotherm
skew.ax.axvline(0, color='cyan', linestyle='--', linewidth=1.5)

# Plot the data using normal plotting functions, in this case using
# log scaling in Y, as dictated by the typical meteorological plot.
skew.plot(p, t, 'darkred')
skew.plot(p, d, 'darkblue')
# Plot parcel profile
skew.plot(p, parcel_prof, 'black')
# Shade areas of CAPE and CIN
skew.shade_cin(p, t, parcel_prof, d) # Light blue shading
skew.shade_cape(p, t, parcel_prof) # Light red shading

plt.title('Purdue Sounding, 11 October 2021 1745 UTC')
plt.xlabel('Temperature (deg C)')
plt.ylabel('Pressure (hPa)')

### HODOGRAPH INSET ###
# Create an inset axes object that is 30% width and height of the
# figure and put it in the upper right hand corner.
ax_hod = inset_axes(skew.ax, '30%', '30%', loc=1)
hodo = Hodograph(ax_hod, component_range=80.)
hodo.add_grid(increment=20)
hodo.plot_colormapped(u, v, z)  # Plot a line colored by height
plt.xlabel('u (kts)')  # I've shortened these labels because the inset is small.
plt.ylabel('v (kts)')
### END OF HODOGRAPH INSET ###

plt.savefig('skew3.png')
plt.show()

"""# KLAF Weather Plot"""

# Commented out IPython magic to ensure Python compatibility.
# Plots will appear in this notebook
# %matplotlib inline
# Suppress most (but not all) warnings
import warnings
warnings.simplefilter('ignore')
# Other import statements
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from metpy.units import units
import scipy.stats as stats

fileName = 'EAPS227_20211006.csv'
wxt = pd.read_csv(fileName, header=[2], skiprows = [3], parse_dates=[0], infer_datetime_format=True, na_values = ['  '])

wxt

wxt.units = {
    'Date/Time' : None,
    'WindDir' : 'degrees',
    'WindSp' : 'mph',
    'AirTemp' : 'degF',
    'RH' : None,
    'BP' : 'inHg',
    'RainInten': 'inches/hour'
}

from metpy.calc import dewpoint_from_relative_humidity
dewpoint_from_relative_humidity?

# Add Dewpoint to our dataframe:
wxt['Dewpoint'] = dewpoint_from_relative_humidity(wxt['AirTemp'].values.squeeze() * units(wxt.units['AirTemp']), \
                                                 wxt['RH'].values.squeeze()/100. * units(wxt.units['RH']))
wxt

wxt.units['Dewpoint'] = 'degC'
wxt.units

import datetime as dt

import matplotlib as mpl

from metpy.plots import add_metpy_logo

# Make meteogram plot
class Meteogram(object):
    """ Plot a time series of meteorological data from a particular station as a
    meteogram with standard variables to visualize, including thermodynamic,
    kinematic, and pressure. The functions below control the plotting of each
    variable.
    TO DO: Make the subplot creation dynamic so the number of rows is not
    static as it is currently. """

    def __init__(self, fig, dates, probeid, time=None, axis=0):
        """
        Required input:
            fig: figure object
            dates: array of dates corresponding to the data
            probeid: ID of the station
        Optional Input:
            time: Time the data is to be plotted
            axis: number that controls the new axis to be plotted (FOR FUTURE)
        """
        if not time:
            time = dt.datetime.utcnow()
        self.start = dates[0]
        self.fig = fig
        self.end = dates[-1]
        self.axis_num = 0
        self.dates = mpl.dates.date2num(dates)
        self.time = time.strftime('%Y-%m-%d %H:%M UTC')
        self.title = 'Latest Ob Time: {0}\nProbe ID: {1}'.format(self.time, probeid)

    def plot_winds(self, ws, wd, wsmax, plot_range=None):
        """
        Required input:
            ws: Wind speeds (knots)
            wd: Wind direction (degrees)
            wsmax: Maximum wind speeds
        Optional Input:
            plot_range: Data range for making figure (list of (min,max,step))
        """
        # PLOT WIND SPEED AND WIND DIRECTION
        self.ax1 = fig.add_subplot(4, 1, 1)
        ln1 = self.ax1.plot(self.dates, ws, label='Wind Speed')
        self.ax1.fill_between(self.dates, ws, 0)
        self.ax1.set_xlim(self.start, self.end)
        if not plot_range:
            plot_range = [0, 15, 1]
        self.ax1.set_ylabel('Wind Speed (knots)', multialignment='center')
        self.ax1.set_ylim(plot_range[0], plot_range[1], plot_range[2])
        self.ax1.grid(b=True, which='major', axis='y', color='k', linestyle='--',
                      linewidth=0.5)
        #ln2 = self.ax1.plot(self.dates, wsmax, '.r', label='3-sec Wind Speed Max')
        ln2 = None

        ax7 = self.ax1.twinx()
        ln3 = ax7.plot(self.dates, wd, '.k', linewidth=0.5, label='Wind Direction')
        ax7.set_ylabel('Wind\nDirection\n(degrees)', multialignment='center')
        ax7.set_ylim(0, 360)
        #ax7.set_yticks(np.arange(45, 405, 90), ['NE', 'SE', 'SW', 'NW'])
        #lines = ln1 + ln2 + ln3
        lines = ln1 + ln3

        labs = [line.get_label() for line in lines]
        ax7.xaxis.set_major_formatter(mpl.dates.DateFormatter('%d/%H UTC'))
        ax7.legend(lines, labs, loc='best',
                   bbox_to_anchor=(0.5, 1.2), ncol=3, prop={'size': 12})

    def plot_thermo(self, t, td, plot_range=None):
        """
        Required input:
            T: Temperature (deg F)
            TD: Dewpoint (deg F)
        Optional Input:
            plot_range: Data range for making figure (list of (min,max,step))
        """
        # PLOT TEMPERATURE AND DEWPOINT
        if not plot_range:
            plot_range = [10, 90, 2]
        self.ax2 = fig.add_subplot(4, 1, 2, sharex=self.ax1)
        ln4 = self.ax2.plot(self.dates, t, 'r-', label='Temperature')
        self.ax2.fill_between(self.dates, t, td, color='r')

        self.ax2.set_ylabel('Temperature\n(F)', multialignment='center')
        self.ax2.grid(b=True, which='major', axis='y', color='k', linestyle='--',
                      linewidth=0.5)
        self.ax2.set_ylim(plot_range[0], plot_range[1], plot_range[2])

        ln5 = self.ax2.plot(self.dates, td, '-', color = 'purple', label='Dewpoint')
        self.ax2.fill_between(self.dates, td, self.ax2.get_ylim()[0], color='purple')

        ax_twin = self.ax2.twinx()
        ax_twin.set_ylim(plot_range[0], plot_range[1], plot_range[2])
        lines = ln4 + ln5
        labs = [line.get_label() for line in lines]
        ax_twin.xaxis.set_major_formatter(mpl.dates.DateFormatter('%d/%H UTC'))

        self.ax2.legend(lines, labs, loc='best',
                        bbox_to_anchor=(0.5, 1.2), ncol=2, prop={'size': 12})

    def plot_rh(self, rh, plot_range=None):
        """
        Required input:
            RH: Relative humidity (%)
        Optional Input:
            plot_range: Data range for making figure (list of (min,max,step))
        """
        # PLOT RELATIVE HUMIDITY
        if not plot_range:
            plot_range = [0, 100, 4]
        self.ax3 = fig.add_subplot(4, 1, 3, sharex=self.ax1)
        self.ax3.plot(self.dates, rh, 'g-', label='Relative Humidity')
        self.ax3.legend(loc='best', bbox_to_anchor=(0.5, 1.22), prop={'size': 12})
        self.ax3.grid(b=True, which='major', axis='y', color='k', linestyle='--',
                      linewidth=0.5)
        self.ax3.set_ylim(plot_range[0], plot_range[1], plot_range[2])

        self.ax3.fill_between(self.dates, rh, self.ax3.get_ylim()[0], color='g')
        self.ax3.set_ylabel('Relative Humidity\n(%)', multialignment='center')
        self.ax3.xaxis.set_major_formatter(mpl.dates.DateFormatter('%d/%H UTC'))
        axtwin = self.ax3.twinx()
        axtwin.set_ylim(plot_range[0], plot_range[1], plot_range[2])

    def plot_pressure(self, p, plot_range=None):
        """
        Required input:
            P: Mean Sea Level Pressure (hPa)
        Optional Input:
            plot_range: Data range for making figure (list of (min,max,step))
        """
        # PLOT PRESSURE
        if not plot_range:
            plot_range = [970, 1030, 2]
        self.ax4 = fig.add_subplot(4, 1, 4, sharex=self.ax1)
        self.ax4.plot(self.dates, p, 'm', label='Mean Sea Level Pressure')
        self.ax4.set_ylabel('Mean Sea\nLevel Pressure\n(mb)', multialignment='center')
        self.ax4.set_ylim(plot_range[0], plot_range[1], plot_range[2])

        axtwin = self.ax4.twinx()
        axtwin.set_ylim(plot_range[0], plot_range[1], plot_range[2])
        axtwin.fill_between(self.dates, p, axtwin.get_ylim()[0], color='m')
        axtwin.xaxis.set_major_formatter(mpl.dates.DateFormatter('%d/%H UTC'))

        self.ax4.legend(loc='best', bbox_to_anchor=(0.5, 1.2), prop={'size': 12})
        self.ax4.grid(b=True, which='major', axis='y', color='k', linestyle='--',
                      linewidth=0.5)

fig = plt.figure(figsize=(20, 16))
add_metpy_logo(fig, 75, 75)
meteogram = Meteogram(fig, wxt['Date/Time'].values.squeeze(), 'WXT')
meteogram.plot_winds(wxt['WindSp'].values.squeeze() * units(wxt.units['WindSp']),
                     wxt['WindDir'].values.squeeze() * units(wxt.units['WindDir']),
                     wxt['WindSp'].values.squeeze() * units(wxt.units['WindSp']))
meteogram.plot_thermo((wxt['AirTemp'].values.squeeze() * units(wxt.units['AirTemp'])).to(units('degF')),
                      (wxt['Dewpoint'].values.squeeze() * units(wxt.units['Dewpoint'])).to(units('degF')))
meteogram.plot_rh(wxt['RH'].values.squeeze())
meteogram.plot_pressure(wxt['BP'].values.squeeze() * units(wxt.units['BP']).to(units('hPa')))
plt.suptitle('WXT')
plt.savefig(fileName[:-3] + 'png')

laf = pd.read_csv("LAF.csv")
laf

laf.metar[0]


for i in range(1, len(laf)):
    if i%100 == 0: print("Parsing METAR number ", i)
    tmp = parse_metar_to_dataframe(laf.metar[i], year = 2021, month = 10)
    laf_metar = pd.concat([laf_metar, tmp])

laf_metar

# Assign units to each column in the dataframe.
laf_metar.units = \
{'station_id': None,
 'latitude': 'degrees',
 'longitude': 'degrees',
 'elevation': 'meters',
 'date_time': None,
 'wind_direction': 'degrees',
 'wind_speed': 'kts',
 'eastward_wind': 'kts',
 'northward_wind': 'kts',
 'current_wx1': None,
 'current_wx2': None,
 'current_wx3': None,
 'low_cloud_type': None,
 'low_cloud_level': 'feet',
 'medium_cloud_type': None,
 'medium_cloud_level': 'feet',
 'high_cloud_type': None,
 'high_cloud_level': 'feet',
 'highest_cloud_type': None,
 'highest_cloud_level:': None,
 'cloud_coverage': None,
 'air_temperature': 'degC',
 'dew_point_temperature': 'degC',
 'altimeter': 'inHg',
 'air_pressure_at_sea_level': 'hPa',
 'present_weather': None,
 'past_weather': None,
 'past_weather2': None,
 'rh' : None}

 from metpy.calc import relative_humidity_from_dewpoint
laf_metar['rh'] = relative_humidity_from_dewpoint(laf_metar.air_temperature.values * units(laf_metar.units['air_temperature']),
                      laf_metar.dew_point_temperature.values * units(laf_metar.units['dew_point_temperature']))
laf_metar

from metpy.calc import altimeter_to_sea_level_pressure
altimeter_to_sea_level_pressure?

laf_metar['air_pressure_at_sea_level'] = altimeter_to_sea_level_pressure(
    laf_metar['altimeter'].values * units(laf_metar.units['altimeter']),
    laf_metar['elevation'].values * units(laf_metar.units['elevation']),
    laf_metar['air_temperature'].values * units(laf_metar.units['air_temperature'])).to(units('hPa'))
laf_metar

fig = plt.figure(figsize=(20, 16))
add_metpy_logo(fig, 75, 75)
meteogram = Meteogram(fig, laf_metar.date_time.values, laf_metar.station_id[0])
meteogram.plot_winds(laf_metar.wind_speed.values * units(laf_metar.units['wind_speed']),
                     laf_metar.wind_direction.values * units(laf_metar.units['wind_direction']),
                     laf_metar.wind_speed.values * units(laf_metar.units['wind_speed']))
meteogram.plot_thermo((laf_metar.air_temperature.values * units(laf_metar.units['air_temperature'])).to(units('degF')),
                      (laf_metar.dew_point_temperature.values * units(laf_metar.units['dew_point_temperature'])).to(units('degF')))
meteogram.plot_rh(laf_metar.rh.values*100.)
meteogram.plot_pressure(laf_metar.air_pressure_at_sea_level.values * units(laf_metar.units['air_pressure_at_sea_level']))
plt.suptitle(laf_metar.station_id[0])
plt.savefig('LAF.png')

wxt.loc[wxt['Date/Time'] > pd.datetime(2021,10,8)].head()

laf_metar.loc[laf_metar['date_time'] > pd.datetime(2021,10,8)].head()

laf_metar = laf_metar[laf_metar['date_time'].isin(wxt['Date/Time'])].drop_duplicates(subset=['date_time']).dropna(subset = ['air_temperature'])
laf_metar

wxt = wxt[wxt['Date/Time'].isin(laf_metar['date_time'])]
wxt

test = (wxt['AirTemp'].values * units('degF')).to(units('degC'))
truth = laf_metar['air_temperature'].values * units('degC')

fig = plt.figure(figsize = (10, 10))
# Scatterplot of WXT vs KLAF temperature data
# Note that I have to
plt.scatter(truth, test)
# Plot 1:1 line
plt.plot(np.arange(0, 31), np.arange(0, 31), 'k--', alpha = 0.3)
plt.axis('equal')
plt.xlim(0,30)
plt.ylim(0,30)
plt.xlabel('KLAF Temperature (deg C)')
plt.ylabel('WXT Temperature (deg C)')
plt.title('WXT vs. KLAF temperature')
plt.grid()

error = test - truth
print('Error = ', error) # print error values to the screen

N = len(test)
print('N = ', N)

bias = (1 / N) * np.nansum(error)
print('Bias = ', bias)

test = test - bias

fig = plt.figure(figsize = (10, 10))
# Scatterplot of WXT vs KLAF temperature data
# Note that I have to
plt.scatter(truth, test)
# Plot 1:1 line
plt.plot(np.arange(0, 31), np.arange(0, 31), 'k--', alpha = 0.3)
plt.axis('equal')
plt.xlim(0,30)
plt.ylim(0,30)
plt.xlabel('KLAF Temperature (deg C)')
plt.ylabel('WXT Temperature (deg C)')
plt.title('WXT vs. KLAF temperature')
plt.grid()

uncertainty = np.sqrt( (1 / (N - 1)) * np.nansum((error - bias) ** 2.) )
print('Uncertainty = ', uncertainty)

# Enter the ASOS RMSE here in degrees F:
asos_rmse = 0.9
(asos_rmse * units('delta_degree_Fahrenheit')).to('delta_degree_Celsius')

t = np.arange(-5, 5.1, 0.1) # Range of temperature differences over which to plot
# Plot the "truth" (KLAF) temperature distribution
plt.plot(t, stats.norm.pdf(t, 0, asos_rmse), 'r', label  = 'KLAF')
# Plot the "test" (WXT) temperature distribution
plt.plot(t, stats.norm.pdf(t, bias, uncertainty), 'b', label = 'WXT')
plt.grid()
plt.xlabel('Difference from truth (deg C)')
plt.ylabel('Probability')
h = plt.legend()
