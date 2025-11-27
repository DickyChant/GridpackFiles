# Misc

This directory contains utility scripts for building and managing gridpack files.

## Scripts

### build_fragment.py
Builds complete generator fragments from templates and configuration files.

```bash
python3 build_fragment.py -p <process> -n <datasetName> -d <directory> -e <beamEnergy> -t <tune> [--lhe] [--concurrent]
```

**Arguments:**
- `-p, --process` - Process name (e.g., `DY`)
- `-n, --datasetName` - Dataset name (e.g., `DYto2L-2Jets_MLL-50_amcatnloFXFX-pythia8`)
- `-d, --directory` - Generator directory (e.g., `MadGraph5_aMCatNLO`)
- `-e, --beamEnergy` - Beam energy in GeV (e.g., `6800`)
- `-t, --tune` - Pythia tune (e.g., `CP5`)
- `--lhe` - Include ExternalLHEProducer (optional)
- `--concurrent` - Enable concurrent processing (optional)

### check.py
Validates JSON configuration files in the `Cards/` directory.

```bash
python3 check.py
```

Checks for:
- Missing required attributes (`model_params`, `template`, `fragment`)
- Invalid attribute types
- Unknown attributes

### make_cards.py
Creates new card directories from skeleton templates.

```bash
python3 make_cards.py Cards/MadGraph5_aMCatNLO/<Process>/<DatasetName>
```

Creates a new directory with:
- `<dataset>.json` - Configuration template
- `<dataset>_proc_card.dat` - Process card template
- `<dataset>_madspin_card.dat` - Madspin card (if applicable)

## Skeletons/

Contains template files for creating new cards:

```
Skeletons/
└── MadGraph5_aMCatNLO/
    ├── skeleton.json
    ├── skeleton_proc_card.dat
    └── skeleton_madspin_card.dat
```
