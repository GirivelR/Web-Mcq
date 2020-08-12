from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://root:giri@localhost:3306/giri', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Student(Base):
    __tablename__ = 'Students'
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer)
    roll_name = Column(String(50))
    class_section = Column(String(50))
    password = Column(String(20))
    school = Column(String(50))
    marks = Column(String(100))
    def __init__(self,teacher_id=None,roll_name=None,class_section=None,password=None,school=None,marks=None):
        self.teacher_id=teacher_id
        self.roll_name=roll_name
        self.class_section=class_section
        self.password=password
        self.school=school
        self.marks=marks
    def insert(self):
        Base.metadata.create_all(engine)
        c1 = Student(teacher_id=self.teacher_id,roll_name=self.roll_name,class_section=self.class_section, password=self.password, school=self.school,marks=self.marks)
        session.add(c1)
        session.commit()
        self.display()
    def login(self):
        result = session.query(Student).all()
        for i in result:
            print(i.roll_name,self.roll_name,i.password,self.password)
            if i.roll_name==self.roll_name and i.password==self.password:
                return [1,i.teacher_id]
        return [0,0]

    def delete(self):
        try:
            session.query(Student).delete()
            session.commit()
            print('deleted')
        except:
            session.rollback()
    def display(self=None):
        dis=session.query(Student).all()
        l=[]
        for i in dis:
            print(type(i.teacher_id),type(self.teacher_id))
            if i.teacher_id==int(self.teacher_id):
                print('s', i.roll_name, i.school, i.password, i.teacher_id, i.marks)
                l.append([i.roll_name,i.teacher_id,i.school,i.class_section,i.marks,i.password])
        for i in dis:
            print('s',i.roll_name,i.school,i.password,i.teacher_id,i.marks)
        print(l)
        return l
    def marksupload(self):
        m=session.query(Student).all()
        for i in m:
            if i.roll_name==self.roll_name:
                i.marks=self.marks
        self.display()
