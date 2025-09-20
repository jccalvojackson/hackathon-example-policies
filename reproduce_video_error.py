#!/usr/bin/env python3
"""
Minimal script to reproduce the torchcodec video decoding error.
"""

import argparse
from pathlib import Path

import torch
from lerobot.datasets.lerobot_dataset import LeRobotDataset


def main():
    parser = argparse.ArgumentParser(description="Reproduce video decoding error")
    parser.add_argument(
        "--dataset",
        type=Path,
        required=True,
        help="Path to the dataset directory that contains corrupted videos",
    )
    parser.add_argument(
        "--episode", type=int, default=0, help="Episode index to process (default: 0)"
    )
    args = parser.parse_args()

    print(f"Loading dataset from: {args.dataset}")

    # Load the dataset
    dataset = LeRobotDataset(
        repo_id=args.dataset,
        root=args.dataset,
    )

    print(f"Dataset loaded with {len(dataset)} samples")

    # Create dataloader - this is where the error occurs
    dataloader = torch.utils.data.DataLoader(
        dataset,
        num_workers=8,  # Multiple workers can trigger the error
        batch_size=1,
        shuffle=False,
        pin_memory=False,
        drop_last=False,
    )

    print("Starting iteration through dataloader...")

    ep = args.episode
    found_any = False
    batch_count = 0

    try:
        for batch in dataloader:
            batch_count += 1

            # Check episode index (matching validate_with_plot.py logic)
            b_ep = batch.get("episode_index")
            if b_ep is None:
                raise KeyError("Expected key 'episode_index' in batch.")
            b_ep = int(b_ep.view(-1)[0].item())

            print(f"Processing batch {batch_count}, episode: {b_ep}")

            if b_ep < ep:
                continue
            if b_ep > ep:
                break

            found_any = True
            print(f"✅ Found target episode {ep}")

            # Print available keys for debugging
            print(f"  - Available keys: {list(batch.keys())}")

            # Access more data fields that might trigger video decoding
            try:
                if "observation.images.cam_high" in batch:
                    print(
                        f"  - Image data shape: {batch['observation.images.cam_high'].shape}"
                    )
                if "action" in batch:
                    print(f"  - Action data shape: {batch['action'].shape}")
                if "timestamp" in batch:
                    print(f"  - Timestamp: {batch['timestamp'].item()}")

                # Try to access all image observations which might trigger video loading
                for key in batch.keys():
                    if "observation.images" in key and hasattr(batch[key], "shape"):
                        print(f"  - {key} shape: {batch[key].shape}")

            except Exception as access_error:
                print(f"  - Error accessing batch data: {access_error}")
                raise  # Re-raise to trigger the outer exception handler

        if not found_any:
            print(f"❌ Never found episode {ep} in dataset")

    except RuntimeError as e:
        print(f"\n🔥 REPRODUCED ERROR: {e}")
        print("\nThis error occurs when:")
        print("1. Video files in the dataset are corrupted")
        print("2. torchcodec cannot decode the video frames")
        print("3. The DataLoader worker process crashes")

        return 1

    print("✅ No error encountered - videos seem to be valid")
    return 0


if __name__ == "__main__":
    exit(main())
