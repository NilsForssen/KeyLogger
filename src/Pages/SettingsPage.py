import tkinter as tk
import os, string


class SettingsPage(tk.Frame):
    """
    Page for chaging and saving the settings of the program
    """

    def __init__(self, master, controller):

        tk.Frame.__init__(self, master)

        self.controller = controller

        self.createWidgets()


    def createWidgets(self):
        """
        Create all the interactive widgets of the page
        """

        self.saveButton = tk.Button(self,
            text="Save Settings",
            background="green2", 
            activebackground="green2",
            command=self.saveSettings)
        self.discardButton = tk.Button(self,
            text="Discard Changes", 
            background="red2",
            activebackground="red2",
            command=self.discardChanges)
        self.defaultButton = tk.Button(self,
            text="Default Settings", 
            background="royalblue2", 
            activebackground="royalblue2",
            command=self.loadDefault)

        self.entryText = tk.StringVar()
        self.validateDirText = tk.StringVar()
        self.blackListText = tk.StringVar()
        self.blackList = tk.StringVar()
        self.DPItext = tk.StringVar()
        self.whiteListText = tk.StringVar()
        self.whiteList = tk.StringVar()

        self.pngBool = tk.BooleanVar()
        self.pdfBool = tk.BooleanVar()
        self.epsBool = tk.BooleanVar()
        self.rawBool = tk.BooleanVar()

        self.entryText.set(self.controller.destinationDir)
        self.DPItext.set(self.controller.readSettings("imageDPI"))
        self.blackList.set("".join(self.controller.readSettings("blackList")))
        self.whiteList.set("".join(self.controller.readSettings("whiteList")))

        self.pngBool.set("png" in self.controller.readSettings("imageFormats"))
        self.pdfBool.set("pdf" in self.controller.readSettings("imageFormats"))
        self.epsBool.set("eps" in self.controller.readSettings("imageFormats"))
        self.rawBool.set("raw" in self.controller.readSettings("imageFormats"))

        self.unsaved = lambda *args : self.saveButton.config(
            background="yellow2",
            activebackground="yellow2")

        self.entryText.trace("w", callback=self.dirEntryCallback)
        self.DPItext.trace("w", callback=self.unsaved)
        self.pngBool.trace("w", callback=self.unsaved)
        self.pdfBool.trace("w", callback=self.unsaved)
        self.epsBool.trace("w", callback=self.unsaved)
        self.rawBool.trace("w", callback=self.unsaved)
        self.blackList.trace("w", callback=self.unsaved)
        self.whiteList.trace("w", callback=self.unsaved)
        
        blackListHeader = tk.Label(self,
            text="Blacklist Characters", 
            font="bold")
        dirHeader = tk.Label(self, 
            text="Default Directory",
            font="bold")
        imageFormatHeader = tk.Label(self,
            text="Image File Format", 
            font="bold")
        whiteListHeader = tk.Label(self,
            text="Whitelist characters", 
            font="bold")

        imageDPIHeader = tk.Label(self,
            text="DPI of image:")
        blackListHeader2 = tk.Label(self,
            text="Current blacklist:")
        whiteListHeader2 = tk.Label(self,
            text="Current whitelist:")

        self.dirEntry = tk.Entry(self, textvariable=self.entryText)
        self.blackListEntry = tk.Entry(self, textvariable=self.blackListText)
        self.DPIEntry = tk.Entry(self, textvariable=self.DPItext)
        self.whiteListEntry = tk.Entry(self, textvariable=self.whiteListText)

        def concVars(headVar, *args):
            """
            Concatenates tk.StringVar headVar in place with given variables
            """

            text = headVar.get()
            added = list(text)

            for char in "".join(list(map(lambda var : var.get() , args))).upper():
                if char in string.ascii_letters:

                    if char not in text and char not in added:
                        added.append(char)
                    elif char in text:
                        try:
                            added.remove(char)
                        except:
                            pass
                else:
                    print("{0} is not a valid character".format(char))

            headVar.set("".join(added))


        def addToBlackList(*args):
            """
            Add entry-text to blackList
            """

            self.whiteList.set("")

            concVars(*args)

            self.blackListText.set("")

            self.unsaved()


        def addToWhiteList(*args):
            """
            Add entry-text to whiteList
            """

            self.blackList.set("")

            concVars(*args)

            self.whiteListText.set("")

            self.unsaved()


        self.browseButton = tk.Button(self,
            text="Browse",
            command=self.browseDirectory)
        self.blackListButton = tk.Button(self, 
            text="Edit Entry",
            command=lambda : addToBlackList(self.blackList, self.blackListText))
        self.whiteListButton = tk.Button(self,
            text="Edit Entry",
            command=lambda : addToWhiteList(self.whiteList, self.whiteListText))

        self.blackListEntry.bind("<Return>",
            lambda e : addToBlackList(self.blackList, self.blackListText))
        self.whiteListEntry.bind("<Return>",
         lambda e : addToWhiteList(self.whiteList, self.whiteListText))

        self.pngCheck = tk.Checkbutton(self,
            text=".png",
            variable=self.pngBool)
        self.pdfCheck = tk.Checkbutton(self, 
            text=".pdf",
            variable=self.pdfBool)
        self.epsCheck = tk.Checkbutton(self, 
            text=".eps",
            variable=self.epsBool)
        self.rawCheck = tk.Checkbutton(self,
            text=".raw", 
            variable=self.rawBool)

        self.validateDirLabel = tk.Label(self,
            textvariable=self.validateDirText)
        self.blackListLabel = tk.Label(self,
            textvariable=self.blackList)
        self.whiteListLabel = tk.Label(self,
            textvariable=self.whiteList)

        dirHeader.grid(columnspan=3, column=0, row=0, sticky="W", padx=20)
        blackListHeader.grid(columnspan=3, column=3, row=0, sticky="W", padx=20)
        imageFormatHeader.grid(columnspan=3, column=0, row=3, sticky="W", padx=20)
        whiteListHeader.grid(columnspan=3, column=3, row=4, sticky="W", padx=20)

        imageDPIHeader.grid(column=1, row=5, sticky="W", padx=20)
        blackListHeader2.grid(columnspan=3, column=3, row=2, sticky="W", padx=20)
        whiteListHeader2.grid(columnspan=3, column=3, row=6, sticky="W", padx=20)

        self.dirEntry.grid(columnspan=2, column=0, row=1, sticky="WE", padx=20)
        self.blackListEntry.grid(columnspan=2, column=3, row=1, sticky="WE", padx=20)
        self.DPIEntry.grid(column=1, row=6, sticky="WE", padx=20)
        self.whiteListEntry.grid(columnspan=2, column=3, row=5, sticky="WE", padx=20)

        self.pngCheck.grid(column=0, row=4, sticky="W", padx=20)
        self.pdfCheck.grid(column=0, row=5, sticky="W", padx=20)
        self.epsCheck.grid(column=0, row=6, sticky="W", padx=20)
        self.rawCheck.grid(column=0, row=7, sticky="W", padx=20)

        self.browseButton.grid(column=2, row=1, sticky="NSEW", padx=20)
        self.blackListButton.grid(column=5, row=1, sticky="NSEW", padx=20)
        self.whiteListButton.grid(column=5, row=5, sticky="NSEW", padx=20)

        self.validateDirLabel.grid(columnspan=3, column=0, row=2, sticky="W", padx=20)
        self.blackListLabel.grid(columnspan=3, column=3, row=3, sticky="W", padx=20)
        self.whiteListLabel.grid(columnspan=3, column=3, row=7, sticky="W", padx=20)

        self.saveButton.grid(columnspan=2, column=0, row=11, sticky="NSEW", padx=20)
        self.discardButton.grid(columnspan=2, column=2, row=11, sticky="NSEW", padx=20)
        self.defaultButton.grid(columnspan=2, column=4, row=11, sticky="NSEW", padx=20)


        self.columnconfigure((0,1,2,3,4,5), weight=1, minsize=800/6)

        self.rowconfigure(11, weight=1)


    def dirEntryCallback(self, *args):
        """
        Check and alert if chosen directory is valid
        """

        if (os.path.exists(self.entryText.get())):
            self.validateDirText.set("Valid Directory")
            self.validateDirLabel.config(
                foreground="green2")
        else:
            self.validateDirText.set("Invalid Directory")
            self.validateDirLabel.config(
                foreground="red2")

        self.unsaved()


    def browseDirectory(self):
        """
        Open filebrowser for user to chose destination folder
        """
        
        path = tk.filedialog.askdirectory(
            title="Choose a directory",
            initialdir=self.controller.destinationDir).replace("/", "\\")

        if path:
            self.saveButton.config(
                background="yellow2",
                activebackground="yellow2")

            self.entryText.set(path)


    def saveSettings(self):
        """
        Save changes in this page into the config file
        """

        newSettings = {}

        if (os.path.exists(self.entryText.get())):
            newSettings["destinationDir"] = self.entryText.get()

        formats = {
            "png" : self.pngBool.get(),
            "pdf" : self.pdfBool.get(),
            "eps" : self.epsBool.get(),
            "raw" : self.rawBool.get()
        }
        newSettings["imageFormats"] = [key for key, value in formats.items() if value]

        dpi = int(self.DPItext.get())

        if dpi > 0:
            newSettings["imageDPI"] = dpi

        newSettings["blackList"] = list(self.blackList.get())
        newSettings["whiteList"] = list(self.whiteList.get())

        self.controller.changeSettings(**newSettings)

        self.saveButton.config(
            background="green2",
            activebackground="green2")


    def discardChanges(self):
        """
        Discard the changes in this page by refreshing it, reloading the config file
        """

        self.controller.loadSettings()
        self.controller.refreshFrame("SettingsPage")


    def loadDefault(self):
        """
        Load the default settings from the default config file into the config file and this page
        """

        with open("defaultConfig.json", "r") as default, open("config.json", "w") as cfg:
            cfg.write(default.read())

            cfg.close()
            default.close()

        self.controller.loadSettings()
        self.controller.refreshFrame("SettingsPage")


    def menuBar(self, root):
        """
        Return the menubar object of this page
        """

        menu = tk.Menu(root)

        menu.add_command(label="Graph", 
            command=lambda : self.controller.refreshFrame("GraphPage"))

        menu.add_command(label="Exit",
            command=self.controller.destroy)

        return menu