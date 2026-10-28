# -*- coding: utf-8 -*-
import pytest

from gilded_rose import Item, GildedRose


from gilded_rose import ItemName

@pytest.fixture
def make_item():
    def _make_item(name = 'foo', sell_in = 0, quality = 0):
        return [Item(name, sell_in, quality)]
    return _make_item

def test_foo():
    items = [Item("foo", 0, 0)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].name == "foo"


def test_items_have_attributes():
    items = [Item("foo", 0, 0)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert hasattr(items[0], "name")
    assert hasattr(items[0], "quality")
    assert hasattr(items[0], "sell_in")


def test_quality_decreases(make_item):
    item = make_item("foo", 1, 1)
    gilded_rose = GildedRose(item)
    gilded_rose.update_quality()
    assert item[0].sell_in == 0
    assert item[0].quality == 0

def test_quality_never_below_zero(make_item):
    item = make_item("foo", 0, 0)
    gilded_rose = GildedRose(item)
    gilded_rose.update_quality()
    assert item[0].sell_in == -1
    assert item[0].quality == 0

def test_quality_twice_degrade(make_item):
    item = make_item("foo", 0, 10)
    gilded_rose = GildedRose(item)
    gilded_rose.update_quality()
    assert item[0].sell_in == -1
    assert item[0].quality == 8

def test_aged_brie(make_item):
    item = make_item("foo", 0, 0)


def test_name():
    assert ItemName.AGED_BRIE == 'Aged Brie'

# todo add aged brie related tests



