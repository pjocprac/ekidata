from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Pref(Base):  # type:ignore
    __tablename__ = "pref"

    pref_cd = Column(Integer, primary_key=True, comment="都道府県コード")
    pref_name = Column(String(length=4), primary_key=True, comment="都道府県名")


class Company(Base):  # type:ignore
    __tablename__ = "company"

    company_cd = Column(Integer, primary_key=True, comment="事業者コード")
    rr_cd = Column(Integer, nullable=False, comment="鉄道コード")
    company_name = Column(String(length=80), nullable=False, comment="事業者名(一般)")
    company_name_k = Column(String(length=80), comment="事業者名(一般・カナ)")
    company_name_h = Column(String(length=80), comment="事業者名(正式名称)")
    company_name_r = Column(String(length=80), comment="事業者名(略称)")
    company_url = Column(String(length=256), comment="Webサイト")
    company_type = Column(Integer, comment="事業者区分(0:その他 1:JR 2:大手私鉄 3:準大手私鉄)")
    e_status = Column(Integer, comment="状態(0:運用中 1:運用前 2:廃止)")
    e_sort = Column(Integer, comment="並び順")


class Line(Base):  # type:ignore
    __tablename__ = "line"

    line_cd = Column(Integer, primary_key=True, comment="路線コード")
    company_cd = Column(
        Integer,
        ForeignKey(Company.company_cd, onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
        comment="事業者コード",
    )
    line_name = Column(String(length=80), nullable=False, comment="路線名称(一般)")
    line_name_k = Column(String(length=80), comment="路線名称(一般・カナ)")
    line_name_h = Column(String(length=80), comment="路線名称(正式名称)")
    line_color_c = Column(String(length=6), comment="路線カラー(コード)")
    line_color_t = Column(String(length=10), comment="路線カラー(名称)")
    line_type = Column(Integer, comment="路線区分(0:その他 1:新幹線 2:一般 3:地下鉄 4:市電・路面電車 5:モノレール・新交通)")
    lon = Column(Float, comment="路線表示時の中央経度")
    lat = Column(Float, comment="路線表示時の中央緯度")
    zoom = Column(Integer, comment="路線表示時のGoogleMap倍率")
    e_status = Column(Integer, comment="状態(0:運用中 1:運用前 2:廃止)")
    e_sort = Column(Integer, comment="並び順")


class Station(Base):  # type:ignore
    __tablename__ = "station"

    station_cd = Column(Integer, primary_key=True, comment="駅コード")
    station_g_cd = Column(Integer, nullable=False, comment="駅グループコード")
    station_name = Column(String(length=80), nullable=False, comment="駅名称")
    station_name_k = Column(String(length=80), comment="駅名称(カナ)")
    station_name_r = Column(String(length=80), comment="駅名称(ローマ字)")
    line_cd = Column(Integer, ForeignKey(Line.line_cd, onupdate="CASCADE", ondelete="CASCADE"), nullable=False, comment="路線コード")
    pref_cd = Column(Integer, ForeignKey(Pref.pref_cd, onupdate="CASCADE", ondelete="CASCADE"), comment="都道府県コード")
    post = Column(String(length=10), comment="駅郵便番号(xxx-xxxx)")
    add = Column(String(length=300), comment="住所")
    lon = Column(Float, comment="経度(世界測地系)")
    lat = Column(Float, comment="緯度(世界測地系)")
    open_ymd = Column(String(length=10), comment="開業年月日(YYYY-mm-dd)")
    close_ymd = Column(String(length=10), comment="廃止年月日(YYYY-mm-dd)")
    e_status = Column(Integer, comment="状態(0:運用中 1:運用前 2:廃止)")
    e_sort = Column(Integer, comment="並び順")


class Join(Base):  # type:ignore
    __tablename__ = "join"

    line_cd = Column(Integer, primary_key=True, comment="路線コード")
    station_cd1 = Column(
        Integer,
        ForeignKey(Station.station_cd, onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
        comment="駅コード１",
    )
    station_cd2 = Column(
        Integer,
        ForeignKey(Station.station_cd, onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
        comment="駅コード２",
    )
