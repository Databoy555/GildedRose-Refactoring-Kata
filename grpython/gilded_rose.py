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

            elif item.name == ItemName.AGED_BRIE:
                item.quality = item.quality + 1

            elif item.name == ItemName.BACKSTAGE:
                # Max is applied later and after sellby zeroing also done later
                if item.sell_in < 6:
                    item.quality += 3

                elif item.sell_in < 11:
                    item.quality +=  2

                else:
                    item.quality += 1

            else:
                if item.quality > 0:
                    item.quality = item.quality - 1

            # This line is problematic as it changes update behaviour mid run
            # Either update sell in at start or at end
            item.sell_in = item.sell_in - 1

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
