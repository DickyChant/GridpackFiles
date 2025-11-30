#!/usr/bin/env python3
"""
Gridpack Files Configuration Manager

This script provides centralized management of gridpack file generation
by reading configuration from config.json and performing various operations.

Usage:
    python3 gridpack_manager.py --action <action> [options]

Actions:
    list-generators     List available generators
    list-campaigns      List available campaigns
    list-processes      List available physics processes
    list-tunes          List available tunes
    list-parton-showers List available parton shower configurations
    validate-config     Validate the config.json file
    make-dirs           Create EOS directory structure
    make-cards          Create new card directory from skeleton
    check-cards         Validate all card JSON files
    generate-fragment   Generate a fragment from templates
"""

import os
import sys
import json
import argparse
from pathlib import Path


def load_config(config_path='config.json'):
    """Load the centralized configuration file."""
    script_dir = Path(__file__).parent
    config_file = script_dir / config_path
    
    if not config_file.exists():
        sys.exit(f"ERROR: Config file not found: {config_file}")
    
    with open(config_file) as f:
        return json.load(f)


def list_generators(config):
    """List available generators."""
    print("Available Generators:")
    print("-" * 40)
    for name, info in config['generators'].items():
        print(f"  {name}: {info['description']}")


def list_campaigns(config):
    """List available campaigns."""
    print("Available Campaigns:")
    print("-" * 40)
    for name, info in config['campaigns'].items():
        tune = info.get('tune', 'N/A')
        beam = info.get('beam', 'N/A')
        print(f"  {name}: tune={tune}, beam={beam} GeV")


def list_processes(config):
    """List available physics processes."""
    print("Available Physics Processes:")
    print("-" * 40)
    for process in config['physics_processes']:
        print(f"  {process}")


def list_tunes(config):
    """List available tunes."""
    print("Available Tunes:")
    print("-" * 40)
    for name, import_path in config['tunes'].items():
        print(f"  {name}: {import_path}")


def list_parton_showers(config):
    """List available parton shower configurations."""
    print("Available Parton Shower Configurations:")
    print("-" * 40)
    for name, info in config['parton_showers'].items():
        print(f"  {name}: {info['description']}")


def validate_config(config):
    """Validate the configuration file."""
    errors = []
    warnings = []
    
    # Check required top-level keys
    required_keys = ['paths', 'generators', 'campaigns', 'tunes', 'parton_showers']
    for key in required_keys:
        if key not in config:
            errors.append(f"Missing required key: {key}")
    
    # Validate paths - check all paths used by functions
    if 'paths' in config:
        required_paths = ['cards_dir', 'campaigns_dir', 'fragments_dir', 'skeletons_dir', 'eos_base_path']
        for path_key in required_paths:
            if path_key not in config['paths']:
                errors.append(f"Missing required path: {path_key}")
    
    # Validate dataset_schema has required structure
    if 'dataset_schema' in config:
        schema = config['dataset_schema']
        if 'mandatory_attributes' not in schema:
            errors.append("dataset_schema missing 'mandatory_attributes'")
        if 'optional_attributes' not in schema:
            errors.append("dataset_schema missing 'optional_attributes'")
    else:
        errors.append("Missing dataset_schema in config")
    
    # Validate generators have required fields
    if 'generators' in config:
        for gen_name, gen_info in config['generators'].items():
            if 'description' not in gen_info:
                warnings.append(f"Generator {gen_name} missing description")
    
    # Validate campaigns have required fields
    if 'campaigns' in config:
        for camp_name, camp_info in config['campaigns'].items():
            if 'tune' not in camp_info:
                warnings.append(f"Campaign {camp_name} missing tune")
            if 'beam' not in camp_info:
                warnings.append(f"Campaign {camp_name} missing beam energy")
    
    # Print results
    if errors:
        print("Validation FAILED:")
        for error in errors:
            print(f"  ERROR: {error}")
    
    if warnings:
        print("Warnings:")
        for warning in warnings:
            print(f"  WARNING: {warning}")
    
    if not errors and not warnings:
        print("Configuration is valid!")
    
    return len(errors) == 0


def make_dirs(config, doit=False):
    """Create EOS directory structure based on config."""
    base_path = config['paths']['eos_base_path']
    generators = config['generators'].keys()
    campaigns = config['campaigns'].keys()
    processes = config['physics_processes']
    
    created = []
    for campaign in campaigns:
        for generator in generators:
            for process in processes:
                fullpath = os.path.join(base_path, campaign, generator, process)
                if not os.path.exists(fullpath):
                    created.append(fullpath)
                    print(f"Would create: {fullpath}")
                    if doit:
                        os.makedirs(fullpath, exist_ok=True)
    
    if not created:
        print("All directories already exist.")
    elif not doit:
        print(f"\nRun with --doit to create {len(created)} directories.")


def make_cards(config, generator, process, dataset_name, doit=False):
    """Create new card directory from skeleton templates."""
    if generator not in config['generators']:
        sys.exit(f"ERROR: Unknown generator: {generator}")
    
    cards_dir = config['paths']['cards_dir']
    skeletons_dir = config['paths']['skeletons_dir']
    
    target_path = os.path.join(cards_dir, generator, process, dataset_name)
    skeleton_path = os.path.join(skeletons_dir, generator)
    
    if os.path.exists(target_path):
        sys.exit(f"ERROR: Path already exists: {target_path}")
    
    if not os.path.exists(skeleton_path):
        sys.exit(f"ERROR: Skeleton path not found: {skeleton_path}")
    
    skeleton_files = config['generators'][generator].get('skeleton_files', [])
    
    print(f"Creating card directory: {target_path}")
    for skel_file in skeleton_files:
        src = os.path.join(skeleton_path, skel_file)
        dst_name = skel_file.replace('skeleton', dataset_name)
        dst = os.path.join(target_path, dst_name)
        print(f"  {skel_file} -> {dst_name}")
    
    if doit:
        os.makedirs(target_path, exist_ok=True)
        for skel_file in skeleton_files:
            src = os.path.join(skeleton_path, skel_file)
            dst_name = skel_file.replace('skeleton', dataset_name)
            dst = os.path.join(target_path, dst_name)
            
            with open(src) as f:
                content = f.read()
            
            # Replace $process placeholder with dataset name
            # (legacy naming from original skeleton files)
            content = content.replace('$process', dataset_name)
            
            with open(dst, 'w') as f:
                f.write(content)
        
        print(f"Card directory created: {target_path}")
    else:
        print("\nRun with --doit to create the directory.")


def check_cards(config):
    """Validate all card JSON files."""
    if 'dataset_schema' not in config:
        print("ERROR: Missing dataset_schema in config")
        return False
    
    schema = config['dataset_schema']
    if 'mandatory_attributes' not in schema or 'optional_attributes' not in schema:
        print("ERROR: dataset_schema missing required keys")
        return False
    
    mandatory_keys = set(schema['mandatory_attributes'].keys())
    optional_keys = set(schema['optional_attributes'].keys())
    
    cards_dir = config['paths']['cards_dir']
    errors = 0
    checked = 0
    
    for generator in config['generators'].keys():
        gen_path = os.path.join(cards_dir, generator)
        if not os.path.exists(gen_path):
            continue
        
        for process in os.listdir(gen_path):
            process_path = os.path.join(gen_path, process)
            if not os.path.isdir(process_path):
                continue
            
            for dataset in os.listdir(process_path):
                dataset_path = os.path.join(process_path, dataset)
                if not os.path.isdir(dataset_path):
                    continue
                
                json_path = os.path.join(dataset_path, f'{dataset}.json')
                if not os.path.isfile(json_path):
                    print(f"MISSING: {json_path}")
                    errors += 1
                    continue
                
                checked += 1
                try:
                    with open(json_path) as f:
                        data = json.load(f)
                    
                    attributes = set(data.keys())
                    missing = mandatory_keys - attributes
                    unknown = attributes - mandatory_keys - optional_keys
                    
                    if missing:
                        print(f"MISSING KEYS in {json_path}: {', '.join(missing)}")
                        errors += 1
                    
                    if unknown:
                        print(f"UNKNOWN KEYS in {json_path}: {', '.join(unknown)}")
                
                except json.JSONDecodeError as e:
                    print(f"JSON ERROR in {json_path}: {e}")
                    errors += 1
    
    print(f"\nChecked {checked} card files, found {errors} errors.")
    return errors == 0


def get_tune_import(config, tune_name):
    """Get the import path for a tune."""
    if tune_name not in config['tunes']:
        sys.exit(f"ERROR: Unknown tune: {tune_name}")
    return config['tunes'][tune_name]


def get_campaign_config(config, campaign_name):
    """Get configuration for a specific campaign."""
    if campaign_name not in config['campaigns']:
        sys.exit(f"ERROR: Unknown campaign: {campaign_name}")
    return config['campaigns'][campaign_name]


def main():
    parser = argparse.ArgumentParser(
        description='Gridpack Files Configuration Manager',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument('--action', '-a', required=True,
                        choices=['list-generators', 'list-campaigns', 'list-processes',
                                 'list-tunes', 'list-parton-showers', 'validate-config',
                                 'make-dirs', 'make-cards', 'check-cards'],
                        help='Action to perform')
    parser.add_argument('--config', '-c', default='config.json',
                        help='Path to config file (default: config.json)')
    parser.add_argument('--doit', action='store_true',
                        help='Actually perform the action (for make-dirs, make-cards)')
    parser.add_argument('--generator', '-g',
                        help='Generator name (for make-cards)')
    parser.add_argument('--process', '-p',
                        help='Process name (for make-cards)')
    parser.add_argument('--dataset', '-d',
                        help='Dataset name (for make-cards)')
    
    args = parser.parse_args()
    
    config = load_config(args.config)
    
    if args.action == 'list-generators':
        list_generators(config)
    elif args.action == 'list-campaigns':
        list_campaigns(config)
    elif args.action == 'list-processes':
        list_processes(config)
    elif args.action == 'list-tunes':
        list_tunes(config)
    elif args.action == 'list-parton-showers':
        list_parton_showers(config)
    elif args.action == 'validate-config':
        sys.exit(0 if validate_config(config) else 1)
    elif args.action == 'make-dirs':
        make_dirs(config, doit=args.doit)
    elif args.action == 'make-cards':
        if not all([args.generator, args.process, args.dataset]):
            sys.exit("ERROR: make-cards requires --generator, --process, and --dataset")
        make_cards(config, args.generator, args.process, args.dataset, doit=args.doit)
    elif args.action == 'check-cards':
        sys.exit(0 if check_cards(config) else 1)


if __name__ == '__main__':
    main()
