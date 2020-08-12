from sqlalchemy import Column, Integer, String ,create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import LONGTEXT
import random

engine = create_engine('mysql://root:giri@localhost:3306/giri', echo=True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Questions(Base):
    __tablename__ = 'Questions'
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer)
    time = Column(Integer)
    duration = Column(Integer)
    question = Column(LONGTEXT())

    def __init__(self,teacher_id,time=0,duration=0,question=None):
        self.teacher_id=teacher_id
        self.time=time
        self.duration=duration
        self.question=question

    def insert(self):
        Base.metadata.create_all(engine)
        c1 = Questions(teacher_id=self.teacher_id, time=self.time, duration=self.duration, question=self.question)
        session.add(c1)
        session.commit()
        self.display()
        return 1

    def delete(self,id):
        #det=session.query(Questions).get(id)
        #session.delete(det)
        session.query(Questions).delete()
        session.commit()
    def display(self):
        dis = session.query(Questions).all()
        for i in dis:
            print('q',i.teacher_id, i.question)