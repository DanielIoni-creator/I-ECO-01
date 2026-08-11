# Vital Signs Monitor — Issue #58 bounty (3 XMR)

Deterministic, dependency-free vital signs monitoring for the MyZubster
nurse robot. Lives next to the legacy stub at
`robots/nurse/monitor/vital_monitor.py` and is fully additive: the existing
file is untouched so this module coexists with any in-flight replacement
PR on the same issue.

## What's included

| File | Purpose |
|------|---------|
| `robots/nurse/vital_signs/__init__.py` | Public re-exports |
| `robots/nurse/vital_signs/monitor.py` | `VitalSignsMonitor` + sensor fusion, alarm manager, dashboard snapshot, hash-chained audit log |
| `robots/nurse/vital_signs/test_vital_signs.py` | 17 unit tests (stdlib `unittest`, pure, deterministic) |
| `robots/nurse/vital_signs/demo.py` | Runnable demo that ingests three patients and prints the dashboard payload |

## Public surface

```python
from robots.nurse.vital_signs import (
    VitalSignsMonitor,
    SensorFusion,
    VitalThresholds,
    AlarmManager,
    DashboardSnapshot,
    BlockchainAuditLog,
)

fusion = SensorFusion(reader=lambda pid: samples[pid])  # plug real GPIO here
monitor = VitalSignsMonitor(
    fusion=fusion,
    alarm_manager=AlarmManager(thresholds=VitalThresholds(max_heart_rate=120, min_spo2=94)),
)
alarm = monitor.ingest("P001")
print(monitor.dashboard().to_json())
```

## Acceptance mapping (issue #58)

| Deliverable | Coverage |
|-------------|----------|
| Integrare sensori (Heart Rate, SpO2, Temperatura) | `SensorFusion.capture()` validates HR / SpO2 / temperature |
| Dashboard in tempo reale | `DashboardSnapshot.render()` / `.to_json()` |
| Allarmi configurabili | `VitalThresholds` + `AlarmManager.evaluate()` |
| Logging dati su blockchain | `BlockchainAuditLog` (SHA-256 hash chain, `verify()`) |

## Run the tests

```bash
cd robots/nurse/vital_signs
python -m unittest test_vital_signs.py -v
```

Expected: `Ran 17 tests in 0.001s — OK`.

## Run the demo

```bash
cd robots/nurse/vital_signs
python demo.py
```

The demo ingests three synthetic patients, raises a tachycardia alarm
on the second, and prints the resulting dashboard JSON plus audit chain
verification status.

## Payout

Per the bounty terms, payment is requested in **Monero (XMR)** on mainnet:

```
46o6gz4Pzn8edEsjgL15jkRzPEakEYefGPoM6nbDqmegDL2GrHxtUonLbKKB7vQEhoWdaAqbNG26She7kaPmkBrxU5ofG8x
```

Address shape (95 characters, network prefix `4`, valid checksum) matches
the configured public Monero receive route in `PUBLIC_PAYOUT_PROFILE.md`.