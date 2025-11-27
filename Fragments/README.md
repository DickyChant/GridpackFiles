# Fragments

This directory contains reusable generator fragment components used to build complete generator configurations.

## Structure

```
Fragments/
├── Filter/          # Event filter configurations
├── Generator/       # External LHE producer configurations
├── PartonShower/    # Parton shower (hadronizer) settings
├── NewTests/        # Test fragment configurations
└── imports.json     # Tune import path mappings
```

## Directory Contents

### Filter/
Contains event filter configuration files (`.dat`) for selecting specific event topologies:
- Lepton filters (e.g., `AtLeastOneE.dat`, `AtLeastOneMu.dat`)
- LHE-level filters (e.g., `LHE_V_Pt*_filter.dat`, `LHE_Gamma_Pt*_filter.dat`)

### Generator/
Contains External LHE Producer configurations:
- `ExternalLHEProducer_MadGraph5_aMCatNLO.dat`
- `ExternalLHEProducer_Powheg.dat`

### PartonShower/
Contains Pythia8 parton shower and hadronization settings:
- `amcatnlo-pythia8.dat` - NLO matching
- `amcatnloFXFX-pythia8.dat` - FxFx merging
- `madgraphMLM-pythia8.dat` - MLM matching
- `PowhegEmissionVetoPythia8.dat` - Powheg emission veto

### NewTests/
Contains test fragment configurations for development and validation.

### imports.json
Maps tune names to their CMSSW configuration import paths:
```json
{
  "tune": {
    "CP5": "Configuration.Generator.MCTunesRun3ECM13p6TeV.PythiaCP5Settings_cfi",
    ...
  }
}
```

## Usage

These fragments are assembled by `Misc/build_fragment.py` to create complete generator configurations.
