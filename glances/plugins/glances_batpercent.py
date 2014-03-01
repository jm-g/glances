#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Glances - An eye on your system
#
# Copyright (C) 2014 Nicolargo <nicolas@nicolargo.com>
#
# Glances is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Glances is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# Import system libs
# batinfo library (optional; Linux-only)
try:
    import batinfo
except:
    pass

# Import Glances lib
from glances_plugin import GlancesPlugin 
from glances.core.glances_timer import getTimeSinceLastUpdate


class Plugin(GlancesPlugin):
    """
    Glances's batterie capacity Plugin

    stats is a list
    """

    def __init__(self):
        GlancesPlugin.__init__(self)

        # Init the sensor class
        self.glancesgrabbat = glancesGrabBat()


    def update(self):
        """
        Update batterie capacity stats
        """

        self.stats = self.glancesgrabbat.getcapacitypercent()


class glancesGrabBat:
    """
    Get batteries stats using the Batinfo librairie
    """

    def __init__(self):
        """
        Init batteries stats
        """
        try:
            self.bat = batinfo.batteries()
            self.initok = True
            self.__update__()
        except Exception:
            self.initok = False

    def __update__(self):
        """
        Update the stats
        """
        if self.initok:
            try:
                self.bat.update()
            except Exception:
                self.bat_list = []
            else:
                self.bat_list = self.bat.stat
        else:
            self.bat_list = []

    def get(self):
        # Update the stats
        self.__update__()
        return self.bat_list

    def getcapacitypercent(self):
        if not self.initok or self.bat_list == []:
            return []
        # Init the bsum (sum of percent) and bcpt (number of batteries)
        # and Loop over batteries (yes a computer could have more than 1 battery)
        bsum = 0
        for bcpt in range(len(self.get())):
            try:
                bsum = bsum + int(self.bat_list[bcpt].capacity)
            except ValueError:
                return []
        bcpt = bcpt + 1
        # Return the global percent
        return int(bsum / bcpt)