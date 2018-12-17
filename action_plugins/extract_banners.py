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

DOCUMENTATION = """
---
module: extract_banners
author: Ansible Network Team
short_description: remove banners from config text
description:
  - The config text specified in C(config) will be used to extract banners
    from it. Banners need to be executed on device in special manner. It
    returns configs with banner removed and a dictionary of banners
version_added: "2.7"
options:
  config:
    description:
      - Config text from which banners need to be extracted.
    required: yes
    default: null
"""

EXAMPLES = """
- name: extract multiline banners
  extract_banners:
    config: "{{ ios_config_text }}"

"""

RETURN = """
config:
  description: returns the config with masked banners
  returned: always
  type: str
banners:
  description: returns the extracted banners
  returned: always
  type: dict
"""
import re
from ansible.plugins.action import ActionBase
from ansible.module_utils._text import to_text
from ansible.errors import AnsibleError

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


class ActionModule(ActionBase):

    def run(self, tmp=None, task_vars=None):
        ''' handler for extract_banners  '''

        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        try:
            config = self._task.args['config']
        except KeyError as exc:
            raise AnsibleError(to_text(exc))

        # make config required argument
        if not config:
            raise AnsibleError('missing required argument `config`')

        banners, masked_config = self._extract_banners(config)
        result['config'] = masked_config
        result['banners'] = banners
        return result

    def _extract_banners(self, config):
        config_lines = config.split('\n')
        found_banner_start = 0
        banner_meta = []
        for linenum, line in enumerate(config_lines):
            if not found_banner_start:
                banner_start = re.search(r'^banner\s+(\w+)\s+(.*)', line)
                if banner_start:
                    banner_cmd = banner_start.group(1)
                    try:
                        banner_delimiter = banner_start.group(2)
                        banner_delimiter = banner_delimiter.strip()
                        banner_delimiter_esc = re.escape(banner_delimiter)
                    except Exception:
                        continue
                    banner_start_index = linenum
                    found_banner_start = 1
                    continue

            if found_banner_start:
                # Search for delimiter found in current banner start
                regex = r'%s' % banner_delimiter_esc
                banner_end = re.search(regex, line)
                if banner_end:
                    found_banner_start = 0
                    kwargs = {
                        'banner_cmd': banner_cmd,
                        'banner_delimiter': banner_delimiter,
                        'banner_start_index': banner_start_index,
                        'banner_end_index': linenum,
                    }
                    banner_meta.append(kwargs)

        # Build banners from extracted data
        banner_lines = []
        for banner in banner_meta:
            banner_lines.append('banner %s %s' % (banner['banner_cmd'],
                                banner['banner_delimiter']))
            banner_conf_lines = config_lines[banner['banner_start_index'] + 1: banner['banner_end_index']]
            for index, conf_line in enumerate(banner_conf_lines):
                banner_lines.append(conf_line)
            banner_lines.append('%s' % banner['banner_delimiter'])

        # Delete banner lines from config
        for banner in banner_meta:
            banner_lines_range = range(banner['banner_start_index'],
                                       banner['banner_end_index'] + 1)
            for index in banner_lines_range:
                config_lines[index] = '! banner removed'

        configs = '\n'.join(config_lines)
        return (banner_lines, configs)
