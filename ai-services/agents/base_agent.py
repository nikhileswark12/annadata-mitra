from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

class BaseAgent(ABC):
    """
    All Annadata Mitra agents extend this class.
    Enforces a consistent interface: validate → process → format_response.
    When a trained model is available, override process() only.
    The validate() and format_response() methods stay the same.
    """

    def __init__(self, name: str):
        self.name = name
        self.model_loaded = False
        logger.info(f"Agent '{name}' initialised (rule-based mode)")

    def run(self, input_data: dict) -> dict:
        """Main entry point called by Flask routes."""
        errors = self.validate(input_data)
        if errors:
            return {
                'status': 'error',
                'message': f'Validation failed: {"; ".join(errors)}',
                'data': None
            }
        try:
            result = self.process(input_data)
            return {
                'status': 'success',
                'message': f'{self.name} completed successfully',
                'data': result,
                'model_type': 'ml-model' if self.model_loaded else 'rule-based'
            }
        except Exception as e:
            logger.error(f"[{self.name}] Error: {e}", exc_info=True)
            return {
                'status': 'error',
                'message': f'{self.name} failed: {str(e)}',
                'data': None
            }

    @abstractmethod
    def validate(self, input_data: dict) -> list:
        """Return list of error strings. Empty list = valid."""
        pass

    @abstractmethod
    def process(self, input_data: dict) -> dict:
        """Core logic. Returns the data payload dict."""
        pass

    def try_load_model(self, model_path: str) -> bool:
        """
        Attempt to load a trained model. Returns True if loaded.
        Called at startup — if file doesn't exist, agent stays rule-based.
        Subclasses override this to load their specific model format.
        """
        import os
        if os.path.exists(model_path):
            try:
                self._load_model_file(model_path)
                self.model_loaded = True
                logger.info(f"[{self.name}] ML model loaded from {model_path}")
                return True
            except Exception as e:
                logger.warning(f"[{self.name}] Model load failed: {e} — staying rule-based")
        return False

    def _load_model_file(self, path: str):
        """Override in subclasses to load the specific model format."""
        pass
