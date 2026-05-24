# Structure for the commands

commands
 |
 |- bunny_root.py
 |- command_group
        |
        |
        |- [group_name]_group.py
        |- command_name_1.py
        |- command_name_2
                |
                |-command_name_2.py
                |-utils
                    |-function1.py
                    |-function2.py

## explanation

the bunny root is the system which register all commands. Its role is to give a prefix to all commands in the form `/lapin group command`
each group of commands has its own directory. The base commands, which requires no permissions, have no specified group (`/lapin help`)

groups are used to group (duh) commands logically, and they will share permissions, for now we have four groups:

`admin` : some small administrative tasks might be performed at one point here.
`sudo` : commands which should only ever be in hand of the server admins on nobody else
`tournament`: commands to handle tournaments
`weekly`: commands to handle weekly races

In a group, directory, there is:

`{group_name}_group.py` file which register all commands from the group.

for example:

```python

import stuff

example = app_commands.Group(
name="example", description="example of group")

@example.command(name="thing")
@requires_group(group="example")
async def do_a_thing_with_a_json_file(interaction: discord.Interaction,
                                      json_config: discord.Attachment):
    await do_a_thing(interaction, json_config)
```
if a command is simple enough, we can have it sit in its own file (for example, the help which contains two formatting methods and one `send message` call)
`help_command.py`

if a command is complex, we should have a directory which will contains the different parts in various files. This will allow us to generalize ui and functions in the long run.
