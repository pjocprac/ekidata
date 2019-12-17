import argparse
import glob
import os
from typing import Dict

import pandas
from progress.bar import ChargingBar
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists

from models import Base, Company, Join, Line, Pref, Station


parser = argparse.ArgumentParser(description="Create MySQL tables of ekidata.jp data")
parser.add_argument("-n", "--dbname", help="database name", default="ekidata")
parser.add_argument("-d", "--datadir", help="data directory of ekidata.jp's csv data", default=".")

MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
MYSQL_PWD = os.getenv("MYSQL_PWD")
MYSQL_USER = os.getenv("MYSQL_USER")


def main():
    args = parser.parse_args()
    dbname = args.dbname
    datadir = args.datadir

    data_filepaths = get_data_filepaths(datadir)
    if not all(data_filepaths.values()):
        print("data file doesn't exists!")
        for key, path in data_filepaths.items():
            print(f"{key}: {path}")
        exit(1)

    pass_str = f":{MYSQL_PWD}" if MYSQL_PWD else ""
    engine_connection_string = f"mysql+mysqlconnector://{MYSQL_USER}{pass_str}@{MYSQL_HOST}"

    create_databse(engine_connection_string, dbname)

    engine = create_engine(f"{engine_connection_string}/{dbname}")
    Session = sessionmaker(autocommit=False, autoflush=True, bind=engine)

    create_tables(engine)

    session = Session()

    insert_pref_data(session)
    insert_company_data(session, data_filepaths["company"])
    insert_line_data(session, data_filepaths["line"])
    insert_station_data(session, data_filepaths["station"])
    insert_join_data(session, data_filepaths["join"])

    session.commit()
    session.close()


def create_databse(connection_string: str, dbname: str):
    db_engine = create_engine(connection_string)
    db_engine.execute(f"DROP DATABASE IF EXISTS {dbname}")
    db_engine.execute(f"CREATE DATABASE {dbname}")


def create_tables(engine):
    Base.metadata.create_all(bind=engine)


def get_data_filepaths(dir):
    results = {}
    for filetype in ["company", "line", "station", "join"]:
        filepaths = glob.glob(f"{dir}/{filetype}*.csv")
        if len(filepaths) > 0:
            filepath = sorted(filepaths, reverse=True)[0]
        else:
            filepath = None

        results[filetype] = filepath

    return results


def insert_company_data(session, filepath: str):
    company_datas = pandas.read_csv(filepath)
    company_datas = company_datas.where((pandas.notnull(company_datas)), None)

    for company_data in ChargingBar("company").iter(company_datas.to_dict(orient="records")):
        session.add(Company(**company_data))

    session.flush()


def insert_line_data(session, filepath: str):
    line_datas = pandas.read_csv(filepath)
    line_datas = line_datas.where((pandas.notnull(line_datas)), None)

    for line_data in ChargingBar("line   ").iter(line_datas.to_dict(orient="records")):
        session.add(Line(**line_data))

    session.flush()


def insert_station_data(session, filepath: str):
    station_datas = pandas.read_csv(filepath)
    station_datas = station_datas.where((pandas.notnull(station_datas)), None)

    for station_data in ChargingBar("station").iter(station_datas.to_dict(orient="records")):
        session.add(Station(**station_data))

    session.flush()


def insert_join_data(session, filepath: str):
    join_datas = pandas.read_csv(filepath)

    known_line_cd: Dict[int, bool] = {}
    known_station_cd: Dict[int, bool] = {}
    for join_data in ChargingBar("join   ").iter(join_datas.to_dict(orient="records")):
        line_cd = join_data["line_cd"]
        station_cd1 = join_data["station_cd1"]
        station_cd2 = join_data["station_cd2"]

        if line_cd not in known_line_cd:
            known_line_cd[line_cd] = session.query(exists().where(Line.line_cd == line_cd)).scalar()

        if station_cd1 not in known_station_cd:
            known_station_cd[station_cd1] = session.query(exists().where(Station.station_cd == station_cd1)).scalar()

        if station_cd2 not in known_station_cd:
            known_station_cd[station_cd2] = session.query(exists().where(Station.station_cd == station_cd2)).scalar()

        if not all([known_line_cd[line_cd], known_station_cd[station_cd1], known_station_cd[station_cd2]]):
            continue

        session.add(Join(**join_data))

    session.flush()


def insert_pref_data(session):
    pref_datas = [
        {"pref_cd": 1, "pref_name": "北海道"},
        {"pref_cd": 2, "pref_name": "青森県"},
        {"pref_cd": 3, "pref_name": "岩手県"},
        {"pref_cd": 4, "pref_name": "宮城県"},
        {"pref_cd": 5, "pref_name": "秋田県"},
        {"pref_cd": 6, "pref_name": "山形県"},
        {"pref_cd": 7, "pref_name": "福島県"},
        {"pref_cd": 8, "pref_name": "茨城県"},
        {"pref_cd": 9, "pref_name": "栃木県"},
        {"pref_cd": 10, "pref_name": "群馬県"},
        {"pref_cd": 11, "pref_name": "埼玉県"},
        {"pref_cd": 12, "pref_name": "千葉県"},
        {"pref_cd": 13, "pref_name": "東京都"},
        {"pref_cd": 14, "pref_name": "神奈川県"},
        {"pref_cd": 15, "pref_name": "新潟県"},
        {"pref_cd": 16, "pref_name": "富山県"},
        {"pref_cd": 17, "pref_name": "石川県"},
        {"pref_cd": 18, "pref_name": "福井県"},
        {"pref_cd": 19, "pref_name": "山梨県"},
        {"pref_cd": 20, "pref_name": "長野県"},
        {"pref_cd": 21, "pref_name": "岐阜県"},
        {"pref_cd": 22, "pref_name": "静岡県"},
        {"pref_cd": 23, "pref_name": "愛知県"},
        {"pref_cd": 24, "pref_name": "三重県"},
        {"pref_cd": 25, "pref_name": "滋賀県"},
        {"pref_cd": 26, "pref_name": "京都府"},
        {"pref_cd": 27, "pref_name": "大阪府"},
        {"pref_cd": 28, "pref_name": "兵庫県"},
        {"pref_cd": 29, "pref_name": "奈良県"},
        {"pref_cd": 30, "pref_name": "和歌山県"},
        {"pref_cd": 31, "pref_name": "鳥取県"},
        {"pref_cd": 32, "pref_name": "島根県"},
        {"pref_cd": 33, "pref_name": "岡山県"},
        {"pref_cd": 34, "pref_name": "広島県"},
        {"pref_cd": 35, "pref_name": "山口県"},
        {"pref_cd": 36, "pref_name": "徳島県"},
        {"pref_cd": 37, "pref_name": "香川県"},
        {"pref_cd": 38, "pref_name": "愛媛県"},
        {"pref_cd": 39, "pref_name": "高知県"},
        {"pref_cd": 40, "pref_name": "福岡県"},
        {"pref_cd": 41, "pref_name": "佐賀県"},
        {"pref_cd": 42, "pref_name": "長崎県"},
        {"pref_cd": 43, "pref_name": "熊本県"},
        {"pref_cd": 44, "pref_name": "大分県"},
        {"pref_cd": 45, "pref_name": "宮崎県"},
        {"pref_cd": 46, "pref_name": "鹿児島県"},
        {"pref_cd": 47, "pref_name": "沖縄県"},
    ]

    for pref_data in ChargingBar("pref   ").iter(pref_datas):
        session.add(Pref(**pref_data))

    session.flush()


if __name__ == "__main__":
    main()
