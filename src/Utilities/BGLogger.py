from pynput.keyboard import Key, Listener, Controller
import string

class KeyboardLogger():
    """
    Class for logging the keyboard in another thread
    Key presses are stored in dictinoary keyDict
    """

    def __init__(self, stop=Key.f12):

        self.logging = False
        self.stopButton = stop

        self.keyDict = {}
        self.wordDict = {}
        self.allowed = string.ascii_uppercase

        self.blackList = []
        self.whiteList = []
    

    def setBlackList(self, blist):
        """
        Set black-list to string of characters and empties white-list.
        Returns new black-list
        """

        self.blackList = blist
        self.whiteList.clear()

        return self.blackList


    def setWhiteList(self, wlist):
        """
        Set white-list to string of characters and empties black-list.
        Returns new white-list
        """

        self.whiteList = wlist
        self.blackList.clear()

        return self.whiteList


    def getBlackList(self):
        """
        Get string of current black-list
        """

        return self.blackList


    def getWhiteList(self):
        """
        Get string of current white-list
        """

        return self.whiteList


    def addSpecialChars(self, charList):
        """
        Add a list of characters to be logged.
        Characters of modifiers are not tracked.
        """

        self.allowed += "".join(charList)
        return self.allowed


    def on_press(self, key):
        """
        Add the given keypress to the dictionary if the key is not some arbitrary symbol.
        """

        if self.checkStop(key):
            try:
                upperKey = key.char.upper()
                if upperKey in self.allowed:
                    if (not self.blackList and not self.whiteList) or ((self.blackList and upperKey not in self.blackList) or (self.whiteList and upperKey in self.whiteList)):
                        print(upperKey)
                        if upperKey in self.keyDict:
                            self.keyDict[upperKey] += 1
                        else:
                            self.keyDict[upperKey] = 1
            except:
                pass
            
        

    def checkStop(self, key):
        """
        Return if the given key is the stopkey.
        If True, this will also stop the logging.
        """

        if key is self.stopButton:
            self.toggle()
        return self.logging


    def toggle(self):
        """
        Toggle the logging
        """

        if self.logging:
            print("Logging Stopped")
            self.logging = False
            self.keyListener.stop()
        else:
            print("Logging Started")
            self.logging = True
            self.run()
        return self.logging


    def flush(self):
        """
        Flush the data-dictionaries
        """

        self.keyDict = {}
        self.wordDict = {}


    def run(self):
        """
        Runs the keyListener
        """

        self.keyListener = Listener(on_press=self.on_press)
        self.keyListener.start()

    def stop(self):
        """
        Stop logger
        """
        self.keyListener.stop()


if __name__ == "__main__":
    x = KeyboardLogger()
    x.toggle()

