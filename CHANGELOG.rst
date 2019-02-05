=========================
Ansible Network cisco_ios
=========================
.. _cisco_ios_v2.7.1:

v2.7.1
======

.. _cisco_ios_v2.7.1_Minor Changes:

Minor Changes
-------------

- Adds parser for reload reason. `ios-#87 <https://github.com/ansible-network/cisco_ios/pull/87>`_.
- Fixed message ``missing required arg: config_manager_text``. `ios-#88 <https://github.com/ansible-network/cisco_ios/pull/88>`_.
- Remove set defaults task files. `ios-#89 <https://github.com/ansible-network/cisco_ios/pull/89>`_.
- Use default template if no specific peer provider folder is present. `ios-#90 <https://github.com/ansible-network/cisco_ios/pull/90>`_.
- Add unconfigure task hooks. `ios-#92 <https://github.com/ansible-network/cisco_ios/pull/92>`_.

.. _cisco_ios_v2.7.0:

v2.7.0
======

.. _cisco_ios_v2.7.0_Major Changes:

Major Changes
-------------

- Initial release of 2.7.0 ``cisco_ios`` Ansible role that is supported with Ansible 2.7.0
- Dependant role ``ansible-network.network-engine`` should be upgraded with version >= 2.7.2 

.. _cisco_ios_v2.7.0_Bugfixes:

Bugfixes
--------

- multiline banner processing (cli_config issue) (#69)
- Ensure that subset is a list. Align docs with fact map (#47)
- Created test for show_interfaces parser (#58)
- fix for 'interfaces' facts (#55)
- fix for handling config text with lines containing only whitespace chars (#64)

.. _cisco_ios_v2.6.3:

v2.6.3
======

.. _cisco_ios_v2.6.3_New Features

New Features
------------

- NEW provider tasks and parsers for net_operations role

.. _cisco_ios_v2.6.3_Bugfixes:

Bugfixes
--------

- configure_user task should use config_manager_file instead of config_manager_text
- uptime facts from cisco IOS has separate keys for year, week, days hours and time

.. _cisco_ios_v2.6.2:

v2.6.2
======

.. _cisco_ios_v2.6.2_New Features

New Features
------------

- NEW Added CPF and Fiber Optic DOM parser
- NEW Added dependency role plugin check

.. _cisco_ios_v2.6.1:

v2.6.1
======

.. _cisco_ios_v2.6.1_New Action Plugins:

New Action Plugins
------------------

- NEW ``ios_user_manager`` action plugin

.. _cisco_ios_v2.6.1_New Tasks:

New Tasks
---------

- NEW ``configure_user`` task

.. _cisco_ios_v2.6.1_Bugfixes:

Bugfixes
--------

- Refactor vrf and bgp output and improve reliability (#29)
- better support for working with config_manager tasks

devel
=====

New Functions
-------------

- NEW `get_facts` retrive and parse facts from cisco ios devices
- NEW `config_manager/get` support for config_manager get function
- NEW `config_manager/load` support for config_manager load function
- NEW `config_manager/save` support for config_manager save function
- NEW `configure_user` support for configuring users on cisco ios devices


Major Changes
-------------

- Initial release of the `cisco_ios` role.
