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
module: ios_bgp
version_added: "2.8"
author: "Nilashish Chakraborty (@nilashishc)"
short_description: Configure global BGP protocol settings on Cisco IOS
description:
  - This module provides configuration management of global BGP parameters
    on devices running Cisco IOS
notes:
  - Tested against Cisco IOS Version 15.6(3)M2
options:
  config:
    description:
      - Specifies the BGP related configuration
    suboptions:
      bgp_as:
        description:
          - Specifies the BGP Autonomous System (AS) number to configure on the device
        type: int
        required: true
      router_id:
        description:
          - Configures the BGP routing process router-id value
        default: null
      log_neighbor_changes:
        description:
          - Enable/disable logging neighbor up/down and reset reason
        type: bool
      neighbors:
        description:
          - Specifies BGP neighbor related configurations
        suboptions:
          neighbor:
            description:
              - Neighbor router address
            required: True
          remote_as:
            description:
              - Remote AS of the BGP neighbor to configure
            type: int
            required: True
          route_reflector_client:
            description:
              - Specify a neighbor as a route reflector client
            type: bool
          route_server_client:
            description:
              - Specify a neighbor as a route server client
            type: bool
          update_source:
            description:
              - Source of the routing updates
          password:
            description:
              - Password to authenticate BGP peer connection
          enabled:
            description:
              - Administratively shutdown or enable a neighbor
            type: bool
          description:
            description:
              - Neighbor specific description
          ebgp_multihop:
            description:
              - Specifies the maximum hop count for EBGP neighbors not on directly connected networks
              - The range is from 0 to 255.
            type: int
          peer_group:
            description:
              - Name of the peer group that the neighbor is a member of
          timers:
            description:
              - Specifies BGP neighbor timer related configurations
            suboptions:
              keepalive:
                description:
                  - Frequency (in seconds) with which the Cisco IOS software sends keepalive messages to its peer.
                  - The range is from 0 to 65535.
                type: int
                required: True
              holdtime:
                description:
                  - Interval (in seconds) after not receiving a keepalive message that the software declares a peer dead.
                  - The range is from 0 to 65535.
                type: int
                required: True
              min_neighbor_holdtime:
                description:
                  - Interval (in seconds) specifying the minimum acceptable hold-time from a BGP neighbor.
                  - The minimum acceptable hold-time must be less than, or equal to, the interval specified in the holdtime argument.
                  - The range is from 0 to 65535.
                type: int
          activate:
            description:
              - Enable the address family for this neighbor
            type: bool
          remove_private_as:
            description:
              - Remove the private AS number from outbound updates
            type: bool
          next_hop_self:
            description:
              - Enable/disable the next hop calculation for this neighbor
            type: bool
          next_hop_unchanged:
            description:
              - Enable/disable propagation of next hop unchanged for iBGP paths to this neighbor
            type: bool
      networks:
        description:
          - Specify networks to announce via BGP
        suboptions:
          prefix:
            description:
              - Network ID to announce via BGP
            required: True
          masklen:
            description:
              - Subnet mask for the network to announce
          route_map:
            description:
              - Route map to modify the attributes
      address_family:
        description:
          - Specifies BGP address family related configurations
        suboptions:
          afi:
            description:
              - Type of address family to configure
            choices:
              - ipv4
              - ipv6
            required: True
          safi:
            description:
              - Specifies the type of cast for the address family
            choices:
              - flowspec
              - unicast
              - multicast
              - labeled-unicast
            default: unicast
          redistribute:
            description:
              - Specifies the redistribute information from another routing protocol
            suboptions:
              protocol:
                description:
                  - Specifies the protocol for configuring redistribute information
                required: True
              id:
                description:
                  - Identifier for the routing protocol for configuring redistribute information
                  - Not valid for protocol - RIP
              metric:
                description:
                  - Specifies the metric for redistributed routes
              route_map:
                description:
                  - Specifies the route map reference
          networks:
            description:
              - Specify networks to announce via BGP
            suboptions:
              prefixcd :
                description:
                  - Network ID to announce via BGP
                required: True
              mask:
                description:
                  - Subnet mask for the network to announce
              route_map:
                description:
                  - Route map to modify the attributes
          neighbors:
            description:
              - Specifies BGP neighbor related configurations
            suboptions:
              neighbor:
                description:
                  - Neighbor router address
                required: True
              remote_as:
                description:
                  - Remote AS of the BGP neighbor to configure
                type: int
                required: True
              route_reflector_client:
                description:
                  - Specify a neighbor as a route reflector client
                type: bool
              route_server_client:
                description:
                  - Specify a neighbor as a route server client
                type: bool
              update_source:
                description:
                  - Source of the routing updates
              password:
                description:
                  - Password to authenticate BGP peer connection
              enabled:
                description:
                  - Administratively shutdown or enable a neighbor
                type: bool
              description:
                description:
                  - Neighbor specific description
              ebgp_multihop:
                description:
                  - Specifies the maximum hop count for EBGP neighbors not on directly connected networks
                  - The range is from 0 to 255.
                type: int
              peer_group:
                description:
                  - Name of the peer group that the neighbor is a member of
              timers:
                description:
                  - Specifies BGP neighbor timer related configurations
                suboptions:
                  keepalive:
                    description:
                      - Frequency (in seconds) with which the Cisco IOS software sends keepalive messages to its peer.
                      - The range is from 0 to 65535.
                    type: int
                    required: True
                  holdtime:
                    description:
                      - Interval (in seconds) after not receiving a keepalive message that the software declares a peer dead.
                      - The range is from 0 to 65535.
                    type: int
                    required: True
                  min_neighbor_holdtime:
                    description:
                      - Interval (in seconds) specifying the minimum acceptable hold-time from a BGP neighbor.
                      - The minimum acceptable hold-time must be less than, or equal to, the interval specified in the holdtime argument.
                      - The range is from 0 to 65535.
                    type: int
              activate:
                description:
                  - Enable the address family for this neighbor
                type: bool
              remove_private_as:
                description:
                  - Remove the private AS number from outbound updates
                type: bool
              next_hop_self:
                description:
                  - Enable/disable the next hop calculation for this neighbor
                type: bool
              next_hop_unchanged:
                description:
                  - Enable/disable propagation of next hop unchanged for iBGP paths to this neighbor
                type: bool   
          auto_summary:
            description:
              - Enable automatic network number summarization
            type: bool
          synchronization:
            description:
              - Enable IGP synchronization
            type: bool
  operation:
    description:
      - Specifies the operation to be performed on the BGP process configured on the device
      - Merge will configure the device based on the options specified and negate the configurations that are
        not specified for that option(i.e, networks, neighbors, etc.) in the task but present in running-configuration
      - Replace will remove the existing BGP configuration on the device and re-configure it with the options specified
      - Delete will remove the existing BGP configuration from the device
    default: merge
    choices:
      - merge
      - replace
      - delete
extends_documentation_fragment: ios
"""

EXAMPLES = """
- name: configure global bgp as 65000
  ios_bgp:
    config:
      bgp_as: 65535
      router_id: 1.1.1.1
      log_neighbor_changes: True
      neighbors:
        - neighbor: 192.168.10.1
          remote_as: 65535
          timers:
            keepalive: 300
            holdtime: 360
            min_neighbor_holdtime: 360
        - neighbor: 2.2.2.2
          remote_as: 500
      networks:
        - network: 10.0.0.0
          route_map: RMAP_1
        - network: 192.168.2.0
          mask: 255.255.254.0
      address_family:
        - afi: ipv4
          safi: unicast
          redistribute:
            - protocol: ospf
              id: 223
              metric: 10
    operation: merge

- name: remove bgp as 65000 from config
  ios_bgp:
    config:
      bgp_as: 65000
    operation: delete
"""

RETURN = """
commands:
  description: The list of configuration mode commands to send to the device
  returned: always
  type: list
  sample:
    - router bgp 65535
    - bgp router-id 1.1.1.1
    - bgp log-neighbor-changes
    - neighbor 192.168.10.1 remote-as 65535
    - neighbor 192.168.10.1 timers 300 360 360
    - neighbor 2.2.2.2 remote-as 500
    - network 10.0.0.0 route-map RMAP_1
    - network 192.168.2.0 mask 255.255.254.0
    - address-family ipv4
    - redistribute ospf 223 metric 70
    - exit-address-family
"""
from ansible.module_utils._text import to_text
from ansible.module_utils.network.ios.providers.module import NetworkModule
from ansible.module_utils.network.ios.providers.cli.config.bgp import REDISTRIBUTE_PROTOCOLS


def main():
    """ main entry point for module execution
    """
    network_spec = {
        'prefix': dict(required=True),
        'mask': dict(),
        'route_map': dict(),
    }

    redistribute_spec = {
        'protocol': dict(choices=REDISTRIBUTE_PROTOCOLS, required=True),
        'id': dict(),
        'metric': dict(type='int'),
        'route_map': dict(),
    }

    timer_spec = {
        'keepalive': dict(type='int', required=True),
        'holdtime': dict(type='int', required=True),
        'min_neighbor_holdtime': dict(type='int'),
    }

    neighbor_spec = {
        'neighbor': dict(required=True),
        'remote_as': dict(type='int', required=True),
        'update_source': dict(),
        'password': dict(no_log=True),
        'enabled': dict(type='bool'),
        'description': dict(),
        'ebgp_multihop': dict(type='int'),
        'timers': dict(type='dict', elements='dict', options=timer_spec),
        'route_reflector_client': dict(type='bool'),
        'route_server_client': dict(type='bool'),
        'peer_group': dict(),
        'activate': dict(type='bool'),
        'remove_private_as': dict(type='bool'),
        'next_hop_self': dict(type='bool'),
        'next_hop_unchanged': dict(type='bool')
    }

    address_family_spec = {
        'afi': dict(choices=['ipv4', 'ipv6'], required=True),
        'safi': dict(choices=['flowspec', 'labeled-unicast', 'multicast', 'unicast'], default='unicast'),
        'networks': dict(type='list', elements='dict', options=network_spec),
        'redistribute': dict(type='list', elements='dict', options=redistribute_spec),
        'neighbors': dict(type='list', elements='dict', options=neighbor_spec),
        'auto_summary': dict(type='bool'),
        'synchronization': dict(type='bool')
    }

    config_spec = {
        'bgp_as': dict(type='int', required=True),
        'router_id': dict(),
        'log_neighbor_changes': dict(type='bool'),
        'neighbors': dict(type='list', elements='dict', options=neighbor_spec),
        'address_family': dict(type='list', elements='dict', options=address_family_spec),
        'networks': dict(type='list', elements='dict', options=network_spec)
    }

    argument_spec = {
        'config': dict(type='dict', elements='dict', options=config_spec),
        'operation': dict(default='merge', choices=['merge', 'replace', 'delete'])
    }

    module = NetworkModule(argument_spec=argument_spec,
                           supports_check_mode=True)

    try:
        result = module.edit_config(config_filter='| section bgp')
    except Exception as exc:
        module.fail_json(msg=to_text(exc))

    module.exit_json(**result)


if __name__ == '__main__':
    main()
