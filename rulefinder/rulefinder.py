import xml.etree.ElementTree as ET
import ipaddress
import socket
import re

from rulefinder.constants import ENTRIES, XPATHS, BOOLEAN_ATTRS
from rulefinder.api_wrapper import PA_API

class Rulefinder():

    '''
    Main rulefinder class
    '''

    def __init__(
        self,
        host: str=None,
        search_obj: str=None,
        key: str=None,
        dgrp: str=None):

        '''
        Assigning objects for later use

        :param host: String containing Panorama IP or FQDN
        :param search_obj: String containing object to find
        :param key: String containing API key for Panorama
        :param dgrp: String containing device group
        '''

        self.host = host
        self.search_obj = search_obj
        self.key = key

        if dgrp:
            self.dgrp = dgrp
            self.getrules = PA_API.get_post_rulebase(host=self.host, dgroup=self.dgrp, key=self.key)
            self.root = ET.fromstring(self.getrules.text)

        if search_obj:
            self.getobs = PA_API.get_all_shared_objects(host=self.host, key=self.key)
            self.objectroot = ET.fromstring(self.getobs.text)

    def obj_converter(self):

        '''
        Obtains both IP and FQDN of self.search_obj

        :param self: uses self.search_obj (String)
        :return: String of IP and FQDN of self.search_obj
        '''

        try:
            ipaddress.IPv4Network(self.search_obj)
            obj_fqdn = socket.getfqdn(self.search_obj)
            obj_ip = self.search_obj
            return obj_fqdn, obj_ip

        except ipaddress.AddressValueError:
            try:
                obj_ip = socket.gethostbyname(self.search_obj)
            except socket.gaierror:
                obj_ip = None
            finally:
                obj_fqdn = self.search_obj

            return obj_fqdn, obj_ip

    def find_object(self) -> dict:

        '''
        Function to check if IP or FQDN of self.search_obj exists in Panorama
        Calls Panorama and gets all objects in shared
        Iterates over all objects and checks if IP/FQDN matches search_obj
        If found, adds key/val pair to dictionary

        :return: Dictionary of all found objects

        TODO: 
        Add optional check to find objects that cover the subnet
        Find associated object address groups
        Find associated URL categories 
        '''

        obj_fqdn, obj_ip = self.obj_converter()
        objects = {}

        for obs in self.objectroot.findall(XPATHS["objects"]):

            try:
                ip_adr = obs.find("ip-netmask").text

                if ip_adr == obj_ip:

                    object_name = obs.get('name')
                    objects[object_name] = obj_ip

                # This is to cover the IPs that are specified with a /32 netmask
                elif ip_adr == (f"{self.obj_ip}/32"):

                    object_name = obs.get('name')
                    objects[object_name] = (f"{self.obj_ip}/32")

            # Returns attribute error if "ip-netmask" doesn't exist
            # which means it's an fqdn or other object so we ignore the error
            except AttributeError:
                pass

            try:
                fqdn = obs.find("fqdn").text

                if re.search(f'{fqdn}', f'{obj_fqdn}', re.IGNORECASE):
                    object_name = obs.get('name')
                    objects[object_name] = obj_fqdn

            # Ignoring for same reasoning above
            except AttributeError:
                pass

        return objects


    def update_db(self):

        '''
        Generator function to get all rule attributes

        :return: Generator object returning dictionary of all values
        '''

        for rules in self.root.findall(XPATHS["rules"]):
            name = rules.get("name")

            rule_attrs = {
                "uuid": rules.get("uuid"),
                "dgrp": self.dgrp,
                "name": name,
                "from": ['any'],
                "to": ['any'],
                "source": ['any'],
                "source-user": ['any'],
                "destination": ['any'],
                "category": ['any'],
                "application": ['any'],
                "service": ['any'],
                "negate-source": "",
                "negate-destination": "",
                "action": rules.find("action").text,
                "disabled": ""
            }

            for attr in BOOLEAN_ATTRS:

                try:
                    val = rules.find(f"{attr}").text

                    if val == "yes":
                        rule_attrs[f"{attr}"] = "TRUE"
                    else:
                        rule_attrs[f"{attr}"] = "FALSE"

                except AttributeError:
                    rule_attrs[f"{attr}"] = "FALSE"

            for entry in ENTRIES:
                entry_list = []
                for info in self.root.findall(XPATHS['entries'].format(name, entry)):
                    entry_list.append(info.text)

                if len(entry_list) != 0:
                    rule_attrs[entry] = entry_list

            yield rule_attrs
                        