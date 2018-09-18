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

from ckanext.ckanpackager.model.DownloadQueue import DLQueue

Base = declarative_base()


class DLQueueContent(Base):
    """
    Table for holding the contents of a queue
    """
    __tablename__ = 'ckanpackager_dl_queue_item'

    id = Column(Integer, primary_key=True)
    inserted_on = Column(DateTime, default=func.now())  # the current timestamp
    download_queue = Column(Integer,
           ForeignKey(DLQueue.id, onupdate='CASCADE',
                      ondelete='CASCADE'), nullable=False)
    resource = Column(types.UnicodeText,
           ForeignKey(model.resource_table.c.id, onupdate='CASCADE',
                      ondelete='CASCADE'), nullable=False)
