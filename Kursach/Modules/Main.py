from security import Ui_Security
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDir
import design, design_auth, security, Login, AccessRules, AccessDB  # Это наш конвертированный файл дизайна
import os

class SecurityPopup(QtWidgets.QMainWindow, security.Ui_Security):
    def __init__(self, path, userLevel):
        super().__init__()
        self.path = path
        self.con = AccessDB.connectToDB()
        #self.userList = AccessDB.selectUsers(self.con, path)    #username, ID, access, owner
        #self.allUserList = AccessDB.selectOnlyUsers(self.con)  #username, ID
        self.usersWithLevels = AccessDB.selectPathLevel(self.con, path)
        #self.mergedUserList = list()
        self.userLevel = userLevel
        self.setupUi(self, path, self.usersWithLevels)
        #self.mergedUserList = self.mergeUserLists()
        #self.listWidget.setCurrentRow(0)
        #self.currentUser = self.listWidget.currentItem()
        #self.currentUser = self.currentUser.text().split("  /////   ")
        #self.currentUser = int(self.currentUser[0])
        #self.initRules()
        #self.listWidget.itemSelectionChanged.connect(self.changeUser)
        self.btnSetSec.clicked.connect(self.confirm)
        
    def mergeUserLists(self):
        print(self.allUserList)
        print(self.userList)
        
        for user in self.allUserList:
            found = 0
            if self.userList != None:
                for userL in self.userList:
                    if user[1] == userL[1]:
                        self.mergedUserList.append([userL[0], userL[1], userL[2], userL[3]])
                        found = 1
                        break
            if found == 0:
                self.mergedUserList.append([user[0],user[1],"rwx",0])
        for user in self.mergedUserList:  
                self.listWidget.addItem(str(user[1]) + "  /////   " + str(user[0]))
        #self.listWidget.
        return self.mergedUserList

    def initRules(self):
        pathLevel = AccessDB.selectPathLevel(self.con, self.path)
        if pathLevel > 0:
            self.comboBox.setCurrentIndex(pathLevel-1)
        else:
            self.comboBox.setCurrentIndex(0)
        
        return 0
    

    def changeUser(self):
        # try:
        #     userID = self.listWidget.CurrentItem()
        #     userID.split("  /////   ")
        #     userID = userID[0]
        #     print(userID)
        # except:
        #     userID = 1
        # if self.currentUser == None:
        #     self.currentUser = self.listWidget.currentItem()
        #     self.currentUser = self.currentUser.text().split("  /////   ")
        #     self.currentUser = int(self.currentUser[0])
        #     self.initRules()
        userID = self.listWidget.currentItem()
        userID = userID.text().split("  /////   ")
        userID = int(userID[0])
        print(userID)
        rule = ''
        if self.checkRead.isChecked():        #change
            rule += 'r'
        if self.checkWrite.isChecked():      #change
            rule += 'w'
        if self.checkExec.isChecked():     #change
            rule += 'x'
        if rule == '':
            rule = 'n'
        print(self.path)
        print(self.mergedUserList)
        tmp = list(self.mergedUserList[self.currentUser])
        index = self.mergedUserList.index(tmp)
        self.mergedUserList.pop(index)
        tmp.pop(2)
        tmp.insert(2, rule)
        self.mergedUserList.insert(index, tmp)
        self.currentUser = userID
        self.initRules()

    def confirm(self):
        level = str(self.comboBox.currentText())
        print(self.path)
        AccessDB.setLevel(level, self.userLevel, self.path, self.con)


    
            

        

class AuthWindow(QtWidgets.QMainWindow, design_auth.Ui_AuthWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.loggedIn = 0
        self.usrID = -1
        self.usrLevel = -1
        self.btnAuth.clicked.connect(self.auth)
        self.btnSignUp.clicked.connect(self.register)
        
    def auth(self):
        print(self.loggedIn)
        if self.loggedIn == 0:
            print("if")
            userLevel, userID = Login.logIn(self.inputLogin.text(), self.inputPass.text())
            if userID != -1:
                self.usrID = userID
                self.loggedIn = 1
                for i in range(0,userLevel):
                    self.comboLevel.addItem(str(i+1))
                self.btnAuth.setText("Set session level")
            else:
                print("Login failed")   # change to message box or label
        else:
            print("else")
            self.usrLevel = int(self.comboLevel.currentText())
            self.close()
            self.window = ExampleApp(self.inputLogin.text(), self.usrID, self.usrLevel)
            self.window.show()
        

    def register(self):
        userLevel, userID = Login.addUser(self.inputLogin.text(), self.inputPass.text())
        if userID != -1:
            self.close()
            self.window = ExampleApp(self.inputLogin.text(), userID, userLevel)
            self.window.show()
        else:
            print("Register failed")   # change to message box or label
        
class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

    global path
    path = QDir.homePath()
    #path = '/'
    #QDir("/home/pda7271")
    print(path)

    def __init__(self, login, userID, userLevel):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.username = login
        self.userID = userID
        self.userLevel = userLevel
        self.con = AccessDB.connectToDB()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.authWindow = None
        self.actionLogOut.triggered.connect(self.auth)
        self.actionOpen.triggered.connect(self.open_folder)
        self.btnBrowse.clicked.connect(self.browse_folder) #Home
        self.btnOpen.clicked.connect(self.open_folder) #Open
        self.listWidget.itemDoubleClicked.connect(self.open_folder)
        self.btnSec.clicked.connect(self.security)
        self.btnBack.clicked.connect(self.back_folder) #Back
        self.menuUserName.setTitle(login) #get userName from db
        
    def auth(self):
        self.close()
        self.authWindow = AuthWindow()
        self.authWindow.show()
        
    def security(self):
        print('security settings here popup')
        item = self.listWidget.currentItem()
        if item:
            if int(self.userLevel) < int(AccessDB.selectPathLevel(self.con, path + '/' + item.text())):
                print("access denied!!11!!!")
                return
            self.window = SecurityPopup(path + '/' + item.text(), self.userLevel)
        else:
            if int(self.userLevel) < int(AccessDB.selectPathLevel(self.con, path)):
                print("access denied!!11!!!")
                return
            self.window = SecurityPopup(path, self.userLevel)
        self.window.show()

    def open_folder(self):
        global path
        print('1')
        #print('clicked items:', self.listWidget.selectedItems())
        item = self.listWidget.currentItem()
        print('2')
        if item:  #if
            print('3')
            #print(path.QtCore.QDir.exists())
            path = path + '/' + item.text()
            if os.path.isdir(path):
                accs, reload = AccessRules.checkAccessMand(self.userLevel, path)
                if reload == "0": 
                    if accs.find('r') != -1:
                        print('4')
                        rule, rule_code = self.parseRules(accs)
                        try:
                            os.chmod(path, int(rule_code))
                        except:
                            print("Error in chmod")
                            index = path.rfind('/', 0)
                            path = path[0:index]
                        
                        print('file  dir:',path)
                        # os.system('sudo chown appusr ' + path)
                        print('dir:',path)
                        self.list_appear()  
                    else:
                        index = path.rfind('/', 0)
                        path = path[0:index]
                        print('file  dir:',path)
                        print("Access denied")        
                else:
                    index = path.rfind('/', 0)
                    path = path[0:index]
                    print('file  dir:',path)
                    print("Access denied, please, relogin")      
            elif os.path.isfile(path):
                print('5')
                print('file:',path)
                accs, reload = AccessRules.checkAccessMand(self.userLevel, path)
                if reload == "0":
                    if accs.find('r') != -1: # add "x"
                        print('6')
                        rule, rule_code = self.parseRules(accs)
                        
                        try:
                            os.chmod(path, int(rule_code))
                        except:
                            print("Error in chmod")
                            index = path.rfind('/', 0)
                            path = path[0:index]
                        
                        # os.system('sudo chown appusr ' + path)
                        os.system('xdg-open '+path)
                        index = path.rfind('/', 0)
                        path = path[0:index]
                        print('file  dir:',path)
                    else:
                        index = path.rfind('/', 0)
                        path = path[0:index]
                        print('file  dir:',path)
                        print("Access denied")
                else:
                    index = path.rfind('/', 0)
                    path = path[0:index]
                    print('file  dir:',path)
                    print("Access denied, please, relogin")   
            else:
                print(path)
                print("kak-to plyusuetsya")
                
    def parseRules(self, accs):
        rule_code = 0
        rule = ''
        if accs.find("r"):
            rule += "r"
            rule_code += 2*2
        else:
            rule += "-"
            rule_code += 0
        if accs.find("w"):
            rule += "w"
            rule_code += 1*2
        else:
            rule += "-"
            rule_code += 0
        if accs.find("x"):
            rule += "x"
            rule_code += 1
        else:
            rule += "-"
            rule_code += 0

        rule_code = str(rule_code) + "0" + str(rule_code)
        return rule, rule_code

    def back_folder(self):
        global path
        if path != QtCore.QDir.homePath():
            # os.system('sudo chown root ' + path)
            index = path.rfind('/', 0)
            path = path[0:index]
            #QtCore.QDir.cdUp()
            self.list_appear()        
        
    def browse_folder(self):
        #path = QtWidgets.QFileDialog.getExistingDirectory(self, "Browse..")
        #path = '/home/pda7271/kursovaya'
        #print(path)
        global path
        path = QtCore.QDir.homePath()
        print(path)       
        if path:  # не продолжать выполнение, если пользователь не выбрал директорию
            self.list_appear()
                
    def list_appear(self):
        self.listWidget.clear()
        for file_name in os.listdir(path):  # для каждого файла в директории
                self.listWidget.addItem(file_name)   # добавить файл в listWidget

def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = AuthWindow()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
