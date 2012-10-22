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

from constants import *
from proteus.objects import *

try:
    from suds.sudsobject import asdict
except ImportError, e:
    print "You don't have the python suds library installed."
    sys.exit(1)


class DNS(object):
    """Proteus DNS Management Class"""

    def __init__(self, proteus_client=None):
        """
        :Parameters:
            - `proteus_client` : instance of :py:class:`proteus.api.client.ProteusClient`

        """
        self._client = proteus_client


    def _get_record(
        self,
        hostname,
        zonename,
        view=None,
        view_name=None,
        rec_type=TYPE_HOSTRECORD):
        """
        Generic method to retrieve the Proteus Resource Records

        :Parameters:
            - `hostname` : string
            - `zonename` : string
            - `view` : :py:class:`proteus.objects.apientity.View`
            - `view_name` : string
            - `rec_type` : string [ should be one of :py:data:`proteus.api.constants.DNS_ALLTYPES` ]


        :returns:
            - Depends on the result of Proteus call but can be one of these:
                - :py:class:`proteus.objects.apientity.HostRecord`
                - :py:class:`proteus.objects.apientity.MXRecord`
                - :py:class:`proteus.objects.apientity.TXTRecord`
                - :py:class:`proteus.objects.apientity.HINFORecord`
                - :py:class:`proteus.objects.apientity.CNAMERecord`
                - :py:class:`proteus.objects.apientity.SRVRecord`

        See: [#private_method]_
        """

        if self._client.is_valid_connection():
            if view is not None:
                zone_arr = zonename.split(".")
                count = len(zone_arr)
                parent_view = view.id
            if view_name is not None:
                view_rec = self.get_view(view_name)
                zone_arr = zonename.split('.')
                count = len(zone_arr)
                parent_view = view_rec
            for i in reversed(zone_arr):
                if count != 0:
                    zone = self.get_zone(i, parent_view)
                    if zone is not None:
                        parent_view = zone
                if count == 1:
                    record = self._client._get_entity_by_name(
                        parent_view.id,
                        hostname,
                        rec_type)
                    if record is not None:
                        return APIObject(TypeRecord=record, client=self._client)
                    else:
                        return None
                count = count - 1
        return None

    def _find_zone(self, zonename, view=None, view_name=None):
        """Find last zone from zonename
        
        :param zonename: Zonename i.e. 'subdomain.domain.tld'
        :type zonename: str
        :param view: View Object (can be None when view_name is not None)
        :type view: :py:class:`proteus.objects.apientity.View` 
        :param view_name: View Name (can be None, when view is not None)
        :type view_name: str
        
        :returns: :py:class:`proteus.objects.apientity.Zone`
        
        See: [#private_method]_         
        """
        if self._client.is_valid_connection():
            if view is not None:
                parent_view = view
            if view_name is not None:
                view_rec = self.get_view(view_name)
                parent_view = view_rec
            if zonename is not None or zonename != '':
                zone_arr = zonename.split('.')
                count = len(zone_arr)
                for i in reversed(zone_arr):
                    if count != 0:
                        zone = self.get_zone(i, view=parent_view)
                        if zone is None:
                            return None
                        parent_view = zone
                    if count == 1:
                        return parent_view
                    count -= 1
        return None

    def _get_records_by_zone(self, zone=None, record_type=TYPE_ZONE):
        """Retrieve a list of Resource Records from Proteus
        
        :param zone: Zone
        :type zone: :py:class:`proteus.objects.apientity.Zone`
        :param record_type: Record type to retreive
        :type record_type: str (use constants from :py:mod:`proteus.api.constants`
        
        :returns: 
            - Depending on the input type it can return:
                - :py:class:`proteus.objects.apientity.HostRecord`
                - :py:class:`proteus.objects.apientity.MXRecord`
                - :py:class:`proteus.objects.apientity.TXTRecord`
                - :py:class:`proteus.objects.apientity.SRVRecord`
                - :py:class:`proteus.objects.apientity.HINFORecord`
            
        """
        if self._client.is_valid_connection():
            if zone is not None:
                records = self._client._get_entities(
                    zone.id,
                    record_type,
                    0,
                    9999999)
                rec_list = []
                try:
                    for i in records.item:
                        a = APIObject(TypeRecord=i, client=self._client)
                        if a is not None:
                            rec_list.append(a)
                    return rec_list
                except AttributeError:
                    pass
        return None

    def get_view(self, view_name):
        """
        Get the Proteus View

        :Parameters:
            - `view_name` : string

        :return:
            - :py:class:`proteus.objects.apientity.View`

        """
        if self._client.is_valid_connection():
            view = self._client._get_entity_by_name(
                self._client.Configuration.id,
                view_name,
                TYPE_VIEW)
            return APIObject(TypeRecord=view, client=self._client)
        return None

    def get_views(self):
        """
        Get a list of all Views in Proteus

        :return:
            - list of :py:class:`proteus.objects.apientity.View`

        """
        if self._client.is_valid_connection():
            views = self._client._get_entities(
                self._client.Configuration.id,
                TYPE_VIEW,
                0,
                99999)
            view_arr = []
            for i in views.item:
                view_arr.append(APIObject(TypeRecord=i, client=self._client))
            return view_arr
        return None

    def get_zone(self, zone_name=None, view=None, view_name=None):
        """
        Get a Zone Record from Proteus

        :Parameters:
            - `zone_name` : string
            - `view` : :py:class:`proteus.objects.apientity.View`
            - `view_name` : string

        :returns:
            - :py:class:`proteus.objects.apientity.Zone`

        """
        if self._client.is_valid_connection():
            if zone_name is not None and zone_name != "":
                if view is not None:
                    zone = self._client._get_entity_by_name(
                        view.id,
                        zone_name,
                        TYPE_ZONE)
                    return APIObject(TypeRecord=zone, client=self._client)
                elif view is None \
                    and view_name is not None \
                    and view_name != '':
                    view_rec = self.get_view(view_name)
                    zone = self._client._get_entity_by_name(
                        view_rec.id,
                        zone_name,
                        TYPE_ZONE)
                    return APIObject(TypeRecord=zone, client=self._client)
        return False

    def get_host_record(self, hostname, zonename, view=None, view_name=None):
        """Retrieve Host Record from Proteus
        
        :param hostname: the hostname
        :type hostname: str
        :param zonename: Name of the Zone i.e. 'subzone.domain.tld'
        :type zonename: str
        :param view: View name (can be None when view_name is not None)
        :type view: :py:class:`proteus.objects.apientity.View`
        :param view_name: View Name (can be None when view is not None)
        :type view_name: str
        
        :returns: :py:class:`proteus.objects.apientity.HostRecord`
        """
        return self._get_record(hostname, zonename, view, view_name,
                                TYPE_HOSTRECORD)

    def get_mx_record(self, hostname, zonename, view=None, view_name=None):
        """Retrieve Mailexchanger Record from Proteus
        
        :param hostname: the hostname
        :type hostname: str
        :param zonename: Name of the Zone i.e. 'subzone.domain.tld'
        :type zonename: str
        :param view: View name (can be None when view_name is not None)
        :type view: :py:class:`proteus.objects.apientity.View`
        :param view_name: View Name (can be None when view is not None)
        :type view_name: str
        
        :returns: :py:class:`proteus.objects.apientity.MXRecord`
        """
        return self._get_record(hostname, zonename, view, view_name,
                                TYPE_MXRECORD)

    def get_txt_record(self, hostname, zonename, view=None, view_name=None):
        """Retrieve TXT Record from Proteus
        
        :param hostname: the hostname
        :type hostname: str
        :param zonename: Name of the Zone i.e. 'subzone.domain.tld'
        :type zonename: str
        :param view: View name (can be None when view_name is not None)
        :type view: :py:class:`proteus.objects.apientity.View`
        :param view_name: View Name (can be None when view is not None)
        :type view_name: str
        
        :returns: :py:class:`proteus.objects.apientity.TXTRecord`
        """
        return self._get_record(hostname, zonename, view, view_name,
                                TYPE_TXTRECORD)

    def get_cname_record(self, hostname, zonename, view=None, view_name=None):
        """Retrieve CNAME Record from Proteus
        
        :param hostname: the hostname
        :type hostname: str
        :param zonename: Name of the Zone i.e. 'subzone.domain.tld'
        :type zonename: str
        :param view: View name (can be None when view_name is not None)
        :type view: :py:class:`proteus.objects.apientity.View`
        :param view_name: View Name (can be None when view is not None)
        :type view_name: str
        
        :returns: :py:class:`proteus.objects.apientity.CNAMERecord`
        """
        return self._get_record(hostname, zonename, view, view_name,
                                TYPE_CNAMERECORD)

    def get_hinfo_record(self, hostname, zonename, view=None, view_name=None):
        """Retrieve HINFO Record from Proteus
        
        :param hostname: the hostname
        :type hostname: str
        :param zonename: Name of the Zone i.e. 'subzone.domain.tld'
        :type zonename: str
        :param view: View name (can be None when view_name is not None)
        :type view: :py:class:`proteus.objects.apientity.View`
        :param view_name: View Name (can be None when view is not None)
        :type view_name: str
        
        :returns: :py:class:`proteus.objects.apientity.HINFORecord`
        """
        return self._get_record(hostname, zonename, view, view_name,
                                TYPE_HINFORECORD)

    def get_srv_record(self, hostname, zonename, view=None, view_name=None):
        """Retrieve SRV Record from Proteus
        
        :param hostname: the hostname
        :type hostname: str
        :param zonename: Name of the Zone i.e. 'subzone.domain.tld'
        :type zonename: str
        :param view: View name (can be None when view_name is not None)
        :type view: :py:class:`proteus.objects.apientity.View`
        :param view_name: View Name (can be None when view is not None)
        :type view_name: str
        
        :returns: :py:class:`proteus.objects.apientity.SRVRecord`
        """
        return self._get_record(hostname, zonename, view, view_name,
                                TYPE_SRVRECORD)

    def get_zone_list(self, zonename, view=None, view_name=None,
                      rec_type=DNS_ALLTYPES):
        """Retrieves a list of resource records for a special zone from Proteus
        
        :param zonename: Name of the Zone i.e. 'subzone.domain.tld'
        :type zonename: str
        :param view: View (can be None when view_name is not None)
        :type view: :py:class:`proteus.objects.apientity.View` 
        :param view_name: Name of the View (can be None when view is not None)
        :type view_name: str
        :param rec_type: Type of Record to return
        :type rec_type: str (use one of the constants of 
            :py:mod:`proteus.api.constants` or use DNS_ALLTYPES)
        
        :returns:
            - Depending on the input type it can return:
                - :py:class:`proteus.objects.apientity.HostRecord`
                - :py:class:`proteus.objects.apientity.MXRecord`
                - :py:class:`proteus.objects.apientity.TXTRecord`
                - :py:class:`proteus.objects.apientity.SRVRecord`
                - :py:class:`proteus.objects.apientity.HINFORecord`
            - or when rec_type is DNS_ALLTYPES:
                - return a mixed list of all types above 
        """
        if self._client.is_valid_connection():
            zone = self._find_zone(zonename, view, view_name)
            if rec_type in DNS_ALLTYPES:
                rec_list = []
                rec_list = self._get_records_by_zone(
                    zone,
                    rec_type)
                if rec_list is not None:
                    return rec_list
            elif rec_type == DNS_ALLTYPES:
                zone_list = []
                for i in DNS_ALLTYPES:
                    rec_list = []
                    rec_list = self._get_records_by_zone(zone, i)
                    if rec_list is not None:
                        zone_list.extend(rec_list)
                return zone_list
        return None





