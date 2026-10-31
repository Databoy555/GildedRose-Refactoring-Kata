# -*- coding: utf-8 -*-

from enum import StrEnum
from typing import List

QUALITY_MAX = 50

class ItemName(StrEnum):
    AGED_BRIE = "Aged Brie"
    SULFURAS = "Sulfuras, Hand of Ragnaros"
    BACKSTAGE = "Backstage passes to a TAFKAL80ETC concert"



class GildedRose(object):

    def __init__(self, items: List[Item]):
        self.items = items

    def update_quality(self):
        for item in self.items:
            if item.name == ItemName.SULFURAS:
                continue

            item.sell_in = item.sell_in - 1

            if item.name == ItemName.AGED_BRIE:
                item.quality = item.quality + 1

            elif item.name == ItemName.BACKSTAGE:
                # Max is applied later and after sellby zeroing also done later
                # Based on the tests, 5 days or less relates to update at end of day label 5
                # If we move the sell in days update to the start of the script then we need
                # to update this so += 3 is for day <= 4 (day zero is counted),
                # +=3 for days <= 9

                if item.sell_in <= 4:
                    item.quality += 3

                elif item.sell_in <= 9:
                    item.quality +=  2

                else:
                    item.quality += 1

            else:
                if item.quality > 0:
                    item.quality = item.quality - 1

            # Lets put logic by item type so we can move to item based logic

            # Block dealing with after sell by
            # The double reduction comes because previous block also reduces once
            if item.sell_in < 0:
                if item.name == ItemName.AGED_BRIE:
                    item.quality = item.quality + 1

                elif item.name == ItemName.BACKSTAGE:
                    item.quality = 0

                elif item.quality > 0:
                    item.quality = item.quality - 1

            item.quality = max(0, min(QUALITY_MAX, item.quality))


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
