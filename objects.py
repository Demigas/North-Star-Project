# Python 3.9.6 (tags/v3.9.6:db3ff76, Jun 28 2021, 15:26:21) [MSC v.1929 64 bit (AMD64)] on win32
# Type "help", "copyright", "credits" or "license()" for more information.
import sqlite3 as sql
from typing import Tuple
# import guiwindow
import sys


class Student:
    def __init__(self, StudentID, StudentName, conn: sql.Connection, curs: sql.Cursor):
        self.StudentID = StudentID
        self.conn = conn
        self.curs = curs
        self.StudentName = StudentName

    def addStudent(self):
        query = f"""INSERT INTO Student (StudentID, StudentName)
                    VALUES (?, ?) """

        self.curs.execute(query, [str(self.StudentID), str(self.StudentName)])

    def removeStudent(self):
        query = f"""DELETE
                    FROM Student
                    WHERE StudentID = ? """

        self.curs.execute(query, [str(self.StudentID)])

    def modifyStudent(self):
        query = f"""UPDATE Student
                SET StudentName = ?
                WHERE StudentID = ?
                """
        self.curs.execute(query, [str(self.StudentName), str(self.StudentID)])


class Instructor:
    def __init__(self, InstructorID, InstructorName, conn: sql.Connection, curs: sql.Cursor):
        self.conn = conn
        self.curs = curs
        self.InstructorID = InstructorID
        self.InstructorName = InstructorName


    def addInstructor(self):
        query = f"""INSERT INTO Instructor (InstructorID, InstructorName)
                    VALUES (?, ?) """

        self.curs.execute(query, [str(self.InstructorID), str(self.InstructorName)])

    def removeInstructor(self):
        query = f"""DELETE
                    FROM Instructor
                    WHERE InstructorID = ? """

        self.curs.execute(query, [str(self.InstructorID)])

    def modifyInstructor(self):
        query = f"""UPDATE Instructor
                SET InstructorName = ?
                WHERE InstructorID = ?
                """
        self.curs.execute(query, [str(self.InstructorName), str(self.InstructorID)])


class Course:
    def __init__(self, CourseID, CourseDescription, Coursecredits, conn: sql.Connection, curs: sql.Cursor):
        self.conn = conn
        self.curs = curs
        self.CourseID = CourseID
        self.CourseDescription = CourseDescription
        self.Coursecredits = Coursecredits

    def add(self):
        query = f"""INSERT INTO Course 
                (CourseID, CourseDescription,Coursecredits) 
                VALUES (?,?,?)"""
        self.curs.execute(query, [str(self.CourseID), str(self.CourseDescription), int(self.Coursecredits)])

    def modifyCred(self):
        query = f"""UPDATE Course
                SET Coursecredits =?
                WHERE CourseID = ?"""
        self.curs.execute(query, [int(self.Coursecredits), str(self.CourseID)])

    def modifyDesc(self):
        query = f"""UPDATE Course
                  SET CourseDescription =?
                  WHERE CourseID = ?"""
        self.curs.execute(query, [int(self.CourseDescription), str(self.CourseID)])


    #
    # def modifyname(self):
    #     query = f"""UPDATE Course
    #                           SET CourseID = ?
    #                           WHERE CourseCourseDescription = ?
    #                           """
    #     self.curs.execute(query, [int(self.CourseID), str(self.CourseDescription)])



    def remove(self):
        query = f"""DELETE
                FROM Course
                WHERE CourseID = ? 
                """
        self.curs.execute(query, [str(self.CourseID)])


class CourseSection:
    def __init__(self, CourseID, CourseSectionID, InstructorID, SectionCapacity, conn: sql.Connection,
                 curs: sql.Cursor):
        self.conn = conn
        self.curs = curs
        self.CourseID = CourseID
        self.InstructorID = InstructorID
        self.CourseSectionID = CourseSectionID
        self.SectionCapacity = SectionCapacity

    def add(self):
        query = f"""INSERT INTO CourseSection
                (CourseID, CourseSectionID,InstructorID, SectionCapacity)
                VALUES (?,?,?,?)"""
                #({self.CourseID},{self.CourseSectionID},{self.InstructorID}, {self.SectionCapacity})
        self.curs.execute(query, [str(self.CourseID), str(self.CourseSectionID),str(self.InstructorID),int(self.SectionCapacity)])

    def remove(self):
        query = f"""DELETE
                    FROM CourseSection
                    WHERE CourseSectionID = ?"""
        self.curs.execute(query, [str(self.CourseSectionID)])


    def modifySectionCap(self):
        query = f"""UPDATE CourseSection
                SET SectionCapacity = ?
                WHERE CourseSectionID = ?"""
        self.curs.execute(query, [int(self.SectionCapacity),str(self.CourseSectionID)])

    def modifySectionInstructor(self):
        query = f"""UPDATE CourseSection
                SET InstructorID = ?
                WHERE CourseSectionID = ?"""
        self.curs.execute(query, [str(self.InstructorID), str(self.CourseSectionID)])


class Enrollment:
    # Remove from init once auto inc
    def __init__(self, StudentID, CourseID, CourseSectionID,
                 conn: sql.Connection, curs: sql.Cursor):
        self.conn = conn
        self.curs = curs
        self.StudentID = StudentID
        #self.SectionCapacity = SectionCapacity
        self.CourseSectionID = CourseSectionID
        self.courseFlag = "0"
        self.creditFlag = "0"
        self.CourseID = CourseID

    def delete_enrollment(self):
        query = f"""DELETE FROM Enrollment WHERE StudentID = '{self.StudentID}' 
        AND CourseSectionID = '{self.CourseSectionID}'"""

        self.curs.execute(query)


    def check_credits(self):
        query = f"""SELECT SUM(C.CourseCredits)
                FROM Course C, CourseSection S, Enrollment E
                WHERE E.StudentID = ?
                AND E.CourseSectionID = S.CourseSectionID
                AND S.CourseID = C.CourseID"""
        self.curs.execute(query, [str(self.StudentID)])
        creditamnt = self.curs.fetchone()[0]
        return creditamnt

    # SELECT count* TABLE CRITERIA
    def check_enrollment(self):
        query = f"""SELECT COUNT(*)
                    FROM Enrollment
                    WHERE Enrollment.CourseSectionID = ?"""
        self.curs.execute(query, [str(self.CourseSectionID)])
        capcount = self.curs.fetchone()[0]
        return capcount

    def addCredFlag(self, new_course_add: Course):
        if self.check_credits() + int(new_course_add.Coursecredits) > 12:
            self.creditFlag = "1"
        else:
            self.creditFlag = "0"

    def addCapFlag(self):
        if self.check_enrollment() - 1 < 0:
            self.courseFlag = "1"
        else:
            self.courseFlag = "0"

    def removeCapFlag(self):
        self.CourseFlag = "0"
        self.add_enrollment()

    def removeCreditFlag(self):
        self.CreditFlag = "0"
        self.add_enrollment()

    def add_enrollment(self):
        query = f"""SELECT * FROM Course WHERE CourseID = '{self.CourseID}'"""
        self.curs.execute(query)
        results = self.curs.fetchone()
        course = Course(results[0],results[1],results[2],self.conn, self.curs)
        self.addCredFlag(course)
        self.addCapFlag()


        # Once swapped to auto inc, remove enrollmentid
        query = f"""INSERT INTO Enrollment
            (StudentID, CourseSectionID,CourseFlag,CreditFlag)
            VALUES(?,?,?,?) """
        self.curs.execute(query, [str(self.StudentID),
                                  str(self.CourseSectionID), str(self.courseFlag), str(self.creditFlag)])



# When Link -> Make sure to test display student info using Nates query from github
# def main():
#     db_connection = sql.connect("Northstarproject.db")
#     cursor = db_connection.cursor()
#
#     enrollment1 = Enrollment("004","002299","DRM150","356",db_connection,cursor)
#     enrollment1.add_enrollment()
#     db_connection.commit()
# main()
