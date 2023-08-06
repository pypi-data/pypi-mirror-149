"""Test the Database class."""

import pytest
from world.database import Database


@pytest.fixture
def db():
    return Database()


def test_basic(db):
    assert db.lookup_code('it') == 'Italy'


def test_find_matches(db):
    matches = db.find_matches('italy')
    assert len(matches) == 1
    assert matches[0] == ('it', 'Italy')


def test_find_matches_uppercase(db):
    matches = db.find_matches('ITALY')
    assert len(matches) == 1
    assert matches[0] == ('it', 'Italy')


def test_find_matches_multiple(db):
    matches = db.find_matches('united')
    assert len(matches) == 6
    assert sorted(matches) == [
        ('ae', 'United Arab Emirates (the)'),
        ('gb',
         'United Kingdom of Great Britain and Northern Ireland (the)'),
        ('tz', 'Tanzania, United Republic of'),
        ('uk', 'United Kingdom (common practice)'),
        ('um', 'United States Minor Outlying Islands (the)'),
        ('us', 'United States of America (the)'),
    ]


def test_iteration(db):
    codes = []
    for code in db:
        codes.append(code)
    top_5 = sorted(codes)[:5]
    assert top_5 == ['ac', 'ad', 'ae', 'aero', 'af']
