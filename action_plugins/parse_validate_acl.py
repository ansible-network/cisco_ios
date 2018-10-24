# (c) 2018, Ansible Inc,
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
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import copy
import os
import time
import re
import hashlib

from ansible.module_utils._text import to_bytes, to_text
from ansible.module_utils.connection import Connection
from ansible.errors import AnsibleError
from ansible.plugins.action import ActionBase
from ansible.module_utils.six.moves.urllib.parse import urlsplit
from ansible.utils.path import unfrackpath

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):
        socket_path = None

        result = super(ActionModule, self).run(task_vars=task_vars)

        try:
            show_acl_output_buffer = self._task.args.get('show_acl_output_buffer')
        except KeyError as exc:
            return {'failed': True, 'msg': 'missing required argument: %s' % exc}

        try:
            parser = self._task.args.get('parser')
        except KeyError as exc:
            return {'failed': True, 'msg': 'missing required argument: %s' % exc}

        try:
            generated_flow_file = self._task.args.get('generated_flow_file')
        except KeyError as exc:
            return {'failed': True, 'msg': 'missing required argument: %s' % exc}

        generated_flow_file = unfrackpath(generated_flow_file)
        if not os.path.exists(generated_flow_file):
            return {'failed': True, 'msg': 'path: %s does not exist.' % generated_flow_file}
        dest = generated_flow_file

        parser = unfrackpath(parser)
        if not os.path.exists(parser):
            return {'failed': True, 'msg': 'path: %s does not exist.' % parser}
        parser_file = parser

        #pd_json = self._create_packet_dict(out)
        pd_json = self._parse_acl_with_textfsm(parser_file,
                                    show_acl_output_buffer)
        try:
            changed = self._write_packet_dict(dest, pd_json) 
        except IOError as exc:
            result['failed'] = True
            result['msg'] = ('Exception received : %s' % exc)
   
        result['changed'] = changed
        if changed:
            result['destination'] = dest
        else:
            result['dest_unchanged'] = dest
        
        return result

    def _parse_acl_with_textfsm(self, parser_file, output):
        import textfsm
        tmp = open(parser_file)
        re_table = textfsm.TextFSM(tmp)
        results = re_table.ParseText(output)
        print (results)
        return results

    def _create_packet_dict(self, cmd_out):
        import warnings
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            from trigger.acl import parse
        import netaddr
        import json
        import uuid

        # pd is list of dictionary of packets
        pd = []
        lines = cmd_out.split('\n')
        for index, line in enumerate(lines):
            line = to_bytes(line, errors='surrogate_or_strict')
            pd_it = {}
            try:
                p = parse(line)
            except Exception as e:
                continue

            if p.terms:
                match = p.terms[0].match
                for key in match:
                    if key == 'source-address':
                        for m in match["source-address"]:
                            v = netaddr.IPNetwork(str(m))
                            # Return the host in middle of subnet
                            size_subnet = v.size
                            host_index = int(size_subnet/2)
                            pd_it["src"] = str(v[host_index])
                    if key == 'destination-address':
                        for m in match["destination-address"]:
                            v = netaddr.IPNetwork(str(m))
                            # Return the host in middle of subnet
                            size_subnet = v.size
                            host_index = int(size_subnet/2)
                            pd_it["dst"] = str(v[host_index])
                    if key == 'protocol':
                        for m in match['protocol']:
                            pd_it["proto"] = str(m)
                    if key == 'destination-port':
                        for m in match["destination-port"]:
                            pd_it['dst_port'] = str(m)
                    if key == 'source-port':
                        for m in match["source-port"]:
                            pd_it['src_port'] = str(m)

                action = p.terms[0].action
                for act in action:
                    pd_it["action"] = act

            if pd_it is not None:
                if not "dst" in pd_it:
                    pd_it["dst"] = "any"
                if not "src" in pd_it:
                    pd_it["src"] = "any"
                pd_it["service_line_index"] = str(index)
    #+ '-' + str(uuid.uuid4())[:8]
                pd.append(pd_it)

        return json.dumps(pd, indent=4)


    def _write_packet_dict(self, dest, contents):
        # Check for Idempotency
        if os.path.exists(dest):
            try:
                with open(dest, 'r') as f:
                    old_content = f.read()
            except IOError as ioexc:
                raise IOError(ioexc)
            sha1 = hashlib.sha1()
            old_content_b = to_bytes(old_content, errors='surrogate_or_strict')
            sha1.update(old_content_b)
            checksum_old = sha1.digest()

            sha1 = hashlib.sha1()
            new_content_b = to_bytes(contents, errors='surrogate_or_strict')
            sha1.update(new_content_b)
            checksum_new = sha1.digest()
            if checksum_old == checksum_new:
               return (False)

        try:
            with open(dest, 'w') as f:
                f.write(contents)
        except IOError as ioexc:
            raise IOError(ioexc)

        return (True) 
