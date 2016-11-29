#!/usr/bin/python

import payl
import pcapy
import os
import sys

from impacket import ImpactDecoder, ImpactPacket

def main(argv):
    try:
        infile = argv[1]
        outfile = argv[2]
        print infile
        cap = pcapy.open_offline(infile)
        fdataset = open(outfile + ".csv", "w")

        line = "src_addr, src_port, dest_addr, dest_port, protocol, seq_num, length"
        for i in range(0, 256):
            line += ", {}". format(i)

        fdataset.write(line + "\n")

        while (1):
            (header, packet) = cap.next()
            if not header:
                break
            parse(fdataset, header, packet)
    except IndexError as e:
        print "Usage : python pcap_to_r.py <filename-in> <filename-out>"
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

            if isinstance(transporthdr, ImpactPacket.TCP):
                s_port = transporthdr.get_th_sport()
                d_port = transporthdr.get_th_dport()
                seq_num = transporthdr.get_th_seq()
                d_length = len(transporthdr.get_data_as_string())
                protocol = "tcp_ip"
            elif isinstance(transporthdr, ImpactPacket.UDP):
                s_port = transporthdr.get_uh_sport()
                d_port = transporthdr.get_uh_dport()
                seq_num = 0
                d_length = transporthdr.get_uh_ulen()
                protocol = "udp_ip"
            elif isinstance(transporthdr, ImpactPacket.ICMP):
                s_port = 0
                d_port = 0
                seq_num = 0
                d_length = 0
                protocol = "icmp"
            elif isinstance(transporthdr, ImpactPacket.IGMP):
                s_port = 0
                d_port = 0
                seq_num = 0
                d_length = 0
                protocol = "igmp"
            else:
                s_port = 0
                d_port = 0
                seq_num = 0
                d_length = -1
                protocol = transporthdr.__class__

            payload = transporthdr.get_data_as_string()

            grams = payl.get_byte_freq(payload, d_length)
            line = "{},{},{},{},{},{},{}".format(s_addr, s_port, d_addr, d_port, protocol, seq_num, d_length)

            for value in grams.itervalues():
                line += ",{}".format(round(value,3))

            fdataset.write(line + "\n")

if __name__ == '__main__':
	main(sys.argv)