import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def main():
    
    df = pd.read_csv("./data.csv")
    object1 = df[["FirstObjectDistance_X", "FirstObjectDistance_Y"]]
    
    object1[object1 == 0] = np.nan
    
    
    object1["FirstObjectDistance_X"].interpolate(method='polynomial', order=3, inplace=True)
    plt.plot(object1["FirstObjectDistance_X"], object1["FirstObjectDistance_Y"])
    
    plt.show()
    pass



if __name__ == "__main__":
    main()