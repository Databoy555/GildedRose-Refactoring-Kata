# -*- coding: utf-8 -*-

"""
Keeping doc strings to a minimum as code should be self documenting
In line comments made to explain some decisions/document behaviour
"""

from abc import ABC, abstractmethod
from enum import StrEnum
from typing import List

QUALITY_MAX: int = 50

class ItemName(StrEnum):
    AGED_BRIE = "Aged Brie"
    SULFURAS = "Sulfuras, Hand of Ragnaros"
    BACKSTAGE = "Backstage passes to a TAFKAL80ETC concert"
    CONJURED = "Conjured"


class GildedRose(object):
    def __init__(self, items: List[Item]):
        self.items = items

    def update_quality(self):
        for item in self.items:
            acc = Accountant.assign_accountant(item)
            acc.perform_daily_update()

# Not adding typing here as instructions ask for no modification to Item class
class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class Accountant(ABC):
    """
    An accountant ABC. Subclasses responsible for inventory management
    """
    item_managed = None

    def __init__(self, item):
        self.item = item

    @abstractmethod
    def update_quality(self):
        pass

    def update_sell_in(self):
        self.item.sell_in -= 1

    def perform_min_max_checks(self):
        self.item.quality = max(0, min(QUALITY_MAX, self.item.quality))

    def perform_daily_update(self):
        self.update_sell_in()
        self.update_quality()
        self.perform_min_max_checks()

    @classmethod
    def get_subclass_mapping(cls) -> dict:
        subclasses = cls.__subclasses__()
        mapping = {klass.item_managed: klass for klass in subclasses}
        return mapping

    @classmethod
    def assign_accountant(cls, item) -> Accountant:
        mapping = cls.get_subclass_mapping()
        return mapping.get(item.name, GenericAccountant)(item)


class GenericAccountant(Accountant):
    """
    For regular items without special rules
    """
    item_managed = 'Generic'

    def update_quality(self):
        self.item.quality -= 1

        if self.item.sell_in < 0:
            self.item.quality -= 1


class BrieAccountant(Accountant):
    item_managed = ItemName.AGED_BRIE

    def update_quality(self):
        self.item.quality = self.item.quality + 1

        if self.item.sell_in < 0:
            self.item.quality = self.item.quality + 1


class BackstageAccountant(Accountant):
    item_managed = ItemName.BACKSTAGE

    def update_quality(self):
        """
        Based on the tests, 5 days or less relates to update at end of day label 5
        If we move the sell in days update to the start of the script then we need
        to update this so += 3 is for day <= 4 (day zero is counted),
        +=3 for days <= 9
        """
        item = self.item
        if item.sell_in < 0:
            item.quality = 0

        elif item.sell_in <= 4:
            item.quality += 3

        elif item.sell_in <= 9:
            item.quality += 2

        else:
            item.quality += 1


class SulfurasAccountant(Accountant):
    item_managed = ItemName.SULFURAS

    def update_sell_in(self):
        pass

    def update_quality(self):
        pass

    def perform_min_max_checks(self):
        pass


class ConjuredAccountant(Accountant):
    item_managed = ItemName.CONJURED

    def update_quality(self):
        self.item.quality -= 2
        if self.item.sell_in < 0:
            self.item.quality -= 2
