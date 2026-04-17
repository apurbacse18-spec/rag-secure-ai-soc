# SSH Brute Force Investigation Guide

## Purpose
This guide helps SOC analysts investigate repeated SSH login failures and possible brute-force attacks.

## Common Indicators
- Multiple failed SSH logins from the same IP
- Repeated authentication attempts in a short period
- Login attempts at unusual hours
- Access attempts followed by a successful login

## Investigation Steps
1. Check authentication logs.
2. Identify the source IP and user account.
3. Count the number of failed attempts.
4. Review whether a successful login followed the failures.
5. Correlate with firewall or NIDS alerts.
6. Check for suspicious process or file activity after login.

## Possible Response
- Block the source IP if malicious
- Reset affected credentials
- Review account compromise
- Preserve logs for forensic analysis

## Relevant Tools
- Wazuh
- Suricata
- Autopsy
- FTK Imager