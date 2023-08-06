from typing import List, Tuple
import os
from invertedai_simulate.dataset.models import DataLoader
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class CacheDataDB:
    """
    A class holds a sqlite engine session that is able to read from and write to the passed sql_file
    """
    def __init__(self, sql_file):
        self.sql_file = sql_file
        if os.path.dirname(sql_file) and not os.path.exists(os.path.dirname(sql_file)):
            os.makedirs(os.path.dirname(sql_file))
        self.engine = create_engine(f'sqlite:///{sql_file}')
        self.session = sessionmaker(self.engine)
        self._init_database()

    def _init_database(self):
        DataLoader.__table__.create(self.engine, checkfirst=True)

    def insert_cached_object(self, items: List[Tuple[bytes, bytes, bytes]]):
        with self.session() as session:
            for i, (obs, rewards, info) in enumerate(items):
                data = DataLoader(OBS=obs, REWARDS=rewards, INFO=info)
                session.add(data)
                if i % 1000 == 0:
                    session.commit()
            session.commit()

    def load_data_by_idx(self, idx: int) -> DataLoader:
        with self.session() as session:
            result = session.query(DataLoader).filter(DataLoader.IDX == idx).first()
        return result

    def select_all(self, limit=1000, offset=0) -> List[DataLoader]:
        with self.session() as session:
            results = session.query(DataLoader).limit(limit).offset(offset).all()
        return results

    def count_all(self) -> int:
        with self.session() as session:
            results = session.query(DataLoader).count()
        return results
