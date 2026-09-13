# VaaniX Semantic Packet Protocol

## Packet Structure

| Field | Size | Description |
|---|---:|---|
| Version | 1 byte | Protocol version |
| Language | 1 byte | Source language |
| Message ID | 2 bytes | Message identifier |
| Sequence | 1 byte | Packet sequence |
| Priority | 1 byte | Message priority |
| Payload Length | 2 bytes | Payload size |
| Payload | Variable | Semantic information |
| CRC | 4 bytes | Error detection |

## Priority

0 - Normal
1 - Important
2 - Urgent
3 - Emergency
