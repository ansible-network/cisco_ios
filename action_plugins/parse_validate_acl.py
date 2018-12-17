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
import netaddr
import json
import socket

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
        dest = generated_flow_file

        parser = unfrackpath(parser)
        if not os.path.exists(parser):
            return {'failed': True, 'msg': 'path: %s does not exist.' % parser}
        parser_file = parser

        pd_json = self._parse_acl_with_textfsm(
            parser_file, show_acl_output_buffer)
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

    def _create_packet_dict(self, cmd_out):
        import warnings
        with warnings.catch_warnings(record=True):
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
            except Exception:
                continue

            if p.terms:
                match = p.terms[0].match
                for key in match:
                    if key == 'source-address':
                        for m in match["source-address"]:
                            v = netaddr.IPNetwork(str(m))
                            # Return the host in middle of subnet
                            size_subnet = v.size
                            host_index = int(size_subnet / 2)
                            pd_it["src"] = str(v[host_index])
                    if key == 'destination-address':
                        for m in match["destination-address"]:
                            v = netaddr.IPNetwork(str(m))
                            # Return the host in middle of subnet
                            size_subnet = v.size
                            host_index = int(size_subnet / 2)
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
                if "dst" not in pd_it:
                    pd_it["dst"] = "any"
                if "src" not in pd_it:
                    pd_it["src"] = "any"
                pd_it["service_line_index"] = str(index)
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

    def _parse_acl_with_textfsm(self, parser_file, output):
        import textfsm
        tmp = open(parser_file)
        re_table = textfsm.TextFSM(tmp)
        results = re_table.ParseText(output)
        fsm_results = []
        for item in results:
            facts = {}
            facts.update(dict(zip(re_table.header, item)))
            fsm_results.append(facts)

        pd = []
        parsed_acl = []
        # Convert dictionary of terms into flows dictionary
        for term in fsm_results:
            pd_it = {}
            original_terms = {}
            for k, v in term.items():
                if k == 'LINE_NUM' and v == '':
                    # Empty line with just name
                    continue
                elif k == 'LINE_NUM' and v != '':
                    pd_it["service_line_index"] = v
                    original_terms["service_line_index"] = v
                if k == 'PROTOCOL' and v != '':
                    pd_it["proto"] = v
                    original_terms['proto'] = v
                if k == 'ACTION' and v != '':
                    pd_it["action"] = v
                    original_terms['action'] = v
                if k == 'SRC_NETWORK' and v != '':
                    if 'SRC_WILDCARD' in term:
                        src_mask = term['SRC_WILDCARD']
                        src_invert_mask = sum([bin(255 - int(x)).count("1") for x in
                                              src_mask.split(".")])
                    else:
                        src_invert_mask = '32'
                    cidr = "%s/%s" % (v, src_invert_mask)
                    src_ip = netaddr.IPNetwork(cidr)
                    size_subnet = src_ip.size
                    host_index = int(size_subnet / 2)
                    pd_it['src'] = str(src_ip[host_index])
                    original_terms['src'] = src_ip
                if k == 'SRC_ANY' and v != '':
                    pd_it['src'] = "any"
                    original_terms['src'] = netaddr.IPNetwork('0.0.0.0/0')
                if k == 'SRC_HOST' and v != '':
                    pd_it['src'] = v
                    original_terms['src'] = v
                if k == 'SRC_PORT' and v != '':
                    if not v[0].isdigit():
                        v = str(socket.getservbyname(v))
                    pd_it['src_port'] = v
                    original_terms['src_port'] = v
                if k == 'DST_NETWORK' and v != '':
                    if 'DST_WILDCARD' in term:
                        dst_mask = term['DST_WILDCARD']
                        dst_invert_mask = sum([bin(255 - int(x)).count("1") for x in
                                              dst_mask.split(".")])
                    else:
                        dst_invert_mask = '32'
                    d_cidr = "%s/%s" % (v, dst_invert_mask)
                    dst_ip = netaddr.IPNetwork(d_cidr)
                    d_size_subnet = dst_ip.size
                    d_host_index = int(d_size_subnet / 2)
                    pd_it['dst'] = str(dst_ip[d_host_index])
                    original_terms['dst'] = dst_ip
                if k == 'DST_ANY' and v != '':
                    pd_it['dst'] = "any"
                    original_terms['dst'] = netaddr.IPNetwork('0.0.0.0/0')
                if k == 'DST_HOST' and v != '':
                    pd_it['dst'] = v
                    original_terms['dst'] = v
                if k == 'DST_PORT' and v != '':
                    if not v[0].isdigit():
                        v = str(socket.getservbyname(v))
                    pd_it['dst_port'] = v
                    original_terms['dst_port'] = v

            if pd_it:
                pd.append(pd_it)
            if original_terms:
                parsed_acl.append(original_terms)

        # Store parsed acl on this object for later processing
        self._parsed_acl = parsed_acl
        return json.dumps(pd, indent=4)
