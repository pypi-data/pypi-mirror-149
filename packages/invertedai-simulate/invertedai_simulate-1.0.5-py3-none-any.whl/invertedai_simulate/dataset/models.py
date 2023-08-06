from sqlalchemy import Column, Integer, BLOB
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class DataLoader(Base):
    __tablename__ = 'IAI_ENV_DATASET'
    IDX = Column(Integer, primary_key=True, autoincrement=True)  # start at 1
    OBS = Column(BLOB)
    REWARDS = Column(BLOB, nullable=True)
    INFO = Column(BLOB, nullable=True)
