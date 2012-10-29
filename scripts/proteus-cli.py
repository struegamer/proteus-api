#!/usr/bin/python
# -*- coding: utf-8 -*-
###############################################################################
# python-proteus - Proteus IPAM Python Library
# Copyright (C) 2012 Stephan Adig <sh@sourcecode.de>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
###############################################################################

import sys
import os
import os.path
import argparse

try:
    from yaml import load
except ImportError, e:
    print('You are missing PyYaml')
    sys.exit(1)

DEFAULT_CONFIG_FILE = '~/.proteus/config.yaml'

try:
    from proteus.api import ProteusClient
    from proteus.api import constants
    from proteus import HostRecord
except ImportError, e:
    print e
    sys.exit(1)

def prepare_parser(parser=None):
    if parser is None:
        parser = argparse.ArgumentParser(prog='proteus-cli')
    parser.add_argument('-C', '--config-file', default=DEFAULT_CONFIG_FILE,
                        action='store', metavar='FILENAME', dest='configfile',
                        help='Proteus CLI Config Filename')
    parser.add_argument('-I', '--instance', default=None, action='store',
                        metavar='INSTANCE-NAME', dest='instance',
                        help='Proteus Instance Name', required=True)
    parser.add_argument('-c', '--proteus-config', action='store',
                        metavar='CONFIGNAME', dest='proteus_config_name',
                        help='Proteus Configuration Object', required=True)
    parser.add_argument('-F', '--format', action='store',
                        metavar='[pretty,json]', choices=['pretty', 'json'],
                        default='pretty', dest='output_format',
                        help='Output Format')
    subparser = parser.add_subparsers(help='Proteus Resource Commands',
                                      dest='resource_cmd')
    prepare_parser_dns(subparser)

def prepare_parser_dns(subparser=None):
    if subparser is None:
        return False
    parser = subparser.add_parser('dns', help='Proteus DNS Commands')
    parser.add_argument('-v', '--view', action='store', default=None,
                        metavar='VIEWNAME', dest='proteus_view_name',
                        help='Viewname', required=True)
    parser.add_argument('-l', '--list-zone', action='store',
                        default=None,
                        metavar='ZONENAME', dest='proteus_list_zonename',
                        help='Zonename i.e. sub.domain.tld')
    parser.add_argument('-t', '--record-type', default=constants.DNS_ALLTYPES,
                        action='store', metavar='RECORD_TYPE',
                        dest='proteus_record_type', help='Record Type')


def load_config(filename=None):
    if filename is None or filename == '':
        return None
    configfile = file(os.path.expanduser(filename), 'rb')
    config = load(configfile)
    return config

def _init_proteus(args=None):
    if args is None:
        return None
    config = None
    proteus_config = None
    if args.configfile is not None and args.configfile != '':
        config = load_config(args.configfile)
    if args.instance is not None and args.instance != '':
        proteus_config = config['proteus'].get(args.instance, None)
        if args.proteus_config_name is not None and args.proteus_config_name != '':
            proteus_config_index = proteus_config['configs'].index(args.proteus_config_name)
            proteus_client = ProteusClient(proteus_config['url'],
                                           proteus_config['username'],
                                           proteus_config['password'],
                                           proteus_config['configs'][proteus_config_index])
            return proteus_client
    return None

def process_dns_commands(client=None, args=None):
    if client is None or args is None:
        return None
    if args.proteus_list_zonename is not None:
        rec_type = args.proteus_record_type
        viewname = args.proteus_view_name
        if viewname is not None:
            client.login()
            zonelist = client.DNS.get_zone_list(args.proteus_list_zonename,
                                                        view_name=viewname,
                                                        rec_type=eval('constants.{0}'.format(rec_type)))
            client.logout()
            if args.output_format == 'pretty':
                print('No.        | Hostname                                 | Zonename')
                print('-----------+------------------------------------------+------------------------------')
                print('1234567890 + 1234567890123456789012345678901234567890 | ')
                counter = 0
                for zone in zonelist:
                    counter += 1
                    if isinstance(zone, HostRecord):
                        print('{0:10d} | {1:>40s} | '.format(counter, zone.name, args.proteus_list_zonename))
                print('-------------------------------------------------------------------------------------')
                print('Number of Records: {0:10d}'.format(counter))

def do_process(args=None):
    if args is None:
        return False
    proteus_client = _init_proteus(args)
    if proteus_client is not None:
        if args.resource_cmd == 'dns':
            process_dns_commands(proteus_client, args)
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='proteus-cli')
    prepare_parser(parser)

    args = parser.parse_args()
    result = do_process(args)

