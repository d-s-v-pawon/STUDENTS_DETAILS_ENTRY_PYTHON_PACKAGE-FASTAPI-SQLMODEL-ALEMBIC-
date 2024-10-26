import re
import random
import copy
from tabulate import tabulate
import string
class STUDENTS:
    name_chars=[string.whitespace[0]]
    for i in range(26):
        name_chars.append(string.ascii_uppercase[i])
    genders=['MALE','FEMALE']
    standards=[1,2,3,4,5,6,7,8,9,10]
    max_percentage=100
    def __init__(self,name,gender,age,sch_name,standard,section,r_no,c_no,percent):
        class Invalidname(Exception):
            pass
        class Invalidgender(Exception):
            pass
        class Invalidclass(Exception):
            pass
        class Invalidcontact(Exception):
            pass
        class Invalidpercent(Exception):
            pass
        try:
            name=name.upper()
            for i in name:
                if i not in STUDENTS.name_chars:
                    raise Invalidname
                else:
                    pass
            self.name=name
        except Invalidname:
            print("NAME SHOULD CONTAIN ONLY ALPHABETS")
            while(True):                
                self.name=input("ENTER VALID NAME:")
                self.name=self.name.upper()
                for i in self.name:
                    if i not in STUDENTS.name_chars:
                        self.name=''
                        break
                if len(self.name)>2:
                    print(self.name)
                    break
        try:
            gender=gender.upper()
            if gender not in STUDENTS.genders:
                raise Invalidgender
            self.gender=gender
        except Invalidgender:
            print("STUDENT MUST BE MALE OR FEMALE")
            while(True):
                self.gender=input("ENTER THE CORRECT GENDER:")
                self.gender=self.gender.upper()
                if self.gender not in STUDENTS.genders:
                    self.gender=''
                else:
                    print(self.gender)
                    break
        self.age=age
        self.sch_name=sch_name
        try:
            if standard not in STUDENTS.standards:
                raise Invalidclass
            self.standard=standard
        except Invalidclass:
            print("THE SCHOOLS CONSISTS STANDARDS FROM 1 TO 10 ONLY")
            while(True):
                self.standard=int(input("ENTER THE CORRECT STANDARD:"))
                if self.standard in STUDENTS.standards:
                    print(self.standard)
                    break                    
        self.section=section
        self.r_no=r_no
        try:
            if len(str(c_no))!=10:
                raise Invalidcontact
            self.c_no=c_no
        except Invalidcontact:
            print("CONTACT NUMBER CONTAINS ONLY 10DIGITS IN MAXIMUM")
            while(True):
                self.c_no=int(input("ENTER VALID CONTACT:"))
                if len(str(self.c_no))==10:
                    break
        try:
            if percent>STUDENTS.max_percentage:
                raise Invalidpercent
            self.percent=percent
        except Invalidpercent:
            print("PERCENTAGE SHOULD NOT EXCEED 100")
            while(True):
                self.percent=int(input("ENTER VALID PERCENTAGE:"))
                if self.percent<STUDENTS.max_percentage:
                    break
        finally:
            print(f"THE STUDENT {self.name} GENERAL DETAILS ENTRY IS COMPLETED")
    def stu_details(self):
        print("THE STUDENT DETAILS ARE AS FOLLOWS")
        print("NAME OF THE STUDENT:",self.name)
        print("GENDER:",self.gender)
        print("AGE:",self.age)
        print("SCHOOL NAME:",self.sch_name)
        print("CLASS:",self.standard)
        print("SECTION:",self.section)
        print("ROLL NUMBER:",self.r_no)
        print("CONTACT NUMBER:",self.c_no)
        print("ANNUAL PERCENTAGE:",self.percent)
    def ext_acts(self):
        class highstd(Exception):
            pass
        class noact(Exception):
            pass
        try:
            if self.standard==10:
                raise highstd
        except highstd:
            print("THE STUDENT IS NOT HAVE THE CHANCE TO PARTICIPATE IN CO-CURRICULAR ACTIVITIES")
        else:
            print("THE STUDENT IS ELLIGIBLE TO LEARN EXTRA CO-CURRICULAR ACTIVITIES")
            CO_ACTS=["STUDENT COUNCIL","SCHOOL NEWSPAPER","DRAMA","BOOK CLUB","POETRY","EDITING","MASS DRILL","CULTURAL EVENTS","SOCIAL WORKK"]
            print("THE FOLLOWING ARE THE CO-CURRICULAR ACTIVITIES IN THE SCHOOL")
            print(*CO_ACTS,sep=",")
            try:
                stu_co_act=input(f"ENTER THE ACTIVITY WHICH {self.name} IS LIKELY TO PARTICIPATE IN THE ABOVE LIST:")
                stu_co_act=stu_co_act.upper()
                if stu_co_act not in CO_ACTS:
                    raise noact
            except noact:
                print("PLEASE,TRY AGAIN")
                print("NEXT TIME CHOOSE WISELY WIHIN THE ABOVE ACTVITY LIST ONLY")
            else:
                print(f"GOOD CHOICE!AND WISH YOU GOOD LUCK TO GAIN GOOD KNOWLEDGE IN THE {stu_co_act} ACTIVITY")
        finally:
            print("THE CO-CURRICULAR ACTIVITIES SESSION ENDED")

