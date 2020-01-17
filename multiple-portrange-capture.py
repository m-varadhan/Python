from binascii import hexlify  
from ctypes import create_string_buffer, addressof  
from socket import socket, AF_PACKET, SOCK_RAW, SOL_SOCKET  
from struct import pack, unpack  
  
  
# A subset of Berkeley Packet Filter constants and macros, as defined in  
# linux/filter.h.  
  
# Instruction classes  
BPF_LD = 0x00  
BPF_JMP = 0x05  
BPF_RET = 0x06  
  
# ld/ldx fields  
BPF_H = 0x08  
BPF_B = 0x10  
BPF_ABS = 0x20  
  
# alu/jmp fields  
BPF_JEQ = 0x10  
BPF_JGE = 0x30  
BPF_JGT = 0x20
BPF_JSET = 0x40  
BPF_K = 0x00  

OP_LDH = BPF_LD + BPF_H + BPF_ABS
OP_LDB = BPF_LD + BPF_B + BPF_ABS
OP_LDXB = (0xb1)
OP_LDHX = (0x48)
OP_JEQ = BPF_JMP + BPF_JEQ
OP_JGE = BPF_JMP + BPF_JGE
OP_JGT = BPF_JMP + BPF_JGT
OP_JST = BPF_JMP + BPF_JSET
OP_RET = BPF_RET

#IP HEADER VALUE
MGX_SCTP = 0x84
MGX_UDP  = 0x11
MGX_TCP  = 0x6
MGX_IP6=0x86dd
MGX_IP4=0x800
MGX_IP=0xc
MGX_FRAG=0x1ffff
MGX_LOAD_X=0xe
MGX_PASS =  0x4000
MGX_DROP =  0x0

#IP HEADER ADRESS
ADR_IP6_SPORT=0x36
ADR_IP6_DPORT=0x38
ADR_IP4_SPORT_X=0xe
ADR_IP4_DPORT_X=0x10
ADR_IP6_PROTO=0x14
ADR_IP4_PROTO=0x17
ADR_FRAG=0x14

PORTLIST = [(55061,55065),(5060,5065)]
(STPORT_FINAL, EDPORT_FINAL) = PORTLIST[-1]

IFF_PROMISC = 0x100
SIOCGIFFLAGS = 0x8913
SIOCSIFFLAGS = 0x8914

import ctypes

class ifreq(ctypes.Structure):
	_fields_ = [("ifr_ifrn", ctypes.c_char * 16),
                ("ifr_flags", ctypes.c_short)]
  
def bpf_stmt(code, jt, jf, k):  
	print(code, jt, jf, k)
	return pack('HBBI', code, jt, jf, k)  
  
port = 55060
  
  
# Ordering of the filters is backwards of what would be intuitive for   
# performance reasons: the check that is most likely to fail is first.  
filters_list_template = [  
("LB_IP"     		, OP_LDH	, 0			, 0			, MGX_IP ),
("LB_IP6"   		, OP_JEQ	, 0			, "LB_IP4"		, MGX_IP6 ),
("LB_PROTO"  		, OP_LDB	, 0			, 0			, ADR_IP6_PROTO ),
("LB_SCTP"   		, OP_JEQ	, "LB_IP6_SPORT_CHK" 	, 0			, MGX_SCTP ),
("LB_TCP"    		, OP_JEQ	, "LB_IP6_SPORT_CHK" 	, 0			, MGX_TCP ),
("LB_UDP"    		, OP_JEQ	, 0			, "LB_FAIL"		, MGX_UDP ),

("LB_IP6_SPORT_CHK" 	, OP_LDH	, 0			, 0			, ADR_IP6_SPORT ),
#("LB_STPORT_GE" 	, OP_JGE	, 0			, "LB_IP6_DPORT_CHK"	, STPORT_FINAL ),
#("LB_EDPORT_GT"   	, OP_JGT	, "LB_IP6_DPORT_CHK" 	, "LB_PASS"		, EDPORT_FINAL ),

("LB_IP6_DPORT_CHK" 	, OP_LDH	, 0			, 0			, ADR_IP6_DPORT ),
#("LB_STPORT_GE" 	, OP_JGE	, 0			, "LB_FAIL"		, STPORT_FINAL ),
#("LB_EDPORT_GT"   	, OP_JGT	, "LB_FAIL"		, "LB_PASS"		, EDPORT_FINAL ),

("LB_IP4"      		, OP_JEQ	, 0			, "LB_FAIL"		, MGX_IP4),
("LB_PROTO"     	, OP_LDB	, 0			, 0			, ADR_IP4_PROTO ),
("LB_SCTP"      	, OP_JEQ	, "LB_FRAG_CHK"		, 0			, MGX_SCTP ),
("LB_TCP"       	, OP_JEQ	, "LB_FRAG_CHK"		, 0			, MGX_TCP ),
("LB_UDP"       	, OP_JEQ	, 0			, "LB_FAIL"		, MGX_UDP ),
("LB_FRAG_LOAD" 	, OP_LDH	, 0			, 0			, ADR_FRAG ),
("LB_FRAG_CHK"  	, OP_JST	, "LB_FAIL"		, 0			, MGX_FRAG ),
("LB_LOAD_X"    	, OP_LDXB	, 0			, 0			, MGX_LOAD_X ),

("LB_IP4_SPORT_CHK" 	, OP_LDHX	, 0			, 0			, ADR_IP4_SPORT_X ),
#("LB_STPORT_GE" 	, OP_JGE	, 0			, "LB_IP4_DPORT_CHK"	, STPORT_FINAL ) ,
#("LB_EDPORT_GT"  	, OP_JGT	, "LB_IP4_DPORT_CHK"	, "LB_PASS"		, EDPORT_FINAL ),

("LB_IP4_DPORT_CHK" 	, OP_LDHX	, 0			, 0			, ADR_IP4_DPORT_X ),
#("LB_STPORT_GE" 	, OP_JGE	, 0			, "LB_FAIL"		, STPORT_FINAL ),
#("LB_EDPORT_GT"  	, OP_JGT	, "LB_FAIL"		, 0			, EDPORT_FINAL ),

("LB_PASS" 		, OP_RET	, 0			, 0			, MGX_PASS ),
("LB_FAIL" 		, OP_RET	, 0			, 0			, MGX_DROP ),
]


i=0
while i < len(filters_list_template):
	(lb, op, t, f, k) = filters_list_template[i]
	if lb is "LB_IP6_SPORT_CHK":
		j=0
		PORTLIST_LEN=len(PORTLIST)
		for (stport, edport) in PORTLIST:
			if j < PORTLIST_LEN:
				filters_list_template.insert(i, ("LB_STPORT_GE", OP_JGE, 0, 1, stport))
				filters_list_template.insert(i, ("LB_EDPORT_GT", OP_JGT, 0, "LB_PASS", edport))
			else:
				filters_list_template.insert(i, ("LB_STPORT_GE", OP_JGE, 0, "LB_IP6_DPORT_CHK", stport))
				filters_list_template.insert(i, ("LB_EDPORT_GT", OP_JGT, "LB_IP6_DPORT_CHK", "LB_PASS", edport))
			j+=1
			i+=2
	if lb is "LB_IP4_SPORT_CHK":
		j=0
		PORTLIST_LEN=len(PORTLIST)
		for (stport, edport) in PORTLIST:
			if j < PORTLIST_LEN:
				filters_list_template.insert(i, ("LB_STPORT_GE", OP_JGE, 0, 1, stport))
				filters_list_template.insert(i, ("LB_EDPORT_GT", OP_JGT, 0, "LB_PASS", edport))
			else:
				filters_list_template.insert(i, ("LB_STPORT_GE", OP_JGE, 0, "LB_IP4_DPORT_CHK", stport))
				filters_list_template.insert(i, ("LB_EDPORT_GT", OP_JGT, "LB_IP4_DPORT_CHK", "LB_PASS", edport))
			j+=1
			i+=2
	elif lb is "LB_IP6_DPORT_CHK" or lb is "LB_IP4_DPORT_CHK":
		j=0
		PORTLIST_LEN=len(PORTLIST)
		for (stport, edport) in PORTLIST:
			if j < PORTLIST_LEN:
				filters_list_template.insert(i, ("LB_STPORT_GE", OP_JGE, 0, 1, stport))
				filters_list_template.insert(i, ("LB_EDPORT_GT", OP_JGT, 0, "LB_PASS", edport))
			else:
				filters_list_template.insert(i, ("LB_STPORT_GE", OP_JGE, 0, "LB_FAIL", stport))
				filters_list_template.insert(i, ("LB_EDPORT_GT", OP_JGT, "LB_FAIL", "LB_PASS", edport))
			j+=1
			i+=2
	i+=1

filters_list_real=[]
lb_idx=len(filters_list_template)+1
label={}
for (lb, op, t, f, k) in reversed(filters_list_template):
	filters_list_real.append( (op, 
				    label.get(t,lb_idx)-lb_idx,
				    label.get(f,lb_idx)-lb_idx,
				    k
				   ) )
	label[lb] = lb_idx-1
	lb_idx -= 1

filters_list = []
lb_idx=0
#for (op, t, f, k) in map(lambda (op, t, f, k): (int(op), int(t),  int(f),  int(k)),  reversed(filters_list_real)):
for (op, t, f, k) in reversed(filters_list_real):
	#print(lb_idx, op, t, f, k)
	filters_list.append(bpf_stmt(op,t,f,int(k)))
	lb_idx += 1

## Create filters struct and fprog struct to be used by SO_ATTACH_FILTER, as  
## defined in linux/filter.h.  
filters = ''.join(filters_list)  
b = create_string_buffer(filters)  
mem_addr_of_filters = addressof(b)  
fprog = pack('HL', len(filters_list), mem_addr_of_filters)  
  
# As defined in asm/socket.h  
SO_ATTACH_FILTER = 26  
  
# Create listening socket with filters  
s = socket(AF_PACKET, SOCK_RAW, 0x0800)  
s.setsockopt(SOL_SOCKET, SO_ATTACH_FILTER, fprog)  
s.bind(('br0', 0x0800))  

ifr = ifreq()
ifr.ifr_ifrn = "br0"


import fcntl

fcntl.ioctl(s.fileno(), SIOCGIFFLAGS, ifr)

ifr.ifr_flags |= IFF_PROMISC
fcntl.ioctl(s.fileno(), SIOCSIFFLAGS, ifr) # S for Set

  
while True:  
    bufsize = 1024*10
    data, addr = s.recvfrom(bufsize)  
    print 'got data from', addr[0], addr[1], ':', hexlify(data)  
