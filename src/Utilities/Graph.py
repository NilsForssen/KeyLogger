from matplotlib.figure import Figure
from matplotlib import rcParams
import matplotlib.pyplot as plt
import numpy as np

rcParams["axes.titlesize"] = 17

class BarGraph():
    """
    Class for creating a bar-graph from a data-dict
    """

    def __init__(self, dataDir={}):

        self.oldData = {}
        self.loadData(dataDir)
        self.yTicksDefault = [0,10,20,30,40,50,60,70,80,90,100]
        
    def loadData(self, newData, mode="values"):
        """
        Load the data into x and y axis,
        mode=values (default) displays the bar chart with loaded data
        mode=percent displays the bar chart y axis in percent of total
        """
        newData = dict(sorted(newData.items(),
            key=lambda nD:(nD[1], nD[0]), reverse=True))

        self.xList = [x for x in newData]

        if mode == "values":
            self.yList = [newData[x] for x in newData]

        elif mode == "percent":
            total = 0
            for x in newData:
                total += newData[x]
            self.yList = [newData[x]*(100/total) for x in newData]


    def figSetup(self,title, xlabel="X", ylabel="Y" , size=(5,5)):
        """
        Setup and return the figure used when plotting the dictionary.
        This figure can be displayed in tkinter.
        """

        self.fig, self.ax = plt.subplots(figsize=size)
        self.labels = (xlabel, ylabel)
        self.title = title
        self.setLimits()

        return self.fig


    def setLimits(self, yTicks=None):
        """
        Set x,y limits and ticks of figure
        """

        yTicks = yTicks or self.yTicksDefault
        plt.xticks(np.arange(len(self.xList)), labels=self.xList)
        plt.yticks(yTicks)

        plt.ylim(bottom=0, top=max(yTicks) * 1.1)
        plt.ylabel(self.labels[1])
        plt.xlabel(self.labels[0])
        plt.title(self.title, )

    
    def plotData(self):
        """
        Plot the loaded data in the figure
        """

        plt.clf()
        try:
            yLimits = [y + 10 for y in range(int(max(self.yList))) if y % 10 == 0]
            yLimits.append(0)
            
        except ValueError:
            yLimits = []

        
        self.setLimits(yTicks=yLimits)

        rects = plt.bar(np.arange(len(self.xList)), 
            self.yList,
            align="center")

        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width()/2,
                1.01*height, 
                str(int(round(height))),
                ha='center', va='bottom')


    def saveImg(self,*args, **kwargs):
        """
        Save an image of the figure
        """

        plt.savefig(*args, **kwargs)


if __name__ == "__main__":
    Grapher = BarGraph()    