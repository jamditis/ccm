#!/usr/bin/env python3
"""
Recovery Data Merge Script

Merges recovered video processing results from the recovery directory
into the main results directory, updating checkpoints accordingly.

Usage:
    python scripts/merge_recovery.py

This script:
1. Validates recovery data exists and is complete
2. Backs up existing main results
3. Merges batch files from recovery to main
4. Updates checkpoint.json with merged totals
5. Generates a merge report
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path


def load_json(filepath):
    """Load JSON file with error handling."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing {filepath}: {e}")
        return None


def save_json(filepath, data):
    """Save data to JSON file."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def merge_recovery_data():
    """Main merge function."""
    # Paths
    base_dir = Path(__file__).parent.parent
    recovery_dir = base_dir / 'analysis' / 'video_results_recovery'
    main_dir = base_dir / 'analysis' / 'video_results_with_costs'
    checkpoint_path = base_dir / 'checkpoint.json'
    backup_dir = base_dir / 'analysis' / 'backup_before_merge'

    print("=" * 60)
    print("Recovery Data Merge Script")
    print("=" * 60)

    # Check if recovery directory exists
    if not recovery_dir.exists():
        print(f"\nNo recovery directory found at: {recovery_dir}")
        print("Nothing to merge. Exiting.")
        return False

    # Check if main directory exists
    if not main_dir.exists():
        print(f"\nMain results directory not found at: {main_dir}")
        print("Please run video processing first. Exiting.")
        return False

    # List recovery files
    recovery_batches = list(recovery_dir.glob('batch_*.json'))
    if not recovery_batches:
        print(f"\nNo batch files found in recovery directory.")
        print("Nothing to merge. Exiting.")
        return False

    print(f"\nFound {len(recovery_batches)} recovery batch files to merge.")

    # Create backup
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = backup_dir / timestamp

    print(f"\nCreating backup at: {backup_path}")
    shutil.copytree(main_dir, backup_path)
    print("Backup created successfully.")

    # Merge batch files
    merged_count = 0
    skipped_count = 0

    for batch_file in sorted(recovery_batches):
        dest_file = main_dir / batch_file.name

        if dest_file.exists():
            # Compare file sizes to detect potential conflicts
            src_size = batch_file.stat().st_size
            dest_size = dest_file.stat().st_size

            if src_size != dest_size:
                print(f"  Overwriting {batch_file.name} (recovery: {src_size}B, main: {dest_size}B)")
            else:
                print(f"  Skipping {batch_file.name} (identical)")
                skipped_count += 1
                continue

        shutil.copy2(batch_file, dest_file)
        merged_count += 1
        print(f"  Merged {batch_file.name}")

    # Copy influencer directories
    influencer_dirs = [d for d in recovery_dir.iterdir() if d.is_dir()]
    for inf_dir in influencer_dirs:
        dest_inf_dir = main_dir / inf_dir.name

        if dest_inf_dir.exists():
            # Merge contents
            for item in inf_dir.iterdir():
                dest_item = dest_inf_dir / item.name
                if item.is_file():
                    shutil.copy2(item, dest_item)
        else:
            shutil.copytree(inf_dir, dest_inf_dir)

        print(f"  Merged influencer directory: {inf_dir.name}")

    # Update checkpoint
    checkpoint = load_json(checkpoint_path)
    if checkpoint:
        # Count total videos in recovery
        recovery_video_count = 0
        for batch_file in recovery_batches:
            batch_data = load_json(batch_file)
            if batch_data and 'videos' in batch_data:
                recovery_video_count += len(batch_data['videos'])

        old_total = checkpoint.get('total_processed', 0)
        checkpoint['total_processed'] = old_total + recovery_video_count
        checkpoint['last_merge'] = datetime.now().isoformat()
        checkpoint['merge_details'] = {
            'recovery_videos': recovery_video_count,
            'batches_merged': merged_count,
            'batches_skipped': skipped_count
        }

        save_json(checkpoint_path, checkpoint)
        print(f"\nCheckpoint updated: {old_total} -> {checkpoint['total_processed']} videos")

    # Generate merge report
    report = {
        'timestamp': datetime.now().isoformat(),
        'batches_merged': merged_count,
        'batches_skipped': skipped_count,
        'influencer_dirs_merged': len(influencer_dirs),
        'backup_location': str(backup_path),
        'status': 'success'
    }

    report_path = main_dir / f'merge_report_{timestamp}.json'
    save_json(report_path, report)

    print("\n" + "=" * 60)
    print("Merge Complete!")
    print("=" * 60)
    print(f"  Batches merged: {merged_count}")
    print(f"  Batches skipped: {skipped_count}")
    print(f"  Backup saved to: {backup_path}")
    print(f"  Report saved to: {report_path}")
    print("\nYou can now delete the recovery directory if desired:")
    print(f"  rm -rf {recovery_dir}")

    return True


if __name__ == '__main__':
    merge_recovery_data()
