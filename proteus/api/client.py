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

###############################################################################
#
# Additional Copyright and Trademark Information
#
# Proteus (tm) IP Addess Management (IPAM)
# is a product of BLUECAT Networks (tm) and is not OpenSource.
#
###############################################################################

import sys

try:
    from suds.client import Client
    from suds.sudsobject import asdict
except ImportError, e:
    print "You don't have the python suds library installed."
    sys.exit(1)

from proteus.objects import *

TYPE_CONFIGURATION = 'Configuration'
TYPE_VIEW = 'View'
TYPE_ZONE = 'Zone'
TYPE_HOSTRECORD = 'HostRecord'
TYPE_MXRECORD = 'MXRecord'
TYPE_TXTRECORD = 'TXTRecord'
TYPE_CNAMERECORD = 'AliasRecord'
TYPE_HINFORECORD = 'HINFORecord'
TYPE_IP4BLOCK = 'IP4Block'


DNS_ALLTYPES = [
    TYPE_ZONE,
    TYPE_HOSTRECORD,
    TYPE_MXRECORD,
    TYPE_TXTRECORD,
    TYPE_CNAMERECORD,
    TYPE_HINFORECORD
    ]

TYPES = (
    TYPE_CONFIGURATION,
    TYPE_VIEW,
    TYPE_ZONE,
    TYPE_HOSTRECORD,
    TYPE_IP4BLOCK
    )


class ProteusClientApi(object):
    def __init__(self, api_url=None, api_user=None, api_password=None):
        self._api_url = api_url
        self._api_user = api_user
        self._api_password = api_password
        self._client = None
        self._is_connected = None
        self._is_authenticated = None

    def _connect(self):
        if self._client is not None:
            raise Exception('Disconnect first')
        if self._api_url[:-1] != '/':
            self._api_url += '/'
        self._client = Client('%sServices/API?wsdl' % self._api_url)
        self._client.set_options(location='%sServices/API' % self._api_url)
        self._is_connected = True

    def _disconnect(self):
        self._client = None
        self._is_connected = False

    def login(self):
        try:
            self._connect()
            self._client.service.login(self._api_user, self._api_password)
            self._is_authenticated = True
            return True
        except Exception, e:
            print e
            return False

    def logout(self):
        try:
            self._client.service.logout()
            self._is_authenticated = False
            self._disconnect()
            return True
        except Exception, e:
            print e

    def _get_entity_by_name(self, parent_id, entity_name, entity_type):
        if entity_type not in TYPES:
            raise Exception("Unknown Entity Type")
        if self._is_connected:
            try:
                entity = self._client.service.getEntityByName(
                    parent_id,
                    entity_name,
                    entity_type
                )
                return entity
            except Exception, e:
                print e
                return False
        return None

    def _get_entities(self, parent_id, entity_type, start=1, count=1):
        if self._is_connected:
            try:
                entity = self._client.service.getEntities(
                    parent_id,
                    entity_type,
                    start,
                    count
                )
                return entity
            except Exception, e:
                print e
                return False
        return None

    def is_valid_connection(self):
        if self._is_connected and self._is_authenticated:
            return True
        return False


class ProteusClient(ProteusClientApi):
    def __init__(
        self,
        api_url=None,
        api_user=None,
        api_password=None,
        config_name=None):

        super(ProteusClient, self).__init__(api_url, api_user, api_password)
        self._config_name = config_name
        self._configuration = None

    def _get_configuration(self):
        if self.is_valid_connection():
            try:
                # parent_id is 0 for configuratioin objects
                configuration = self._get_entity_by_name(
                    0,
                    self._config_name,
                    TYPE_CONFIGURATION
                )
                self._configuration = APIObject(
                    TypeRecord=asdict(configuration))
                return True
            except Exception, e:
                print e
                return False
        return False

    def get_view(self, view_name):
        if self._configuration is None:
            self._get_configuration()
        if self.is_valid_connection():
            view = self._get_entity_by_name(
                self._configuration.id,
                view_name,
                TYPE_VIEW)
            return APIObject(TypeRecord=asdict(view))
        return None

    def get_views(self):
        if self._configuration is None:
            self._get_configuration()
        if self.is_valid_connection():
            views = self._get_entities(
                self._configuration.id,
                TYPE_VIEW,
                0,
                99999)
            view_arr = []
            for i in views.item:
                view_arr.append(APIObject(TypeRecord=asdict(i)))
            return view_arr
        return None

    def get_zone(self, zone_name=None, view_id=None, view_name=None):
        if self._configuration is None:
            self._get_configuration()
        if self.is_valid_connection():
            if zone_name is not None and zone_name != "":
                if view_id is not None and view_id >= 0:
                    zone = self._get_entity_by_name(
                        view_id,
                        zone_name,
                        TYPE_ZONE)
                    return APIObject(TypeRecord=asdict(zone))
                elif view_id is None \
                    and view_name is not None \
                    and view_name != '':
                    view = self.get_view(view_name)
                    zone = self._get_entity_by_name(
                        view['id'],
                        zone_name,
                        TYPE_ZONE)
                    return APIObject(TypeRecord=asdict(zone))
        return False

    def get_record(
        self,
        hostname,
        zonename,
        view=None,
        view_name=None,
        rec_type=TYPE_HOSTRECORD):
        if self.is_valid_connection():
            if self._configuration is None:
                self._get_configuration()
            if view is not None:
                zone_arr = zonename.split(".")
                count = len(zone_arr)
                parent_id = view.id
            if view_name is not None:
                view_rec = self.get_view(view_name)
                zone_arr = zonename.split('.')
                count = len(zone_arr)
                parent_id = view_rec.id
            for i in reversed(zone_arr):
                print i
                print count
                if count != 0:
                    zone = self.get_zone(i, parent_id)
                    if zone is not None:
                        parent_id = zone.id
                if count == 1:
                    print zone.name
                    record = self._get_entity_by_name(
                        parent_id,
                        hostname,
                        rec_type)
                    if record is not None:
                        return APIObject(TypeRecord=asdict(record))
                    else:
                        return None
                count = count - 1
        return None

    def get_host_record(self, hostname, zonename, view=None, view_name=None):
        return self.get_record(
            hostname,
            zonename,
            view,
            view_name,
            TYPE_HOSTRECORD)

    def get_mx_record(self, hostname, zonename, view=None, view_name=None):
        return self.get_record(
            hostname,
            zonename,
            view,
            view_name,
            TYPE_MXRECORD)

    def get_txt_record(self, hostname, zonename, view=None, view_name=None):
        return self.get_record(
            hostname,
            zonename,
            view,
            view_name,
            TYPE_TXTRECORD)

    def get_cname_record(self, hostname, zonename, view=None, view_name=None):
        return self.get_record(
            hostname,
            zonename,
            view,
            view_name,
            TYPE_CNAMERECORD)

    def get_hinfo_record(self, hostname, zonename, view=None, view_name=None):
        return self.get_record(
            hostname,
            zonename,
            view,
            view_name,
            TYPE_HINFORECORD)

    def get_records_by_parent(self, zone=None, record_type=TYPE_ZONE):
        if self.is_valid_connection():
            if self._configuration is None:
                self._get_configuration()
            if zone is not None:
                print zone
                records = self._get_entities(zone.id, record_type, 0, 9999999)
                rec_list = []
                try:
                    for i in records.item:
                        a = APIObject(TypeRecord=asdict(i))
                        if a is not None:
                            rec_list.append(a)
                    return rec_list
                except AttributeError:
                    pass
        return None

    def get_hosts_by_parent(self, zone=None):
        return self.get_records_by_parent(zone, TYPE_HOSTRECORD)

    def get_zones_by_parent(self, zone=None):
        return self.get_records_by_parent(zone, TYPE_ZONE)

    def get_mxs_by_parent(self, zone=None):
        return self.get_records_by_parent(zone, TYPE_MXRECORD)

    def get_txts_by_parent(self, zone=None):
        return self.get_records_by_parent(zone, TYPE_TXTRECORD)

    def get_cnames_by_parent(self, zone=None):
        return self.get_records_by_parent(zone, TYPE_CNAMERECORD)

    def get_hinfo_by_parent(self, zone=None):
        return self.get_records_by_parent(zone, TYPE_HINFORECORD)

    def get_zone_list(self, zonename, view=None, view_name=None):
        if self._configuration is None:
            self._get_configuration()
        if self.is_valid_connection():
            if view is not None and view_name is None:
                zone_arr = zonename.split('.')
                count = len(zone_arr)
                parent_id = view.id
            if view is None and view_name is not None:
                zone_arr = zonename.split('.')
                count = len(zone_arr)
                view_rec = self.get_view(view_name)
                parent_id = view_rec.id

            for i in reversed(zone_arr):
                print count
                if count != 0:
                    zone = self.get_zone(i, parent_id)
                    if zone is None:
                        return None
                    parent_id = zone.id
                if count == 1:
                    zone_list = []
                    for i in DNS_ALLTYPES:
                        rec_list = []
                        rec_list = self.get_records_by_parent(zone, i)
                        if rec_list is not None:
                            zone_list.extend(rec_list)
                    return zone_list
                count = count - 1
        return None

