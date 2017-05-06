from bottle.ext import sqlalchemy
from sqlalchemy import Column, Boolean, Integer, String, create_engine

from sqlalchemy.orm import sessionmaker
import ParkingConfig as config
import sys
sys.path.append('/Users/braj/git/ParkingLots/')
print sys.path
from backend.models.ParkingLot import ParkingLot
from backend.models.Vehicle import Vehicle
from BaseDeclerative import Base



class BaseDao(object):
    engine = create_engine('sqlite:////'+config.DB_PATH+config.DB_NAME, echo=True)


    def __init__(self):
        Base.metadata.create_all(self.engine)
        self.create_session = sessionmaker(bind=self.engine)

    def insertIntoTable(self, objectType):
        session = self.create_session()
        session.add(objectType)
        session.commit()

    def readRowFromTable(self, objectType, id):
        session = self.create_session()
        result = session.query(objectType).filter_by(lotId = id).first()
        return result



class TestClass(Base):
    __tablename__ = "testclass"
    id = Column(Integer, primary_key=True)
    task = Column(String, nullable=False)
    status = Column(Boolean, nullable=False)

    def __init__(self, task, status):
        self.task = task
        self.status = status

def main():
    dao = BaseDao()
    # dao.insertIntoTable(ParkingLot(10,12,15,5))
    # dao.insertIntoTable(Vehicle("two", 100))
    # dao.insertIntoTable(ParkingLot(10, 12, 15, 5))
    print dao.readRowFromTable(ParkingLot, 1).twoWheelerParkingPrice


if __name__ == '__main__':
    main()