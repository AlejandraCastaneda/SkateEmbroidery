#%%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#%%       # clean original CSV file 

# Read the CSV file into a Pandas DataFrame
data = pd.read_csv('/Users/alejc/OneDrive/Desktop/CS181MCS/skateembroidery/data/UCDavis.csv')

# Display the columns in the DataFrame
print("Columns before removing:")
print(data.columns.tolist())

# Remove a columns
columns_to_remove = ['track_fid','track_seg_id','track_seg_point_id','ele','time','magvar','geoidheight'
                    ,'name','cmt','desc','src','link1_href','link1_text','link1_type','link2_href','link2_text'
                    ,'link2_type','sym','type','fix','sat','hdop','vdop','pdop','ageofdgpsdata','dgpsid']
for c in columns_to_remove:
    if c in data.columns:
        data.drop(columns=c, inplace=True)
    else:
        print(f"Column '{c}' not found.")

# Display the columns in the modified DataFrame
print("\nColumns after removing:")
print(data.columns.tolist())

# Write the modified DataFrame to a new CSV file
# data.to_csv('Clean_UCD.csv', index=False)  # Set index=False to avoid writing row indices

#%%     # find max / min 

# Read the CSV file into a DataFrame
data = pd.read_csv('/Users/alejc/OneDrive/Desktop/CS181MCS/skateembroidery/data/clean_UCD.csv')

# Display the maximum and minimum values for each column
for column in data.columns:
    if pd.api.types.is_numeric_dtype(data[column]):
        max_value = data[column].max()
        min_value = data[column].min()
        print(f"Column '{column}': Max = {max_value}, Min = {min_value}")

#%%          # Normalize 

update = pd.read_csv('/Users/alejc/OneDrive/Desktop/CS181MCS/skateembroidery/data/clean_UCD.csv')

# Calculate the ranges for X and Y coordinates
x_min, x_max = update['X'].min(), update['X'].max()
y_min, y_max = update['Y'].min(), update['Y'].max()

# Define the target ranges for the 200x300 coordinate plane
x_target_min, x_target_max = 0, 200
y_target_min, y_target_max = 0, 300

# Calculate the scaling factors for X and Y coordinates
x_scaling_factor = (x_target_max - x_target_min) / (x_max - x_min)
y_scaling_factor = (y_target_max - y_target_min) / (y_max - y_min)

# Apply proportional scaling to the X and Y coordinates
update['X'] = ((update['X'] - x_min) * x_scaling_factor + x_target_min).round(2)
update['Y'] = ((update['Y'] - y_min) * y_scaling_factor + y_target_min).round(2)

update.to_csv('normUCD.csv', index=False)  # Set index=False to avoid writing row indices

#%%       # find velocities 

updatedX = update['X'][ :: 10].to_numpy()
updatedY =  update['Y'][ :: 10].to_numpy()

velocity = [0]

# calculates velocity using the pythagreom thm 
for i in range(1, len(updatedX)):
    currentX = updatedX[i]
    currentY = updatedY[i]

    prevX = updatedX[i - 1]
    prevY = updatedY[i - 1]

    x = (currentX - prevX) ** 2
    y = (currentY - prevY) ** 2

    velocity.append(np.sqrt(x + y))

#%%      # Plot Scatter plot 

# plots a scatter plot of X,Y points lighter points are faster velocity 
plt.scatter(updatedX, updatedY, c=velocity)

# %%
