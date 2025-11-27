# Cards

This directory contains generator input cards organized by generator type and physics process.

## Structure

```
Cards/
├── MadGraph5_aMCatNLO/    # MadGraph5_aMC@NLO generator cards
│   ├── DY/                # Drell-Yan processes
│   ├── GJ/                # Gamma+Jets processes
│   ├── QCD/               # QCD multijet processes
│   ├── SingleT/           # Single top processes
│   ├── TT/                # Top pair processes
│   └── ...
└── Powheg/                # Powheg generator cards
    ├── DY/
    ├── TT/
    └── ...
```

## Dataset Directory Contents

Each dataset directory (e.g., `DYto2L-2Jets_MLL-50_amcatnloFXFX-pythia8/`) contains:

- `<dataset>.json` - Configuration file with:
  - `model_params` - Reference to model parameter file
  - `template` - Reference to run card template  
  - `fragment` - Pythia8 process parameters
  - Optional: `fragment_filter`, `model_params_vars`, `template_vars`

- `<dataset>_proc_card.dat` - MadGraph process card defining the physics process

## Creating New Cards

Use the skeleton templates in `Misc/Skeletons/` to create new card directories:

```bash
cd Misc
python3 make_cards.py Cards/MadGraph5_aMCatNLO/<Process>/<DatasetName>
```

## Validation

Run the check script to validate all card configurations:

```bash
cd Misc
python3 check.py
```
