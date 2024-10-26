from sqlmodel import SQLModel , Field 
from sqlalchemy import Column,BigInteger,Integer

class StudentsBase(SQLModel):
            NAMES : str = Field(nullable=False)
            GENDERS : str = Field(nullable=False)
            AGES : int = Field(nullable=False)

class STUDENTS_DETAILS(StudentsBase,table=True):            
            SCHOOL_NAMES : str = Field(nullable=False)
            STANDARDS : int = Field(nullable=False)
            SECTIONS : str = Field(nullable=False)
            ROLL_NUMBERS : int = Field(sa_column=Column(Integer, nullable=False))
            CONTACT_NUMBERS : int = Field(sa_column=Column(BigInteger,nullable=False,primary_key=True,unique=True))
            PERCENTAGES : float = Field(nullable=False)
