# -*- coding: utf-8 -*-
"""combined labs.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1FOCF-dNO9VduyyxnmfCcC6MtFbVEHdpS

# lab 1
"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline  # Ensures plots are displayed inline in Jupyter Notebook

# Import necessary libraries
import pandas as pd  # For data manipulation
import matplotlib.pyplot as plt  # For plotting

# Load data from a CSV file, parsing the first column as dates and inferring datetime format
data = pd.read_csv("SC231.csv", parse_dates=[0], infer_datetime_format=True)

# Display the loaded data (for inspection)
data

# Plot Temperature over Time (automatic)
data.plot("Time (automatic)", "Temperature (deg C)")

# Create a scatter plot of Time vs Temperature with grid
data.plot.scatter("Time (automatic)", "Temperature (deg C)", grid=True)

# Access the Temperature (deg C) column
data["Temperature (deg C)"]

# Convert the Temperature column into an array of values
data["Temperature (deg C)"].values

# Plot a histogram of the Temperature values
data.hist("Temperature (deg C)")
plt.title("Temperature in SC 231")  # Set title for the histogram
plt.xlabel("Temperature (deg C)")  # Label x-axis
plt.ylabel("Frequency")  # Label y-axis

# Boxplot of Temperature (deg C)
data.boxplot("Temperature (deg C)")

# Boxplot grouped by Thermometer number
data.boxplot("Temperature (deg C)", by="Thermometer number")
plt.suptitle('')  # Suppress default title when grouping

# Boxplot grouped by Observer's initials
data.boxplot("Temperature (deg C)", by="Observer's initials")
plt.suptitle('')  # Suppress default title

# Set the instruction time as a datetime object
instruction_time = pd.to_datetime('2021-08-25T10:10:00')

# Create a new column to label rows based on whether time is before or after the instruction time
data["Instructions"] = "Before"  # Default label
data.loc[data['Time (automatic)'] > instruction_time, "Instructions"] = "After"  # Update label to 'After' for later rows

# Display the updated data with Instructions column
data

# Group the data by "Instructions" and calculate the count of Temperature readings for each group
data.groupby("Instructions")["Temperature (deg C)"].count()

# Group the data by "Instructions" and calculate the standard deviation of Temperature for each group
data.groupby("Instructions")["Temperature (deg C)"].std()

# Boxplot of Temperature grouped by the Instructions column
data.boxplot("Temperature (deg C)", by="Instructions")
plt.title('')  # Suppress default title
plt.ylabel("Temperature (deg C)")  # Label y-axis

# Import t-test from scipy for statistical analysis
from scipy.stats import ttest_ind

# Extract Temperature values for "Before" and "After" groups
T_before = data.loc[data["Instructions"] == "Before"]["Temperature (deg C)"].values
T_after = data.loc[data["Instructions"] == "After"]["Temperature (deg C)"].values

# Perform a t-test to compare the means of the two groups (Before and After)
ttest_ind(T_before, T_after, nan_policy='omit')  # 'omit' excludes NaN values in the calculation

"""# lab 2"""

# Import necessary libraries
import matplotlib.pyplot as plt  # For plotting
import pandas as pd  # For data manipulation

# Define a dictionary with data to create a DataFrame
d = {'Shady-Sunny': ['Shady', 'Shady', 'Shady', 'Shady', 'Shady', 'Sunny', 'Sunny', 'Sunny', 'Sunny', 'Sunny', 'Sunny', 'Sunny', 'Sunny'], # Case sensitive, condition for shading
     'Rad. Shield': [False, False, False, False, False, False, True, False, True, False, True, False, True], # True = Shield used, False = Shield not used
     'Kestrel Temp F': [68.8, 68.6, 70.5, 70.9, 68.6, 73.7, 73.3, 73.4, 73.2, 76.5, 76.3, 79.4, 79.1], # Temperature in Fahrenheit from Kestrel
     'KLAF Temp F': [61.0, 61.0, 61.0, 61.0, 61.0, 61.0, 61.0, 61.0, 61.0, 61.0, 61.0, 61.0, 61.0]}  # Temperature in Fahrenheit from KLAF station

# Create a DataFrame from the dictionary
df = pd.DataFrame(data=d)

# Print out the contents of the DataFrame "df" to check the data
df

# Plot Kestrel and KLAF temperatures over the measurement number
df.plot(y=['Kestrel Temp F', 'KLAF Temp F'])
plt.grid()  # Add grid lines to the plot
plt.title('Air Temperature')  # Set the plot title
plt.xlabel("Measurement number")  # Label the x-axis
plt.ylabel("Temperature (deg F)")  # Label the y-axis
plt.show()  # Display the plot

# Create a boxplot of Kestrel Temperature grouped by Shady-Sunny condition
df.boxplot("Kestrel Temp F", by="Shady-Sunny")
plt.ylabel("Temperature (deg F)")  # Label the y-axis
plt.show()  # Display the plot

# Create a boxplot of Kestrel Temperature grouped by both Shady-Sunny condition and Rad. Shield
df.boxplot("Kestrel Temp F", by=["Shady-Sunny", "Rad. Shield"])
plt.ylabel("Temperature (deg F)")  # Label the y-axis
plt.show()  # Display the plot

# Calculate the temperature difference between Kestrel and KLAF (Kestrel-KLAF) and add as a new column
df['Kestrel-KLAF'] = df['Kestrel Temp F'] - df['KLAF Temp F']

# Print out the updated DataFrame with the new column "Kestrel-KLAF"
df

# Create a boxplot of the temperature difference (Kestrel-KLAF) grouped by Shady-Sunny condition and Rad. Shield
df.boxplot("Kestrel-KLAF", by=["Shady-Sunny", "Rad. Shield"])
plt.ylabel("Temperature difference (deg F)")  # Label the y-axis
plt.show()  # Display the plot

# Group the data by Shady-Sunny and Rad. Shield, then calculate the mean of the temperature columns
df.groupby(["Shady-Sunny", "Rad. Shield"]).mean()

"""# lab 4"""

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline  # Ensures that plots are displayed inline in Jupyter Notebook

# Import necessary libraries
import numpy as np  # For numerical operations
import pandas as pd  # For data manipulation
import matplotlib.pyplot as plt  # For plotting
import seaborn as sns  # For advanced statistical plotting
import scipy.stats as stats  # For statistical functions (e.g., normal distribution)

# Load the Columbian Park dataset and parse the 'observation_time' column as dates
cp = pd.read_csv('columbian_park_2021.csv', parse_dates=['observation_time'])

# Add a descriptive name for the station instead of the default station code
cp['name'] = 'Columbian Park'
cp  # Display the loaded Columbian Park data

# Load the Pedestrian Bridge dataset and parse the 'observation_time' column as dates
pb = pd.read_csv('pedestrian_bridge_2021.csv', parse_dates=['observation_time'])
pb  # Display the loaded Pedestrian Bridge data

# Identify the earliest observation time in the Columbian Park data
startDate = cp['observation_time'].min()  # Should be on 26 March 2021
print("Start Date: ", startDate)

# Filter the Pedestrian Bridge data to start from the same start date as Columbian Park
pb = pb[pb['observation_time'] >= startDate]
pb  # Display the filtered Pedestrian Bridge data

# Keep only rows where the observation times match between both datasets
pb = pb[pb['observation_time'].isin(cp['observation_time'])]  # Drop unmatched rows from Pedestrian Bridge
cp = cp[cp['observation_time'].isin(pb['observation_time'])]  # Drop unmatched rows from Columbian Park

# Print the length of the filtered data for both locations
print("Length of Columbian Park data: ", len(cp))
print("Length of Pedestrian Footbridge data: ", len(pb))

# Scatter plot comparing wind gust speeds from both locations
fig = plt.figure(figsize=(6, 6))  # Create a figure with specific size
plt.scatter(cp['wind_gust_speed_mph'], pb['wind_gust_speed_mph'])
plt.plot([0, 20], [0, 20], 'k--', label="1:1 line")  # Add a 1:1 reference line
plt.axis('equal')  # Ensure equal scaling of x and y axes
plt.grid()  # Add a grid to the plot
plt.xlabel('Columbian Park wind speed')  # Label x-axis
plt.ylabel('Pedestrian Bridge wind speed')  # Label y-axis
plt.xticks(np.arange(0, 25, 5))  # Place x-ticks every 5 units from 0 to 25
plt.yticks(np.arange(0, 25, 5))  # Place y-ticks every 5 units from 0 to 25
plt.title('Scatterplot of WHIN wind speeds')  # Set plot title
plt.legend()  # Display legend

# Combine the data from both locations into one DataFrame
whin = cp.append(pb, ignore_index=True)
whin  # Display the combined data

# Calculate and display the mean wind speed for each location
whin.groupby(by='name')['wind_speed_mph'].mean()

# Line plot of wind speeds over time for both locations
fig = plt.figure(figsize=(10, 6))  # Create a larger figure for the plot
ax = plt.subplot(111)  # Add a subplot to the figure
sns.lineplot(data=whin, x='observation_time', y='wind_speed_mph', hue='name')  # Create the line plot
fig.autofmt_xdate()  # Rotate and scale x-axis time labels for readability
plt.title('WHIN wind speeds in 2021')  # Set plot title

# Histogram of wind speeds with separate distributions for each location
sns.histplot(data=whin, x='wind_speed_mph', hue='name', bins=np.arange(0, 20, 1))

# Jointplot to visualize the relationship between wind speeds from both locations
sns.jointplot(x=cp["wind_speed_mph"], y=pb["wind_speed_mph"], kind="hist")

# Boxplot of wind speeds by location (Columbian Park vs Pedestrian Bridge)
fig = plt.figure(figsize=(6, 6))
sns.boxplot(data=whin, x="name", y="wind_speed_mph")
plt.ylabel("Wind Speed (mph)")  # Label y-axis
plt.show()  # Display the plot

# Calculate and display the mean wind gust speed for each location
whin.groupby(by='name')['wind_gust_speed_mph'].mean()

# Histogram of wind gust speeds with separate distributions for each location
sns.histplot(data=whin, x='wind_gust_speed_mph', hue='name', bins=np.arange(0, 30, 1))

# Filter out rows where wind gust speed is 0 mph
whin = whin[whin['wind_gust_speed_mph'] > 0.]  # Keep only gusts > 0 mph

# Calculate and display the mean wind gust speed for each location after filtering
means = whin.groupby(by='name')['wind_gust_speed_mph'].mean()
means  # Display the calculated means

# Calculate and display the standard deviation of wind gust speeds for each location
stds = whin.groupby(by='name')['wind_gust_speed_mph'].std()
stds  # Display the calculated standard deviations

# Plot the normalized probability distribution of wind gust speeds for both locations
speeds = np.arange(1, 25, 1)  # Define a range of wind gust speeds
for loc, color in zip(['Columbian Park', 'Pedestrian Bridge'], ['darkblue', 'darkorange']):
    # Plot vertical lines at the mean wind gust speeds
    plt.plot([means[loc], means[loc]], [0, 0.1], color=color, label=loc)
    # Fill the area under the normal distribution curve for each location
    plt.fill_between(speeds, stats.norm.pdf(speeds, means[loc], stds[loc]), color=color, alpha=0.5)

# Display the legend, labels, and title for the plot
plt.legend(title='Location')
plt.xlabel('Wind gust speed (mph)')
plt.ylabel('Normalized probability')
plt.title('Wind Gust Probabilities')