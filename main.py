import sqlite3
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QMainWindow, QPushButton, QLabel, QMessageBox
from PyQt5.QtGui import QIcon
# If code under uic and loadUi is displaying error try and run anyway maybe an error with pycharm
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5 import QtGui, QtSql
import functools
import objects
import pandas as pd


conn = sqlite3.connect('Northstarproject.db')
curs = conn.cursor()


class MainWindow(QDialog):

    def __init__(self):
        super().__init__()
        loadUi("MainWindow.ui", self)
        self.thing.clicked.connect(self.idChecker)
        self.label.setText("Enter ID")

    def idChecker(self):
        loginID = self.line.text()
        if self.studentId(loginID):
            newWind = StudentInfoMain()

            newWind.label1.setText(self.line.text())

            widget.addWidget(newWind)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        elif self.clerkID(loginID):
            newWind = ClerkTools()
            widget.addWidget(newWind)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            self.label.setText("Invalid ID")
            self.show()

    def clerkID(self, ID):
        conn = sqlite3.connect('Northstarproject.db')
        curs = conn.cursor()
        sql = "select InstructorId from Instructor"
        curs.execute(sql)
        res = curs.fetchall()
        print(res)
        row = [item[0] for item in res]
        return ID in row

    def studentId(self, ID):
        conn = sqlite3.connect('Northstarproject.db')
        curs = conn.cursor()
        sql = "select StudentId from Student"
        curs.execute(sql)
        res = curs.fetchall()
        row = [item[0] for item in res]
        return ID in row

    def rtnID(self):
        return self.line.text()


class ClerkTools(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("Clerk-Tools.ui", self)
        self.EnterButton.clicked.connect(self.radioSelection)
        self.cancel.clicked.connect(self.CancelButton)

    def radioSelection(self):
        if self.radio1.isChecked():
            self.GoToFacultyDataMain()
        if self.radio2.isChecked():
            self.GoToAdminStudentIDSearch()
        if self.radio3.isChecked():
            self.GoToAddStudentToCourse()
        if self.radio4.isChecked():
            self.GoToModifySection_Course()
        if self.radio5.isChecked():
            self.GoToFlags()
        if self.radio6.isChecked():
            self.GoToMaintainStudentData()
        if self.radio7.isChecked():
            self.GoToCourseWindow()

    def CancelButton(self):
        newWind = MainWindow()
        widget.addWidget(newWind)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToFacultyDataMain(self):
        newWindow = FacultyDataMain()
        widget.addWidget(newWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToAdminStudentIDSearch(self):
        newWindow = ClerkStudentIDEntry()
        widget.addWidget(newWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToAddStudentToCourse(self):
        newWindow = AddStudentToCourse()
        widget.addWidget(newWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToModifySection_Course(self):
        newWindow = ModifySection_Course()
        widget.addWidget(newWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToFlags(self):
        newWindow = FlagStudentIDEntry()
        widget.addWidget(newWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToMaintainStudentData(self):
        newWindow = MaintainStudentData()
        widget.addWidget(newWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def GoToCourseWindow(self):
        newWindow = CourseWindow()
        widget.addWidget(newWindow)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class FacultyDataMain(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("Faculty-data-main.ui", self)
        self.cancel.clicked.connect(self.CancelButton)

        try:
            self.pushButton_3.clicked.connect(self.add_instructor)
            self.pushButton_4.clicked.connect(self.modify_instructor)
            self.pushButton_2.clicked.connect(self.remove_instructor)
        except Exception as e:
            print(Exception, e)

    def CancelButton(self):
        newWind = ClerkTools()
        widget.addWidget(newWind)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def add_instructor(self):
        try:
            new_instructor = objects.Instructor(self.lineEdit.text(), self.lineEdit_2.text(), conn, curs)
            new_instructor.addInstructor()
            conn.commit()
        except Exception as E:
            print(Exception, E)

    def modify_instructor(self):
        new_instructor = objects.Instructor(self.lineEdit.text(), self.lineEdit_2.text(), conn, curs)
        query = f"""SELECT EXISTS(SELECT * FROM Instructor WHERE InstructorID = '{new_instructor.InstructorID}')"""
        curs.execute(query)
        result = curs.fetchall()
        print(result)
        if result[0][0] == 1:
            print("ID FOUND")
            new_instructor.modifyInstructor()
            conn.commit()
        else:
            self.error_window.exec_()

    def remove_instructor(self):
        try:
            new_instructor = objects.Instructor(self.lineEdit.text(), self.lineEdit_2.text(), conn, curs)

            query = f"""SELECT EXISTS(SELECT * FROM Instructor WHERE InstructorID = '{self.lineEdit.text()}')"""
            curs.execute(query)
            if curs.fetchone()[0] == 1:

                query = f"""SELECT EXISTS(SELECT * FROM Instructor WHERE InstructorID = '{self.lineEdit.text()}')"""
                curs.execute(query)
                result = curs.fetchall()
                print(result)
                if result[0][0] == 1:
                    print("ID FOUND")
                    new_instructor.removeInstructor()
                    conn.commit()
                else:
                    self.error_window.exec_()

            else:
                self.enrolls_exist.exec_()

        except Exception as e:
            print(Exception, e)


class FacultyDataErrorwin1(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("Faculty-data-error-win1.ui", self)
        self.cancel.clicked.connect(self.CancelButton)

    def CancelButton(self):
        newWind = ClerkTools()
        widget.addWidget(newWind)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class FacultyDataErrorwin2(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("Faculty-data-error-win2.ui", self)
        self.cancel.clicked.connect(self.CancelButton)

    def CancelButton(self):
        newWind = ClerkTools()
        widget.addWidget(newWind)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ModifySection_Course(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("Add-Modify-Section-or-Course.ui", self)
        self.cancel.clicked.connect(self.CancelButton)
        self.addButton.clicked.connect(self.add_section)
        self.deleteButton.clicked.connect(self.remove_section)
        self.modButton.clicked.connect(self.mod_section)

        self.existing_id = QMessageBox()
        self.existing_id.setText("ID Already Exists, please enter a different ID")

        self.not_existing_id = QMessageBox()
        self.not_existing_id.setText("Course doesn't exist!")

        self.not_existing_fac = QMessageBox()
        self.not_existing_fac.setText("Faculty member doesn't exist!")

    def CancelButton(self):
        newWind = ClerkTools()
        widget.addWidget(newWind)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def mod_section(self):
        new_section = objects.CourseSection(self.crsID.text(), self.crsSecID.text(), self.facID.text(), 6, conn, curs)

        query = f"""SELECT EXISTS(SELECT * FROM CourseSection WHERE CourseSectionID = '{self.crsSecID.text()}')"""
        curs.execute(query)

        if curs.fetchone()[0] == 1:
            query = f"""SELECT EXISTS(SELECT * FROM Instructor WHERE InstructorID = '{self.facID.text()}')"""
            curs.execute(query)
            if curs.fetchone()[0] == 1:
                new_section.modifySectionInstructor()
                conn.commit()
            else:
                self.not_existing_fac.exec()
        else:
            self.not_existing_id.exec()

    def add_section(self):
        query = f"""SELECT EXISTS(SELECT * FROM Course WHERE CourseID = '{self.crsID.text()}')"""
        curs.execute(query)

        if curs.fetchone()[0] == 1:

            query = f"""SELECT EXISTS(SELECT * FROM Instructor WHERE InstructorID = '{self.facID.text()}')"""
            curs.execute(query)
            if (curs.fetchone()[0] == 1):
                new_section = objects.CourseSection(self.crsID.text(), self.crsSecID.text(), self.facID.text(), 6, conn,
                                                    curs)

                try:
                    new_section.add()
                    conn.commit()
                except Exception as e:
                    self.existing_id.exec()
            else:
                self.not_existing_fac.exec()
        else:
            self.not_existing_id.exec()

    def remove_section(self):
        new_section = objects.CourseSection(self.crsID.text(), self.crsSecID.text(), self.facID.text(), 6, conn, curs)

        try:
            query = f"""SELECT EXISTS(SELECT * FROM CourseSection WHERE CourseID = '{self.crsID.text()}' and CourseSectionID = '{self.crsSecID.text()}')"""
            curs.execute(query)
        except Exception as e:
            print(Exception, e)

        if curs.fetchone()[0] == 1:
            try:
                new_section.remove()
                conn.commit()
            except Exception as e:
                print(Exception, e)
        else:
            self.not_existing_id.exec()


class MaintainStudentData(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("Maintain-Student-Data.ui", self)
        self.cancel.clicked.connect(self.CancelButton)
        self.addButton.clicked.connect(self.add_student)
        self.modButton.clicked.connect(self.modify_student)
        self.removeButton.clicked.connect(self.remove_student)

        self.error_window = QMessageBox()
        self.error_window.setText("Invalid ID, please enter a Valid ID")

        self.enrolls_exist = QMessageBox()
        self.enrolls_exist.setText("Student currently enrolled. Please delete enrollments first.")

    def CancelButton(self):
        newWind = ClerkTools()
        widget.addWidget(newWind)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def add_student(self):
        new_student = objects.Student(self.idEntry.text(), self.nameEntry.text(), conn, curs)
        try:
            new_student.addStudent()
            conn.commit()
        except Exception as E:
            self.error_window.exec_()

    def modify_student(self):
        new_student = objects.Student(self.idEntry.text(), self.nameEntry.text(), conn, curs)
        query = f"""SELECT EXISTS(SELECT * FROM Student WHERE StudentID = '{new_student.StudentID}')"""
        curs.execute(query)
        result = curs.fetchall()
        print(result)
        if result[0][0] == 1:
            print("ID FOUND")
            new_student.modifyStudent()
            conn.commit()
        else:
            self.error_window.exec_()

    def remove_student(self):
        try:
            new_student = objects.Student(self.idEntry.text(), self.nameEntry.text(), conn, curs)

            query = f"""SELECT EXISTS(SELECT * FROM Enrollment WHERE StudentID = '{new_student.StudentID}')"""
            curs.execute(query)
            if curs.fetchone()[0] == 0:

                query = f"""SELECT EXISTS(SELECT * FROM Student WHERE StudentID = '{new_student.StudentID}')"""
                curs.execute(query)
                result = curs.fetchall()
                print(result)
                if result[0][0] == 1:
                    print("ID FOUND")
                    new_student.removeStudent()
                    conn.commit()
                else:
                    self.error_window.exec_()

            else:
                self.enrolls_exist.exec_()

        except Exception as e:
            print(Exception, e)


class AddStudentToCourse(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("Add-Student-to-Course.ui", self)
        self.cancel.clicked.connect(self.CancelButton)
        self.label3.setStyleSheet('color: red')
        self.addButton.clicked.connect(self.add_enrollment)

        self.display = QPushButton(self)
        self.display.move(290, 420)
        self.display.setText("Delete")
        self.display.resize(75, 23)
        self.display.clicked.connect(self.remove_class)

        self.error = QMessageBox(self)
        self.error.setText("No matching course. Enter a valid course.")

    def add_enrollment(self):
        try:

            Enrollent = objects.Enrollment(self.stdID.text(), self.crsID.text(), self.crsSecID.text(), conn, curs)
            Enrollent.add_enrollment()
            conn.commit()

        except Exception as E:
            print(Exception, E)

    def remove_class(self):
        try:


            Enrollent = objects.Enrollment(self.stdID.text(), self.crsID.text(), self.crsSecID.text(), conn, curs)
            query = f"""SELECT EXISTS(SELECT * FROM Enrollment WHERE StudentID = '{Enrollent.StudentID}' AND 
                        CourseSectionID = '{Enrollent.CourseSectionID}')"""

            curs.execute(query)
            results = curs.fetchone()[0]

            if results == 1:
                Enrollent.delete_enrollment()
                conn.commit()
            else:
                self.error.exec()
        except Exception as E:
            print(Exception, E)

    def CancelButton(self):
        newWind = ClerkTools()
        widget.addWidget(newWind)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class CourseWindow(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("CoursesWindow.ui", self)
        self.label1.setText("")
        self.cancel.clicked.connect(self.CancelButton)
        self.addButton.clicked.connect(self.add_Course)
        self.modButton.clicked.connect(self.radioSelect)
        self.rmvButton.clicked.connect(self.rmv)

    def add_Course(self):
        new_Course = objects.Course(self.idEntry.text(), self.nameEntry.text(), self.crsCredit.text(), conn, curs)
        try:
            new_Course.add()
            conn.commit()
            self.label1.setText("Course Added")
            self.show()
        except Exception as E:

            newWind = CourseErrorWindow()
            widget.addWidget(newWind)
            newWind.label1.setText("Course Already Exists")
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def remove_Course(self):
        try:
            new_Course = objects.Course(self.idEntry.text(), self.nameEntry.text(), self.crsCredit.text(), conn, curs)
            new_Course.remove()
            conn.commit()
            self.label1.setText("Course Removed")
            self.show()

        except Exception as E:

            newWind = CourseErrorWindow()
            widget.addWidget(newWind)
            newWind.label1.setText("Invalid ID, That ID does not exist")
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def rmv(self):
        id = self.idEntry.text()

        if self.cID(id):
            new_Course = objects.Course(self.idEntry.text(), self.nameEntry.text(), self.crsCredit.text(), conn, curs)
            new_Course.remove()
            conn.commit()
            self.label1.setText("Course Removed")
            self.show()
        else:
            newWind = CourseErrorWindow()
            widget.addWidget(newWind)
            newWind.label1.setText("Invalid ID, That ID does not exist")
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def cID(self, ID):
        sql = "select CourseId from Course"
        curs.execute(sql)
        res = curs.fetchall()
        row = [item[0] for item in res]
        return ID in row

    def cName(self, name):
        sql = "select CourseName from Course"
        curs.execute(sql)
        res = curs.fetchall()
        row = [item[0] for item in res]
        return name in row

    def radioSelect(self):
        if self.radio1.isChecked():
            self.mod_course_id()
        if self.radio2.isChecked():
            pass
            # self.mod_course_name()

    def mod_course_id(self):
        new_Course = objects.Course(self.idEntry.text(), self.nameEntry.text(), self.crsCredit.text(), conn, curs)
        if self.cID(new_Course.CourseID):
            new_Course.modifyID(self.idEntry.text())
            conn.commit()

        else:
            newWind = CourseErrorWindow()
            widget.addWidget(newWind)
            newWind.label1.setText("Invalid Course Name, That Name does not exist")
            print(new_Course.CourseDescription)
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def mod_course_name(self):
        new_Course = objects.Course(self.idEntry.text(), self.nameEntry.text(), self.crsCredit.text(), conn, curs)
        pass

        # if radio2 and  modButton pressed and course ID not found go to error window and change text to red and output ID not found

        # if radio1 and  modButton pressed and course name not found go to error window and change text to red and output name not found

    def CancelButton(self):
        newWind = ClerkTools()
        widget.addWidget(newWind)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class CourseErrorWindow(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("CourseErrorWindow.ui", self)
        self.label1.setText("")
        self.cancel.clicked.connect(self.CancelButton)

    def add_Course(self):
        new_Course = objects.Course(self.idEntry.text(), self.nameEntry.text(), self.crsCredit.text(), conn, curs)
        try:
            new_Course.add()
            conn.commit()
            self.label1.setText("Course Added")
            self.show()
        except Exception as E:

            newWind = CourseErrorWindow()
            widget.addWidget(newWind)
            newWind.label1.setText("Course Already Exists")

            widget.setCurrentIndex(widget.currentIndex() + 1)

    def radioSelect(self):
        if self.radio1.isChecked():
            pass
            # self.mod_course_id()
        if self.radio2.isChecked():
            pass
            # self.mod_course_name()

    def mod_course_id(self):
        pass

    def mod_course_name(self):
        pass



    def CancelButton(self):
        newWind = CourseWindow()
        widget.addWidget(newWind)
        widget.setCurrentIndex(widget.currentIndex() + 1)



class ClerkStudentIDEntry(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("Clerk-Student-info-ID-Entry.ui", self)
        self.cancel.clicked.connect(self.CancelButton)
        self.searchButton.clicked.connect(self.GoToClerkStudentInfo)

    def GoToClerkStudentInfo(self):
        try:
            query = f"""SELECT StudentName FROM Student WHERE StudentID = '{self.lineEdit.text()}'"""
            curs.execute(query)
        except Exception as E:
            print(Exception, E)

        try:
            AdmStdInfo = ClerkStudentInfoDisplay(self.lineEdit.text(), curs.fetchone()[0])
        except Exception as E:
            print(Exception, E)
        widget.addWidget(AdmStdInfo)
        widget.setFixedWidth(900)
        widget.setFixedHeight(620)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def CancelButton(self):
        newWind = ClerkTools()
        widget.addWidget(newWind)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class ClerkStudentInfoDisplay(QDialog):
    def __init__(self, id_num, studentName):
        super().__init__()

        loadUi("Clerk-Student-Info-Display.ui", self)
        self.cancel.clicked.connect(self.CancelButton)

        self.display = QPushButton(self)
        self.display.move(320, 40)
        self.display.setText("Display")
        self.display.resize(80, 30)
        self.display.clicked.connect(self.view_info)

        self.student_id = id_num
        try:
            self.idNum.setText(id_num)
            self.stdName.setText(studentName)
        except Exception as E:
            print(Exception, E)


    def CancelButton(self):
        newWind = ClerkTools()
        widget.addWidget(newWind)
        widget.setFixedWidth(630)
        widget.setFixedHeight(620)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def view_info(self):
        try:
            query = f"""SELECT Enrollment.StudentID, Enrollment.CourseSectionID, CourseDescription, CourseFlag, CreditFlag FROM
                        Enrollment INNER JOIN Student S on S.StudentID = Enrollment.StudentID
                        INNER JOIN CourseSection Sec on sec.CourseSectionID = Enrollment.CourseSectionID
                        INNER JOIN Course C on Sec.CourseID = C.CourseID WHERE Enrollment.StudentID = '{self.student_id}'"""

            df = pd.read_sql_query(query, conn)
            print(df)
        except Exception as E:
            print(Exception, E)


class ClerkCourseSearch(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("Add-Student-to-Course.ui", self)
        self.cancel.clicked.connect(self.CancelButton)

    def CancelButton(self):
        newWind = ClerkTools()
        widget.addWidget(newWind)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class FlagStudentIDEntry(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("Flags-Student-info-ID-Entry.ui", self)
        self.cancel.clicked.connect(self.CancelButton)
        self.searchButton.clicked.connect(self.GoToStudentFlags)

    def GoToStudentFlags(self):
        newWindow = Flags(self.idEntry.text())
        widget.addWidget(newWindow)
        widget.setFixedWidth(670)
        widget.setFixedHeight(620)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def CancelButton(self):
        newWind = ClerkTools()
        widget.addWidget(newWind)
        widget.setCurrentIndex(widget.currentIndex() + 1)




class Flags(QDialog):
    def __init__(self, id_num):
        super().__init__()
        loadUi("Flags.ui", self)
        self.stuID = id_num
        self.cancel.clicked.connect(self.CancelButton)

        self.display = QPushButton(self)
        self.display.move(320, 40)
        self.display.setText("Display")
        self.display.resize(80, 30)

        try:
            self.rmvButton.clicked.connect(self.removeflagcourse)
            self.display.clicked.connect(self.display_flags)
        except Exception as E:
            print(Exception, E)

    def CancelButton(self):
        newWind = ClerkTools()
        widget.addWidget(newWind)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def display_flags(self):

        # GUI Expert - Need to get this into the display somehow. -Nate
        query = f"""SELECT CourseSectionID, CourseFlag, CreditFlag FROM Enrollment WHERE StudentID = '{self.stuID}'
        AND CourseFlag != '0' OR CreditFlag != '0' """

        try:
            df = pd.read_sql_query(query, conn)
            print(df)
        except Exception as e:
            print(Exception, e)

    def removeflagcourse(self):
        try:

            query = f"""UPDATE Enrollment SET CourseFlag = '0' WHERE CourseSectionID = '{self.crsSecID.text()}'"""
            query2 = f"""UPDATE Enrollment SET CreditFlag = '0' WHERE CourseSectionID = '{self.crsSecID.text()}'"""

            curs.execute(query)
            curs.execute(query2)
            conn.commit()

        except Exception as E:
            print(Exception, E)


class StudentInfoMain(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("Student-Info.ui", self)
        self.infobttn.clicked.connect(self.goToStudentInfo)
        self.Add_Drop_bttn.clicked.connect(self.goToCourseSearch)
        self.cancel.clicked.connect(self.CancelButton)

        self.label1.setHidden(True)

    def CancelButton(self):
        newWind = MainWindow()
        widget.addWidget(newWind)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToStudentInfo(self):
        query = f"""SELECT StudentName FROM Student WHERE StudentID = '{self.idNum.text()}'"""
        curs.execute(query)

        StdInfo = StudentInfoDisplay(self.idNum.text(), curs.fetchone()[0])
        widget.addWidget(StdInfo)

        StdInfo.idNum.setText(self.label1.text())

        widget.setFixedWidth(900)
        widget.setFixedHeight(620)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def goToCourseSearch(self):
        crsSrch = CourseSearch()
        widget.addWidget(crsSrch)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class StudentInfoDisplay(QDialog):
    def __init__(self, id_num, studentName):
        super().__init__()
        loadUi("Student-Info-Display.ui", self)
        self.cancel.clicked.connect(self.CancelButton)
        self.idNum = id_num
        self.stdName = studentName

def CancelButton(self):
        newWind = StudentInfoMain()
        widget.addWidget(newWind)
        widget.setFixedWidth(630)
        widget.setFixedHeight(620)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class CourseSearch(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("Maintain-Course-Data.ui", self)
        self.cancel.clicked.connect(self.CancelButton)

    def CancelButton(self):
        newWind = StudentInfoMain()
        widget.addWidget(newWind)
        widget.setCurrentIndex(widget.currentIndex() + 1)


app = QApplication(sys.argv)
login = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(login)
widget.setFixedWidth(630)
widget.setFixedHeight(620)
widget.setWindowTitle("NORTH-STAR Registration System")
widget.setWindowIcon(QtGui.QIcon("NSIcon.png"))
widget.show()
app.exec_()
