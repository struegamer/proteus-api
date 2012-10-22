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
except ImportError, e:
    print "You don't have the python suds library installed."
    sys.exit(1)


from constants import *
from proteus.objects import *
from dns import DNS


class ProteusClientApi(object):
    """ Low Level Proteus SOAP Wrapper Class"""
    def __init__(self, api_url=None, api_user=None, api_password=None):
        """Constructor

        :Parameters:
            - `api_url` : string
            - `api_user` : string
            - `api_password` : string

        Example:
            >>> from proteus.api import ProteusClientApi
            >>> pc=ProteusClientApi(
                'http://proteus.domain.tld/',
                'username',
                'password')
        """
        self._api_url = api_url
        self._api_user = api_user
        self._api_password = api_password
        self._client = None
        self._is_connected = None
        self._is_authenticated = None

    def _connect(self):
        """
        Establish connection to Proteus SOAP Service
        """
        if self._client is not None:
            raise Exception('Disconnect first')
        if self._api_url[-1] != '/':
            self._api_url += '/'
        self._client = Client('%sServices/API?wsdl' % self._api_url)
        self._client.set_options(location='%sServices/API' % self._api_url)
        self._is_connected = True

    def _disconnect(self):
        """
        Disconnect from Proteus SOAP Service
        """
        self._client = None
        self._is_connected = False

    def login(self):
        """
        Connect and login

        Example:
            >>> from proteus.api import ProteusClientApi
            >>> pc=ProteusClientApi(
                'http://proteus.domain.tld/',
                'username',
                'password')
            >>> pc.login()
        """
        try:
            self._connect()
            self._client.service.login(self._api_user, self._api_password)
            self._is_authenticated = True
            return True
        except Exception, e:
            print e
            return False

    def logout(self):
        """
        Logout and disconnect

        Example:
            >>> from proteus.api import ProteusClientApi
            >>> pc=ProteusClientApi(
                'http://proteus.domain.tld/',
                'username',
                'password')
            >>> pc.login()
            >>> ...
            >>> pc.logout()
        """
        try:
            self._client.service.logout()
            self._is_authenticated = False
            self._disconnect()
            return True
        except Exception, e:
            print e

    def _get_entity_by_name(self, parent_id, entity_name, entity_type):
        """
        Wrapper for Proteus SOAP API Method getEntityByName

        :Parameters:
            - `parent_id` : int
            - `entity_name` : string
            - `entity_type` : string [ use one of the TYPE_* constants from :py:mod:`proteus.api.constants` ]

        :return:
            APIEntity

        """
        if entity_type not in ALL_TYPES:
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
        """
        Get a list of Proteus Entities

        :Parameters:
            - `parent_id` : int
            - `entity_type` : string [ use one of the TYPE_* constants from :py:mod:`proteus.api.constants` ]
            - `start` : int [1-based]
            - `count` : int

        :return:
            `APIEntityArray`
        """
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
        """
        Checks if the client is connected and authenticated
        """
        if self._is_connected and self._is_authenticated:
            return True
        return False


class ProteusClient(ProteusClientApi):
    """
    Usable Proteus Client
    """
    def __init__(
        self,
        api_url=None,
        api_user=None,
        api_password=None,
        config_name=None):
        """
        :Parameters:
            - `api_url` : string
            - `api_user` : string
            - `api_password` : string
            - `config_name` : string

        Example:
            >>> from proteus.api import ProteusClientApi
            >>> pc=ProteusClientApi(
                'http://proteus.domain.tld/',
                'username',
                'password',
                'proteus_configuration_object_name')

        """
        super(ProteusClient, self).__init__(api_url, api_user, api_password)
        self._config_name = config_name
        self._configuration = None
        self._get_configuration()
        self._dns = DNS(self)

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
                    TypeRecord=configuration, client=self._client)
                return True
            except Exception, e:
                print e
                return False
        return False

    def get_dns(self):
        return self._dns
    DNS = property(get_dns, doc='DNS Class Property')

    def get_configuration(self):
        if self._configuration is None:
            self._get_configuration()
        return self._configuration
    Configuration = property(get_configuration, doc='Configuration Property')

