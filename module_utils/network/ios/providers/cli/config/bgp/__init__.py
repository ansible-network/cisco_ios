# This code is part of Ansible, but is an independent component.
# This particular file snippet, and this file snippet only, is BSD licensed.
# Modules you write using this snippet, which is embedded dynamically by Ansible
# still belong to the author of the module, and may assign their own license
# to the complete work.
#
# (c) 2016 Red Hat Inc.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice,
#      this list of conditions and the following disclaimer in the documentation
#      and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
import re

from ansible.module_utils.six import iteritems
from ansible.module_utils.network.common.utils import to_list
from ansible.module_utils.network.ios.providers.providers import register_provider
from ansible.module_utils.network.ios.providers.providers import CliProvider
from ansible.module_utils.network.ios.providers.cli.config.bgp.neighbors import Neighbors
from ansible.module_utils.network.ios.providers.cli.config.bgp.address_family import AddressFamily

REDISTRIBUTE_PROTOCOLS = frozenset(['ospf', 'ospfv3', 'eigrp', 'isis',
                                    'static', 'connected', 'odr', 'lisp', 'mobile', 'rip'])


@register_provider('ios', 'ios_bgp')
class Provider(CliProvider):

    def render(self, config=None):
        commands = list()

        operation = self.params['operation']
        context = 'router bgp %s' % self.get_value('config.bgp_as')

        if operation == 'delete':
            if not config or context in config:
                commands.append('no %s' % context)

        else:
            if operation == 'replace':
                if config:
                    match = re.search(r'router bgp (\d+)', config, re.M)
                    if match:
                        commands.append('no router bgp %s' % match.group(1))
                config = None

            context_commands = list()

            for key, value in iteritems(self.get_value('config')):
                if value is not None:
                    meth = getattr(self, '_render_%s' % key, None)
                    if meth:
                        resp = meth(config)
                        if resp:
                            context_commands.extend(to_list(resp))

            if context_commands:
                commands.append(context)
                commands.extend(context_commands)
                commands.append('exit')

        return commands

    def _render_router_id(self, config=None):
        cmd = 'bgp router-id %s' % self.get_value('config.router_id')
        if not config or cmd not in config:
            return cmd

    def _render_log_neighbor_changes(self, config=None):
        cmd = 'bgp log-neighbor-changes'
        log_neighbor_changes = self.get_value('config.log_neighbor_changes')
        if log_neighbor_changes is True:
            if not config or cmd not in config:
                return cmd
        elif log_neighbor_changes is False:
            if config and cmd in config:
                return 'no %s' % cmd

    def _render_networks(self, config=None):
        commands = list()
        safe_list = list()

        for entry in self.get_value('config.networks'):
            network = entry['prefix']
            cmd = 'network %s' % network
            if entry['mask']:
                cmd += ' mask %s' % entry['mask']
                network += ' mask %s' % entry['mask']
            if entry['route_map']:
                cmd += ' route-map %s' % entry['route_map']
                network += ' route-map %s' % entry['route_map']

            safe_list.append(network)

            if not config or cmd not in config:
                commands.append(cmd)

        if config:
            matches = re.findall(r'network (.*)', config, re.M)
            for entry in set(matches).difference(safe_list):
                commands.append('no network %s' % entry)

        return commands

    def _render_neighbors(self, config):
        """ generate bgp neighbor configuration
        """
        return Neighbors(self.params).render(config)

    def _render_address_family(self, config):
        """ generate address-family configuration
        """
        return AddressFamily(self.params).render(config)
