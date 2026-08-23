import json
import os
import logging

class KnowledgeLoader:
    def __init__(self):
        self.base_dir = os.path.join(os.path.dirname(__file__), '../knowledge')
        self._cache = {}

    def load(self, domain, resource):
        """Loads a specific JSON resource from a domain."""
        cache_key = f"{domain}/{resource}"
        if cache_key in self._cache:
            return self._cache[cache_key]

        file_path = os.path.join(self.base_dir, domain, f"{resource}.json")
        if not os.path.exists(file_path):
            logging.error(f"Knowledge resource not found: {file_path}")
            return None

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._cache[cache_key] = data
                return data
        except Exception as e:
            logging.error(f"Error loading knowledge resource {file_path}: {e}")
            return None

    def cache(self):
        """Pre-loads all JSON resources into memory."""
        self._cache.clear()
        if not os.path.exists(self.base_dir): return
        for domain in os.listdir(self.base_dir):
            domain_path = os.path.join(self.base_dir, domain)
            if os.path.isdir(domain_path):
                for file in os.listdir(domain_path):
                    if file.endswith('.json'):
                        resource = file[:-5]
                        self.load(domain, resource)

    def reload(self):
        """Clears the cache and reloads."""
        self.cache()

    def exists(self, domain, resource):
        """Checks if a knowledge resource exists."""
        return os.path.exists(os.path.join(self.base_dir, domain, f"{resource}.json"))

    def list_resources(self, domain):
        """Returns all available resources for a domain."""
        domain_path = os.path.join(self.base_dir, domain)
        if not os.path.isdir(domain_path):
            return []
        return [f[:-5] for f in os.listdir(domain_path) if f.endswith('.json')]

knowledge_loader = KnowledgeLoader()
