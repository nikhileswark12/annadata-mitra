
import importlib
packages = {
  'flask': 'flask', 'flask_cors': 'flask_cors', 'pandas': 'pandas',
  'sklearn': 'scikit-learn', 'numpy': 'numpy', 'joblib': 'joblib',
  'PIL': 'pillow', 'dotenv': 'python-dotenv', 'scipy': 'scipy', 'statsmodels': 'statsmodels'
}
for mod, pkg in packages.items():
    try:
        m = importlib.import_module(mod)
        v = getattr(m, '__version__', 'unknown')
        print(f'OK: {pkg} ({v})')
    except ImportError:
        print(f'MISSING: {pkg}')
