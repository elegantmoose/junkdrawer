"""
Example plugin module. For whatever operation or function required modularity,
create a module for it filled with the varying functions for it. For example,
if creating a readers module, may have a reader function for all different
file formats (csv, JSON). We then register all the functions with a global dict,
that they can be accessed during runtime to access each of the plugins from a single,
uniform function that carries out the plugin operation.
"""

# At runtime this dict will be filled with all the plugins defined
_PLUGINS = dict()


def register(plugin):
    """decorator that acts as a registration function, adding the 
    supplied plugin to the global map of them"""
    _PLUGINS[plugin.__name__] = plugin
    return plugin


def plugin_operation(plugin, *args, **kwargs):
    """this is the external function/interface that is used. It has access to all defined
    plugins and will call the specified plugin accordingly
    
    Args:
        plugin (string): which plugin to call
    """
    if plugin in _PLUGINS:
        return _PLUGINS[plugin](*args, *kwargs)
    else:
        raise TypeError(f"{plugin} plugin not found.")


@register
def plugin1(*args, **kwargs):
    # carry out specific implementation and operation of the plugin
    return


@register
def plugin2(*args, **kwargs):
    # carry out specific implementation and operation of the plugin
    return


@register
def pluginN(*args, **kwargs):
    # carry out specific implementation and operation of the plugin
    return