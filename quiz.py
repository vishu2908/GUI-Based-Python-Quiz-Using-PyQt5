import sys
from _thread import start_new_thread
import time
import PyQt5
import PyMySQL
from PyQt5.QtWidgets import *
from userlogin import MyLogin
from exam import MainWindow
from QuizDB import DBWindow
import smtplib  #for Sending mail





#database update window




class MyDBWindow(DBWindow,QMainWindow):
        def __init__(self):
                QMainWindow.__init__(self)
                self.setupUi(self)
                self.dbConnect()
                self.groupBox.setEnabled(False)
                self.lblMsg.hide()
                self.btNew.clicked.connect(self.btAddNew_clicked)
                self.btSave.clicked.connect(self.btSave_clicked)
                self.btDelete.clicked.connect(self.btDelete_clicked)
                self.btUpdate.clicked.connect(self.btUpdate_clicked)
                self.btClear.clicked.connect(self.btClear_clicked)
                self.btClose.clicked.connect(self.btClose_clicked)
                self.table1.cellClicked.connect(self.cellClicked)
#database connection
        def dbConnect(self):
                try:
                        global db
                        global cursor
                        db=PyMySQL.connect("localhost","root","tiger","exam")
                        cursor=db.cursor()
                        count=cursor.execute("select* from questions")
                       # print(count)
                        row=cursor.fetchall()
                        self.table1.setRowCount(count)
                        for i in range(0,count,1):
                            for j in range(0,7,1):
                                    self.table1.setItem(i,j,QTableWidgetItem(str(row[i][j])))
                except Exception as e:
                        print(e)
#clear All button
        def btClear_clicked(self):
                self.clearAll()
#close button
        def btClose_clicked(self):
                self.close()
#new ques button
        def btAddNew_clicked(self):
                qno=self.GenerateQuesNo()
                self.t1.setText(str(qno))
                self.groupBox.setEnabled(True)
                self.clearAll()
#generate ques no button
        def GenerateQuesNo(self):
                print("ok")
                try:
                        count=cursor.execute("select max(qno) from questions")
                        row=cursor.fetchone()
                        qno=1
                        if count==0:
                                qno=1
                        else:
                                qno=row[0]+1
                                return qno
                except Exception as e:
                        print(e)
#click feature
        def cellClicked(self):
                self.groupBox.setEnabled(True)
                try:
                        row=self.table1.currentRow()
                        #col=self.table1.currentColumn()
                        self.t1.setText(self.table1.item(row,0).text())
                        self.t2.setText(self.table1.item(row,1).text())
                        self.t3.setText(self.table1.item(row,2).text())
                        self.t4.setText(self.table1.item(row,3).text())
                        self.t5.setText(self.table1.item(row,4).text())
                        self.t6.setText(self.table1.item(row,5).text())
                        self.t7.setText(self.table1.item(row,6).text())
                except Exception as e:
                        print(e)
#update button
        def btUpdate_clicked(self):
                try:
                        qno=int(self.t1.text())
                        qdesc=self.t2.text()
                        option1=self.t3.text()
                        option2=self.t4.text()
                        option3=self.t5.text()
                        option4=self.t6.text()
                        crtoption=self.t7.text()
                        query="""update questions set qdesc='%s',option1='%s',option2='%s',option3='%s',option4='%s',answer='%s' where qno=%d""" %(qdesc,option1,option2,option3,option4,crtoption,int(qno))
                        cursor.execute(query)
                        db.commit()
                        self.dbConnect()
                        self.lblMsg.setText("Record Updated Successfully")
                        self.lblMsg.show()
                        
                except Exception as e:
                        print(e)
# save button
        def btSave_clicked(self):
                try:
                        qno=self.t1.text()
                        self.t1.setText(""+qno)
                        qdesc=self.t2.text()
                        option1=self.t3.text()
                        option2=self.t4.text()
                        option3=self.t5.text()
                        option4=self.t6.text()
                        crtoption=self.t7.text()
                        query="insert into questions values (%d,'%s','%s','%s','%s','%s','%s')" % (int(qno),qdesc,option1,option2,option3,option4,crtoption)
                        print(query)
                        cursor.execute(query)
                        db.commit()
                        self.dbConnect()
                        self.lblMsg.setText("Record Added Successfully")
                        self.lblMsg.show()
                        self.t1.setText("")
                        self.groupBox.setEnabled(False)

                except Exception as e:
                        print(e)
#delete button
        def btDelete_clicked(self):
                self.groupBox.setEnabled(True)
                self.t1.setEnabled(True)
                try:
                        qno=int(self.t1.text())
                        query="delete from questions where qno=%d" % (qno)
                        cursor.execute(query)
                        db.commit()
                        self.dbConnect()
                        self.lblMsg.setText("Record Deleted Successfully")
                        self.lblMsg.show()
                except Exception as e:
                        print(e)
                        self.lblMsg.show()
                        self.lblMsgSetText("Enter Qno to be deleted")
                        
        
#clear all function
        def clearAll(self):
                self.t2.setText("")
                self.t3.setText("")
                self.t4.setText("")
                self.t5.setText("")
                self.t6.setText("")
                self.t7.setText("")
                

#quiz window



class MyWindow(MainWindow,QMainWindow):
    qcorrect=0
    qwrong=0
    QNO=1
    NOQ=5
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        global seconds
        seconds=30
        self.lcd.display(seconds)

        t=time.localtime()
        ct=time.asctime(t)
        self.lblDate.setText(""+ct)

        self.label8.hide()
        self.label9.hide()
        self.table1.hide()
        self.btAns.setEnabled(False)
        self.quesBox.hide()

        self.btLogOut.clicked.connect(self.btLogout_clicked)
        self.btBegin.clicked.connect(self.btBegin_clicked)
        self.btNext.clicked.connect(self.btNext_clicked)
        self.btAns.clicked.connect(self.GetResult)
        
    def display(self,sec):
        for i in range(sec,-1,-1):
            self.lcd.display(i)
            time.sleep(1)
        else:

            self.btAns.setEnabled(True)
            self.quesBox.hide()
            self.label8.show()
            self.label8.setText("QUIZ IS OVER!!! KINDLY SUBMIT YOUR ANSWERS")
    def btBegin_clicked(self):
        self.btBegin.setEnabled(False)
        self.quesBox.show()
        self.quesBox.setEnabled(True)
        self.getQuestions(MyWindow.QNO)
        
        start_new_thread(self.display,(seconds,))
        
    def btLogout_clicked(self):
        self.close()

    def getQuestions(self,qno):
        global ans
        try:
            query="select * from questions where qno=%d"%(qno)
            print(query)
            cursor.execute(query)
            data=cursor.fetchone()

            if data!=None:
                self.lblQues.setText(data[1])
                self.rb1.setText(data[2])
                self.rb2.setText(data[3])
                self.rb3.setText(data[4])
                self.rb4.setText(data[5])
                ans=data[6]
        except Exception as e:
            print(e)
            
    def btNext_clicked(self):
        try:
            if MyWindow.QNO<=(MyWindow.NOQ):
                choice=""
                if self.rb1.isChecked():
                    choice="option1"
                elif self.rb2.isChecked():
                    choice="option2"
                elif self.rb3.isChecked():
                    choice="option3"
                elif self.rb4.isChecked():
                    choice="option4"

                #print(ans,choice)
                if ans==choice:
                    MyWindow.qcorrect+=1
                else:
                    MyWindow.qwrong+=1

                #print(MyWindow.qcorrect,MyWindow.qwrong)

                MyWindow.QNO+=1
                self.getQuestions(MyWindow.QNO)

            else:

                self.quesBox.hide()
                self.label8.show()
                self.label8.setText("QUIZ IS OVER!!! KINDLY SUBMIT YOUR ANSWERS")

        except Exception as e:
            print(e)

    def GetResult(self):
        try:
            status=""
            score=MyWindow.qcorrect/(MyWindow.NOQ)*100
            if score>=60:
                status="Qualified"
                self.label8.setText("CONGRATS!!! You have QUALIFIED for the next round.")
            else:
                status="Not Qualified"
                self.label8.setText("SORRY!!! You have NOT QUALIFIED for the next round.")

            email=self.t1.text()
            name=self.t2.text()
            t=time.localtime()
            ct=time.asctime(t)
            q="DELETE FROM RESULT WHERE email='%s'"%(email)
            cursor.execute(q)
            db.commit()
            
            query="INSERT INTO RESULT VALUES('%s','%s',%d,%d,%d,'%s','%s')"%(email,name,MyWindow.qcorrect,MyWindow.qwrong,score,status,str(ct))
            print(query)
            cursor.execute(query)
            db.commit()
            self.label8.show()
            self.label9.setText("Your Result has been sent to your registered Email.Kindly Check It")
            self.label9.show()

            self.table1.setGeometry(10,210,701,131)
            self.table1.show()
            self.createTable()
            #content type &subject are required to send html mail using html tags
            message="""MIME-Version: 1.0
Content-type:text/html
Subject:Python Quiz Result """
            message+="\n<h1>"+self.label8.text()+"</h1>"
            message+="""<table border=2 cellspacing=5><th>Name<th>Correct<th>Wrong<th>score<th>status<th>DOE
<tr><td>%s<td>%d<td>%d<td>%d<td>%s<td>%s</tr></table>"""%(name,MyWindow.qcorrect,MyWindow.qwrong,score,status,str(ct))
            self.sendEmail(message)                       
        except Exception as e:
                print(e)


        #email button
    def sendEmail(self,message):
        sender='mail2vishu.cs@gmail.com'
        to=self.t1.text()
        receivers=[to]
        try:
                smtpObj=smtplib.SMTP('smtp.gmail.com',25,'localhost')
                smtpObj.starttls()
                smtpObj.login("mail2vishu.cs","Cool@vishal")
                smtpObj.sendmail(sender,receivers,message)
                print("successfully sent email")
        except Exception as e:
                print(e)
            
    def createTable(self):
        try:
            email=self.t1.text()
            query="select * from result where email='%s'"%(email)
            cursor.execute(query)
            data=cursor.fetchone()

            #table filling
            self.table1.setItem(0,0,QTableWidgetItem("Email"))
            self.table1.setItem(0,1,QTableWidgetItem("Name"))
            self.table1.setItem(0,2,QTableWidgetItem("Correct"))
            self.table1.setItem(0,3,QTableWidgetItem("Wrong"))
            self.table1.setItem(0,4,QTableWidgetItem("Score"))
            self.table1.setItem(0,5,QTableWidgetItem("Status"))
            self.table1.setItem(0,6,QTableWidgetItem("DateOfExam"))
            for i in range(1,2,1):
                for j in range(0,7,1):
                    self.table1.setItem(i,j,QTableWidgetItem(str(data[j])))

        except Exception as e:
            print(e)
        
class AppWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.connectDB()
        self.ui=MyLogin()
        self.ui.setupUi(self)
        self.ui.button2.clicked.connect(self.button2_clicked)
        self.ui.gb1.setEnabled(False)
        self.ui.gb2.setEnabled(False)
        
        
        self.ui.rb1.clicked.connect(self.rb1_clicked)
        self.ui.rb2.clicked.connect(self.rb2_clicked)
        self.ui.button1.clicked.connect(self.button1_clicked)
        self.ui.button_1.clicked.connect(self.button3_clicked)
        self.ui.button2_2.clicked.connect(self.button4_clicked)

            
    def connectDB(self):
        global db
        global cursor
        db=PyMySQL.connect("localhost","root","tiger","exam")
        cursor=db.cursor()

    def rb1_clicked(self):
        try:
            if self.ui.rb1.isChecked():
                self.ui.t3.setText("")
                self.ui.t4.setText("")
                self.ui.label2.setText("")
                self.ui.gb1.setEnabled(True)
                self.ui.gb2.setEnabled(False)
        except Exception as e:
            print(e)

    def rb2_clicked(self):
        try:
            if self.ui.rb2.isChecked():
                self.ui.t1.setText("")
                self.ui.t2.setText("")
                self.ui.label1.setText("")
                self.ui.gb2.setEnabled(True)
                self.ui.gb1.setEnabled(False)
                self.ui.label2.setText("Please login as 'admin' to manage Quiz")
        except Exception as e:
            print(e)

    def button3_clicked(self):
        self.ui.t1.setText("")
        self.ui.t2.setText("")
        self.ui.label1.setText("")

  
    def button4_clicked(self):
        self.ui.t3.setText("")
        self.ui.t4.setText("")
        self.ui.label2.setText("")

    def button1_clicked(self):
        try:
            uname=self.ui.t1.text()
            passw=self.ui.t2.text()
            query="insert into login values('%s','%s')"%(uname,passw)
            print(query)
            count=cursor.execute(query)
            if(count==1):
                self.ui.label1.setText("You are registered successfully")

            db.commit()
            message="""MIME-Version: 1.0
Content-type:text/html
Subject:Welcome to Python Quiz"""
            message+="\n<h1>"+"Thanks for Registration in PYTHON QUIZ!!"+"</h1>\n"+"<h3>"+"Login Now to attempt the Quiz."+"</h3>"
            self.sendEmail(message)
        except Exception as e:
            print(e)
            self.ui.label1.setText("You are already registered")

    def sendEmail(self,message):
        sender='mail2vishu.cs@gmail.com'
        to=self.ui.t1.text()
        receivers=[to]
        try:
                smtpObj=smtplib.SMTP('smtp.gmail.com',25,'localhost')
                smtpObj.starttls()
                smtpObj.login("mail2vishu.cs","Cool@vishal")
                smtpObj.sendmail(sender,receivers,message)
                print("successfully sent email")
        except Exception as e:
                print(e)
      
    def button2_clicked(self):
        try:
            uname=self.ui.t3.text()
            passw=self.ui.t4.text()
            query="select * from login where email='%s' and password='%s'"%(uname,passw)
            print(query)
            count=cursor.execute(query)
            if count==1 and uname=="admin":
                self.winDB=MyDBWindow()  
                self.winDB.show()
                self.close()
            elif count==1:
                self.m=MyWindow()
                self.m.t1.setText(uname)    
                self.m.show()
                self.close()
            else:
                self.ui.label2.setText("Invalid Username/Password")
        except Exception as e:
            print(e)

app=QApplication(sys.argv)
w=AppWindow()
w.show()
