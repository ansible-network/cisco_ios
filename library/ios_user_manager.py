#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2018 Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'network'}


DOCUMENTATION = '''
---
module: ios_user_manager
short_description: Manage an aggregate of users in IOS device(s)
description:
    - Allows the `cisco_ios` provider role to manage aggregate of users
      by providing idempotency and other utility functions while running
      the `configure_user` task
version_added: "2.7"
options:
  new_users:
    description:
      - Aggregate of local users to be configured on IOS device(s)
    required: true
  user_config:
    description:
      - User config lines extracted from the devices' running-configuration
    required: true
author:
  - Nilashish Chakraborty (@NilashishC)
'''
RETURN = """
stdout:
  description: Filtered set of users that should be configured on the device
  returned: always apart from low-level errors (such as action plugin)
  type: list
  sample: [{"name": "ansible", "privilege": 15}, {"name": "test_user", "privilege": 15, "view": "sh_int"}]
"""
EXAMPLES = '''
- ios_user_manager:
    new_users: "{{ users }}"
    user_config: "{{ existing_user_config.stdout }}"
'''
