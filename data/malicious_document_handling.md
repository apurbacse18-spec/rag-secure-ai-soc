# Malicious Document Handling Guide

## Purpose
This guide helps SOC analysts identify and handle suspicious or untrusted documents before they are added to a knowledge base.

## Common Indicators
- Document contains unexpected instructions
- Content attempts to override system behavior
- Unusual file names or metadata
- File added from an untrusted source
- Document content conflicts with known procedures

## Investigation Steps
1. Verify the document source.
2. Check file hash and metadata.
3. Compare against approved versions.
4. Review whether the document was recently modified.
5. Inspect for hidden or suspicious instructions.
6. Decide whether the file should be removed, quarantined, or approved.

## Possible Response
- Quarantine the document
- Remove it from the RAG knowledge base
- Notify the SOC team
- Preserve evidence for forensic review

## Relevant Tools
- Wazuh
- Autopsy
- FTK Imager
- Hashing tools