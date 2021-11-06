#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
script_name.py
Description of script_name.py.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


class Database:
    engine = create_engine('sqlite:///test.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base = declarative_base()


class Media(Database.Base):
    __tablename__ = 'media'

    id = Column(Integer, primary_key=True)
    path = Column(String)
    md5_checksum = Column(String)


Database.Base.metadata.create_all(Database.engine)


def add_media(path):
    media = Media(path=path, md5_checksum="")
    Database.session.add(media)
    Database.session.commit()


def main():
    """docstring for main"""
    pass

if __name__ == '__main__':
    main()
