import sys, re
try:
    from PyQt5.QtSvg import QSvgWidget
except ImportError:
    QSvgWidget = None

from pjanice import *
from PyQt5.QtWidgets import QDialog, QApplication, QTabWidget, QTableWidgetItem, QCheckBox
from PyQt5.QtCore import QSettings, QVariant, Qt, QEvent
from PyQt5.Qt import pyqtSlot, pyqtSignal
from stdcomqt5 import *
from stdcomqt5widget import *



class pjaniceGeneric(QDialog):

    """
    Stec OPCUA Server used fpr anyone whishing use or make a OPCUA Server to Multiverse
    """

    MultiverseHostname = None
    MultiversePort = None

    cBridge = None
    currentSub = ""
    data = []
    suspectTable = False


    def __init__(self, cBridge : stdcomPyQt = None):
        """
         def __init__(self, cBridge : stdcomPyQt = None):
        :param cBridge: If you are passing a cBridge and it is controlled here, pass it else it will make one
        """

        super().__init__()
        self.ui =  Ui_pjanice()
        self.ui.setupUi(self)

        self.show()
        self.treeViewTags = stdcomqt5qtreeMorph(self.ui.treeWidgetUI, ["hello.there"], self)

        self.treeViewTags.newTextSignal.connect(self.slotSelected)
        self.MultiverseHostname = self.ui.lineEditIpAddress.text()
        self.MultiversePort = int(self.ui.lineEditServicePort.text())

        if cBridge is not None:
            self.cBridge = cBridge
        else:
            self.cBridge = stdcomPyQt()


        self.cBridge.sigNames.connect(self.slotNames)
        self.cBridge.sigNewData.connect(self.slotNewData)
        self.cBridge.sigNewDesc.connect(self.slotDesc)

        self.LoadConfig()
        self.ui.pushButtonConfigure.clicked.connect(self.SaveConfig)

        self.ui.tableWidgetData.itemChanged.connect(self.on_any_itemChanged)



    def closeEvent(self, event: QEvent = None):
        """
        internal use
        :param event:
        :return:
        """
        if self.cBridge is not None:
            self.cBridge.terminate()
            self.cBridge = None
        event.accept()

    @pyqtSlot(list)
    def slotNames(self, names):
        self.treeViewTags.AddNames(names)

    @pyqtSlot(str,str)
    def slotDesc(self, name, desc) :
        self.treeViewTags.AddDesc(name,desc)
        if name == self.currentSub :
            self.ui.plainTextEditDesc.clear()
            self.ui.plainTextEditDesc.insertPlainText(desc)


    @pyqtSlot(str, str)
    def slotSelected(self, name, desc):
        if self.currentSub != "" :
            self.cBridge.unsubscribe(self.currentSub)

        self.currentSub = name
        self.cBridge.subscribe(name)

        self.ui.lineEditTag.setText(name)
        self.ui.plainTextEditDesc.clear()
        if desc != "" :
            self.ui.plainTextEditDesc.insertPlainText(desc)


    @pyqtSlot(str, list)
    def slotNewData(self, name, data):
        """
        data as it comes in from Multiverse
        :param name:
        :param data:
        :return:
        """
        if name == self.currentSub :
            self.ui.tableWidgetData.clear()
            self.ui.tableWidgetData.setRowCount(len(data))
            self.ui.tableWidgetData.setColumnCount(1)

            self.suspectTable = True
            self.data = data
            for i in range(0,len(data) ) :
                d = QTableWidgetItem( str(data[i]))
                self.ui.tableWidgetData.setItem(i,0, d)

            self.suspectTable = False

    @pyqtSlot()
    def SaveConfig(self):

        """
        Saves all setup data
        :return:
        """

        settings = VSettings("stec-pjanice")
        self.MultiverseHostname = self.ui.lineEditIpAddress.text()
        self.MultiversePort = int(self.ui.lineEditServicePort.text())

        settings.setValue('MultiverseHostname', self.MultiverseHostname)
        settings.setValue('MultiversePort', self.MultiversePort)

        settings.sync()

        if self.cBridge is not None:
            self.cBridge.terminate()

        self.cBridge.setDestination(self.MultiverseHostname, self.MultiversePort)
        self.cBridge.LoadcBridge()


    @pyqtSlot()
    def LoadConfig(self):
        """
        loads all configurations
        :return:
        """
        settings = VSettings("stec-pjanice")
        self.MultiverseHostname = str(settings.value("MultiverseHostname", self.MultiverseHostname))
        self.MultiversePort = int(settings.value("MultiversePort", self.MultiversePort))
        self.ui.lineEditIpAddress.setText(self.MultiverseHostname)
        self.ui.lineEditServicePort.setText(str(self.MultiversePort))

        if self.cBridge is not None:
            self.cBridge.terminate()

        self.cBridge.setDestination(self.MultiverseHostname, self.MultiversePort)
        self.cBridge.LoadcBridge()

    @pyqtSlot(QTableWidgetItem )
    def on_any_itemChanged(self, itm : QTableWidgetItem ) :
        c = itm.column()
        r = itm.row()

        if self.suspectTable is False :
            print("Changed R/C ", r, "/", c, itm.text())
            if r < len(self.data) :
                self.data[r] = itm.text()
                self.cBridge.writeValues(self.currentSub, self.data)



if __name__ == "__main__":
    """
    bumped version
    """
    if "--version" in sys.argv:
        print("1.5.0")
        sys.exit()

    nextProject = False


    app = QApplication(sys.argv)

    window = pjaniceGeneric()
    window.setWindowTitle("Stec PJanice Viewer")

    window.show()  # IMPORTANT!!!!! Windows are hidden by default.

    # Start the event loop.
    app.exec_()
    window.Terminate()