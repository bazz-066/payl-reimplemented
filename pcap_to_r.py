#!/usr/bin/python

import payl
import pcapy
import os
import sys

from impacket import ImpactDecoder, ImpactPacket

def main(argv):
    try:
        infile = argv[1]
        print infile
        cap = pcapy.open_offline(infile)
        fdataset = open("datapcap.csv", "w")

        line = "src_addr, src_port, dest_addr, dest_port, length"
        for i in range(0, 256):
            line += ", {}". format(i)

        fdataset.write(line + "\n")

        while (1):
            (header, packet) = cap.next()
            if not header:
                break
            parse(fdataset, header, packet)
    except IndexError as e:
        print "Usage : python pcap_to_r.py <filename>"
    fdataset.close()


def parse(fdataset, header, packet):
    decoder = ImpactDecoder.EthDecoder()
    ether = decoder.decode(packet)
    #print str(ether.get_ether_type()) + " " + str(ImpactPacket.IP.ethertype)

    if ether.get_ether_type() == ImpactPacket.IP.ethertype:
        iphdr = ether.child()
        transporthdr = iphdr.child()
        if transporthdr.get_data_as_string() != '' and isinstance(transporthdr, ImpactPacket.TCP):
            s_addr = iphdr.get_ip_src()
            d_addr = iphdr.get_ip_dst()
            s_port = transporthdr.get_th_sport()
            d_port = transporthdr.get_th_dport()
            d_length = transporthdr.get_size()
            payload = transporthdr.get_data_as_string()

            grams = payl.get_byte_freq(payload, d_length)
            line = "{},{},{},{},{}".format(s_addr, s_port, d_addr, d_port, d_length)

            for value in grams.itervalues():
                line += ",{}".format(value)

            fdataset.write(line + "\n")

if __name__ == '__main__':
	main(sys.argv)