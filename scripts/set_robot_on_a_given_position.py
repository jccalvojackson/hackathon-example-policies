from dataclasses import dataclass

import grpc
import numpy as np
import torch

from example_policies.robot_deploy.action_translator import ActionMode, ActionTranslator
from example_policies.robot_deploy.robot_io.robot_client import RobotClient
from example_policies.robot_deploy.robot_io.robot_interface import (
    RobotInterface,
)
from example_policies.robot_deploy.robot_io.robot_service import (
    robot_service_pb2,
    robot_service_pb2_grpc,
)


@dataclass
class DummyConfig:
    metadata = None


def main(server: str, action: torch.Tensor):
    channel = grpc.insecure_channel(server)
    stub = robot_service_pb2_grpc.RobotServiceStub(channel)
    # prepare_request = robot_service_pb2.PrepareExecutionRequest()
    # prepare_request.execution_mode = (
    #     robot_service_pb2.ExecutionMode.EXECUTION_MODE_CARTESIAN_TARGET_QUEUE
    # )
    # stub.PrepareExecution(prepare_request)
    cfg = DummyConfig()
    robot_interface = RobotInterface(stub, cfg)
    robot_interface.send_action(action, ActionMode.ABS_TCP)


if __name__ == "__main__":
    SERVER_ENDPOINT = "192.168.0.207:50051"
    tcp_torch_step_1 = torch.tensor(
        [
            -0.22568389773368835,
            0.745937705039978,
            0.3866482377052307,
            0.04157385602593422,
            0.954410970211029,
            0.09571849554777145,
            0.27965912222862244,
            0.2665419578552246,
            0.7410882711410522,
            0.3717521131038666,
            0.004377448465675116,
            -0.937037467956543,
            -0.05347206071019173,
            0.345083087682724,
            0,
            0,
        ]
    )[None, :]
    tcp_torch_step_2 = torch.tensor(
        [
            -0.39821743965148926,
            0.7588139772415161,
            0.45840808749198914,
            0.018458731472492218,
            0.9588937163352966,
            0.06460884213447571,
            0.27569523453712463,
            0.12317447364330292,
            0.7276370525360107,
            0.4175536334514618,
            -0.04559018462896347,
            -0.9448632001876831,
            -0.0346456877887249,
            0.322420209646225,
            0,
            0,
        ]
    )[None, :]

    tcp_torch_step_3 = torch.tensor(
        [
            -0.3581012189388275,
            0.7647845149040222,
            0.42845311760902405,
            0.00610016006976366,
            0.965373158454895,
            0.041757140308618546,
            0.25743696093559265,
            0.07413417845964432,
            0.763433039188385,
            0.41522377729415894,
            -0.069739431142807,
            -0.9292187094688416,
            -0.029516272246837616,
            0.3616873621940613,
            0,
            0,
        ]
    )[None, :]
    main(SERVER_ENDPOINT, tcp_torch_step_3)
