# -*- coding: utf-8 -*-
import unittest
import pytest

from gilded_rose import Item, GildedRose


def test_addition():
    assert 2 + 2 == 4

def test_foo():
    items = [Item("foo", 0, 0)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    assert items[0].name == "foo"

