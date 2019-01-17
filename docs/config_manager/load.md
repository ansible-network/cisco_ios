# Load configuration onto device
The `config_manager/load` function will take a Cisco IOS configuration file and load it
onto the device.  This function supports either merging the configuration with
the current active configuration or replacing the current active configuration
with the provided configuration file.  

The `config_manager/load` function will return the full configuration diff in the
`ios_diff` fact.

NOTE: When performing a configuration replace function be sure to specify the
entire configuration to be loaded otherwise you could end up not being able to
reconnect to your IOS device after the configuration has been loaded.

## How to load and merge a configuration
Loading and merging a configuration file is the default operation for the
`config_manager/load` function.  It will take the contents of a Cisco IOS configuration
file and merge it with the current device active configurations.

Below is an example of calling the `config_manager/load` function from the playbook.

```
- hosts: cisco_ios

  roles:
    - name ansible_network.cisco_ios
      function: config_manager/load
      config_manager_text: "{{ lookup('file', 'ios.cfg') }}"
```

The above playbook will load the specified configuration file onto each device
in the `cisco_ios` host group.

## How to replace the current active configuration
The `config_manager/load` function also supports replacing the current active
configuration with the configuration file located on the Ansible controller.
In order to replace the device's active configuration, set the value of the
`config_manager_replace` setting to `True`.

```
- hosts: cisco_ios

  roles:
    - name ansible_network.cisco_ios
      function: config_manager/load
      config_manager_text: "{{ lookup('file', 'ios.cfg') }}"
      config_manager_replace: true
```


## Arguments

### config_manager_text

This value accepts the text form of the configuration to be loaded on to the remote device. 
The configuration file should be the native set of commands used to configure the remote device.

The default value is `null`

### config_manager_replace

Specifies whether or not the source configuration should replace the current
active configuration on the target IOS device.  When this value is set to
False, the source configuration is merged with the active configuration.  When
this value is set to True, the source configuration will replace the current
active configuration

The default value is `False`

### ios_config_remove_temp_files

Configures the function to remove or not remove the temp files created when
preparing to load the configuration file.  There are two locations for temp
files, one on the Ansible controller and one on the device.  This argument
accepts a boolean value.

The default value is `True`

### ios_config_rollback_enabled

Configures whether or not automatic rollback is enabled during the execution of
the function.  When enabled, if an error is enountered, then the configuration
is automatically returned to the original running-config.  If disabled, then
the rollback operation is not performed automatically.

The default value is `True`

