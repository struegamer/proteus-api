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


class APIObject(object):
    def __new__(cls, *args, **kwargs):
        _apientity = None
        obj_type = None
        if 'TypeRecord' in kwargs:
            _apientity = kwargs.get('TypeRecord', None)
            if len(_apientity) == 0:
                return None
            obj_type = _apientity.get('type', None)
            del kwargs['TypeRecord']
        kwargs['data'] = _apientity
        if obj_type is not None:
            if obj_type.lower() == 'zone':
                return Zone(*args, **kwargs)
            if obj_type.lower() == 'configuration':
                return Configuration(*args, **kwargs)
            if obj_type.lower() == 'view':
                return View(*args, **kwargs)
            if obj_type.lower() == 'hostrecord':
                return HostRecord(*args, **kwargs)
            if obj_type.lower() == 'mxrecord':
                return MXRecord(*args, **kwargs)
            if obj_type.lower() == 'txtrecord':
                return TXTRecord(*args, **kwargs)
            if obj_type.lower() == 'aliasrecord':
                return CNAMERecord(*args, **kwargs)
            if obj_type.lower() == 'hinforecord':
                return HINFORecord(*args, **kwargs)
            if obj_type.lower() == 'srvrecord':
                return SRVRecord(*args, **kwargs)

        return None

    def __init__(self, *args, **kwargs):
        print self.__class__.__name__


class ProteusPropertyObject(object):
    def __init__(self, properties=None):
        self._property_string = None
        if properties is not None:
            self._property_string = properties
        self._parse_properties()

    def _parse_properties(self):
        if self._property_string is None:
            return None
        property_list = self._property_string[:-1].split('|')
        self.__dict__['_property_list'] = []
        for i in property_list:
            arr = iter(i.split('='))
            dc = dict(zip(arr, arr))
            self.__dict__['_property_list'].append(i.split('=')[0])
            self.__dict__.update(dc)

    def __repr__(self):
        a = super(ProteusPropertyObject, self).__repr__()
        return '%s | Property List: %s' % (a, self._property_list)


class ProteusDataObjects(object):
    def __init__(self, *args, **kwargs):
        self._raw_data = None
        if 'data' in kwargs:
            self._raw_data = kwargs.get('data', None)
        if self._raw_data is not None:
            if 'properties' in self._raw_data:
                self._raw_data['properties'] = ProteusPropertyObject(
                    self._raw_data['properties'])

    def __getattr__(self, name):
        if name in self.__dict__['_raw_data']:
            return self._raw_data[name]
        return super(ProteusDataObjects, self).__getattr__(name)

    def __repr__(self):
        a = super(ProteusDataObjects, self).__repr__()
        return '%s | Members: %s' % (a, self._raw_data.keys())


class Zone(ProteusDataObjects):
    pass


class Configuration(ProteusDataObjects):
    pass


class View(ProteusDataObjects):
    pass


class HostRecord(ProteusDataObjects):
    pass


class TXTRecord(ProteusDataObjects):
    pass


class MXRecord(ProteusDataObjects):
    pass


class CNAMERecord(ProteusDataObjects):
    pass


class HINFORecord(ProteusDataObjects):
    pass


class SRVRecord(ProteusDataObjects):
    pass


class SOARecord(ProteusDataObjects):
    pass


class DNSOptionsRecord(ProteusDataObjects):
    pass
