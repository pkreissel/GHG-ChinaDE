import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import sys
from matplotlib.animation import FuncAnimation
import math
import calendar
import matplotlib.image as image


population = pd.read_csv("Population.csv", skiprows = 3)
co2 = pd.read_csv("CO2.csv")

fig = plt.figure(figsize=(14,14))
ax= plt.subplot(aspect='equal')

plt.axis('off')
ax.set_title("Persönliche CO2-Emissionen jedes 50-Jährigen \n (1967-2016)", color='white', fontdict={'fontsize': 35}, ha ="center")
ax.text(-0.1,-0.1, "Sources> CO2 Emissions: PIK, population: Worldbank", color = "white", size=10, transform=ax.transAxes)
ax.text(0.95,-0.1, "@pkreissel \n @volksverpetzer", color = "white", size=15, transform=ax.transAxes)

imc = image.imread('chn.png')
imde = image.imread('de.png')
ax.imshow(imc, aspect='auto', extent=(0.68, 0.82, .8, .9), zorder=-1, transform=ax.transAxes)
ax.imshow(imde, aspect='auto', extent=(0.18, 0.33, .8, .9), zorder=-1, transform=ax.transAxes)

#fig.show()

#popnow = population.loc[population["Country Name"] == "Germany"]
co2_de = co2[co2.columns[-50:]].loc[(co2["country"] == "DEU") & (co2["entity"] == "KYOTOGHG") & (co2["category"] == "IPCM0EL") & (co2["scenario"] == "HISTTP")]
co2_c = co2[co2.columns[-50:]].loc[(co2["country"] == "CHN") & (co2["entity"] == "KYOTOGHG") & (co2["category"] == "IPCM0EL") & (co2["scenario"] == "HISTTP")]
popend = population[population.columns[-52:-2]].loc[population["Country Name"] == "Germany"].mean(axis = 1)
co2end = co2_de.sum(axis = 1)
maximum = popend.iloc[0] / co2end.iloc[0]*1000
print(maximum)
chn = 0
deu = 0

plt.ylim(0,800)
plt.bar(["deu","chn"], height = [deu, chn])

def update(i):
    global deu
    global chn
    print(i)
    ax.text(0.5,0, "{:2d} Jahre alt \n {:4d}".format(i, 2016 - 49 + i) , transform=ax.transAxes, color="black", backgroundcolor = '#ffffff', size = 25, ha ="center")

    popnow = population.loc[population["Country Name"] == "Germany"][str(2016 - 49 + i)]
    co2now = co2_de[str(2016 - 49 + i)]
    yvalue = (co2now.iloc[0] / popnow.iloc[0])
    deu = deu + yvalue*1000
    percent = deu/maximum
    print(yvalue*1000)
    ax.text(0.25,0.15, "{:06.2f} \n Tonnen CO2eq".format(deu) , transform=ax.transAxes, color="white", backgroundcolor = '#323331', size = 25, ha ="center")

    popnow = population.loc[population["Country Name"] == "China"][str(2016 - 49 + i)]
    co2now = co2_c[str(2016 - 49 + i)]
    yvalue = (co2now.iloc[0] / popnow.iloc[0])
    chn = chn + yvalue*1000
    percent = chn/maximum
    ax.text(0.75 ,0.15, "{:06.2f} \n Tonnen CO2eq".format(chn) , transform=ax.transAxes, color="white", backgroundcolor = '#323331', size = 25, ha ="center")
    plt.bar(["deu","chn"], height = [deu, chn], color = ["black", "red"])

def init():
    pass

anim = FuncAnimation(fig, update, frames=50, interval=200, repeat_delay = 4000, repeat = True, init_func = init)

anim.save('ghg.gif', dpi=120, writer='pillow', savefig_kwargs={'facecolor': '#323331'})
