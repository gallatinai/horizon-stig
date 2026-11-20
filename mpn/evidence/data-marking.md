# Data marking of Horizon output

Release 2026.45.4-uds.1, commit b84b9af. Read 2026-11-20 (horizon-data-marking-table).

| Status | Count |
|---|---|
| Output paths with a marking | 0 |
| Output paths without a marking | 10 |

Check requirement: top and bottom marking on screens and reports. Where no classification document exists, the highest classification of the system.

| Output path | Marking today | Required by the check |
|---|---|---|
| Every on-screen page | none | Top and bottom of the screen |
| Branch reports panel | none | Top and bottom of the report |
| Patient movement SITREP, Export .txt | none | Top and bottom of the report |
| Patient movement SITREP, Copy Markdown | none | Top and bottom of the report |
| File download | none added; the uploaded bytes are returned unchanged | Highest classification of the system |
| Chat web artifact | none | Top and bottom of the screen |
| Browser print of any page | none; no print stylesheet or print call | Top and bottom of the page |
| API responses | none | Highest classification of the system |
| Command line output | none | Highest classification of the system |
| Map coordinate copy | none | Highest classification of the system |
