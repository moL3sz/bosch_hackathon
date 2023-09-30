import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math


def main():
    
    df = pd.read_csv("./data.csv")
    df["Vector"] = np.sqrt((df["FirstObjectDistance_X"] - (df["FirstObjectSpeed_X"] + df["FirstObjectDistance_X"]))**2 + \
        (df["FirstObjectDistance_Y"] - (df["FirstObjectSpeed_Y"] + df["FirstObjectDistance_Y"]))**2)
    
   
    plt.plot(df["Timestamp"],[df["FirstObjectDistance_X"],df["FirstObjectDistance_Y"]], )
    
    plt.show()
    pass



if __name__ == "__main__":
    main()