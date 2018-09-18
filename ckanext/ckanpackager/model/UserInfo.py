#!/usr/bin/env python
# encoding: utf-8
"""
Created by 'ianh' on 2018-09-18.
"""

import sys
import os
import ckan.model as model
from ckan.model.resource import Resource
from sqlalchemy import Column, Integer, DateTime, String, func, ForeignKey, types
# from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BIDUserInfo(Base):
    """
    Table for holding extra user info
    """
    __tablename__ = 'ckanpackager_userinfo'

    id = Column(Integer, primary_key=True)
    inserted_on = Column(DateTime, default=func.now())  # the current timestamp
    signup_reason = Column(String)
    user = Column(types.UnicodeText,
           ForeignKey(model.user_table.c.id, onupdate='CASCADE',
                      ondelete='CASCADE'), nullable=False)

