import importlib.util
import os.path
import logging


def get_package_path(package_name):
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        logging.error("Package not found")
        return "Package not found"
    else:
        logging.warning(package_name.__doc__)
        logging.info(os.path.dirname(spec.origin))
        return f"The {package_name} package is located at {os.path.dirname(spec.origin)}"


if __name__ == "__main__":
    print(get_package_path('my_HWs_for_py_123'))
    print(get_package_path("unexisted_package"))
