"""
Plugin Modules

Created this pattern independently but then there was a great PyCon 2019 talk about it
that is great for presenting to new audience (Geir Arne Hjelle: Adding Flexibility to Your Apps -
https://www.youtube.com/watch?v=98s9YfoXB68)
"""

import plugin_module


def plugin_module_operation(*args, **kwargs):
    """call plugin operation"""
    # any preprocessing and logic, for instance to determine which plugin to use
    plugin = "plugin1"
    return plugin_module.plugin_operation(plugin, *args, **kwargs)


def main():
   plugin_module_operation(args)


if __name__ == "__main__":
    main()