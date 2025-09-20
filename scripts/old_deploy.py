import pathlib

import wandb
from example_policies.robot_deploy import policy_loader
from example_policies.robot_deploy.deploy import deploy_policy
from example_policies.robot_deploy.robot_io.robot_interface import (
    RobotClient,
)

# CHECKPOINT_DIR = pathlib.Path("outputs/mh2_ckp_step_1_and_2/100000/pretrained_model")
CHECKPOINT_DIR = pathlib.Path("outputs/vastai/125000/pretrained_model")
CHECKPOINT_DIR_2 = pathlib.Path("outputs/mh2_ckp_step_2_tcp/075000/pretrained_model")
CHECKPOINT_DIR_3 = pathlib.Path("outputs/mh2_ckp_step_3_tcp/115000/pretrained_model")

wandb_checkpoint_path = None
# data/output/checkpoints/last/pretrained_model
if wandb_checkpoint_path:
    last_checkpoint_path = pathlib.Path(wandb_checkpoint_path) / "checkpoints" / "last"
    run = wandb.init()
    artifact = run.use_artifact("jc-cj/uncategorized/060000:v0", type="dataset")
    artifact.download(root=str(last_checkpoint_path))

# TODO: Change to the robot's IP address.
SERVER_ENDPOINT = "192.168.0.207:50051"

# Inference frequency in Hz. Higher values result in smoother but potentially faster movements.
INFERENCE_FREQUENCY_HZ: float = 5.0

print(f"Attempting to load policy 1 from: {CHECKPOINT_DIR}")
print(f"Attempting to load policy 2 from: {CHECKPOINT_DIR_2}")
print(f"Robot server endpoint: {SERVER_ENDPOINT}")
print(f"Inference frequency: {INFERENCE_FREQUENCY_HZ} Hz")


policy1, cfg1 = policy_loader.load_policy(CHECKPOINT_DIR)
policy2, cfg2 = policy_loader.load_policy(CHECKPOINT_DIR_2)
policy3, cfg3 = policy_loader.load_policy(CHECKPOINT_DIR_3)

print("✅ Both policies loaded successfully!")


# Change the device on both configs, not the policies!!
cfg1.device = "cuda"
cfg2.device = "cuda"
cfg3.device = "cuda"
policy1.to(cfg1.device)  # or "cpu"
policy2.to(cfg2.device)  # or "cpu"
policy3.to(cfg3.device)  # or "cpu"
policy1.n_action_steps = 10  # Number of actions to predict in each forward pass
policy2.n_action_steps = 10  # Number of actions to predict in each forward pass
policy3.n_action_steps = 10  # Number of actions to predict in each forward pass


deploy_policy(
    policy1,
    # policy2=policy2,
    cfg1=cfg1,
    # cfg2=cfg2,
    hz=INFERENCE_FREQUENCY_HZ,
    server=SERVER_ENDPOINT,
)
