# -*- coding: utf-8 -*-
import pytest

from gilded_rose import Item, GildedRose


from gilded_rose import ItemName

@pytest.fixture
def make_item():
    def _make_item(name = 'foo', sell_in = 0, quality = 0):
        return [Item(name, sell_in, quality)]
    return _make_item


@pytest.fixture()
def make_item_and_add_to_gilded_rose(make_item):
    def _make_item_and_update_once(name = 'foo', sell_in = 0, quality = 0):
        items = make_item(name, sell_in, quality)
        return GildedRose(items)
    return _make_item_and_update_once



def test_foo():
    items = [Item("foo", 0, 0)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].name == "foo"

def test_foo2(make_item_and_add_to_gilded_rose):
    items = make_item_and_add_to_gilded_rose("foo", 0, 0)
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



def test_quality_max(make_item):
    item = make_item(ItemName.AGED_BRIE, 5, 50)
    gilded_rose = GildedRose(item)
    gilded_rose.update_quality()
    assert item[0].sell_in == 4
    assert item[0].quality == 50

def test_aged_brie(make_item):
    item = make_item(ItemName.AGED_BRIE, 5, 10)
    gilded_rose = GildedRose(item)
    gilded_rose.update_quality()
    assert item[0].sell_in == 4
    assert item[0].quality == 11


def test_surphuras(make_item_and_add_to_gilded_rose):
    gilded_rose = make_item_and_add_to_gilded_rose(ItemName.SULFURAS, 10, 10)
    gilded_rose.update_quality()
    assert gilded_rose.items[0].sell_in == 10
    assert gilded_rose.items[0].quality == 10


def test_backstage_passes(make_item_and_add_to_gilded_rose):
    gilded_rose = make_item_and_add_to_gilded_rose(ItemName.BACKSTAGE, 6, 10)
    gilded_rose.update_quality()
    assert gilded_rose.items[0].sell_in == 5
    assert gilded_rose.items[0].quality == 12
    gilded_rose.update_quality()
    assert gilded_rose.items[0].sell_in == 4
    assert gilded_rose.items[0].quality == 15


def test_multiple_items():
    items = [Item("foo", 10, 10), Item(ItemName.AGED_BRIE, 4, 0)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert gilded_rose.items[0].sell_in == 9
    assert gilded_rose.items[0].quality == 9
    assert gilded_rose.items[1].sell_in == 3
    assert gilded_rose.items[1].quality == 1