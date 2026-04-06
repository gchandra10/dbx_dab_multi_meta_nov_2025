# Personal Bundle (PCI DATA)

This is to demonstrate how to handle PCI data using DLT-META.

## resources/person_r2s_job.yml

- New job to deploy PCI UDFs
  - Added job deploy_pci_udfs:
    - Task create_pci_udfs is a spark_python_task running **src/deploy_pci_udfs.py**.
    - Passes ${var.catalog} and ${var.schema} so the script can create sec.encrypt_pci (and sec.decrypt_pci) in the same catalog/schema used by the pipelines.

    - Ensures PCI encryption functions exist before any PCI pipeline runs.
    - Encrypted PCI columns are stored as base64-encoded strings (not raw BINARY) for ease of inspection/debugging.

----

## conf/personal_onboarding.json

PCI-specific config

**In bronze_table_properties:**

```
"bronze_table_properties": {
  "pipelines.reset.allowed": "true",
  "delta.columnMapping.mode": "name",
  "delta.checkpointRetentionDuration": "30 days",
  "delta.deletedFileRetentionDuration": "30 days",
  "delta.logRetentionDuration": "30 days",
  "pci": "True",
  "pci_columns": "credit_card_number,cvv"
}
```

- pci: "True" – flags this data flow as PCI.
- pci_columns: "credit_card_number,cvv" – tells the custom transform which columns to encrypt.

----

## src/bronze_pci_encrypt

- Reads pci / pci_columns from dataflow_spec.tableProperties.
  - if pci=False then no encryption
  - if pci=True then encrypts the columns given under pci_columns
- Reads catalog / database from dataflow_spec.targetDetails.
- Calls {catalog}.{schema}.encrypt_pci(col) for each PCI column.