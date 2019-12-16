#!/usr/bin/env python3
"""Pattoo classes querying the Language table."""

from collections import namedtuple

# Import project libraries
from pattoo_shared.constants import MAX_KEYPAIR_LENGTH
from pattoo_shared import log
from pattoo.db import db
from pattoo.db.models import Language as _Language


def idx_exists(idx):
    """Determine whether primary key exists.

    Args:
        idx: idx_language

    Returns:
        result: True if exists

    """
    # Initialize key variables
    result = False
    rows = []

    # Get the result
    with db.db_query(20046) as session:
        rows = session.query(_Language.idx_language).filter(
            _Language.idx_language == idx)

    # Return
    for _ in rows:
        result = True
        break
    return bool(result)


def exists(code):
    """Determine whether code exists in the Language table.

    Args:
        code: language code

    Returns:
        result: Language.idx_language value

    """
    # Initialize key variables
    result = False
    rows = []

    # Lowercase the code
    code = code.lower()

    # Ignore certain restricted keys
    with db.db_query(20031) as session:
        rows = session.query(_Language.idx_language).filter(
            _Language.code == code.encode())

    # Return
    for row in rows:
        result = row.idx_language
        break
    return result


def insert_row(code, description=''):
    """Create a Language table entry.

    Args:
        code: Language code
        description: Language code description

    Returns:
        None

    """
    # Verify values
    if bool(description) is False or isinstance(description, str) is False:
        description = 'Change me. Language name not provided.'
    else:
        description = description[:MAX_KEYPAIR_LENGTH]
    if bool(code) is False or isinstance(code, str) is False:
        log_message = 'Language code "{}" is invalid'.format(code)
        log.log2die(20033, log_message)

    # Lowercase the code
    code = code.lower()

    # Insert
    with db.db_modify(20032, die=True) as session:
        session.add(_Language(
            code=code.encode(), description=description.strip().encode()))


def update_description(code, description):
    """Upadate a Language table entry.

    Args:
        code: Language code
        description: Language code description

    Returns:
        None

    """
    # Update
    with db.db_modify(20048, die=False) as session:
        session.query(_Language).filter(
            _Language.code == code.encode()).update(
                {'description': description.strip().encode()}
            )


def cli_show_dump():
    """Get entire content of the table.

    Args:
        None

    Returns:
        result: List of NamedTuples

    """
    # Initialize key variables
    result = []

    # Get the result
    with db.db_query(20049) as session:
        rows = session.query(_Language)

    # Process
    for row in rows:
        Record = namedtuple('Record', 'idx_language code description')
        result.append(
            Record(
                idx_language=row.idx_language,
                description=row.description.decode(),
                code=row.code.decode()))
    return result
