# -*- coding: utf-8 -*-

from enum import StrEnum
from typing import List
from abc import ABC, abstractmethod


QUALITY_MAX = 50

class ItemName(StrEnum):
    AGED_BRIE = "Aged Brie"
    SULFURAS = "Sulfuras, Hand of Ragnaros"
    BACKSTAGE = "Backstage passes to a TAFKAL80ETC concert"

class generic_accountant():
    def __init__(self, item):
        self.item = item

    def update_quality(self):
        self.item.quality -= 1

        if self.item.sell_in < 0:
            self.item.quality -= 1



class GildedRose(object):
    def __init__(self, items: List[Item]):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if item.name == ItemName.SULFURAS:
                continue

            item.sell_in = item.sell_in - 1

            # Now we update the qualities for rest
            if item.name == ItemName.AGED_BRIE:
                item.quality = item.quality + 1

                if item.sell_in < 0:
                    item.quality = item.quality + 1


            elif item.name == ItemName.BACKSTAGE:
                # Max is applied later and after sellby zeroing also done later
                # Based on the tests, 5 days or less relates to update at end of day label 5
                # If we move the sell in days update to the start of the script then we need
                # to update this so += 3 is for day <= 4 (day zero is counted),
                # +=3 for days <= 9
                if item.sell_in < 0:
                    item.quality = 0

                elif item.sell_in <= 4:
                    item.quality += 3

                elif item.sell_in <= 9:
                    item.quality +=  2

                else:
                    item.quality += 1

            else: # Other items
                ga = generic_accountant(item)
                ga.update_quality()

            item.perform_min_max_checks()


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    # Could convert this into property
    def perform_min_max_checks(self):
        self.quality = max(0, min(QUALITY_MAX, self.quality))

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


