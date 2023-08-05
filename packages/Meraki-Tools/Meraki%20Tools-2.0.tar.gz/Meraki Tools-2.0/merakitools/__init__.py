from pkg_resources import get_distribution

release = get_distribution('Meraki_Tools').version
__version__ = '.'.join(release.split('.')[:3])