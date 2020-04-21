import tkinter as tk
from Utilities import BGLogger, Graph
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class GraphPage(tk.Frame):

    def __init__(self, master, controller):

        tk.Frame.__init__(self, master)

        self.controller = controller
        self.Logger = BGLogger.KeyboardLogger()
        self.Grapher = Graph.BarGraph()

        self.createWidgets()

    def setLists(self):
        """
        Set black and white-list of keyboardlogger
        """

        # Set blackList, if empty, set instead whiteList
        blackList, whiteList = self.controller.readSettings("blackList", "whiteList").values()
        if blackList:
            self.Logger.setBlackList(blackList)
        elif whiteList:
            self.Logger.setWhiteList(whiteList)


    def createWidgets(self):

        self.setLists()

        self.rowconfigure((0,1,2), weight=1)
        self.columnconfigure(1, weight=1)

        def saveImg():

            fTypes, dpi = self.controller.readSettings("imageFormats", "imageDPI").values()


            """
            I know the following line isnt very practical
            but hey, who doesn't like a one-liner
            """
            fileTypeList = tuple(map(lambda f, t : tuple((s+t) for s in f), [("", "*.")]*len(fTypes), fTypes))

            location = tk.filedialog.asksaveasfilename(
                initialdir=self.controller.destinationDir,
                title="save image",
                defaultextension="png",
                filetypes=fileTypeList)

            name, ext = os.path.splitext(location)
            if location:
                self.Grapher.saveImg(location, format=ext.replace(".", ""), dpi=dpi)


        self.keyLogButton = tk.Button(self,
            text="Start logging", 
            background="green2",
            activebackground="green2",
            command=lambda : self.setToggleState(self.Logger.toggle()))
        self.graphButton = tk.Button(self,
            text="Update Graph",
            background="yellow2",
            activebackground="yellow2",
            command=self.plotData)
        self.saveImgButton = tk.Button(self,
            text="Save Image",
            background="royalblue1",
            activebackground="royalblue1",  
            command=saveImg)

        self.graphCanvas = FigureCanvasTkAgg(self.Grapher.figSetup(
            title="Letter Frequency",
            xlabel="Character",
            ylabel="Percentage (%)",
            size=(10, 6)), master= self)
        

        self.keyLogButton.grid(row=0, column=0, sticky="NSEW")
        self.graphButton.grid(row=1, column=0 ,sticky="NSEW")
        self.saveImgButton.grid(row=2, column=0, sticky="NSEW")

        self.graphCanvas.get_tk_widget().grid(
           row=0, rowspan=3, column=1, sticky="NSEW")


    def setToggleState(self, default=None):

        toggleBool = default or self.Logger.logging

        if toggleBool:

            self.keyLogButton.config(
                text="Stop logging",
                relief="raised",
                background="red2",
                activebackground="red2")

            self.after(100, self.setToggleState)
        else:

            self.setLists()

            self.keyLogButton.config(
                text="Start logging",
                relief="raised",
                background="green2",
                activebackground="green2")


    def plotData(self, event=None):

        self.Grapher.loadData(self.Logger.keyDict, mode="percent")
        self.Grapher.plotData()
        self.graphCanvas.draw()


    def menuBar(self, root):

        def newLOG():

            self.Logger.flush()
            self.plotData()

        def readLOGFile(self, path):

            try:
                with open(path, mode="r") as file:
                    newDict = {}
                    for line in file.readlines():
                        line = line.replace("'", "")
                        key, value = line.split(":")
                        newDict[key.strip()] = int(value.strip())
                    return newDict

            except IOError:
                print("{} not found".format(path))


        def writeLOGFile(self, path, dataDict):

            try:
                with open(path, mode="w") as file:
                    for key in dataDict:
                        file.write("{}:{}\n".format(key, dataDict[key]))

            except:
                print("Unable to open file")


        def loadLOGFile(self, replace=True):

            if self.Logger.logging:
                self.Logger.keyLogToggle()

            filePath = tk.filedialog.askopenfilename(
                initialdir=self.controller.destinationDir,
                title="Select file",
                filetypes=(("log files", "*.LOG"),))

            self.Logger.keyDict = self.readLOGFile(filePath)


        def saveNewLOGFile(self):

            if self.Logger.logging:
                self.keyLogToggle()

            filePath = tk.filedialog.asksaveasfilename(
                initialdir=self.controller.destinationDir,
                defaultextension=".dat",
                title="Create file",
                filetypes=(("log file", "*.LOG"),))

            self.writeLOGFile(filePath, self.Logger.keyDict)


        def saveToLOGFile(self):

            if self.Logger.logging:
                self.keyLogToggle()

            filePath = tk.filedialog.askopenfilename(
                initialdir=self.controller.destinationDir, 
                title="Select file", 
                filetypes=(("log file", "*.LOG"),))

            oldData = self.readLOGFile(filePath)
            newData = self.Logger.keyDict

            for key in oldData:
                if key in newData:
                    newData[key] += oldData[key]
                else:
                    newData[key] = oldData[key]

            self.writeLOGFile(filePath, self.Logger.keyDict)

        menu = tk.Menu(root)

        filemenu = tk.Menu(menu, tearoff=0)
        filemenu.add_command(label="New Log", command=newLOG)
        filemenu.add_command(label="Open Log", command=loadLOGFile)
        filemenu.add_command(label="Save As", command=saveNewLOGFile)
        filemenu.add_command(label="Save To", command=saveToLOGFile)

        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.controller.destroy)
        menu.add_cascade(label="File", menu=filemenu)

        helpmenu = tk.Menu(menu, tearoff=0)
        helpmenu.add_command(label="About")
        menu.add_cascade(label="Help", menu=helpmenu)

        menu.add_command(label="Settings",
            command=lambda : self.controller.showFrame("SettingsPage"))
        menu.add_command(label="Exit", 
            command=self.controller.destroy)

        return menu
