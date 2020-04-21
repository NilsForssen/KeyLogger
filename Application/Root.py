import tkinter as tk
import os, json, sys
from Pages import GraphPage, SettingsPage

class Root(tk.Tk):
    """
    Root class of tkinter application
    """

    def __init__(self):

        tk.Tk.__init__(self)

        self.loadSettings()

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (GraphPage.GraphPage, SettingsPage.SettingsPage):
            pageName = F.__name__
            frame = F(master=self.container, controller=self)
            self.frames[pageName] = frame
            frame.grid(row=0, column=0, sticky="NSEW")

        with open("defaultConfig.json", "r") as cfg:
            settings = json.load(cfg)
            settings["destinationDir"] = os.path.dirname(os.path.abspath(__file__))

        with open("defaultConfig.json", "w") as cfg:
            json.dump(settings, cfg, indent=4)

        self.showFrame("GraphPage")


    def loadSettings(self):
        """
        Load the application wide settings
        """

        with open("config.json", "r") as cfg:
            settings = json.load(cfg)

        with open("config.json", "w") as cfg:
            json.dump(settings, cfg, indent=4)

        self.thisDir = os.path.dirname(os.path.abspath(__file__))

        if not settings["destinationDir"]:
            self.destiantionDir = self.changeSettings(destinationDir=self.thisDir)

        self.destinationDir = settings["destinationDir"]

        self.iconbitmap(os.path.join(self.thisDir, "Sprites/icon.ico"))
        self.resizable(False, False)
        self.geometry(newGeometry="{0}x{1}+{2}+{3}".format(
            settings["winX"],
            settings["winY"],
            settings["offsetX"],
            settings["offsetY"]))


    def readSettings(self, *args):
        """
        Returns values of the given settings
        """

        with open("config.json", "r") as cfg:
            settings = json.load(cfg)

            if len(args) - 1:
                return {key:settings[key] for key in args}
            else:
                return settings[args[0]]


    def changeSettings(self, **kwargs):
        """
        Change given settings
        """

        with open("config.json", "r") as cfg:
            settings = json.load(cfg)
            for setting, value in kwargs.items():
                settings[setting] = value

        with open("config.json", "w") as cfg:
            json.dump(settings, cfg, indent=4)

        self.loadSettings()

        return kwargs.values()


    def showFrame(self, pageName):
        """
        Raise frame of given page name
        """

        frame = self.frames[pageName]
        menuBar = frame.menuBar(self)
        self.config(menu=menuBar)
        frame.tkraise()

    def refreshFrame(self, pageName):

        frame = self.frames[pageName]

        frame.grid_forget()
        
        self.frames[pageName].__init__(
            master=self.container, 
            controller=self)

        self.frames[pageName].grid(row=0, column=0, sticky="NSEW")

        menuBar = self.frames[pageName].menuBar(self)
        self.config(menu=menuBar)
        self.frames[pageName].tkraise()


if __name__ == "__main__":
    app = Root()
    app.mainloop()

