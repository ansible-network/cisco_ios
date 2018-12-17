# (c) 2018, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'network'}
import re
import base64
import hashlib

from ansible.plugins.action import ActionBase


class UserManager:

    def __init__(self, new_users, user_config_data):
        self.__new_users = new_users
        self.__user_config_data = user_config_data

    @staticmethod
    def calculate_fingerprint(sshkey):
        if ' ' in sshkey:
            keyparts = sshkey.split(' ')
            keyparts[1] = hashlib.md5(base64.b64decode(keyparts[1])).hexdigest().upper()
            return ' '.join(keyparts)

        else:
            return 'ssh-rsa %s' % hashlib.md5(base64.b64decode(sshkey)).hexdigest().upper()

    def _parse_view(self, data):
        match = re.search(r'view (\S+)', data, re.M)
        if match:
            return match.group(1)

    def _parse_sshkey(self, data):
        match = re.search(r'key-hash (\S+ \S+(?: .+)?)$', data, re.M)
        if match:
            return match.group(1)

    def _parse_privilege(self, data):
        match = re.search(r'privilege (\S+)', data, re.M)
        if match:
            return int(match.group(1))

    def generate_existing_users(self):
        match = re.findall(r'(?:^(?:u|\s{2}u))sername (\S+)', self.__user_config_data, re.M)
        if not match:
            return []

        existing_users = []

        for user in set(match):
            regex = r'username %s .+$' % user
            cfg = re.findall(regex, self.__user_config_data, re.M)
            cfg = '\n'.join(cfg)
            sshregex = r'username %s\n\s+key-hash .+$' % user
            sshcfg = re.findall(sshregex, self.__user_config_data, re.M)
            sshcfg = '\n'.join(sshcfg)

            obj = {
                'name': user,
                'sshkey': self._parse_sshkey(sshcfg),
                'privilege': self._parse_privilege(cfg),
                'view': self._parse_view(cfg)
            }

            filtered = {k: v for k, v in obj.items() if v is not None}
            obj.clear()
            obj.update(filtered)

            existing_users.append(obj)

        return existing_users

    def filter_users(self):
        want = self.__new_users
        for user in want:
            if 'sshkey' in user:
                user['sshkey'] = self.calculate_fingerprint(user['sshkey'])

        have = self.generate_existing_users()
        filtered_users = [x for x in want if x not in have]

        changed = True if len(filtered_users) > 0 else False

        return changed, filtered_users


class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)

        try:
            new_users = self._task.args['new_users']
            user_config_data = self._task.args['user_config']
        except KeyError as exc:
            return {'failed': True, 'msg': 'missing required argument: %s' % exc}

        result['changed'], result['stdout'] = UserManager(new_users, user_config_data).filter_users()

        return result
