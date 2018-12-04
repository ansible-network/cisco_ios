===============================
cisco_ios
===============================

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
