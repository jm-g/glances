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

from time import time

# Global list to manage the elapsed time
last_update_times = {}


def getTimeSinceLastUpdate(IOType):
    global last_update_times
    # assert(IOType in ['net', 'disk', 'process_disk'])
    current_time = time()
    last_time = last_update_times.get(IOType)
    if not last_time:
        time_since_update = 1
    else:
        time_since_update = current_time - last_time
    last_update_times[IOType] = current_time
    return time_since_update


class Timer:
    """
    The timer class
    A simple chrono
    """

    def __init__(self, duration):
        self.duration = duration
        self.start()

    def start(self):
        self.target = time() + self.duration

    def reset(self):
        self.start()

    def set(self, duration):
        self.duration = duration

    def finished(self):
        return time() > self.target

