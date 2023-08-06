import logging
import os
import re
import sys
from typing import List

import dns.exception
import dns.resolver
import getconf
if sys.version_info.major == 2:
    from srvlookup import _build_result_set
else:
    from srvlookup.main import _build_result_set

# The available formats for returning service host and port settings. See the
# find_service method below.
FORMAT_LIST_OF_STRING = 0
FORMAT_LIST_OF_TUPLE = 1
FORMAT_STRING = 2

# Remove annoying ERROR log messages from srvlookup module since we expect calls
# to fail sometimes and we catch exceptions.
logging.getLogger('srvlookup').setLevel(logging.FATAL)
logger = logging.getLogger(__name__)


class ServiceConfig(object):
    def __init__(self, env_namespace=None, ini_files=None, defaults=None, default_disable_srv_lookup=False):
        """
        Manage service configuration using environment variables, config files and defaults. Also
        provide methods for doing service discovery.
        Configuration order of precedence:
          * environment variables, then
          * config files, then
          * defaults.
        Args:
            env_namespace (str or None): The prefix to use when looking up configuration settings in
                environment variables. For example, if the namespace is 'my_service' and you request
                the value of 'section.field', the environment variable 'MY_SERVICE_SECTION_FIELD'
                will be looked up. If None (the default), no prefix is used.
            ini_files (list of str): The configuration files, in .ini format, to read.
            defaults (dict): Default configuration values. The dict maps section names, to dicts
                mapping field names to values, for example: {'section': {'field': 'value'}}. All
                keys and values must be strings.
            default_disable_srv_lookup (Bool): default behaviour of find_service()
        """
        if env_namespace is None:
            env_namespace = getconf.NO_NAMESPACE
        if ini_files is not None and not isinstance(ini_files, list):
            ini_files = [ini_files]
        self.env_namespace = env_namespace
        self.ini_files = ini_files if ini_files is not None else []
        # Map all strings to unicode since getconf has an issue that breaks its getlist() method
        # on a str rather than unicode value.
        self.defaults = self._normalise_defaults_dict(defaults)
        self.default_disable_srv_lookup = default_disable_srv_lookup
        self._load_config()

    def reload(self, **kwargs):
        """
        Change the environment namespace, config files or defaults. This method has the same
        arguments as __init__().
        """
        if 'env_namespace' in kwargs:
            env_namespace = kwargs['env_namespace']
            if env_namespace is None:
                env_namespace = getconf.NO_NAMESPACE
            self.env_namespace = env_namespace
        if 'ini_files' in kwargs:
            ini_files = kwargs['ini_files']
            if not isinstance(ini_files, list):
                ini_files = [ini_files]
            self.ini_files = ini_files
        if 'defaults' in kwargs:
            self.defaults = self._normalise_defaults_dict(kwargs['defaults'])
        self._load_config()

    def _normalise_defaults_dict(self, defaults):
        """
        typecast config into unicode strings
        """
        if defaults is None:
            defaults = {}
        if sys.version_info.major == 3:
            return {
                str(section_name): {
                    str(field): str(value)
                    for field, value in section_dict.items()}
                for section_name, section_dict in defaults.items()}
        return {
            unicode(section_name): {
                unicode(field): unicode(value)
                for field, value in section_dict.items()}
            for section_name, section_dict in defaults.items()}

    def _load_config(self):
        for ini_file in self.ini_files:
            if (ini_file is not None) and (not os.path.exists(ini_file)):
                logger.warning('ini-file does not exist: %s', ini_file)
        self._config = getconf.ConfigGetter(
            self.env_namespace,
            config_files=self.ini_files,
            defaults=self.defaults)
        self._service_cache = {}  # {key: (expiry_time, [(host, port), ...])}

    def _get_section_setting(self, key):
        """
        Map all preceding dots to underscores, except for the last dot.
        This assumes all .ini section nesting is at most one level
        """
        key_split = re.split('\.|\-', key)
        if len(key_split) > 1:
            setting = key_split.pop(-1)
            setting_prefix = "_".join(key_split)
            key = "{}.{}".format(setting_prefix, setting)
        return key

    def _flatten_service_key(self, service_key):
        """
        Map all dots and hyphens in service key to underscores
        """
        return re.sub('[.-]', '_', service_key)

    def _get(self, key, method):
        key = self._get_section_setting(key)
        return getattr(self._config, method)(key)

    def get(self, key):
        """
        Read a configuration setting and return the value as a string.
        Args:
            key (str): The key of the value to look up, in the format 'section.field'. This will
                look for the environment variable PREFIX_SECTION_FIELD, and if not found, the
                section and field in all config files specified in the constructor, and if not found
                the value in defaults['section']['value'].
        """
        return str(self._get(key, 'getstr'))

    get_str = get

    def get_list(self, key):
        """
        Read a configuration setting and return the value as a list of strings.
        This will split on ','.
        """
        return self._get(key, 'getlist')

    def get_bool(self, key):
        """
        Read a configuration setting and return the value as a boolean.
        """
        return self._get(key, 'getbool')

    def get_int(self, key):
        """
        Read a configuration setting and return the value as an integer.
        """
        return self._get(key, 'getint')

    def get_float(self, key):
        """
        Read a configuration setting and return the value as a float.
        """
        return self._get(key, 'getfloat')

    def get_section(self, section_name):
        """
        Return a dict-like object that can be used to query all fields in the given section.
        """
        return self._get(section_name, 'get_section')

    @staticmethod
    def _srv_to_host_port(service_key, prefix, protocol, use_tcp):
        """
        A wrapper around SRV lookups to return a list of (host, port) tuples.
        Some clients support delimited strings, lists, or only single host:port combinations, so we
        just send a list back for the configuration below to specify what it needs.
        Args:
            service_key (str): The service name key to look up.
            use_tcp (boolean): Uses TCP instead of UDP to do DNS lookups.
        Returns: (list of (str, int)): The list of (host, port) records.
        """
        srv_records = []
        try:
            records_lookup = dns.resolver.query('_%s._%s.%s' % (prefix, protocol, service_key), 'SRV', tcp=use_tcp)
            srv_collection = srvlookup._build_result_set(records_lookup)
            srv_records = [(srv.host, srv.port) for srv in srv_collection]
        except dns.resolver.NXDOMAIN as e:
            # Exception will look like
            # None of DNS query names exist: _http._tcp.kafka.,
            # _http._tcp.kafka.hq.takealot.com., _http._tcp.kafka.stagealot.com.
            logger.info(e)
            # So fall back to non-prefixed keys
            try:
                records_lookup = dns.resolver.query(service_key, 'SRV', tcp=use_tcp)
                srv_collection = srvlookup._build_result_set(records_lookup)
                srv_records = [(srv.host, srv.port) for srv in srv_collection]
            except Exception as e:
                logger.info('failed to resolve service; query=%s, message=%s', service_key, e)
        except Exception as e:
            # No SRV DNS entries were found, most likely due to the service being queried is not
            # currently pushing SRV records to SkyDNS
            logger.info('failed to resolve service; query=%s, message=%s', service_key, e)
        return srv_records

    @classmethod
    def _srv_to_host_port_with_domains(cls, service_key, prefix, protocol, use_tcp):
        """
        A wrapper around SRV lookups to return a list of (host, port) tuples.
        Some clients support delimited strings, lists, or only single host:port combinations, so we
        just send a list back for the configuration below to specify what it needs.
        Args:
            service_key (str): The service name key to look up.
            disable_srv_lookup (bool): Setting to enable or disable dns resolution for
                                       service host and port
            use_tcp (boolean): Uses TCP instead of UDP to do DNS lookups.
        Returns: (list of (str, int)): The list of (host, port) records.
        """
        srv_records = cls._srv_to_host_port(service_key, prefix, protocol, use_tcp)
        if not srv_records:
            search_domains_string = os.getenv("DNS_SEARCH_DOMAINS")
            if search_domains_string:
                search_domains = search_domains_string.split(",")
                for domain in search_domains:
                    fqdn = "{}.{}".format(service_key, domain)
                    srv_records = cls._srv_to_host_port(fqdn, prefix, protocol, use_tcp)
                    if srv_records:
                        break
        return srv_records

    def _config_to_host_port(self, service_key):
        """
        Return a list of (host, port) tuples from the current configuration (which can comprise
        environment variables, ini files and default settings). It basically calls self.get_str()
        with 'service_key.host_port' as argument, which should return a string with the format
        'host1:port1,host2:port2,...', which will be parsed into a list of (host, port) tuples.
        If the 'service_key.host_port' config setting is not found, it will look for
        'service_key.host' and 'service_key.port' separately and return them in a list with exactly
        1 (host, port) tuple.
        The typical use case is initialising a ServiceConfig instance with no namespace and putting
        the service host and port into an environment variable. For example, for the service key
        'kafka', the environment variable could look like this:
            KAFKA_HOST_PORT="kafka01:6667,kafka02:6667,kafka03:6667,kafka04:6667,kafka05:6667"
        Args:
            service_key (str): The environment variable key to look up. The key will always be
                converted to upper case before looking it up in the environment.
        Returns: (list of (str, int)): The list of (host, port) records.
        """
        service_key = self._flatten_service_key(service_key)
        # Try the host_port field first
        value = self.get_str(service_key + '.host_port')

        if value:
            try:
                result = []
                for host_port in value.split(','):
                    host, _, port = host_port.partition(':')
                    port = int(port) if port else None
                    result.append((host.strip(), port))
            except (TypeError, ValueError) as e:
                logger.info('failed to resolve service host and port; message=%s', e)
            else:
                return result

        # host_port not found - try host and port fields separately
        logger.info('failed to resolve environment variable: %s', str(service_key).upper() + "_HOST_PORT")
        host = self.get_str(service_key + '.host')
        if host:
            port = self.get_str(service_key + '.port')
            port = int(port) if port else None
            return [(host, port)]

        logger.info('failed to resolve environment variables: %s, %s', str(service_key).upper() + "_HOST",
                    service_key.upper() + "_PORT")

        # Nothing found
        raise ServiceNotFound('service %r not found' % service_key)

    @staticmethod
    def _format_result(result, format_):
        """
        Format the result
        Args:
        result: list(tuple(str, int)): list of host, port
        format (FORMAT_LIST_OF_STRING or FORMAT_LIST_OF_TUPLE or FORMAT_STRING): In what format
                to return the list of service hosts and ports.
                  * FORMAT_LIST_OF_STRING: Return as a list of 'host:port' strings. This is the default.
                  * FORMAT_LIST_OF_TUPLE: Return as a list of (str, int) tuples containing the host
                    and port number.
                  * FORMAT_STRING: Return as a comma-separated string, 'host1:port1,host2:port2,...'.
        Returns: list of hosts and ports with format depending no the `format` argument.
        """
        if format_ == FORMAT_LIST_OF_TUPLE:
            return result
        result = [host + ('' if port is None else ':' + str(port)) for host, port in result]
        if format_ == FORMAT_LIST_OF_STRING:
            return result
        if format_ == FORMAT_STRING:
            return ','.join(result)
        raise ValueError('Unknown format %r' % format_)

    def find_service(self, service_key, format=FORMAT_LIST_OF_STRING,
                     cache_ttl=30, disable_srv_lookup=None, prefix='http',
                     protocol='tcp', use_tcp=True) -> List[str]:
        """
        Return a list of hosts and ports for the given service key.
        This will first try to look up the SRV record for the service and, failing that, look for
        environment variables matching the service key.
        Args:
            service_key (str): The service to look up.
            disable_srv_lookup (bool): Setting to enable or disable dns resolution for service host and port
            format (FORMAT_LIST_OF_STRING or FORMAT_LIST_OF_TUPLE or FORMAT_STRING): In what format
                to return the list of service hosts and ports.
                  * FORMAT_LIST_OF_STRING: Return as a list of 'host:port' strings. This is the default.
                  * FORMAT_LIST_OF_TUPLE: Return as a list of (str, int) tuples containing the host
                    and port number.
                  * FORMAT_STRING: Return as a comma-separated string, 'host1:port1,host2:port2,...'.
            cache_ttl (int): For how many seconds to cache the result of a service lookup. Default:
                0 (no caching).
            prefix (str): name of the specific port you're looking for
            protocol (str): protocol used on the port
            use_tcp (boolean): Use TCP instead of UDP for lookups
        Returns: list of hosts and ports with format depending no the `format` argument.
        """
        if disable_srv_lookup is None:
            disable_srv_lookup = self.default_disable_srv_lookup

        srv_records = None
        if not disable_srv_lookup:
            srv_records = self._srv_to_host_port_with_domains(service_key, prefix, protocol, use_tcp)
        if not srv_records:
            srv_records = self._config_to_host_port(service_key)
        if not srv_records:
            raise ServiceNotFound('service %r not found' % service_key)

        result = srv_records
        return self._format_result(result, format)


class ServiceNotFound(Exception):
    pass
