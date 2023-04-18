import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import zipfile
import tempfile
# import os
import seaborn as sb
sb.set_theme()

def roundCond(num):
    if num > 1:
        return round(num, 2)
    else:
        return round(num, 7)

def calc_stats(arr, name):
    z = 1.96

    iterNum = arr.shape[0] - 1
    arr = arr[1:iterNum]
    # n = arr.shape[0]

    min = roundCond(arr.min())
    max = roundCond(arr.max())
    mean = roundCond(arr.mean())
    std = roundCond(arr.std())
    q1 = roundCond(np.quantile(arr, 0.25))
    median = roundCond(np.median(arr))
    q3 = roundCond(np.quantile(arr, 0.75))
    cl95_low = roundCond(mean - (z * std) / (iterNum)**(0.5))
    cl95_up = roundCond(mean + (z * std) / (iterNum)**(0.5))

    return {"Name": name, "Min": min, "Max": max, "Mean": mean, "St. dev.": std, 
            "Q1": q1, "Median": median, "Q3": q3, "Cl 95% Lower": cl95_low, "Cl 95% Upper": cl95_up}

def calc_before_after(car_scoot, name):
    # car_scoot is a list [car, scoot] with same car/scooter variables
    car = car_scoot[0]
    scoot = car_scoot[1]

    iterNum = car.shape[0]
    
    before = roundCond(car[0] + scoot[0])
    after = roundCond(car[iterNum-1] + scoot[iterNum-1])
    diff = roundCond(((after - before) / before) *100)

    return { "Name": name, "Before": before, "After": after, "Diff %": diff}

def boxplot(arrays, colNames, title, yLabel):
    # If more than one arrays then concatenate
    if len(arrays) > 1:
        shape = arrays[0].shape[0]
        arrConc = np.concatenate([arrays[0].reshape(shape, 1), 
                                    arrays[1].reshape(shape, 1)], axis=1)
    else:
        arrConc = arrays[0]
    
    df = pd.DataFrame(arrConc, columns=colNames)
    ax = df.plot(kind='box',
                 figsize=(8,8),
                 boxprops=dict(linestyle='-', linewidth=1.5, color="red"),
                 medianprops=dict(linestyle='-', linewidth=1.5, color="blue"),
                 whiskerprops=dict(linestyle='--', linewidth=1.0, color="magenta"),
                 capprops=dict(linestyle='-', linewidth=.75, color="green"),
                 flierprops=dict(marker='o', markeredgecolor='g', markersize=3),
                 showfliers=True, 
                 grid=True, 
                 rot=0)
    ax.set_xlabel('Mode')
    ax.set_ylabel(yLabel)
    ax.set_title(title)

    # Save in a temp file
    tempFile = tempfile.NamedTemporaryFile(suffix='.png')
    plt.savefig(tempFile, dpi=300, facecolor='white')

    # plt.show()

    return tempFile

def descrstat(carCO2, carCOST, carSAFETY, 
              escootCO2, escootCOST, escootSAFETY):
    # print(carCO2)
    tables = {"Car CO2": carCO2,
              "E-Scooter CO2": escootCO2,
              "Car cost": carCOST,
              "E-scooter cost": escootCOST,
              "Car safety": carSAFETY,
              "E-scooter safety": escootSAFETY}
    
    # colNames = list(tables.keys())
    dataStats = []
    for key, val in tables.items():
        dataStats.append(calc_stats(val, key))
    
    df = pd.DataFrame(dataStats)
    
    print(df)    
    return df

def perchange(carVKM, escootVKM,
              carCO2, carCOST, carSAFETY, 
              escootCO2, escootCOST, escootSAFETY):
    
    iterNum = carVKM.shape[0]
    
    car_co2_change = np.zeros(iterNum)
    car_co2_change_per = np.zeros(iterNum-1)
    escoot_co2_change = np.zeros(iterNum)
    escoot_co2_change_per = np.zeros(iterNum-1)
    
    for i in range(iterNum):
        car_co2_change[i] = carCO2[i] - carCO2[0]
        escoot_co2_change[i] = escootCO2[i] - escootCO2[0]

    # total_co2_change = carCO2 + escootCO2
    for i in range(1, iterNum):
        car_co2_change_per[i-1] = car_co2_change[i] / carCO2[0]
        escoot_co2_change_per[i-1] = escoot_co2_change[i] / escootCO2[0]
        
    car_scoots = [
        [carVKM, escootVKM],
        [carCO2, escootCO2],
        [carCOST, escootCOST],
        [carSAFETY, escootSAFETY]]
    
    names = ['Vehicle/km', 'CO2 (kg)', 'Cost of use (€)', 'Safety (fatalities)']
    dataBA = []
    
    for i, car_scoot in enumerate(car_scoots):
        dataBA.append(calc_before_after(car_scoot=car_scoot, name=names[i]))

    df = pd.DataFrame(dataBA)
   
    return df

