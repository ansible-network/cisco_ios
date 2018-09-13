# Configure VPN as initiator
The `cloud_vpn/configure_vpn_initiator` function will configure IPSEC VPN as initiator
on Cisco IOS devices.
It is performed by calling the `cloud_vpn/configure_vpn_initiator` task from the role.
The task will process variables needed for VPN configuration and apply it to the device.

Below is an example to configure an IPSEC VPN as initiator on CSR device, where
the responder is AWS VPN:

```
- hosts: cisco_ios

  tasks:
    - name: Configure IPSEC VPN as initiator
      include_role:
        name: ansible-network.cisco_ios
        tasks_from: cloud_vpn/configure_vpn_initiator
      vars:
        cloud_vpn_name: myvpn
        cloud_vpn_psk: mypsksecret
        cloud_vpn_initiator_provider: csr
        cloud_vpn_initiator_outside_interface: GigabitEthernet1
        cloud_vpn_initiator_tunnel_ip: 169.254.56.25
        cloud_vpn_initiator_tunnel_failover_ip: 169.254.56.29
        cloud_vpn_responder_provider: aws_vpn
        cloud_vpn_responder_public_ip: 18.191.132.220
        cloud_vpn_responder_failover_ip: 18.191.132.221
        cloud_vpn_responder_tunnel_ip: 169.254.56.26
        cloud_vpn_responder_tunnel_failover_ip: 169.254.56.30
```

## Notes
None
