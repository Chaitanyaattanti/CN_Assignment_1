# **Computer Networks Assignment 1**
**DNS Resolver with Custom Header**

Download the sample packet capture file 8.pcap from the following link: https://drive.google.com/file/d/1mYjJznwiDRGd1O8cMntyIOwWfRbkwcbk/view?usp=sharing

##  Overview

This Assignment implements a **custom DNS resolver system** with a **client–server architecture**.

* The **client** reads DNS queries from a `.pcap` file, attaches a **custom header (HHMMSSID)**, and sends them to the server.
* The **server** processes the request, applies **time-based rules**, assigns an IP from a predefined pool, and returns the resolved result.
* The client logs all results into the  `report.txt` file.

---

##  Features

* **Custom Header Format (8 bytes):**

  * `HH` – Hour (24-hour format)
  * `MM` – Minute
  * `SS` – Second
  * `ID` – Sequential ID starting from 00

  Example: `12341600` → 12:34:16, ID = 00

* **Time-Based IP Resolution Rules:**

  * Morning (04:00–11:59) → Pool Index 0–4
  * Afternoon (12:00–19:59) → Pool Index 5–9
  * Night (20:00–03:59) → Pool Index 10–14

* **IP Pool containing 15 IPs:**

  ```
  192.168.1.1 – 192.168.1.15
  ```

* **Report Output:**
  All resolved queries are added in `report.txt` in the format:

  ```
  CustomHeader   Domain   ResolvedIP
  ```

---

##  How to Run

### 1. Start the Server

```bash
python3 server.py
```

Output:

```
[SERVER] Listening on 127.0.0.1:9999...
```

### 2. Run the Client

```bash
python3 client.py
```

This will:

* Read DNS queries from `8.pcap`
* Add custom header + DNS packet
* Send to server
* Receive resolved IPs
* Add results in  the `report.txt`

---

##  Example Output

### Console Logs

```
[SERVER] example.com -> 192.168.1.6 (Header=12341600)
[CLIENT] example.com -> 192.168.1.6 (Header=12341600)
```
---


### report.txt

```
CustomHeader   Domain       ResolvedIP
12341600       example.com  192.168.1.6
12341601       test.com     192.168.1.7
12341602       abc.org      192.168.1.8
```

---

##  Requirements

* `scapy` library for PCAP parsing

Install dependencies:

```bash
pip install scapy
```

---

## Note:

* If no domain is parsed, `UNKNOWN` will be shown.
* Only DNS queries (`UDP dst port 53`) are processed.
* IP assignment depends strictly on **time slot + sequence ID** rules.

---

