class Scope:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._services = {}
        return cls._instance

    def register(self, interface, instance):
        self._services[interface] = instance

    def resolve(self, interface):
        return self._services[interface]


application_scope = Scope()
