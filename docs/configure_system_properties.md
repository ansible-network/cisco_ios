# Configure System properties on the device

The `configure_system_properties` function can be used to set system properties on 
Cisco IOS devices.  This function is only supported over `network_cli` connection
type and requires the `ansible_network_os` value set to `ios`.

## How to set System properties on the device

To set System properties on the device, simply include this function in the playbook
using either the `roles` directive or the `tasks` directive.  If no other
options are provided, then all of the available facts will be collected for the
device.

Below is an example of how to use the `roles` directive to set system properties
on the Cisco IOS device.

```
- hosts: ios

  roles:
  - name ansible-network.cisco_ios
    function: configure_system_properties
  vars:
    system_properties:
      - hostname: test-ios
        domain_name: hostname.com
        ip_domain_name: test_ip_domain.com
        ip_name_server: 192.168.1.1
        vrf_name: vrf-01
        vrf_description: new vrf named as vrf-01
        vrf_address_family: ipv4 multicast
        vrf_ipv4: multicast multitopology
        vrf_route_target: 100:26
        vrf_vnet: 4
        vrf_vpn: 2:3
        vrf_rd: 101:3
```

The above playbook will set the hostname, domain-name and the name-server values to
the host under the `ios` top level key.  

### Implement using tasks

The `configure_system_properties` function can also be implemented using the `tasks` 
directive instead of the `roles` directive.  By using the `tasks` directive, you can
control when the fact collection is run. 

Below is an example of how to use the `configure_system_properties` function with `tasks`.

```
- hosts: ios

  tasks:
    - name: set system properties to ios devices
      import_role:
        name: ansible-network.cisco_ios
        tasks_from: configure_system_properties
      vars:
        system_properties:
          - hostname: test-ios
            domain_name: hostname.com
            ip_domain_name: test_ip_domain.com
            ip_name_server: 192.168.1.1
            vrf_name: vrf-01
            vrf_description: new vrf named as vrf-01
            vrf_address_family: ipv4 multicast
            vrf_ipv4: multicast multitopology
            vrf_route_target: 100:26
            vrf_vnet: 4
            vrf_vpn: 2:3
            vrf_rd: 101:3
```

## Adding new parsers

Over time new parsers can be added (or updated) to the role to add additional
or enhanced functionality.  To add or update parsers perform the following
steps:

* Add (or update) command parser located in `parse_templates/cli`

## Arguments

### hostname

This will set the System host name for the Cisco IOS device.

The default value is `omit` which means even if the user doesn't pass the respective
value the role will continue to run without any failure.

### domain_name

This will set the System domain name for the Cisco IOS device.

The default value is `omit` which means even if the user doesn't pass the respective 
value the role will continue to run without any failure.

### ip_domain_name

This will define the default domain name.

The default value is `omit` which means even if the user doesn't pass the respective
value the role will continue to run without any failure.

### ip_name_server

This will set the Domain Name Server (DNS) for the Cisco IOS device.

The default value is `omit` which means even if the user doesn't pass the respective 
value the role will continue to run without any failure.

### vrf_name

VRF name that need to be configured for the Cisco IOS device. Also, this is mandatory
parameter for VRF configuration.

The default value is `omit` which means even if the user doesn't pass the respective
value the role will continue to run without any failure.

### vrf_description

A description for the VRF to be configured for the Cisco IOS device.

The default value is `omit` which means even if the user doesn't pass the respective
value the role will continue to run without any failure.

### vrf_address_family

Enter Address Family command mode for the Cisco IOS device.

The default value is `omit` which means even if the user doesn't pass the respective
value the role will continue to run without any failure.

### vrf_ipv4

This will set the VRF IPv4 configuration for the Cisco IOS device.

The default value is `omit` which means even if the user doesn't pass the respective
value the role will continue to run without any failure.

### vrf_route_target

Specify Target VPN Extended Communities.

The default value is `omit` which means even if the user doesn't pass the respective
value the role will continue to run without any failure.

### vrf_vnet

Specifies the Virtual NETworking configuration.

The default value is `omit` which means even if the user doesn't pass the respective
value the role will continue to run without any failure.
            
### vrf_vpn

Configure VPN ID as specified in rfc2685.

The default value is `omit` which means even if the user doesn't pass the respective
value the role will continue to run without any failure.

### vrf_rd

Specifies the Route Distinguisher.

The default value is `omit` which means even if the user doesn't pass the respective
value the role will continue to run without any failure.

### state

This will set the hostname, domain-name, name-server and VRF value to the Cisco IOS
device and if the value of the state is changed to `absent`, role will go ahead and try 
to delete the hostname, domain-name, name-server and VRF passed via the arguments.

The default value is `present` which means even if the user doesn't pass the respective
argument, the role will go ahead and try to set the hostname, domain-name, name-server 
and VRF via the arguments passed to the Cisco IOS device.

## Notes

None
