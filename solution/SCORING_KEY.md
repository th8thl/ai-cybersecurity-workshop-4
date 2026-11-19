# Reference scoring key

| Starter source | Expected finding | Repair |
|---|---|---|
| review_examples/file_imports.py | CWE-502, unsafe deserialization of uploaded data | Accept JSON and validate the ticket fields before creating the ticket. |
| review_examples/attachments.py | CWE-22, path traversal in attachment lookup | Resolve the path inside the current ticket folder and require a matching attachment record for that ticket. |

Score each distinct known issue once per tool. A source-supported matching claim earns a confirmed finding. A known issue absent from the report is a miss. An incorrect claim about the reviewed code is a false alarm. Unsupported claims require adjudication before scoring. These workshop examples have no assigned CVE.

