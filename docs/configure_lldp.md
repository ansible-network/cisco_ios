# Configure LLDP on the device

The `configure_lldp` function can be used to set LLDP on Cisco IOS devices.
This function is only supported over `network_cli` connection type and 
requires the `ansible_network_os` value set to `ios`.

## How to set LLDP on the device

To set LLDP on the device, simply include this function in the playbook
using either the `roles` directive or the `tasks` directive.  If no other
options are provided, then all of the available facts will be collected for 
the device.

Below is an example of how to use the `roles` directive to set LLDP on the
Cisco IOS device.

```
- hosts: ios

  roles:
  - name ansible-network.cisco_ios
    function: configure_lldp
  vars:
    lldp:
      - holdtime: 60
        reinit: 4
        timer: 60
        tlv-select: management-address
        interface: GigabitEthernet 0/3
        receive: enable
        transmit: disable
```

The above playbook will set the LLDP with holdtime, reinit, tlv-select, receive,
and transmit to particular interface under the `ios` top level key.  

### Implement using tasks

The `configure_lldp` function can also be implemented using the `tasks` directive
instead of the `roles` directive.  By using the `tasks` directive, you can
control when the fact collection is run. 

Below is an example of how to use the `configure_lldp` function with `tasks`.

```
- hosts: ios

  tasks:
    - name: set lldp to ios devices
      import_role:
        name: ansible-network.cisco_ios
        tasks_from: configure_lldp
      vars:
        lldp:
          - holdtime: 60
            reinit: 4
            timer: 60
            tlv-select: management-address
            interface: GigabitEthernet 0/3
            receive: enable
            transmit: disable
```

## Adding new parsers

Over time new parsers can be added (or updated) to the role to add additional
or enhanced functionality.  To add or update parsers perform the following
steps:

* Add (or update) command parser located in `parse_templates/cli`

## Arguments

### holdtime

LLDP holdtime specifies the length of time that information from an LLDP packet should
be held by the receiving device before aging and removing it.

The default value is `omit` which means even if the user doesn't pass the respective
value the role will continue to run without any failure.

### reinit

LLDP reint specifies the length of time, the initialization of LLDP on an interface should 
be delayed.

The default value is `omit` which means even if the user doesn't pass the respective
value the role will continue to run without any failure.

### timer

LLDP timer specifies the LLDP packet rate.

The default value is `omit` which means even if the user doesn't pass the respective 
value the role will continue to run without any failure.

### tlv-select
LLDP tlv-select specifies that transmission of the selected TLV in LLDP packets is disabled.
The tlv-name can be one of these LLDP TLV types:

* mac-phy-cfg
* management-address
* port-description
* port-vlan
* power-management
* system-capabilities
* system-description
* system-name

The default value is `omit` which means even if the user doesn't pass the respective
value the role will continue to run without any failure.

### interface

When you enable LLDP globally on the router, all supported interfaces are automatically 
enabled for LLDP receive and transmit operations. It can be overriden by disabling these 
operations for a particular interface.

### receive

LLDP receive disables LLDP receive operations on the interface. It can only be set if value
of interface is set as `recieve` operations will be enabled/disabled on the respective interface.

### transmit

LLDP receive disables LLDP transmit operations on the interface. It can only be set if value
of interface is set as `transmit` operations will be enabled/disabled on the respective interface.

### state

This sets the LLDP value to the Cisco IOS-XR device and if the value of the state is changed
to `absent`, the role will go ahead and try to delete the condifured LLDP via the arguments
passed.

The default value is `present` which means even if the user doesn't pass the respective
argument, the role will go ahead and try to set the LLDP via the arguments passed to the 
Cisco IOS-XR device.

## Notes

None
