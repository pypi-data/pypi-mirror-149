from abc import ABC

import stevedore
import stevedore.exception


class ExtensionError(Exception):
    pass

    
def on_load_failure(manager, entrypoint, exception):
    raise LoadFailure(manager, entrypoint, exception)
    
    
class LoadFailure(Exception):
    
    def __init__(self, manager, entrypoint, exception):
        self.manager = manager
        self.entrypoint = entrypoint
        self.__cause__ = exception
        super().__init__(f"{type(manager).__name__} failed to load entrypoint {entrypoint}")
        

def create_extension(kind, namespace, name, exception_type, *args, **kwargs):
    try:
        manager = stevedore.driver.DriverManager(
            namespace=namespace,
            name=name,
            invoke_on_load=True,
            invoke_args=args,
            invoke_kwds={**kwargs, "name": name},
            on_load_failure_callback=on_load_failure,
        )
    except stevedore.exception.NoMatches as no_matches:
        names = list_extensions(namespace)
        name_list = ", ".join(names)
        raise exception_type(
            f"No {kind} matching {name !r}. Available {kind}s: {name_list}") from no_matches
    driver = manager.driver
    return driver


def list_extensions(namespace):
    """List the names of the extensions available in a given namespace.
    """
    extensions = stevedore.ExtensionManager(
        namespace=namespace,
        invoke_on_load=False,
        on_load_failure_callback=on_load_failure,
    )
    return extensions.names()


class Extension(ABC):

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name
