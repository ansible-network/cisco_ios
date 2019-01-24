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
from ansible.module_utils.network.ios.providers.providers import CliProvider
from ansible.module_utils.network.ios.providers.cli.config.bgp.neighbors import Neighbors


class AddressFamily(CliProvider):

    def render(self, config=None):
        commands = list()
        safe_list = list()

        router_context = 'router bgp %s' % self.get_value('config.bgp_as')
        context_config = None

        for item in self.get_value('config.address_family'):
            context = 'address-family %s' % item['afi']
            if item['safi'] != 'unicast':
                context += ' %s' % item['safi']
            context_commands = list()

            if config:
                context_path = [router_context, context]
                context_config = self.get_config_context(config, context_path, indent=1)

            for key, value in iteritems(item):
                if value is not None:
                    meth = getattr(self, '_render_%s' % key, None)
                    if meth:
                        resp = meth(item, context_config)
                        if resp:
                            context_commands.extend(to_list(resp))

            if context_commands:
                commands.append(context)
                commands.extend(context_commands)
                commands.append('exit-address-family')

            safe_list.append(context)

        if self.params['operation'] == 'replace':
            if config:
                resp = self._negate_config(config, safe_list)
                commands.extend(resp)

        return commands

    def _negate_config(self, config, safe_list=None):
        commands = list()
        matches = re.findall(r'(address-family .+)$', config, re.M)
        for item in set(matches).difference(safe_list):
            commands.append('no %s' % item)
        return commands

    def _render_auto_summary(self, item, config=None):
        cmd = 'auto-summary'
        if item['auto_summary'] is False:
            cmd = 'no %s' % cmd
        if not config or cmd not in config:
            return cmd

    def _render_synchronization(self, item, config=None):
        cmd = 'synchronization'
        if item['synchronization'] is False:
            cmd = 'no %s' % cmd
        if not config or cmd not in config:
            return cmd

    def _render_networks(self, item, config=None):
        commands = list()
        safe_list = list()

        for entry in item['networks']:
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

        if self.params['operation'] == 'replace':
            if config:
                matches = re.findall(r'network (.*)', config, re.M)
                for entry in set(matches).difference(safe_list):
                    commands.append('no network %s' % entry)

        return commands

    def _render_redistribute(self, item, config=None):
        commands = list()
        safe_list = list()

        for entry in item['redistribute']:
            option = entry['protocol']

            cmd = 'redistribute %s' % entry['protocol']

            if entry['id'] and entry['protocol'] in ('ospf', 'ospfv3', 'eigrp'):
                cmd += ' %s' % entry['id']
                option += ' %s' % entry['id']

            if entry['metric']:
                cmd += ' metric %s' % entry['metric']

            if entry['route_map']:
                cmd += ' route-map %s' % entry['route_map']

            if not config or cmd not in config:
                commands.append(cmd)

            safe_list.append(option)

        if self.params['operation'] == 'replace':
            if config:
                matches = re.findall(r'redistribute (\S+ \S+)', config, re.M)
                for entry in set(matches).difference(safe_list):
                    commands.append('no redistribute %s' % entry)
        return commands

    def _render_neighbors(self, item, config):
        """ generate bgp neighbor configuration
        """
        return Neighbors(self.params).render(config, nbr_list=item['neighbors'])
