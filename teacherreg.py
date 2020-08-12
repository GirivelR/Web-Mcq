from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('mysql://root:giri@localhost:3306/giri', echo=True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Teacher(Base):
    __tablename__ = 'Teacher'
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer)
    name = Column(String(50))
    password = Column(String(50))
    subject = Column(String(50))

    def __init__(self,teacher_id=None,name=None,password=None,subject=None,):
        self.teacher_id=teacher_id
        self.name=name
        self.password=password
        self.subject=subject

    def insert(self):
        Base.metadata.create_all(engine)
        print(self.teacher_id)
        if session.query(Teacher).filter(Teacher.teacher_id!=self.teacher_id):
            c1 = Teacher(teacher_id=self.teacher_id,name=self.name, password=self.password, subject=self.subject)
            session.add(c1)
            session.commit()
        else:
            self.insert()

    def login(self):
        result = session.query(Teacher).all()
        for i in result:
            print(i.name,self.name,i.password,self.password)
            if i.name==self.name and i.password==self.password:
                return [1,i.teacher_id]
        return [0,0]

    def delete(self):
        try:
            num_rows_deleted = session.query(Teacher).delete()
            session.commit()
        except:
            session.rollback()
    def display(self):
        dis=session.query(Teacher).all()
        for i in dis:
            print(i.name,i.password,i.teacher_id)