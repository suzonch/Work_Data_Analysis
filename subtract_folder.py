# The following program subtracts one folder from another if both folder has  same number
# of files(csv in this case), and all the files in both folder are of same number of rows and columns
import pandas as pd
import glob
# Path for 2 folders
path1 = r"/home/suzon/Work/LED_tests/long_run/long_LTW/45_LTW2/*.csv"
path2 = r"/home/suzon/Work/LED_tests/long_run/long_LTW/dark/*.csv"
counter = 0
# Using zip, we can run multiple loops in parallel
# In our case we must sort the files while reading with glob
for (fname1, fname2) in zip(sorted(glob.glob(path1)),sorted(glob.glob(path2))):
# Read files in both folder with pandas and put them in 2 dataframe
    data1 = pd.read_csv(fname1, header=None)
    df1 = pd.DataFrame(data1)
    data2 = pd.read_csv(fname2, header=None)
    df2 = pd.DataFrame(data2)
# As our filename contains unix timestamp, we can extract the timestamp slicing the filename
# Change the ranges depending on file path path manually
    timestamp = str(fname1[58:-4])
    print(timestamp)
    timestamp2 = str(fname2[54:-6])
    print(timestamp2)
# Subtract one dataframe from another, as sorted they should match the sequence
# Fill empty cell with 0 to avoid "NAN"
    df = df1.subtract(df2,fill_value = 0)
# Round to one decimal place
    df = df.round(1)
# Set all the negatives to zero
    df[df < 0] = 0
    counter = counter +1
#    print(df)
# Save each file(dataframe) including the timestamp extracted
#    df.to_csv(f"/home/suzon/Work/LED_tests/long_run/long_LTW/45_LTW2_Filtered/filteredSpec_{timestamp}.csv",header=False, index=False)
# Just to check that we're not calculating with wrong files with different timestamp
    if timestamp == timestamp2:
        print("Working...")
    else:
        raise Exception("You're in trouble!")
print(counter,"files processed and saved")