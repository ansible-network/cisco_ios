# Configure VPN routing as initiator
The `cloud_vpn/configure_routing_initiator` function will configure the routing where
a VPN as initiator has been configured previously on Cisco IOS devices.
It is performed by calling the `cloud_vpn/configure_routing_initiator` task from the role.
The task will process variables needed for routing configuration and apply it to the device.

Below is an example to configure routing on a CSR device configured as initiator,
where the responder is AWS VPN.

```
- hosts: cisco_ios

  tasks:
    - name: Configure initiator routing
      include_role:
        name: ansible-network.cisco_ios
        tasks_from: cloud_vpn/configure_routing_initiator
      vars:
        cloud_vpn_responder_provider: aws_vpn
        cloud_vpn_responder_cidr: 192.168.0.0/24
```

## Notes
None
