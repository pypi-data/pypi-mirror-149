import pkg_resources


def get_sphinx_terminhtml_version() -> str:
    try:
        return pkg_resources.get_distribution("sphinx_terminhtml").version
    except pkg_resources.DistributionNotFound:
        return "unknown"
