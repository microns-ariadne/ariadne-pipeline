from cliff import commandmanager

class CommandManager(commandmanager.CommandManager):
    def __init__(self, namespace, convert_underscores=True):
        self.group_list = []
        super(CommandManager, self).__init__(namespace, convert_underscores)

    def load_commands(self, namespace):
        self.group_list.append(namespace)
        return super(CommandManager, self).load_commands(namespace)

    def add_command_group(self, group=None):
        """Adds another group of command entrypoints"""
        if group:
            self.load_commands(group)

    def get_command_groups(self):
        """Returns a list of the loaded command groups"""
        return self.group_list

    def get_command_names(self, group=None):
        """Returns a list of commands loaded for the specified group"""
        group_list = []
        if group is not None:
            for ep in pkg_resources.iter_entry_points(group):
                cmd_name = (
                    ep.name.replace('_', ' ')
                    if self.convert_underscores
                    else ep.name
                )
                group_list.append(cmd_name)
            return group_list
        return list(self.commands.keys())
