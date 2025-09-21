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
    joint_action: torch.Tensor,
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
    robot_interface.send_action(
        joint_action,
        ActionMode.ABS_JOINT,
        RobotClient.JOINT_DIRECT,
    )
    sleep(3)


if __name__ == "__main__":
    SERVER_ENDPOINT = "192.168.0.207:50051"
    joint_torch_step_1 = torch.tensor(
        [
            0.4471760094165802,
            -1.2342418432235718,
            0.45227089524269104,
            -1.954215168952942,
            -2.240309953689575,
            3.6498403549194336,
            1.901563048362732,
            -0.10643364489078522,
            -1.7152258157730103,
            -0.788551926612854,
            -2.6066625118255615,
            -1.9385480880737305,
            2.618283987045288,
            0.16568933427333832,
            0,
            0,
        ]
    )[None, :]
    joint_torch_step_2 = torch.tensor(
        [
            -0.18202824890613556,
            -1.6736795902252197,
            0.38071638345718384,
            -2.3399906158447266,
            1.7071672677993774,
            2.034407377243042,
            -1.3984428644180298,
            0.31682440638542175,
            -0.2519884705543518,
            -1.0262212753295898,
            -1.5539188385009766,
            -1.3682128190994263,
            2.4204294681549072,
            0.35241031646728516,
            0,
            0,
        ]
    )[None, :]
    joint_torch_step_3 = torch.tensor(
        [
            -0.19314666092395782,
            -1.5037035942077637,
            0.20229555666446686,
            -2.5593416690826416,
            1.8637012243270874,
            1.715293049812317,
            -1.789493203163147,
            0.10661439597606659,
            -1.3886662721633911,
            -0.6962682604789734,
            -2.128901243209839,
            -1.8944792747497559,
            2.2690141201019287,
            0.0272686704993248,
            0,
            0,
        ]
    )[None, :]
    tcp_torch_step_1 = torch.tensor(
        [
            -0.42565616965293884,
            0.7437244057655334,
            0.444048136472702,
            -0.12877345085144043,
            0.9702804088592529,
            0.06199071183800697,
            0.1952703595161438,
            0.1799883097410202,
            0.6719077229499817,
            0.43928056955337524,
            -0.08927492797374725,
            -0.9476412534713745,
            -0.08635035902261734,
            0.29419323801994324,
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
        joint_torch_step_1,
    )
