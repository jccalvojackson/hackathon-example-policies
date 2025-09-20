from lerobot.datasets.lerobot_dataset import LeRobotDataset

from example_policies import lerobot_patches

lerobot_patches.apply_patches()


repo_id = "jccj/step_1_2_3_tcp_one_hot"
dataset = LeRobotDataset(
    repo_id=repo_id,
    root="data/lerobot/step_1_2_3_tcp_one_hot",
).push_to_hub()
