from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///schools.db')
Session = sessionmaker(bind=engine)

class SchoolPerformance(Base):
    __tablename__ = 'performance'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    performance_metric = Column(String)

Base.metadata.create_all(engine)

def save_school_performance_data(data):
    session = Session()
    school = SchoolPerformance(name=data['name'], performance_metric=data['metric'])
    session.add(school)
    session.commit()
    session.close()

def get_worst_performing_high_schools():
    session = Session()
    schools = session.query(SchoolPerformance).order_by(SchoolPerformance.performance_metric).all()
    session.close()
    return schools
