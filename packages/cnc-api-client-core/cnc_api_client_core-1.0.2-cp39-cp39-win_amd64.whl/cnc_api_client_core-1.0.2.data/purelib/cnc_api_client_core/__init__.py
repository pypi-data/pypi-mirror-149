import sys, os, sys, platform
from os import environ
import importlib, importlib.machinery, importlib.util

class PyVerNotSupported(Exception):
  pass

def findmodule():
  pyver = f"{sys.version_info.major}.{sys.version_info.minor}"
  ossys = platform.system()
  libdir = None

  if not (pyver in ["3.9", "3.10"]): 
    raise PyVerNotSupported(f"cnc_api_client_core doesn't support Python{pyver}.")

  if ossys == "Windows":
    if (sys.maxsize > 2**32):
      #Win x64
      libdir = "Win64"

  if libdir:
    sdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), libdir)
    if not os.path.exists(sdir):
      raise ValueError("cnc_api_client_core module not found. Try to reinstall the cnc_api_client_core package or check for support compatibility.")
    for fname in os.listdir(sdir):
      if 'cnc_api_client_core' in fname:
        return os.path.join(sdir, os.path.basename(fname))
    raise ValueError("cnc_api_client_core module not found. Try to reinstall the cnc_api_client_core package.")
  else:
    raise ValueError("Unsupported platform.")

def new_import():
    modulefullpath = findmodule()
    loader = importlib.machinery.ExtensionFileLoader("cnc_api_client_core", modulefullpath)
    spec = importlib.util.spec_from_file_location("cnc_api_client_core", modulefullpath,
        loader=loader, submodule_search_locations=None)
    ld = loader.create_module(spec)
    package = importlib.util.module_from_spec(spec)
    sys.modules["cnc_api_client_core"] = package
    spec.loader.exec_module(package)
    return package

# import the shared lib
package = new_import()