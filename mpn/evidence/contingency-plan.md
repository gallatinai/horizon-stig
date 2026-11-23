# Contingency plan: Horizon on MPN

| Item | Value |
|---|---|
| Application | Horizon (StratNav) on MPN |
| Release | 2026.45.4-uds.1 |
| Availability level (high, moderate or low) | |
| Plan owner | |
| Plan approver | |
| Approval date | |

## Recovery provision for the availability level

| Level | Plan provision |
|---|---|
| High: smooth transfer of all mission or business essential functions to an alternate site for the duration of an event with little or no loss of operational continuity | |
| Moderate: resumption of mission or business essential functions within 12 hours activation or as defined in the contingency plan | |
| Low: partial resumption of mission or business essential functions within 5 to 30 days of activation as defined in the contingency plan | |

## Essential mission and business functions

| Function | Contingency requirement |
|---|---|
| | |

## Backup and recovery in release 2026.45.4-uds.1

| Item | Value | Evidence |
|---|---|---|
| Cluster resource backup | Velero, daily at 03:00, retention 240 hours, volume snapshots off | `core-velero` |
| PostgreSQL, NATS and SeaweedFS | 1 replica each; the rendered release holds no backup, schedule or volume snapshot resource for them | `mpn-release-recovery-render` |
| Backup owner | | |
| Date of last restore test | | |
