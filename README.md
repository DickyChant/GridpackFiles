# Gridpack Files

Repository to store cards and job metadata for the Gridpack Machine.

## Directory Structure

### `Cards/`
Contains time-independent input files organized by generator and process.

```
Cards/
├── MadGraph5_aMCatNLO/   # MadGraph5 generator cards
│   ├── DY/              # Drell-Yan processes
│   ├── GJ/              # Gamma+Jets processes
│   ├── QCD/             # QCD processes
│   └── ...
└── Powheg/              # Powheg generator cards
    ├── DY/
    ├── TT/
    └── ...
```

Each process directory contains dataset subdirectories with:
- `<dataset>.json` - Configuration file with model parameters, templates, and fragment settings
- `<dataset>_proc_card.dat` - Process card for the generator

### `Campaigns/`
Contains time-dependent metadata about production campaigns (e.g., Run3Summer22, Run3Summer23).

```
Campaigns/
├── Run3Summer22/
│   ├── Run3Summer22.json       # Campaign configuration
│   ├── MadGraph5_aMCatNLO/
│   │   ├── ModelParams/        # Model parameter files
│   │   └── Templates/          # Run card templates
│   └── Powheg/
└── Run3Summer23/
    └── ...
```

### `Fragments/`
Contains reusable generator fragment components.

```
Fragments/
├── Filter/          # Filter configuration files (.dat)
├── Generator/       # External LHE producer configurations
├── PartonShower/    # Parton shower settings (e.g., Pythia8)
├── NewTests/        # Test fragment configurations
└── imports.json     # Tune import mappings
```

### `Misc/`
Contains utility scripts for building and managing gridpack files.

- `build_fragment.py` - Build generator fragments from templates
- `check.py` - Validate JSON configuration files in Cards/
- `make_cards.py` - Create new card directories from skeleton templates
- `Skeletons/` - Template files for new card creation

### `Validation/`
Contains scripts for local validation and McM interaction.

- `submit_jobs.py` - Submit validation jobs locally
- `parse_jobs.py` - Parse job logs and extract validation results
- `forge_prepids.py` - Edit/clone McM prepids with validation results
- `makeDirs.py` - Create directory structure in EOS area
- See [Validation/README.md](Validation/README.md) for detailed usage instructions

## Quick Start

### Creating New Cards
```bash
cd Misc
python3 make_cards.py Cards/MadGraph5_aMCatNLO/<Process>/<DatasetName>
```

### Validating Card Configuration
```bash
cd Misc
python3 check.py
```

### Building Fragments
```bash
cd Misc
python3 build_fragment.py -p <process> -n <datasetName> -d <directory> -e <beamEnergy> -t <tune>
```

## Contributing

When adding new datasets:
1. Create a new directory under the appropriate `Cards/<Generator>/<Process>/` path
2. Add the required JSON configuration and proc_card files
3. Run `check.py` to validate your configuration
