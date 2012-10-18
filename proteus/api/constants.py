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


""" Constants """

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

ALL_TYPES = (
    TYPE_CONFIGURATION,
    TYPE_VIEW,
    TYPE_HOSTRECORD,
    TYPE_MXRECORD,
    TYPE_TXTRECORD,
    TYPE_CNAMERECORD,
    TYPE_HINFORECORD,
    TYPE_IP4BLOCK
    )
