#
# (c) 2018 Red Hat, Inc.
#
# Copyright (c) 2017 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import re


INTERFACE_NAMES = {
    'Gi': 'GigabitEthernet',
}


def expand_interface_name(name):
    match = re.match('([a-zA-Z]*)', name)
    if match and match.group(1) in INTERFACE_NAMES:
        matched = match.group(1)
        name = name.replace(matched, INTERFACE_NAMES[matched])
    return name


class FilterModule(object):
    """Filters for working with output from network devices"""

    filter_map = {
        'expand_interface_name': expand_interface_name
    }

    def filters(self):
        return self.filter_map
