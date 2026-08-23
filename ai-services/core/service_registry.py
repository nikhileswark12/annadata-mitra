class ServiceRegistry:
    def __init__(self):
        self._services = {}

    def register(self, name, service_instance):
        if hasattr(service_instance, 'initialize'):
            service_instance.initialize()
            if getattr(service_instance, '_fallback_active', False):
                raise Exception(f"Service {name} failed to load model and fell back.")
        self._services[name] = service_instance

    def get(self, name):
        if name not in self._services:
            raise ValueError(f"Service {name} not found in registry")
        return self._services[name]

registry = ServiceRegistry()
