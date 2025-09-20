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

    try:
        for i, batch in enumerate(dataloader):
            print(f"Processing batch {i}")

            # Check episode index
            if "episode_index" in batch:
                ep_idx = int(batch["episode_index"].view(-1)[0].item())
                print(f"Episode index: {ep_idx}")

                if ep_idx == args.episode:
                    print(f"Found target episode {args.episode}")
                elif ep_idx > args.episode:
                    print(f"Reached episode {ep_idx}, stopping")
                    break

            # The error typically occurs here when trying to access video data
            if i > 10:  # Limit iterations for testing
                print("Processed 10 batches successfully, stopping")
                break

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
