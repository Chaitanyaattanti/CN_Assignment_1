import socket
from scapy.all import PcapReader, DNS, DNSQR, UDP

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 9999  

def get_queries(pcap_file, limit=None):
    """Extract DNS queries (UDP dst port 53) with custom HHMMSSID header"""
    queries = []
    seq = 0
    with PcapReader(pcap_file) as pcap:
        for pkt in pcap:
            if pkt.haslayer(DNS) and pkt[DNS].qr == 0:
                if pkt.haslayer(UDP) and pkt[UDP].dport == 53:
                    dom = pkt[DNSQR].qname.decode().strip(".")
                    # HHMMSS from packet time
                    seconds=24*60*60
                    ts = int(pkt.time) % seconds
                    hh = ts // 3600
                    mm = (ts % 3600) // 60
                    ss = ts % 60
                    hdr = f"{hh:02d}{mm:02d}{ss:02d}{seq:02d}"
                    seq += 1
                    queries.append((hdr, dom))
                    if limit and seq >= limit:
                        break
    return queries

def run_client(pcap_file):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    queries = get_queries(pcap_file)

    results = []
    for hdr, dom in queries:
        msg = f"{hdr}|{dom}"
        sock.sendto(msg.encode(), (SERVER_HOST, SERVER_PORT))
        data, _ = sock.recvfrom(4096)
        rhdr, rdom, ip = data.decode().split("|")
        print(f"[CLIENT] {rdom} -> {ip} (Header={rhdr})")
        results.append((rhdr, rdom, ip))

    # Write report
    with open("report.txt", "w") as f:
        f.write("CustomHeader\tDomain\tResolvedIP\n")
        for h, d, ip in results:
            f.write(f"{h}\t{d}\t{ip}\n")

if __name__ == "__main__":
    pcap_file = r"/Users/chaitanyaattanti/Downloads/8.pcap"  # Set PCAP path here
    run_client(pcap_file)
