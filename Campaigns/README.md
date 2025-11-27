# Campaigns

This directory contains time-dependent metadata about Monte Carlo production campaigns.

## Structure

```
Campaigns/
├── Run3Summer22/
│   ├── Run3Summer22.json       # Campaign configuration
│   ├── MadGraph5_aMCatNLO/
│   │   ├── ModelParams/        # Model parameter files (massW.dat, massZ.dat)
│   │   └── Templates/          # Run card templates (LO/NLO)
│   └── Powheg/
│       ├── ModelParams/
│       └── Templates/
├── Run3Summer23/
├── Run3Winter22/
├── RunIII2024Summer24/
└── RunIISummer20UL16/
```

## Campaign Configuration

Each campaign has a `<Campaign>.json` file containing:

```json
{
    "chain": "chain_Run3Summer22wmLHEGS_flow...",
    "model_params_vars": {},
    "template_vars": {},
    "fragment_vars": {
        "concurrentLHEforMadGraph5_aMCatNLO": "False",
        "concurrentLHEforPowheg": "True",
        "concurrentPS": "Concurrent"
    },
    "tune": "CP5",
    "beam": 6800,
    "gridpack_directory": "/eos/cms/store/group/phys_generator/cvmfs/gridpacks/PdmV/Run3Summer22"
}
```

**Fields:**
- `chain` - McM chain name for the production workflow
- `tune` - Pythia tune to use (e.g., CP5)
- `beam` - Beam energy in GeV
- `gridpack_directory` - EOS path for gridpack storage
- `fragment_vars` - Variables for fragment generation
- `model_params_vars` / `template_vars` - Variable overrides

## Templates

### ModelParams/
Contains model parameter files defining particle masses and widths:
- `massW.dat` - W boson mass parameters
- `massZ.dat` - Z boson mass parameters

### Templates/
Contains run card templates:
- `LO_run_card.dat` - Leading order run card
- `NLO_run_card.dat` - Next-to-leading order run card
