#!/usr/bin/python

import sys
import json
import socket
import struct
import math
from collections import defaultdict
from cStringIO import StringIO

class TreeNode:
    def __init__(self, ntype, nid, nptr, par_nid, par_nptr, active, bw_perc, bw_cap,
            ch_count, rt_cap, pkts_queued, ch_ts, ul_ts, rt_ts, 
            total_bytes, virt_x, fsc_m2, vtperiod,
            parentperiod, vtadj,
            cvtmin, cvtmax,
            myf, cfmin,
            sip, sport, dip,
            dport, name_str):
        self.ntype = ntype
        self.nid = nid
        self.nptr = nptr
        self.par_nid = par_nid
        self.par_nptr = par_nptr
        self.active = active
        self.bw_perc = bw_perc
        self.bw_cap = bw_cap
        self.ch_count = ch_count
        self.rt_cap = rt_cap
        self.pkts_queued = pkts_queued
        self.ch_ts = ch_ts
        self.ul_ts = ul_ts
        self.rt_ts = rt_ts
        self.total_bytes = total_bytes
        self.virt_x = virt_x
        self.fsc_m2 = fsc_m2
        self.vtperiod = vtperiod
        self.parentperiod = parentperiod
        self.vtadj = vtadj
        self.cvtmin = cvtmin
        self.cvtmax = cvtmax
        self.myf = myf 
        self.cfmin = cfmin
        self.sip = sip
        self.sport = sport
        self.dip = dip
        self.dport = dport
        self.name_str = name_str
        self.ch_list = []

    def get_nid(self):
        return self.nid

    def get_nptr(self):
        return self.nptr

    def get_par_nid(self):
        return self.par_nid

    def get_par_nptr(self):
        return self.par_nptr

    def get_ch_count(self):
        return self.ch_count

    def get_ntype(self):
        return self.ntype

    def get_active_status(self):
        return self.active

    def get_pkts_queued(self):
        return self.pkts_queued

    def get_name_str(self):
        return self.name_str

    def add_child(self, tree_node):
        self.ch_list.append(tree_node)
        return

    def get_ch_list(self):
        return self.ch_list

    def child_flow_type(self):
        if (len(self.ch_list)):
            return self.ch_list[0].get_ntype()
        return -1

    def str(self):
        if (self.ntype == 0):
            out_str = 'Root'
            out_str = out_str.ljust(10)
            out_str += ' ( CC: ' + str(self.ch_count) + ' , AS: ' +\
            str(self.active) + ' , WT: ' +\
            str(self.bw_perc) + ' , BC: ' + str(self.bw_cap / 125) + ' kbps )'
        elif (self.ntype == 1):
            out_str = self.name_str
            out_str = out_str.ljust(30)
            out_str += ' ( CC: ' + str(self.ch_count) + ' , AS: ' +\
            str(self.active) + ' , WT: ' +\
            str(self.bw_perc) + ' , BC: ' + str(self.bw_cap / 125) + ' kbps )'
        elif (self.ntype == 2):
            out_str = 'Flow'
            # DRR Case: Lower 32 bits represent Node id. Upper 32 bits represent flow_id of this node
            # Reason  : DRR case can have multiple flows under the same node
            out_str += ' - ' + str((self.nid - pow(2,31)) & 0xFFFFFFFF) + '/' + str(self.nid >> 32)
            out_str = out_str.ljust(20)
            out_str += ' ( AS: ' +\
            str(self.active) + ' , PQ: ' + str(self.pkts_queued) + ' )'
            if (self.sip != 0):
                out_str += ' (' +\
                        socket.inet_ntoa(struct.pack('!L', self.sip)) +\
                        ':' + str(self.sport) + ' -> ' +\
                        socket.inet_ntoa(struct.pack('!L', self.dip)) +\
                        ':' + str(self.dport) + ')'
        else:
            print 'ERROR - Invalid Type'

        '''
        out_str += ' - ' + str(self.nid) + ' / ' + str(self.nptr)
        out_str += ' ( ' +\
		' CT: ' + str(self.ch_ts) +\
		' , VX: ' + str(self.virt_x) +\
		' , FM: ' + str(self.fsc_m2) +\
		' , SP: ' + str(self.vtperiod) +\
		' , PP: ' + str(self.parentperiod) +\
		' , VA: ' + str(self.vtadj) +\
		' , CM: ' + str(self.cvtmin) +\
		' , CX: ' + str(self.cvtmax) +\
		' , UT: ' + str(self.ul_ts) +\
		' , MF: ' + str(self.myf) +\
		' , CF: ' + str(self.cfmin) +\
		' , RT: ' + str(self.rt_ts) +\
		' , RC: ' + str(self.rt_cap) +\
		' , TB: ' + str(self.total_bytes) +\
		' )'
        '''
        return out_str

    def printtest(self):
        print self.nid
        print self.nptr
        print self.bw_perc
        print self.ch_count
        print len(self.ch_list)
        return 0

def DrawTree(tree_node, space, recr):
    space.write('  + ')
    space.write(tree_node.str())
    space.write('\n')
    recr = recr + 1
    for cont in tree_node.get_ch_list():
        count = recr
        while (count > 0):
            space.write('   ')
            count = count - 1
        DrawTree(cont, space, recr)
    return

def ActiveUpCheck(dct):
    for k,v in dct.iteritems():
        if v.get_ntype() == 2 and v.get_active_status() == 1:
            cont = v
            key1 = str(cont.get_nid()) + str(cont.get_nptr())
            key2 = str(cont.get_par_nid()) + str(cont.get_par_nptr())
            while key1 != '00' and key2 != '00':
                tn = dct[key2]
                if tn.get_active_status() != 1:
                    print 'Active-up Inconsistency check'
                    exit(-1)
                cont = tn
                key1 = str(cont.get_nid()) + str(cont.get_nptr())
                key2 = str(cont.get_par_nid()) + str(cont.get_par_nptr())
    return

def ActiveDownCheck(tree_node):
    ch_cnt = len(tree_node.get_ch_list())
    exist = 0
    if (tree_node.get_ntype() == 2):
        if (tree_node.get_active_status() != 1):
            print 'Active-down Inconsistency check' + tree_node.str()
            exit(-1)
        else:
            return
    for cont in tree_node.get_ch_list():
        if (cont.get_active_status() == 1):
            exist = 1
            ActiveDownCheck(cont)
    if (exist == 0):
        print 'Active-down Inconsistency check'
        exit(-1)

def SanityCheck(tree_node):
    ch_cnt = len(tree_node.get_ch_list())
    if ((ch_cnt != tree_node.get_ch_count()) and (ch_cnt > 0)):
        # Skipe child count sanity for biz nodes. In new flow, only active flows are returned 
        # from debug dump. So, expected that actual child count != actual active flow count provided
        if (tree_node.child_flow_type() != 2):
            print 'Child count check failed' + tree_node.str()
            exit(-1)
    if (tree_node.get_ntype() != 2 and tree_node.get_pkts_queued() > 0):
        print 'Pkt queue > 0 for non flows- inconsistent' + tree_node.str()
        exit(-1)
    if (tree_node.get_ntype() == 2 and tree_node.get_pkts_queued() == 0 and 
            tree_node.get_active_status() != 0):
        print 'Pkt queue and active status inconsistent' + tree_node.str()
        exit(-1)
    if (tree_node.get_ntype() == 2 and tree_node.get_pkts_queued() > 0 and 
            tree_node.get_active_status() != 1):
        print 'Pkt queue and active status inconsistent' + tree_node.str()
        exit(-1)
    for cont in tree_node.get_ch_list():
        SanityCheck(cont)
    return

def vc_qos_view(json_cont):
    i = 0
    ht = dict() 
    for cont in json_cont['sch_dump']:
        tn = TreeNode(cont['type'],
                cont['nid'], cont['nptr'],
                cont['par_nid'], cont['par_nptr'],
                cont['active'], cont['bw_perc'],
                cont['bw_cap'], cont['ch_count'],
                cont['rt_cap'], cont['pkts_queued'],
                cont['ch_ts'], cont['ul_ts'], cont['rt_ts'], 
                cont['total_bytes'], cont['virtual_x'], cont['fsc_m2'], 
                cont['vtperiod'], cont['parentperiod'], cont['vtadj'], 
                cont['cvtmin'], cont['cvtmax'], 
                cont['myf'], cont['cfmin'],
                cont['sip'], cont['sport'],
                cont['dip'], cont['dport'], cont['str_name'])
        key = str(cont['nid']) + str(cont['nptr'])
        ht[key] = tn
       
    for k, v in ht.iteritems():
        par_key = str(v.get_par_nid()) + str(v.get_par_nptr())
        nid_key = str(v.get_nid()) + str(v.get_nptr())
        if nid_key == '00':
            continue
        ht[par_key].add_child(v)
        
    # Child count check
    SanityCheck(ht['00'])
    ActiveUpCheck(ht)
    cont = ht['00']
    if (cont.get_active_status() == 1):
        ActiveDownCheck(ht['00'])
    # Generate tree dump
    space = StringIO()
    print 'CC - Child count\
            AS - Active status\
            PQ - Pks queued\
            WT - QoS Weight\
            BC - Bandwidth cap'
    print '\n'
    '''
    print 'CT - Child virtual timestamp (cl_vt)\
           FM - Virtual bandwidth(fsc.m2)\
           SP - vtperiod\
           PP - parentperiod\
           VX - virtual.x\
           VA - vt_adj\
           CM - cvtmin\
           CX - cvtmax\
           CF - cl_myf\
           TB - cl_total\
           UT - Upperlimit timestamp\
           RT - Realtime timestamp\
           RC - Realtime Cap'
    print '\n'
    '''
    DrawTree(ht['00'], space, 0)
    print space.getvalue()
    return

def vc_qos_view_str(content):
    json_cont = json.loads(content)
    vc_qos_view(json_cont)
    return

if __name__ == '__main__':

    argc = len(sys.argv)
    if (argc != 2):
        print 'Usage : /<script> <path_to_dump_file>'
        exit(-1)

    json_file = open(str(sys.argv[1]))
    json_cont = json.load(json_file)
    vc_qos_view(json_cont)
