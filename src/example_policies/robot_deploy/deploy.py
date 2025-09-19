# Copyright 2025 Poke & Wiggle GmbH. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import threading
import time
from pathlib import Path

import grpc
import torch

from example_policies.robot_deploy.action_translator import ActionTranslator
from example_policies.robot_deploy.debug_helpers.utils import print_info
from example_policies.robot_deploy.policy_loader import load_policy
from example_policies.robot_deploy.robot_io.robot_interface import RobotInterface
from example_policies.robot_deploy.robot_io.robot_service import (
    robot_service_pb2,
    robot_service_pb2_grpc,
)
from example_policies.robot_deploy.utils import print_info
from example_policies.robot_deploy.utils.action_mode import ActionMode


def keyboard_listener(switch_flag):
    """Listen for space bar press to switch policies."""
    try:
        import sys
        import termios
        import tty

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        tty.setraw(sys.stdin.fileno())

        while not switch_flag["done"]:
            char = sys.stdin.read(1)
            if char == " " and not switch_flag["switched"]:
                switch_flag["switched"] = True
                print("\n🔄 Switching to Policy 2!")
                break

        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    except ImportError:
        # Fallback for systems without termios
        while not switch_flag["done"]:
            input_char = input()
            if input_char == "" and not switch_flag["switched"]:  # Enter key
                switch_flag["switched"] = True
                print("\n🔄 Switching to Policy 2!")
                break


def inference_loop(
    policy1,
    policy2,
    cfg,
    hz: float,
    service_stub: robot_service_pb2_grpc.RobotServiceStub,
):
    # Start with policy 1
    current_policy = policy1

    robot_interface = RobotInterface(service_stub, cfg)
    model_to_action_trans = ActionTranslator(cfg)
    dbg_printer = print_info.InfoPrinter(cfg)

    step = 0
    done = False

    # Set up policy switching
    switch_flag = {"switched": False, "done": False}

    # Start keyboard listener thread
    keyboard_thread = threading.Thread(
        target=keyboard_listener, args=(switch_flag,), daemon=True
    )
    keyboard_thread.start()

    print("🤖 Starting inference loop with Policy 1...")
    print("⌨️  Press SPACE to switch to Policy 2")
    period = 1.0 / hz

    while not done:
        start_time = time.time()

        # Check if we need to switch policies
        if switch_flag["switched"]:
            current_policy = policy2
            print("✅ Successfully switched to Policy 2!")
            switch_flag["switched"] = False  # Prevent multiple switches

        print(current_policy.config.input_features)
        observation = robot_interface.get_observation(cfg.device, show=False)

        if observation:
            # Predict the next action with respect to the current observation
            with torch.inference_mode():
                action = current_policy.select_action(observation)
                print("\n=== RAW MODEL PREDICTION ===")
                dbg_printer.print(step, observation, action, raw_action=True)
                print()
            action = model_to_action_trans.translate(action, observation)

            print("\n=== ABSOLUTE ROBOT COMMANDS ===")
            dbg_printer.print(step, observation, action, raw_action=False)

            print("switched:", switch_flag["switched"])
            robot_interface.send_action(action, model_to_action_trans.action_mode)
            # current_policy._queues["action"].clear()

        # wait for execution to finish
        elapsed_time = time.time() - start_time
        sleep_duration = period - elapsed_time
        print(sleep_duration)
        # wait for input
        # input("Press Enter to continue...")
        time.sleep(max(0.0, sleep_duration))

        step += 1

    # Clean up
    switch_flag["done"] = True


def main():
    parser = argparse.ArgumentParser(description="Robot service client")
    parser.add_argument(
        "--checkpoint",
        type=Path,
        required=True,
        help="Path to the policy checkpoint directory.",
    )

    parser.add_argument(
        "--server",
        default="localhost:50051",
        help="Robot service server address (default: localhost:50051)",
    )
    args = parser.parse_args()

    # Select your device
    device = "cpu" if not torch.cuda.is_available() else "cuda"

    policy, cfg = load_policy(args.checkpoint)
    policy.to(device)

    deploy_single_policy(policy, cfg, hz=1.5, server=args.server)


def deploy_single_policy(policy, cfg, hz: float, server: str):
    """Deploy a single policy (for command-line usage)."""
    channel = grpc.insecure_channel(server)
    stub = robot_service_pb2_grpc.RobotServiceStub(channel)
    try:
        # Simple inference loop for single policy
        robot_interface = RobotInterface(stub, cfg)
        model_to_action_trans = ActionTranslator(cfg)
        step = 0
        period = 1.0 / hz

        print("🤖 Starting single policy inference loop...")

        while True:
            start_time = time.time()
            observation = robot_interface.get_observation(cfg.device, show=False)

            if observation:
                with torch.inference_mode():
                    action = policy.select_action(observation)
                action = model_to_action_trans.translate(action, observation)
                robot_interface.send_action(action, model_to_action_trans.action_mode)

            elapsed_time = time.time() - start_time
            time.sleep(max(0.0, period - elapsed_time))
            step += 1

    except KeyboardInterrupt:
        print("Stopping...")
    except Exception as e:
        print(f"Error occurred: {e}")
        raise e
    finally:
        channel.close()
        print("Connection closed.")


def deploy_policy(policy1, policy2, cfg, hz: float, server: str):
    channel = grpc.insecure_channel(server)
    stub = robot_service_pb2_grpc.RobotServiceStub(channel)
    try:
        inference_loop(policy1, policy2, cfg, hz, stub)
    except Exception as e:
        print(f"Error occurred: {e}")
        raise e
    finally:
        channel.close()
        print("Connection closed.")


if __name__ == "__main__":
    main()
