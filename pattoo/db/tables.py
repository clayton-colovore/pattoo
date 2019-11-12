#!/usr/bin/env python3
"""pattoo ORM Table classes.

Used to define the tables used in the database.

"""

# SQLobject stuff
from sqlalchemy import UniqueConstraint, PrimaryKeyConstraint, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, INTEGER
from sqlalchemy.dialects.mysql import NUMERIC, VARBINARY
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref, relationship

from pattoo.db import POOL

###############################################################################
# Create Base SQLAlchemy class. This must be in the same file as the database
# definitions or else the database won't be created on install. Learned via
# trial and error.
BASE = declarative_base()

# GraphQL: Bind engine to metadata of the base class
BASE.metadata.bind = POOL

# GraphQL: Used by graphql to execute queries
BASE.query = POOL.query_property()
###############################################################################


class Agent(BASE):
    """Class defining the pt_agent table of the database."""

    __tablename__ = 'pt_agent'
    __table_args__ = (
        UniqueConstraint(
            'agent_id', 'agent_hostname', 'agent_program', 'polling_interval'),
        {
            'mysql_engine': 'InnoDB'
        }
    )

    idx_agent = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    agent_id = Column(VARBINARY(512), unique=True, nullable=True, default=None)

    agent_hostname = Column(
        VARBINARY(512), unique=False, nullable=True, default=None)

    agent_program = Column(
        VARBINARY(512), unique=False, nullable=True, default=None)

    polling_interval = Column(INTEGER(unsigned=True), server_default='1')

    enabled = Column(INTEGER(unsigned=True), server_default='1')

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))


class DataSource(BASE):
    """Class defining the pt_datasource table of the database."""

    __tablename__ = 'pt_datasource'
    __table_args__ = (
        UniqueConstraint('idx_agent', 'device', 'gateway'),
        {
            'mysql_engine': 'InnoDB'
        }
    )

    idx_datasource = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    idx_agent = Column(
        BIGINT(unsigned=True), ForeignKey('pt_agent.idx_agent'),
        nullable=False, server_default='1')

    device = Column(VARBINARY(512), nullable=True, default=None)

    gateway = Column(VARBINARY(512), nullable=True, default=None)

    enabled = Column(INTEGER(unsigned=True), server_default='1')

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))

    # Use cascade='delete,all' to propagate the deletion of a
    # Agent onto its Data
    agent = relationship(
        Agent,
        backref=backref('agents', uselist=True, cascade='delete,all'))


class DataPoint(BASE):
    """Class defining the pt_datapoint table of the database."""

    __tablename__ = 'pt_datapoint'
    __table_args__ = (
        {
            'mysql_engine': 'InnoDB'
        }
    )

    idx_datapoint = Column(
        BIGINT(unsigned=True), primary_key=True,
        autoincrement=True, nullable=False)

    idx_datasource = Column(
        BIGINT(unsigned=True), ForeignKey('pt_datasource.idx_datasource'),
        nullable=False, server_default='1')

    checksum = Column(VARBINARY(512), unique=True, nullable=True, default=None)

    data_label = Column(VARBINARY(512), nullable=True, default=None)

    data_index = Column(VARBINARY(128), nullable=True, default=None)

    data_type = Column(INTEGER(unsigned=True), server_default='1')

    enabled = Column(INTEGER(unsigned=True), server_default='1')

    last_timestamp = Column(
        BIGINT(unsigned=True), nullable=False, server_default='0')

    ts_modified = Column(
        DATETIME, server_default=text(
            'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),)

    ts_created = Column(
        DATETIME, server_default=text('CURRENT_TIMESTAMP'))

    # Use cascade='delete,all' to propagate the deletion of a
    # DataSource onto its Data
    datasource = relationship(
        DataSource,
        backref=backref('datasources', uselist=True, cascade='delete,all'))


class Data(BASE):
    """Class defining the pt_data table of the database."""

    __tablename__ = 'pt_data'
    __table_args__ = (
        PrimaryKeyConstraint(
            'idx_datapoint', 'timestamp'),
        {
            'mysql_engine': 'InnoDB'
        }
        )

    idx_datapoint = Column(
        BIGINT(unsigned=True), ForeignKey('pt_datapoint.idx_datapoint'),
        nullable=False, server_default='1')

    timestamp = Column(BIGINT(unsigned=True), nullable=False, default='1')

    value = Column(NUMERIC(40, 10), default=None)

    # Use cascade='delete,all' to propagate the deletion of a
    # DataPoint onto its Data
    datapoint = relationship(
        DataPoint,
        backref=backref(
            'numeric_datapoints', uselist=True, cascade='delete,all'))


class DataString(BASE):
    """Class defining the pt_data table of the database."""

    __tablename__ = 'pt_datastring'
    __table_args__ = (
        PrimaryKeyConstraint(
            'idx_datapoint', 'timestamp'),
        {
            'mysql_engine': 'InnoDB'
        }
        )

    idx_datapoint = Column(
        BIGINT(unsigned=True), ForeignKey('pt_datapoint.idx_datapoint'),
        nullable=False, server_default='1')

    timestamp = Column(BIGINT(unsigned=True), nullable=False, default='1')

    value = Column(VARBINARY(512), nullable=True, default=None)

    # Use cascade='delete,all' to propagate the deletion of a
    # DataPoint onto its Data
    datapoint = relationship(
        DataPoint,
        backref=backref(
            'string_datapoints', uselist=True, cascade='delete,all'))
