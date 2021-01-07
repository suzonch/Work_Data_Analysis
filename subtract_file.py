import pandas as pd
import tkinter as tk
from tkinter import filedialog


class filter_file:
    def subtract_file():
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        file_path2 = filedialog.askopenfilename()
        data1 = pd.read_csv(file_path, header=None)
        df1 = pd.DataFrame(data1)
        data2 = pd.read_csv(file_path2, header=None)
        df2 = pd.DataFrame(data2)
        timestamp = str(file_path[46:-4])
        timestamp2 = str(file_path2[42:-6])
        print(timestamp)
        print(timestamp2)
        if timestamp == timestamp2:
            print("works")
#        else:
#            raise Exception("Different file")
        df = df1.subtract(df2, fill_value=0)
        return df
    print(subtract_file())
    subtract_file().to_csv(f"/home/suzon/spec_filtered_verify{timestamp}.csv",header=False, index=None)