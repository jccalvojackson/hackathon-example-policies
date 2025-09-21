from dataclasses import dataclass
from time import sleep

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


def main(
    server: str,
    action: torch.Tensor,
):
    channel = grpc.insecure_channel(server)
    stub = robot_service_pb2_grpc.RobotServiceStub(channel)
    # prepare_request = robot_service_pb2.PrepareExecutionRequest()
    # prepare_request.execution_mode = (
    #     robot_service_pb2.ExecutionMode.EXECUTION_MODE_CARTESIAN_TARGET_QUEUE
    # )
    # stub.PrepareExecution(prepare_request)
    cfg = DummyConfig()
    robot_interface = RobotInterface(stub, cfg)
    robot_interface.send_action(
        action,
        ActionMode.ABS_TCP,
        RobotClient.CART_QUEUE,
    )
    sleep(3)


if __name__ == "__main__":
    SERVER_ENDPOINT = "192.168.0.207:50051"
    tcp_torch_step_1 = torch.tensor(
        [
            -0.2209775149822235,
            0.7327316999435425,
            0.4133017361164093,
            0.008828246034681797,
            0.9450233578681946,
            0.13374213874340057,
            0.2982715666294098,
            0.25627589225769043,
            0.7316980957984924,
            0.38486048579216003,
            0.059342436492443085,
            -0.9599847793579102,
            -0.09864553809165955,
            0.25529736280441284,
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
    main(
        SERVER_ENDPOINT,
        tcp_torch_step_1,
    )
