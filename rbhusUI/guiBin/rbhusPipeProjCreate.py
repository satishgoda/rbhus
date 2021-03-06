#!/usr/bin/python
from PyQt4 import QtCore, QtGui
import glob
import os
import sys


dirSelf = os.path.dirname(os.path.realpath(__file__))
print(dirSelf)
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep) + os.sep + "lib")


import rbhusPipeProjCreateMod
print(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
sys.path.append(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep) + os.sep +"rbhus")
import dbPipe
import constantsPipe
import authPipe
import utilsPipe


try:
  _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
  _fromUtf8 = lambda s: s
  

class Ui_Form(rbhusPipeProjCreateMod.Ui_MainWindow):
  def setupUi(self, Form):
    rbhusPipeProjCreateMod.Ui_MainWindow.setupUi(self,Form)
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(_fromUtf8(dirSelf.rstrip(os.sep).rstrip("guiBin").rstrip(os.sep).rstrip("rbhusUI").rstrip(os.sep)+ os.sep +"etc/icons/rbhusPipe.svg")), QtGui.QIcon.Normal, QtGui.QIcon.On)
    Form.setWindowIcon(icon)
    
    self.dbpipe = dbPipe.dbPipe()
    self.username = None
    try:
      self.username = os.environ['rbhusPipe_acl_user'].rstrip().lstrip()
    except:
      pass
    
    self.center()
    self.setProjTypes()
    self.setDirectory()
    self.dateEditDue.setDateTime(QtCore.QDateTime.currentDateTime())
    self.pushCreate.clicked.connect(self.cProj)
    
    self.timer = QtCore.QTimer()
    self.timer.timeout.connect(self.updateStatus)
    self.timer.start(100)
    self.wtf = "new"
    
    
    
    
    
  def center(self):
    Form.move(QtGui.QApplication.desktop().screen().rect().center()- Form.rect().center())

  
  def updateStatus(self):
    if(self.lineEditName.text()):
      pDets = utilsPipe.getProjDetails(projName=str(self.lineEditName.text()))
      if(pDets):
        self.wtf = constantsPipe.createStatus[pDets['createStatus']]
      else:
        self.wtf = "new"
    self.statusBar.showMessage("status : "+ str(self.wtf))
  
  def cProj(self):
    pType = str(self.comboProjType.currentText())
    pName = str(self.lineEditName.text()) if(self.lineEditName.text()) else None
    pDir = str(self.comboDirectory.currentText())
    pDueDate = str(self.dateEditDue.dateTime().date().year()) +"-"+ str(self.dateEditDue.dateTime().date().month()) +"-"+ str(self.dateEditDue.dateTime().date().day()) +" "+ str(self.dateEditDue.dateTime().time().hour()) +":"+ str(self.dateEditDue.dateTime().time().minute()) +":" + str(self.dateEditDue.dateTime().time().second())
    pAdmins = str(self.lineEditAdmins.text()) if(self.lineEditAdmins.text()) else None
    pAclUser = str(self.lineEditAclUser.text()) if(self.lineEditAclUser.text()) else None
    pAclGroup = str(self.lineEditAclGroup.text()) if(self.lineEditAclGroup.text()) else None
    pRI = 1 if(self.checkRI.isChecked()) else 0
    pDesc = str(self.lineEditDesc.text()) if(self.lineEditDesc.text()) else None
    self.wtf = "connecting"
    utilsPipe.createProj(projType=pType,
                            projName=pName,
                            directory=pDir,
                            admins=pAdmins,
                            rbhusRenderIntegration=pRI,
                            rbhusRenderServer=None,
                            aclUser=pAclUser,
                            aclGroup=pAclGroup,
                            dueDate=pDueDate,
                            description=pDesc)
    
    
  
  
  def setProjTypes(self):
    rows = utilsPipe.getProjTypes()
    self.comboProjType.clear()  
    if(rows):
      for row in rows:
        self.comboProjType.addItem(_fromUtf8(row['type']))
      
      return(1)
    return(0)     
  
  
  def setDirectory(self):
    dirs = utilsPipe.getDirMaps()
    self.comboDirectory.clear()
    if(dirs):
      for d in dirs:
        self.comboDirectory.addItem(_fromUtf8(d['directory']))
      return(1)
    return(0)
    
    
  def setDefaults(self):
    defs = utilsPipe.getDefaults("proj")
    




if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  Form = QtGui.QMainWindow()
  ui = Ui_Form()
  ui.setupUi(Form)
  Form.show()
  sys.exit(app.exec_())
    