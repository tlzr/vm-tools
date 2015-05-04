#!/usr/bin/env python

import argparse
import libvirt
import sys

from xmlbuilder import XMLBuilder


class LibVirtClass():
    def connect(self, URI='qemu:///system'):
        """Make connection to the Hypervisor
           URI: specify which driver a connection refers to
        """
        self.libvirt_connection = libvirt.open(URI)
        if self.libvirt_connection == None:
            print 'Unable to connect to the hypervisor'
            sys.exit(1)

    def close(self):
        """Close connection
        """
        try:
           self.libvirt_connection.close()
        except:
           print 'Unable to close connection to Hypervisor.'

    def create_snapshot(self, domain, snapshot_name, \
                        snapshot_description):
        """Create VM snapshot
           connection: object with a connection to the Hypervisor
           domain: VM name
           snapshot_name
           snapshot_description
        """
        try:
            libvirt_domain = self.libvirt_connection.lookupByName(domain)
            xml_base = XMLBuilder('domainsnapshot')
            xml_base.name(snapshot_name)
            xml_base.description(snapshot_description)
            xml = str(xml_base)
            libvirt_domain.snapshotCreateXML(xml)
        except:
            print 'Unable to create snapshot'
            sys.exit(1)

        print 'Snapshot has been created successfully.'


def main(args):
    lv = LibVirtClass()
    lv.connect()
    lv.create_snapshot(args.domain, args.snapshot_name, \
                       args.snapshot_description)
    lv.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process VM snapshots.')
    parser.add_argument("domain", type=str, help="Domain")
    parser.add_argument('-r', '--snapshot-name', metavar=('SNAME'), type=str,
                        help='snapshot name', required=True)
    parser.add_argument('-sd', '--snapshot-description', metavar=('SDESCRIPTION'), type=str,
                        help='snapshot description', default='blank')
    parser.add_argument('-v', '--version', action='version',
                        version='Version: 1.0')
    args = parser.parse_args()

    main(args)
