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


ROUTING_PROTOCOLS = {'L': 'local', 'C': 'connected', 'S': 'static', 'R': 'rip', 'M': 'mobile', 'B': 'bgp', 'D': 'eigrp', 'EX': 'eigrp external', 'O': 'ospf',
                     'IA': 'ospf inter area', 'N1': 'ospf nssa external type 1', 'N2': 'ospf nssa external type 2', 'E1': 'ospf external type 1',
                     'E2': 'ospf external type 2', 'i': 'is-is', 'su': 'is-is summary', 'L1': 'is-is level-1', 'L2': 'is-is level-2',
                     'ia': 'is-is inter area', '*': 'candidate default', 'U': 'per-user static route', 'o': 'odr',
                     'P': 'periodic downloaded static route', 'H': 'nhrp', 'l': 'lisp', 'a': 'application route',
                     '+': 'replicated route', '%': 'next hop override'}


def expand_interface_name(name):
    match = re.match('([a-zA-Z]*)', name)
    if match and match.group(1) in INTERFACE_NAMES:
        matched = match.group(1)
        name = name.replace(matched, INTERFACE_NAMES[matched])
    return name


def expand_routing_protocol_name(name):
    match = re.match(r'([\S]*)', name)
    if match and match.group(1) in ROUTING_PROTOCOLS:
        matched = match.group(1)
        name = name.replace(matched, ROUTING_PROTOCOLS[matched])
    return name


class FilterModule(object):
    """Filters for working with output from network devices"""

    filter_map = {
        'expand_interface_name': expand_interface_name,
        'expand_routing_protocol_name': expand_routing_protocol_name
    }

    def filters(self):
        return self.filter_map
