#!/usr/bin/python
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'network'}


DOCUMENTATION = """
---
module: ios_capabilities
version_added: "2.7"
short_description: Collect device capabilities from Cisco IOS
description:
  - Collect basic fact capabilities from Cisco NX-OS devices and return
    the capabilities as Ansible facts.
author:
  - Ansible Netowrk Community (ansible-network)
options: {}
"""

EXAMPLES = """
- facts:
"""

RETURN = """
"""
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection

def main():
    """ main entry point for Ansible module
    """
    argument_spec = {}

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    connection = Connection(module._socket_path)
    facts = connection.get_capabilities()
    facts = module.from_json(facts)
    result = {
        'changed': False,
        'ansible_facts': {'cisco_ios': {'capabilities': facts['device_info']}}
    }
    module.exit_json(**result)


if __name__ == '__main__':
    main()
