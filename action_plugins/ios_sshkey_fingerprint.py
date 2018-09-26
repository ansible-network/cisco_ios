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

import base64
import hashlib

from ansible.plugins.action import ActionBase


class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)

        try:
            users = self._task.args['users']
        except KeyError as exc:
            return {'failed': True, 'msg': 'missing required argument: %s' % exc}

        for user in users:
            if 'sshkey' in user:
                user['sshkey'] = self.calculate_fingerprint(user['sshkey'])

        result['users'] = users

        return result


    def calculate_fingerprint(self, sshkey):
        if not sshkey:
            return None
        if ' ' in sshkey:
            keyparts = sshkey.split(' ')
            keyparts[1] = hashlib.md5(base64.b64decode(keyparts[1])).hexdigest().upper()
            return ' '.join(keyparts)
        else:
            return 'ssh-rsa %s' % hashlib.md5(base64.b64decode(sshkey)).hexdigest().upper()
