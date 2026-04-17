# Suspicious Outbound Traffic Investigation Guide

## Purpose
This guide helps SOC analysts investigate unusual outbound network activity from a host.

## Common Indicators
- Large data transfers to unknown IP addresses
- Repeated connections to unfamiliar domains
- DNS spikes followed by outbound traffic
- Traffic to unusual ports or geolocations
- Connections outside normal business hours

## Investigation Steps
1. Review firewall and proxy logs.
2. Identify destination IPs, domains, and ports.
3. Check whether the traffic is expected for the host role.
4. Correlate with process execution logs.
5. Review whether any new files or services were created.
6. Check if the traffic aligns with alert activity from Suricata or Wazuh.

## Possible Response
- Block suspicious destinations
- Isolate the affected host
- Preserve logs and network evidence
- Investigate for malware or unauthorized data transfer

## Relevant Tools
- Wazuh
- Suricata
- Wireshark
- Autopsy
- FTK Imager