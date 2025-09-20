from lerobot.datasets.lerobot_dataset import LeRobotDataset

from example_policies import lerobot_patches

lerobot_patches.apply_patches()


repo_id = "jccj/debug"
dataset = LeRobotDataset(
    repo_id=repo_id,
    root="data/lerobot/debug_data",
).push_to_hub()
