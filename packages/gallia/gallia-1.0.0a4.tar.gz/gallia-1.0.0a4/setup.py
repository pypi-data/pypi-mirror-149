# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gallia',
 'gallia.cursed_hr',
 'gallia.db',
 'gallia.services',
 'gallia.transports',
 'gallia.uds',
 'gallia.uds.core',
 'gallia.udscan',
 'gallia.udscan.scanner']

package_data = \
{'': ['*']}

install_requires = \
['aiofiles>=0.8.0,<0.9.0',
 'aiosqlite>=0.17.0,<0.18.0',
 'argcomplete>=2.0.0,<3.0.0',
 'pyopennetzteil>=0.1.2,<0.2.0',
 'pypenlog>=0.3.2,<0.4.0',
 'python-can>=4.0.0,<5.0.0',
 'pyxcp>=0.16.0,<0.17.0',
 'tabulate>=0.8.9,<0.9.0',
 'types-tabulate>=0.8.8,<0.9.0',
 'zstandard>=0.17.0,<0.18.0']

entry_points = \
{'console_scripts': ['cursed-hr = gallia.cursed_hr.cursed_hr:main',
                     'discover-xcp = gallia.udscan.scanner.find_xcp:main',
                     'gallia = gallia.cli:main'],
 'gallia_scanners': ['discover-can-ids = '
                     'gallia.udscan.scanner.find_can_ids:FindCanIDsScanner',
                     'discover-endpoints = '
                     'gallia.udscan.scanner.find_endpoints:FindEndpoints',
                     'discover-iso-tp-addr = '
                     'gallia.udscan.scanner.find_iso_tp_addr:FindISOTPAddrScanner',
                     'scan-dump-seeds = '
                     'gallia.udscan.scanner.scan_sa_dump_seeds:SaDumpSeeds',
                     'scan-identifiers = '
                     'gallia.udscan.scanner.scan_identifiers:ScanIdentifiers',
                     'scan-memory-functions = '
                     'gallia.udscan.scanner.scan_memory_functions:ScanWriteDataByAddress',
                     'scan-reset = gallia.udscan.scanner.scan_reset:ScanReset',
                     'scan-services = '
                     'gallia.udscan.scanner.scan_services:ScanServices',
                     'scan-sessions = '
                     'gallia.udscan.scanner.scan_sessions:IterateSessions',
                     'simple-dtc = gallia.udscan.scanner.simple_dtc:DTCScanner',
                     'simple-ecu-reset = '
                     'gallia.udscan.scanner.simple_ecu_reset:EcuReset',
                     'simple-get-vin = '
                     'gallia.udscan.scanner.simple_get_vin:GetVin',
                     'simple-iocbi = gallia.udscan.scanner.simple_iocbi:IOCBI',
                     'simple-ping = gallia.udscan.scanner.simple_ping:Ping',
                     'simple-read-by-identifier = '
                     'gallia.udscan.scanner.simple_read_by_identifier:ReadByIdentifier',
                     'simple-read-error-log = '
                     'gallia.udscan.scanner.simple_read_error_log:ReadErrorLog',
                     'simple-rmba = '
                     'gallia.udscan.scanner.simple_rmba:ReadMemoryByAddressScanner',
                     'simple-rtcl = gallia.udscan.scanner.simple_rtcl:RTCL',
                     'simple-send-pdu = '
                     'gallia.udscan.scanner.simple_send_pdu:SendPDU',
                     'simple-test-xcp = '
                     'gallia.udscan.scanner.simple_test_xcp:TestXCP',
                     'simple-wmba = '
                     'gallia.udscan.scanner.simple_wmba:WriteMemoryByAddressScanner',
                     'simple-write-by-identifier = '
                     'gallia.udscan.scanner.simple_write_by_identifier:WriteByIdentifier']}

setup_kwargs = {
    'name': 'gallia',
    'version': '1.0.0a4',
    'description': 'Extendable Pentesting Framework',
    'long_description': '# Gallia\n\n## Documentation\n\nhttps://fraunhofer-aisec.github.io/gallia\n',
    'author': 'AISEC Pentesting Team',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Fraunhofer-AISEC/gallia',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
