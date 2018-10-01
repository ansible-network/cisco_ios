===============================
cisco_ios
===============================

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
