import requests
import json
import pandas
import db_dtypes
import datetime
import copy


from google.cloud import bigquery
# Construct a BigQuery client object.
project_id = 'sbb-project-2023'
client = bigquery.Client(project = project_id)



verboser = True

def verbose(text:str, verboser = verboser):
  if verboser == True:
    print(text)
  else:
    pass

# Set table_id to the ID of the table model to fetch.


def create_user(idcampus_card, campus_cardlastname = "newlastname", campus_cardfirstname = "newfirstname", campus_cardbirth_date = datetime.datetime.strptime("1998.10.03", "%Y.%m.%d"), campus_cardabsorption = 4, campus_cardsex = True, campus_cardweight = 70,campus_carddiffusioncoef = 1, alcohol_authorized = "0"):
  table_id = 'projetalcohol.campus_card'
  to_load = """{"idcampus_card":"***","campus_cardlastname":"****","campus_cardfirstname":"*****","campus_cardbirth_date":"******","campus_cardabsorption":"*******","campus_cardsex":"********","campus_cardweight":"*********","campus_carddiffusioncoef":"**********","alcohol_limit":"***********"}"""
  to_load = to_load.replace("***********", str(alcohol_authorized))
  to_load = to_load.replace("**********", str(campus_carddiffusioncoef))
  to_load = to_load.replace("*********", str(campus_cardweight))
  to_load = to_load.replace("********", str(campus_cardsex))
  to_load = to_load.replace("*******", str(campus_cardabsorption))
  to_load = to_load.replace("******", str(campus_cardbirth_date.strftime('%Y-%m-%d')))
  to_load = to_load.replace("*****", campus_cardfirstname)
  to_load = to_load.replace("****", campus_cardlastname)
  rows_to_insert = [json.loads(to_load.replace("***", idcampus_card))]

  errors = client.insert_rows_json(table_id, rows_to_insert)  # Make an API request.
  if errors == []:
    verbose("New rows have been added.")
  else:
    verbose("Encountered errors while inserting rows in alcohol level: {}".format(errors))


#create_user("1410818", "Konstantinidis", "Stergios", datetime.datetime.strptime("01.06.2000", "%d.%m.%Y"),4,False,84,1)


def add_time_departure(campus_card_uid, departure_time):
  table_id = 'projetalcohol.time_departure'
  to_load = """{"campus_card_idcampus_card":"***","time_departuredate":"*****","time_departuretime":"******"}"""
  to_load = to_load.replace("******", str(datetime.datetime.strptime(departure_time,'%H:%M').strftime('%H:%M:%S')))
  to_load = to_load.replace("*****", (datetime.datetime.now()).strftime('%Y-%m-%d'))
  rows_to_insert = [json.loads(to_load.replace("***", campus_card_uid))]

  errors = client.insert_rows_json(table_id, rows_to_insert)  # Make an API request.
  if errors == []:
    verbose("New rows have been added.")
  else:
    verbose("Encountered errors while inserting rows in alcohol level: {}".format(errors))



def drop_user(campuscard_uid):
   q1 = """DELETE FROM `sbb-project-2023.projetalcohol.campus_card` WHERE idcampus_card = "{}";""".format(str(campuscard_uid))
   client.query(q1)



def get_users_and_uid():
    q1 = """select idcampus_card as campuscard, campus_cardfirstname as firstname
from sbb-project-2023.projetalcohol.campus_card;"""
    query_job = client.query(q1)
  
    firstnames = query_job.to_dataframe()['firstname'].tolist()
    campus_card_uid = query_job.to_dataframe()['campuscard'].tolist()
    usernames = []
    number_of_records = len(campus_card_uid) - 1
    for i in range(number_of_records + 1):
        if firstnames[number_of_records - i] != "newfirstname" and firstnames[number_of_records - i] not in usernames and campus_card_uid[number_of_records - i] not in usernames:
            usernames.append(firstnames[number_of_records - i])
        elif firstnames[number_of_records - i] == "newfirstname" and campus_card_uid[number_of_records - i] not in usernames:
            usernames.append(campus_card_uid[number_of_records - i])
    return usernames


def get_user_data(uidOrName):
   q1 = """select *
from sbb-project-2023.projetalcohol.campus_card
where idcampus_card = "{}"
""".format(uidOrName)
   query_job = client.query(q1)

   if len(query_job.to_dataframe()) == 0:
        q1 = """select *
from sbb-project-2023.projetalcohol.campus_card
where campus_cardfirstname = "{}"
""".format(uidOrName)
        query_job = client.query(q1)
   else:
      pass
   
   return query_job.to_dataframe()
#get_user_data("1410818")

def user_exists(campuscard_id):
  q1 = """select campus_card_idcampus_card as campuscard
from sbb-project-2023.projetalcohol.alcohol_level
where campus_card_idcampus_card = "{}"
limit 1""".format(campuscard_id)
  query_job = client.query(q1)
  if len(query_job.to_dataframe()['campuscard'].tolist()) == 0:
    return False
  else:
    return True



from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_List(object):
    def setupUi(self, List):
        List.setObjectName("List")
        List.resize(493, 378)
        self.buttonBox = QtWidgets.QDialogButtonBox(List)
        self.buttonBox.setGeometry(QtCore.QRect(30, 300, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Save)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(List)
        self.label.setGeometry(QtCore.QRect(200, 40, 121, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(List)
        self.label_2.setGeometry(QtCore.QRect(350, 40, 60, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(List)
        self.label_3.setGeometry(QtCore.QRect(200, 70, 101, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(List)
        self.label_4.setGeometry(QtCore.QRect(200, 100, 91, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(List)
        self.label_5.setGeometry(QtCore.QRect(200, 130, 60, 16))
        self.label_5.setObjectName("label_5")
        self.birthday = QtWidgets.QDateEdit(List)
        self.birthday.setGeometry(QtCore.QRect(350, 130, 110, 24))
        self.birthday.setObjectName("birthday")
        self.DepartureTime = QtWidgets.QLabel(List)
        self.DepartureTime.setGeometry(QtCore.QRect(200, 270, 101, 16))
        self.DepartureTime.setObjectName("DepartureTime")
        self.DepartureTime_2 = QtWidgets.QLabel(List)
        self.DepartureTime_2.setGeometry(QtCore.QRect(350, 270, 101, 16))
        self.DepartureTime_2.setObjectName("DepartureTime_2")
        self.DepartureTime_3 = QtWidgets.QLabel(List)
        self.DepartureTime_3.setGeometry(QtCore.QRect(200, 170, 101, 16))
        self.DepartureTime_3.setObjectName("DepartureTime_3")
        self.DepartureTime_4 = QtWidgets.QLabel(List)
        self.DepartureTime_4.setGeometry(QtCore.QRect(200, 220, 101, 16))
        self.DepartureTime_4.setObjectName("DepartureTime_4")
        self.checkBox = QtWidgets.QCheckBox(List)
        self.checkBox.setGeometry(QtCore.QRect(350, 210, 87, 20))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(List)
        self.checkBox_2.setGeometry(QtCore.QRect(350, 230, 131, 20))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_3 = QtWidgets.QCheckBox(List)
        self.checkBox_3.setEnabled(False)
        self.checkBox_3.setGeometry(QtCore.QRect(350, 250, 131, 20))
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox.setTristate(False)
        self.checkBox_2.setTristate(False)
        self.checkBox_3.setTristate(False)
        self.FirstName = QtWidgets.QLineEdit(List)
        self.FirstName.setGeometry(QtCore.QRect(350, 70, 113, 21))
        self.FirstName.setObjectName("FirstName")
        self.LastName = QtWidgets.QLineEdit(List)
        self.LastName.setGeometry(QtCore.QRect(350, 100, 113, 21))
        self.LastName.setObjectName("LastName")
        self.Weight = QtWidgets.QLineEdit(List)
        self.Weight.setGeometry(QtCore.QRect(350, 170, 113, 21))
        self.Weight.setObjectName("Weight")
        self.comboBox = QtWidgets.QComboBox(List)
        self.comboBox.addItems(get_users_and_uid())
        self.comboBox.setGeometry(QtCore.QRect(20, 50, 131, 26))
        self.comboBox.setObjectName("comboBox")

        self.retranslateUi(List)
        self.buttonBox.accepted.connect(self.on_save) # type: ignore
        self.buttonBox.rejected.connect(self.on_user_selection) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(List)

        self.comboBox.currentTextChanged.connect(self.on_user_selection)
        self.checkBox.stateChanged.connect(self.on_check_box_checked_no_limit)
        self.checkBox_2.stateChanged.connect(self.on_check_box_checked_drive_limit)
 
    def on_save(self):
        
        campuscard_uid = self.label_2.text()
        first_name = self.FirstName.text()
        last_name = self.LastName.text()
        try:
            weight = int(self.Weight.text())
        except:
           weight = 80

        if self.checkBox.isChecked():
           alcohol_authorized = 0
        elif self.checkBox_2.isChecked():
           alcohol_authorized = 1
        else:
           alcohol_authorized = 3
        
        
        birthday = self.birthday.dateTime().toPyDateTime()
        drop_user(campuscard_uid)
        create_user(campuscard_uid,last_name,first_name,birthday,campus_cardweight=weight,alcohol_authorized=alcohol_authorized)
        QtCore.QCoreApplication.instance().quit()  

        add_time_departure(self.label_2.text(),self.DepartureTime_2.text())  
        
    def on_check_box_checked_no_limit(self):
       self.checkBox_2.setCheckState(not self.checkBox.checkState())
       
                                     
    def on_check_box_checked_drive_limit(self):
       self.checkBox.setCheckState(not self.checkBox_2.checkState())
          
        
        


    def on_user_selection(self, value = None):
        if value == None:
            value = self.comboBox.currentText()
        user_infos = get_user_data(value)
        #change the birthday that is dsplayed
        str_date = str(user_infos['campus_cardbirth_date'].tolist()[-1])
        qt_date = QtCore.QDateTime.fromString(str_date, 'yyyy-MM-dd')
        self.birthday.setDateTime(qt_date)

        #Change the displayed firstname
        str_firstName = str(user_infos['campus_cardfirstname'].tolist()[-1])
        self.FirstName.setText(str_firstName)

        #Change the displayed lasttname
        str_lastName = str(user_infos['campus_cardlastname'].tolist()[-1])
        self.LastName.setText(str_lastName)

        #Change the displayed uid
        str_uid = str(user_infos['idcampus_card'].tolist()[-1])
        self.label_2.setText(str_uid)

        #Change the displayed weight
        str_uid = str(user_infos['campus_cardweight'].tolist()[-1])
        self.Weight.setText(str_uid)

        #Select the alcohol limit
        alcohol_limit = str(user_infos['alcohol_limit'].tolist()[-1])
        if alcohol_limit == "0":
          self.checkBox.setChecked(True)
          self.checkBox_2.setChecked(False)
          self.checkBox_3.setChecked(False)

        elif alcohol_limit == "1":
          self.checkBox_2.setChecked(True)
          self.checkBox.setChecked(False)
          self.checkBox_3.setChecked(False)
        else:
           self.checkBox_3.setChecked(True)
           self.checkBox_2.setChecked(False)
           self.checkBox.setChecked(False)

    def retranslateUi(self, List):
        _translate = QtCore.QCoreApplication.translate
        List.setWindowTitle(_translate("List", "Dialog"))
        self.label.setText(_translate("List", "Campus card UID"))
        self.label_2.setText(_translate("List", "UID"))
        self.label_3.setText(_translate("List", "First Name"))
        self.label_4.setText(_translate("List", "Last Name"))
        self.label_5.setText(_translate("List", "BirthDay"))
        self.birthday.setDisplayFormat(_translate("List", "dd.MM.yyyy"))
        self.DepartureTime.setText(_translate("List", "Departure time"))
        self.DepartureTime_2.setText(_translate("List", "18:00"))
        self.DepartureTime_3.setText(_translate("List", "Weight"))
        self.DepartureTime_4.setText(_translate("List", "Alcohol Limit"))
        self.checkBox.setText(_translate("List", "No alcohol"))
        self.checkBox_2.setText(_translate("List", "Be able to drive"))
        self.checkBox_3.setText(_translate("List", "No limit"))
        
            
def launch():
  import sys
  app = QtWidgets.QApplication(sys.argv)
  List = QtWidgets.QDialog()
  ui = Ui_List()
  ui.setupUi(List)
  ui.on_user_selection()
  List.show()
  app.exec_()
  app.quit()

if __name__ == "__main__":
  import sys
  app = QtWidgets.QApplication(sys.argv)
  List = QtWidgets.QDialog()
  ui = Ui_List()
  ui.setupUi(List)
  List.show()
  app.exec_()
  app.quit()