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
import re, q

from ansible.module_utils.six import iteritems
from ansible.module_utils.network.common.utils import to_list
from ansible.module_utils.network.ios.providers.providers import CliProvider


class Neighbors(CliProvider):

    def render(self, config=None, nbr_list=None):
        commands = list()
        safe_list = list()
        if not nbr_list:
            nbr_list = self.get_value('config.neighbors')
        for item in nbr_list:
            neighbor_commands = list()
            context = 'neighbor %s' % item['neighbor']
            cmd = '%s remote-as %s' % (context, item['remote_as'])

            if not config or cmd not in config:
                neighbor_commands.append(cmd)

            for key, value in iteritems(item):
                if value is not None:
                    meth = getattr(self, '_render_%s' % key, None)
                    if meth:
                        resp = meth(item, config)
                        if resp:
                            neighbor_commands.extend(to_list(resp))

            commands.extend(neighbor_commands)
            safe_list.append(context)

        if self.params['operation'] == 'replace':
            if config and safe_list:
                commands.extend(self._negate_config(config, safe_list))

        return commands

    def _negate_config(self, config, safe_list=None):
        commands = list()
        matches = re.findall(r'(neighbor \S+)', config, re.M)
        for item in set(matches).difference(safe_list):
            commands.append('no %s' % item)
        return commands

    def _render_description(self, item, config=None):
        cmd = 'neighbor %s description %s' % (item['neighbor'], item['description'])
        if not config or cmd not in config:
            return cmd

    def _render_enabled(self, item, config=None):
        cmd = 'neighbor %s shutdown' % item['neighbor']
        if item['enabled'] is True:
            cmd = 'no %s' % cmd
        if not config or cmd not in config:
            return cmd

    def _render_route_reflector_client(self, item, config=None):
        cmd = 'neighbor %s route-reflector-client' % item['neighbor']
        if item['route_reflector_client'] is False:
            cmd = 'no %s' % cmd
        if not config or cmd not in config:
            return cmd

    def _render_route_server_client(self, item, config=None):
        cmd = 'neighbor %s route-server-client' % item['neighbor']
        if item['route_server_client'] is False:
            cmd = 'no %s' % cmd
        if not config or cmd not in config:
            return cmd

    def _render_update_source(self, item, config=None):
        cmd = 'neighbor %s update-source %s' % (item['neighbor'], item['update_source'])
        if not config or cmd not in config:
            return cmd

    def _render_password(self, item, config=None):
        cmd = 'neighbor %s password %s' % (item['neighbor'], item['password'])
        if not config or cmd not in config:
            return cmd

    def _render_ebgp_multihop(self, item, config=None):
        cmd = 'neighbor %s ebgp-multihop %s' % (item['neighbor'], item['ebgp_multihop'])
        if not config or cmd not in config:
            return cmd

    def _render_peer_group(self, item, config=None):
        cmd = 'neighbor %s peer-group %s' % (item['neighbor'], item['peer_group'])
        if not config or cmd not in config:
            return cmd

    def _render_activate(self, item, config=None):
        cmd = 'neighbor %s activate' % item['neighbor']
        if item['activate'] is False:
            cmd = 'no %s' % cmd
        if not config or cmd not in config:
            return cmd

    def _render_remove_private_as(self, item, config=None):
        cmd = 'neighbor %s remove-private-as' % item['neighbor']
        if item['remove_private_as'] is False:
            cmd = 'no %s' % cmd
        if not config or cmd not in config:
            return cmd

    def _render_next_hop_self(self, item, config=None):
        cmd = 'neighbor %s next-hop-self' % item['neighbor']
        if item['next_hop_self'] is False:
            cmd = 'no %s' % cmd
        if not config or cmd not in config:
            return cmd

    def _render_next_hop_unchanged(self, item, config=None):
        cmd = 'neighbor %s next-hop-unchanged' % item['neighbor']
        if item['next_hop_unchanged'] is False:
            cmd = 'no %s' % cmd
        if not config or cmd not in config:
            return cmd

    def _render_timers(self, item, config):
        """generate bgp timer related configuration
        """
        keepalive = item['timers']['keepalive']
        holdtime = item['timers']['holdtime']
        min_neighbor_holdtime = item['timers']['min_neighbor_holdtime']
        neighbor = item['neighbor']

        if keepalive and holdtime:
            cmd = 'neighbor %s timers %s %s' % (neighbor, keepalive, holdtime)
            if min_neighbor_holdtime:
                cmd += ' %s' % min_neighbor_holdtime
            if not config or cmd not in config:
                return cmd
        else:
            raise ValueError("required both options for timers: keepalive and holdtime")
