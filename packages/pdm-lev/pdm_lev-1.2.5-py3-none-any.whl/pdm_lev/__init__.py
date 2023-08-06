from .command import Command

def lev_plugin(core):
    core.register_command(Command, "lev")
