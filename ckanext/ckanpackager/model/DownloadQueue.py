#!/usr/bin/env python
# encoding: utf-8
"""
Created by 'ianh' on 2018-09-18.
"""

import sys
import os
import ckan.model as model
from sqlalchemy import Column, Integer, DateTime, String, func, types, ForeignKey
# from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DLQueue(Base):
    """
    Table for holding info on a single users single download queue.xml file
    Individual contents of the queue listed as entries in the QueueContent table
    """
    __tablename__ = 'ckanpackager_dl_queue'

    id = Column(Integer, primary_key=True)
    inserted_on = Column(DateTime, default=func.now())  # the current timestamp
    user = Column(types.UnicodeText,
           ForeignKey(model.user_table.c.id, onupdate='CASCADE',
                      ondelete='CASCADE'), nullable=False)
