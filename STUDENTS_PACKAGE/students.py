import re
import random                            #The Following modules should be imported before creating the class STUDENTS
import string
import json
from sqlmodel import SQLModel , Field 
from sqlalchemy import Column,BigInteger,Integer
from fastapi import FastAPI,Depends
from sqlmodel import Session , select
from sqlmodel import create_engine , Session , SQLModel

DATABASE_URL = 'mssql+pyodbc://@LAPTOP-04Q912VM\SQLEXPRESS/SCHOOL_EDUCATION?driver=ODBC+Driver+17+for+SQL+Server&Trusted_connection=yes'

engine = create_engine(DATABASE_URL)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

app = FastAPI()

class StudentsBase(SQLModel):
        NAMES : str = Field(nullable=False)
        GENDERS : str = Field(nullable=False)
        AGES : int = Field(nullable=False)

class STUDENTS_DETAILS(StudentsBase,table = True):
        __tablename__ = 'STUDENTS_INFO'

        SCHOOL_NAMES : str = Field(nullable=False)
        STANDARDS : int = Field(nullable=False)
        SECTIONS : str = Field(nullable=False)
        ROLL_NUMBERS : int = Field(sa_column=Column(Integer, nullable=False,unique=True))
        CONTACT_NUMBERS : int = Field(sa_column=Column(BigInteger,nullable=False,primary_key=True,unique=True))
        PERCENTAGES : float = Field(nullable=False)

@app.post("/Students_Details_Entry")
def enter_student(student_data : STUDENTS_DETAILS,session : Session = Depends(get_session)):                      
            student = STUDENTS_DETAILS(NAMES=student_data.NAMES,
                                GENDERS=student_data.GENDERS,
                                AGES=student_data.AGES,
                                SCHOOL_NAMES=student_data.SCHOOL_NAMES,
                                STANDARDS=student_data.STANDARDS,
                                SECTIONS=student_data.SECTIONS,
                                ROLL_NUMBERS=student_data.ROLL_NUMBERS,
                                CONTACT_NUMBERS=student_data.CONTACT_NUMBERS,
                                PERCENTAGES=student_data.PERCENTAGES)
            session.add(student)
            session.commit()
            return student

@app.get("/All_Students",response_model=list[STUDENTS_DETAILS])
def get_students(session : Session = Depends(get_session)) -> list[STUDENTS_DETAILS]:            
            students_list = session.exec(select(STUDENTS_DETAILS)).all()
            return students_list


class STUDENTS:                                 #Create a class named STUDENTS

    name_chars=[string.whitespace[0]]           #Creates a list named name_chars with space as an element in the list
    for i in range(26):
        name_chars.append(string.ascii_uppercase[i])        #Appends all the uppercase alphabets into the list name_chars
    data_to_write={                                     #The static properties of the class STUDENTS to be entered into the json file
                    "name_chars":name_chars,
                    "genders":['MALE','FEMALE'],
                    "standards":[1,2,3,4,5,6,7,8,9,10],
                    "max_percentage":100
    }
    with open("STUDENTS_PACKAGE/properties.json","w") as f1:        #Creates/Opens the properties.json file in writing mode and writes all the data into the json file
        json.dump(data_to_write,f1,indent=4)

    def __init__(self,name,gender,age,sch_name,standard,section,r_no,c_no,percent):         #The __init__ constructor is used for taking the students details as instance variables of each individual student


        with open("STUDENTS_PACKAGE/properties.json","r") as json_file:            #The properties.json file is opened in reading mode to work with static data in the file
            data = json.load(json_file)

        #USER-DEFINED EXCEPTIONS CREATION        
        class Invalidname(Exception):                
            pass
        class Invalidgender(Exception):
            pass
        class Invalidage(Exception):
            pass
        class Invalidclass(Exception):
            pass
        class Invalidrollno(Exception):
            pass
        class Invalidcontact(Exception):
            pass
        class Invalidpercent(Exception):
            pass
        try:    
            name=name.upper()           #Converts all the characters of the name into uppercase
            for i in name:
                if i not in data.get('name_chars'):     #Checks for the each character of the name in the name_chars list of the json file
                    raise Invalidname                   #If any letter of the name is not in the name_chars list raises an user defined exception Invalidbname
                else:
                    pass
            self.name=name                  #If no error raised accepts the name as an instance variable
        except Invalidname:                 #This is the except block for the Exception Invalidname
            print("NAME SHOULD CONTAIN ONLY ALPHABETS")
            while(True):                                        #Asks for a valid name until all the letters of the name is in name_chars list
                self.name=input("ENTER VALID NAME:")            
                self.name=self.name.upper()
                for i in self.name:
                    if i not in data.get('name_chars'):
                        self.name=''
                        break
                if len(self.name)>2:
                    print(self.name)
                    break
        try:
            gender=gender.upper()               #Converts all the characters of the gender into uppercase
            if gender not in data.get('genders'):           #Checks for the entered gender name in the genders list of the json file
                raise Invalidgender                     #If the entered gender is not in the genders list raises an user defined exception Invalidgender
            self.gender=gender                      #If no error raised accepts the gender as an instance variable
        except Invalidgender:                   #This is the except block for the Exception Invalidgender
            print("STUDENT MUST BE MALE OR FEMALE")
            while(True):                #Asks for a valid gender until the gender is in genders list
                self.gender=input("ENTER THE CORRECT GENDER:")
                self.gender=self.gender.upper()
                if self.gender not in data.get('genders'):
                    self.gender=''
                else:
                    print(self.gender)
                    break
        try:
            if not str(age).isdigit():      
                raise Invalidage        #If the entered age is not a numerical value raises an exception Invalidage
            self.age=int(age)            #If the entered age is a numerical value directly takes the age as an instance variable
        except Invalidage:          #This is the except block for the Invalidage
            while(True):            #Asks for a valid age until the entered age is an numerical value
                self.age=int(input("ENTER THE VALID AGE(ONLY IN DIGITS):"))
                if str(self.age).isdigit():
                    break
        self.sch_name=sch_name.upper()          #Accepts the school name as an instance variable by default converting into uppercase
        try:
            if int(standard) not in data.get('standards'):           #Checks if the standard of the student is in standards list
                raise Invalidclass                  #If the entered standard of the student is not in the standards list raises an exception Invalidclass
            self.standard=int(standard)                #If no error raised accepts the entered standard as an instance variable
        except Invalidclass:                    #Except block of the Exception Invalidclass
            print("IN GENERAL THE SCHOOLS CONSISTS STANDARDS FROM 1 TO 10 ONLY")
            while(True):            #Asks for a valid standard until the entered standard is in the standards list of a general school
                self.standard=int(input("ENTER THE CORRECT STANDARD:"))
                if self.standard in data.get('standards'):
                    print(self.standard)
                    break                    
        self.section=section.upper()            #Takes the entered section of the student as an instance variable by default in uppercase
        try:
            if not str(r_no).isdigit():         #Check if the roll number contains only digits otherwise raise an exception Invalidrollno
                raise Invalidrollno       #If the entered r_no is not a numerival value raises an exception Invalidrollno
            self.r_no=int(r_no)           #If the entered r_no is a numerical value directly takes the r_no as an instance variable
        except Invalidrollno:          #This is the except block for the Invalidrollno
            while(True):            #Asks for a valid roll number until the entered r_no is an numerical value
                self.r_no=int(input("ENTER THE VALID AGE(ONLY IN DIGITS):"))
                if str(self.r_no).isdigit():
                    break
        try:
            if str(c_no).isdigit():                 #Checks if the contact number contains only digits otherwise raise an exception Invalidcontact
                if len(str(c_no))!=10:              #If the entered number does not contain ten digits raises an exception Invalidcontact:
                    raise Invalidcontact
                self.c_no=int(c_no)                      #If no exception raises takes the contact number as an instance variable
            else:
                raise Invalidcontact
        except Invalidcontact:                      #This the except block for the exception Invalidcontact
            print("CONTACT NUMBER CONTAINS ONLY 10DIGITS IN MAXIMUM")
            while(True):                    #Asks for a valid contact number until the entered contact contains only digits
                self.c_no=int(input("ENTER VALID CONTACT:"))
                if str(c_no).isdigit():
                    if len(str(self.c_no))==10:
                        break
        try:
            if type(percent)==float or str(percent).isdigit():               #Checks if the entered percentage contains only numerical value or the entered percentage is a float value otherwise raises an exception Invalid percent
                if float(percent)>data.get('max_percentage'):              #If entered percentage is greater than maximum percentage raises an exception Invalidpercent
                    raise Invalidpercent
                self.percent=float(percent)          #IF no exception occurs by default takes the percentage of the student as an instance variable
            else:
                raise Invalidpercent
        except Invalidpercent:              #This is the except block for the exception Invalidpercent
            print("PERCENTAGE SHOULD NOT EXCEED 100")
            while(True):                            #Asks for a valid percentage until the entered percentage is less than maximum percentage
                self.percent=float(input("ENTER VALID PERCENTAGE:"))          
                if self.percent<data.get('max_percentage'):
                    break
        finally:
            print(f"THE STUDENT {self.name} GENERAL DETAILS ENTRY IS COMPLETED")


        def add_student_directly():
            db = next(get_session())
            student = STUDENTS_DETAILS(
                NAMES=self.name,
                GENDERS=self.gender,
                AGES=self.age,
                SCHOOL_NAMES=self.sch_name,
                STANDARDS=self.standard,
                SECTIONS=self.section,
                ROLL_NUMBERS=self.r_no,
                CONTACT_NUMBERS=self.c_no,
                PERCENTAGES=self.percent
            )
            enter_student(student, db)
            print("Student added successfully")


        add_student_directly()


        
    def stu_details(self):              #The student object can use this method to shows all the details of the respective student entered
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



    def read(self):                 #The student object can use this method to read the content of some particular subjects
        class Invalidsubject(Exception):            #User-defined exception 
            pass
        print(f"HI! {self.name} HAVE A GREAT READING SESSION")
        SUB=["TELUGU","HINDI","ENGLISH","MATHS","SCIENCE","SOCIAL"]         #List of the subjects to read
        SUBJECTS={"TELUGU":"యోగి వేమన, 17వ శతాబ్దంలో ప్రస్తుతం తెలుగు సాహిత్యంలో ఒక ప్రముఖ కవి-సేంట్‌పోయెట్‌. అతని పద్యాలు జీవితం, ప్రేమ, మరియు విశ్వాన్ని ప్రతినిధించే అంశాలను ప్రతిపాదిస్తాయి. అతని పద్యాలు సరళమైన భాషలో ఉంటాయి మరియు జీవితంలో అద్భుతమైన అంశాలను ప్రతిపాదిస్తాయి.",
                 "HINDI":'''प्रेमचंद, जिनका असली नाम मुंशी प्रेमचंद राय था, एक प्रमुख हिंदी कवि, उपन्यासकार, और समाजशास्त्री थे।उनके उपन्यास और कहानियाँ सामाजिक मुद्दों, जीवन की सच्चाई, और आध्यात्मिकता के मुद्दों पर आधारित थे।''',
                 "ENGLISH":"Elizabeth Alexander is an American poet, writer, and literary scholar. She has made significant contributions to both poetry and academia.",
                 "MATHS":"Calculus: The study of limits, derivatives, and integrals. It helps us understand rates of change and motion.",
                 "SCIENCE":'''Sulfur played a crucial role in the formation of Earth’s first water.Some deep-sea oxygen might be generated by metal-rich chunks on the seafloor.''',
                 "SOCIAL":''' Poverty persists worldwide, leading to unequal access to resources, education, and healthcare.Impact: Poverty perpetuates cycles of disadvantage and limits opportunities.'''}
        try:
            subject=input(f"ENTER THE SUBJECT {self.name} WANTS TO READ:")      #Asks for the input of the subject to read
            subject=subject.upper()
            if subject not in SUB:
                raise Invalidsubject
        except Invalidsubject:          #The exception block for the User-Definde Exception Invalidsubject
            print("THE MAIN SUBJECTS NAMES ARE AS FOLLOWS")
            for i in SUB:           #This for loop prints all the subjects names in order to aware the user about the readable subjects
                if i!=SUB[len(SUB)-1]:
                    print(i,end=',')
                else:
                    print(i)
            while(True):                #Asks for a valid subject input until the subect entered is in the subjects list
                subject=input(f"ENTER THE SUBJECT {self.name} WANTS TO READ IN THE ABOVE LIST:")
                subject=subject.upper()
                if subject in SUB:
                    self.subject=subject
                    break
            print(f"GOOD CHOICE! START READING THE {self.subject} SUBJECT")
            print(f"This is the content for {self.name} to read from the selected {self.subject} subject")
            print(SUBJECTS.get(self.subject))
            self.read_lines=SUBJECTS.get(self.subject)#Assigns the read content to the variable for further use
        else:                           #If no exception occurs the else block will be executed
            self.subject=subject
            print(f"GOOD CHOICE! START READING THE {self.subject} SUBJECT")
            print(f"This is the content for you to read of your selected {self.subject} subject")
            print(SUBJECTS.get(self.subject))
            self.read_lines=SUBJECTS.get(self.subject)
        finally:
            print("READING SESSION ENDED")



    def write(self):                        #The student object can use this method to write the content of some particular subjects
        class Invalidcommand(Exception):
            pass
        class Invalidsubject(Exception):        #User-defined exceptions
            pass
        class notmatch(Exception):
            pass
        try:
            command=input("DO YOU WANT TO WRITE WHAT YOU HAVE READ(Y/N):")          #Asks for the input of the subject to choose to write what student object is read or write something 
            command=command.lower()
            if not re.match("^[y&n]",command):          #If invalid inputs are given raise an exception Invalidcommand
                raise Invalidcommand
        except Invalidcommand:                      #The except block of Invalidcommand
            print("Error! Only letters Y AND N allowed!")
            print("PLEASE TRY AGAIN")
        else:                       #If no error occurs the else block will be executed
            self.command=command
            if(command=="n"):           #If the given command is no then the student can write into the subject he wants
                print(f"HI! {self.name} HAVE A GREAT WRITING SESSION")
                SUBJECTS={"TELUGU":"",
                          "HIINDI":"",
                          "ENGLISH":"",
                          "MATHS":"",           #The dictionary for the subjects to hold the content written into the respected subject
                          "SCIENCE":"",
                          "SOCIAL":""}
                try:
                    subject=input("ENTER THE SUBJECT FOR WHICH YOU WANT TO WRITE THE NOTES:")                   #Asks for the input to enter the subject for which we want to write into the notes             
                    subject=subject.upper()
                    if subject not in SUBJECTS.keys():          #If there is no subject of entered name raises an exception Invalidsubject
                        raise Invalidsubject
                except Invalidsubject:          #The except block fir Invalidsubject
                     print("THE MAIN SUBJECTS NAMES ARE AS FOLLOWS")
                     print(SUBJECTS.keys())
                     while(True):                       #Asks for a valid subject until the entered subject is in the subjects list
                         subject=input("ENTER THE SUBJECT FOR WHICH YOU WANT TO WRITE THE NOTES FROM THE ABOVE LIST:")                        
                         subject=subject.upper()
                         if subject in SUBJECTS.keys():
                             print(f"GOOD CHOICE! START WRITING THE {subject} SUBJECT")
                             SUBJECTS[subject]=input("WRITE WHAT YOU KNOW ABOUT THE SUBJECT:")
                             written_lines=SUBJECTS.get(subject)
                             print(f"THIS IS THE CONTENT YOU HAVE WRITTEN INTO THE {subject} SUBJECT NOTES")
                             print(f"{subject} : {written_lines}")
                             break                
                else:           #If no exception occurs the else block will be executed
                    print(f"GOOD CHOICE! START WRITING THE {subject} SUBJECT")
                    SUBJECTS[subject]=input("WRITE WHAT YOU KNOW ABOUT THE SUBJECT:")
                    written_lines=SUBJECTS.get(subject)
                    print(f"THIS IS THE CONTENT YOU HAVE WRITTEN INTO THE {subject} SUBJECT NOTES")
                    print(f"{subject} : {written_lines}")
            else:           #If the command is yes then the student can write what he read
                print(f"HI! {self.name} HAVE A GREAT WRITING SESSION")
                try:
                    self.written_lines=input("WRITE WHAT YOU HAVE READ:") #Asks to enter the content what student read
                    if self.written_lines!=self.read_lines:         #If read content not matched with write content raises an exception notmatch
                        raise notmatch
                except notmatch:                #The except block for notmatch
                    while(True):            #Takes the input until the read content is correctly written on asking command which is to be yes
                        print("NOT WRITTEN CORRECTLY")
                        command=input("DO YOU WANT TO WRITE AGAIN WHAT YOU HAVE READ(Y/N):")
                        command=command.lower()
                        if not re.match("^[y&n]",command):
                            print("Error! Only letters Y AND N allowed!")
                        elif command == 'Y':
                            self.written_lines=input("WRITE AGAIN")
                            if self.written_lines==self.read_lines:
                                print("YOU ARE CORRECTLY WRITTEN WHAT YOU HAVE READ")
                                break
                        else:
                            print('BETTER LUCK NEXT TIME')
                    return True
                else:
                    print("YOU ARE CORRECTLY WRITTEN WHAT YOU HAVE READ")
                    return True
        finally:
            print("WRITING SESSION ENDED")



    def learn(self):            #The student object can use this method to learn the content of some particular subjects
        class notwritten(Exception):            #User-defined exception
            pass
        try:
            if self.command!="y":               #if the command given in write method related to choose between write something into a different subject or write what student read is not yes raises an exception notwritten
                raise notwritten
        except notwritten:                  #The except block for notwritten
            print("PLEASE,WRITE THE READ CONTENT FIRST")
        else:                                               #If no exception raises then the else block will be executed
            if self.write() == True:            #If the write method returned the bool value True then the student is learnt perfectly about a subject
                print(f"YOU HAVE SUCCESSFULLY LEARNT THE CONTENT IN THE SUBJECT {self.subject}")
            else:
                print(f"STILL YOU HAVE TO WORK HARD ON THIS {self.subject} SUBJECT")
        finally:
            print("LEARNING SESSION ENDED")



    def play(self):                 ##The student object can use this method to know about the info related to playing games
        play={"1":'04',
              "2":'05',
              "3":'02',
              "4":'07',
              "5":'08',             #The dictionary of about classes and their games period respectively
              "6":'10',
              "7":'06',
              "8":'03',
              "9":'09',
              "10":"NONE"}
        GAMES=["BADMINTON","BASKETBALL","CYCLING","TENNIS","CRICKET","CHESS","KABADDI","VOLLEYBALL","SWIMMING","KHOKHO"]            #List of some games & sports
        if str(self.standard) in play.keys():       #If the standard of the student is in play dictionary then the games period for that respected standard is displayed
            print(f"THE GAMES PERIOD FOR CLASS {self.standard} STUDENT IS {play.get(str(self.standard))}")
        else:
            print("WRONG CLASS")
        if self.standard!=10:       #If the standard is not 10 then the student can play games choosen in random by the master in this case the compiler
            print(f"THESE ARE THE GAMES PLAYED BY THE STUDENTS IN THE SCHOOL")
            print(*GAMES,sep=",")
            T_GAME=random.choice(GAMES)
            print(f"NOW THE GAME PLAYED BY THE STUDENT {self.name} IN RANDOM CHOICE BY THE PET TEACHER IS {T_GAME}")


            
    def ext_acts(self):                 #The student object can access this method to enter the student's interested extra-curricular activities
        class highstd(Exception):
            pass
        class noact(Exception):#User-defined exceptions
            pass
        try:
            if self.standard==10:#For 10th class students there will be no extra-curricular acts so raises highstd exception
                raise highstd
        except highstd:
            print("THE STUDENT IS NOT HAVE THE CHANCE TO PARTICIPATE IN CO-CURRICULAR ACTIVITIES")
        else:#The else block will be executed if student is below 10th class
            print("THE STUDENT IS ELLIGIBLE TO LEARN EXTRA CO-CURRICULAR ACTIVITIES")
            CO_ACTS=["STUDENT COUNCIL","SCHOOL NEWSPAPER","DRAMA","BOOK CLUB","POETRY","EDITING","MASS DRILL","CULTURAL EVENTS","SOCIAL WORKK"]
            print("THE FOLLOWING ARE THE CO-CURRICULAR ACTIVITIES IN THE SCHOOL")
            print(*CO_ACTS,sep=",")
            try:
                stu_co_act=input(f"ENTER THE ACTIVITY WHICH {self.name} IS LIKELY TO PARTICIPATE IN THE ABOVE LIST:")#Asks for the ext_curricular_act name
                stu_co_act=stu_co_act.upper()
                if stu_co_act not in CO_ACTS:#If the act not in the CO_ACTS list the noact user defined exception raises
                    raise noact
            except noact:               #The except block for noact
                print("PLEASE,TRY AGAIN")
                print("NEXT TIME CHOOSE WISELY WIHIN THE ABOVE ACTVITY LIST ONLY")
            else:           #else block for noact
                print(f"GOOD CHOICE!AND WISH YOU GOOD LUCK TO GAIN GOOD KNOWLEDGE IN THE {stu_co_act} ACTIVITY")
        finally:
            print("THE CO-CURRICULAR ACTIVITIES SESSION ENDED")