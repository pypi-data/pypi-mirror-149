import importlib.util
import os.path
import logging


def get_package_path(package_name):
    spec = importlib.util.find_spec(package_name)
    if spec is None:
        logging.error("Package not found")
        return "Package not found"
    else:
        pac = __import__(package_name)
        doc = pac.__doc__
        logging.warning(doc if doc is not None else "Package doesn't have documentation")

        logging.info(os.path.dirname(pac.__file__))
        return f"The {package_name} package is located at {pac.__file__}"


if __name__ == "__main__":
    # print(get_package_path('os'))
    print(get_package_path('my_HWs_for_py_123'))
    # print(get_package_path("unexisted_package"))
