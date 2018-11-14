# Get facts from device

The `get_facts` function can be used to collect facts from an Cisco IOS
devices.  This function is only supported over `network_cli` connection
type and requires the `ansible_network_os` value set to `ios`.

## How to get facts from the device

To collect facts from the device, simply include this function in the playbook
using either the `roles` directive or the `tasks` directive.  If no other
options are provided, then all of the available facts will be collected for the
device.

Below is an example of how to use the `roles` directive to collect all facts
from the IOS device.

```
- hosts: cisco_ios

  roles:
    - name ansible-network.cisco_ios
      function: get_facts
```

The above playbook will return the facts for the host under the `cisco_ios`
top level key.  

### Filter the subset of facts returned

By default all available facts will be returned by the `get_facts` function.
If you only want to return a subset of the facts, you can specify the `subset`
variable as a list of keys to return. 

For instance, the below will return only `interfaces` and `system` facts.

```
- hosts: cisco_ios

  roles:
    - name ansible-network.cisco_ios
      function: get_facts
      subset: 
        - system
```

### Implement using tasks

The `get_facts` function can also be implemented using the `tasks` directive
instead of the `roles` directive.  By using the `tasks` directive, you can
control when the fact collection is run. 

Below is an example of how to use the `get_facts` function with `tasks`.

```
- hosts: cisco_ios

  tasks:
    - name: collect facts from cisco ios devices
      import_role:
        name: ansible-network.cisco_ios
        tasks_from: get_facts
      vars:
        subset:
          - system
          - interfaces
```

## Adding new parsers

Over time new parsers can be added (or updated) to the role to add additional
or enhanced functionality.  To add or update parsers perform the following
steps:

* Add (or update) command parser located ino `parse_templates/cli`

* Update the `vars/get_facts_command_map.yaml` file to map the CLI command 
to the parser

The `get_facts_command_map.yaml` file provides a mapping between CLI command 
and parser used to transform the output into Ansible facts. 

### Understanding the mapping file

The command map file provides the mapping between show command and parser file.
The format of the file is a list of objects.  Each object supports a set of
keys that can be configured to provide granular control over how each command
is implemented.

Command map entries support the following keys:

#### command

The `command` key is required and specifies the actual CLI command to execute
on the target device.  The output from the command is then passed to the parser
for further processing.

#### parser

The `parser` key provides the name of the parser used to accept the output from
the command.  The parser value shoule be the command parser filename either
relative to `parser_templates/cli` or absolute path.  This value is required.

#### engine

This key accepts one of two values, either `command_parser` or `textfsm_parser`. 
This value instructs the the parsing function as to which parsing engine to 
use to parse the output from the CLI command.

This key is not required and, if not provided, the engine will assumed to be
`command_parser`

#### groups

Commands can be contained in one (or more) groups to make it easy for playbook
designers to filter specific facts to retreive from the network device.  The
`groups` key must be a list and contain the groups the this command should be
associated with.

#### pre_hook

The `pre_hook` key provides the path to the set of tasks to include prior
to running the command on the CLI.  This is useful if there is a need to check
if a command is available or supported on a particular version.

#### post_hook

The `post_hook` key provides the path to the set of tasks to include after the
command has been run on the target device and its results have been parsed by
the parser. 

## Arguments

### ios_get_facts_subset 

Defines the subset of facts to collection when the `get_facts` function is
called.  This value must be a list value and contain only the sub keys for the
facts you wish to return.

The default value is `default`

#### Aliases

* subset

#### Current supported values for subset are

* default
* all
* interfaces
* bgp
* lldp

### ios_get_facts_command_map

Defines the command / parser mapping file to use when the call to `get_facts`
is made by the playbook.  Normally this value does not need to be modified but
can be used to pass a custom command map to the function.

The default value is `vars/get_facts_command_map.yaml`


## Notes

None


