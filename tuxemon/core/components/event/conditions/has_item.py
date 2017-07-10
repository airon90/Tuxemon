# -*- coding: utf-8 -*-
#
# Tuxemon
# Copyright (c) 2014-2017 William Edwards <shadowapex@gmail.com>,
#                         Benjamin Bean <superman2k5@gmail.com>
#
# This file is part of Tuxemon
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import

from operator import eq, gt, lt

from core.components.event.conditions import get_npc
from core.components.event.eventcondition import EventCondition

cmp = {
    None: gt,
    "less_than": lt,
    "greater_than": gt,
    "equals": eq
}


class HasItemCondition(EventCondition):
    """ Checks to see if a NPC inventory contains something

    inventory_contains [npc or player] [item slug] [operator] [quantity]

    npc or player: "player" or npc slug name; "npc_maple"
    item slug: the item slug name; item_cherry, etc
    operator: numeric comparison operators: less_than, greater_than, equals
    quantity: integer value, non-negative

    operator can be optional; it will default to greater_than
    quantity can be optional; it will default to 0

    if quantity is None, then any number of items over 0 will return True ( quantity > 0 )
    None is not valid input for quantity, but may be used internally
    """
    name = "has_item"

    def test(self, game, condition):
        """Checks to see the player is has a monster in his party

        :param game: The main game object that contains all the game's variables.
        :param condition: A dictionary of condition details. See :py:func:`core.components.map.Map.loadevents`
            for the format of the dictionary.

        :type game: core.control.Control
        :type condition: Dictionary

        :rtype: Boolean
        :returns: True or False

        """
        owner_slug, item_slug = condition.parameters[:2]

        try:
            op = cmp[condition.parameters[2]]
        except IndexError:
            op = cmp[None]

        try:
            q_test = int(condition.parameters[3])
            if q_test < 0:
                raise ValueError
        except IndexError:
            q_test = 0

        npc = get_npc(game, owner_slug)
        item_info = npc.inventory.get(item_slug)
        if item_info is None:
            item_quantity = 0
        else:
            item_quantity = item_info['quantity']

        return op(item_quantity, q_test)

