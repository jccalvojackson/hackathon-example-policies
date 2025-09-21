# Copyright 2025 Poke & Wiggle GmbH. All rights reserved.
import torch

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

ACTION_ARRAY_POS_IDXS = slice(0, 3)
ACTION_ARRAY_QUAT_IDXS = slice(3, 7)
ACTION_ARRAY_ROT_IDXS = slice(3, 6)


DUAL_LEFT_POS_IDXS = slice(0, 3)
DUAL_LEFT_QUAT_IDXS = slice(3, 7)
LEFT_ARM = slice(DUAL_LEFT_POS_IDXS.start, DUAL_LEFT_QUAT_IDXS.stop)

DUAL_RIGHT_POS_IDXS = slice(7, 10)
DUAL_RIGHT_QUAT_IDXS = slice(10, 14)
RIGHT_ARM = slice(DUAL_RIGHT_POS_IDXS.start, DUAL_RIGHT_QUAT_IDXS.stop)

LEFT_GRIPPER_IDX = -2
RIGHT_GRIPPER_IDX = -1


DUAL_DELTA_LEFT_POS_IDXS = slice(0, 3)
DUAL_DELTA_LEFT_ROT_IDXS = slice(3, 6)
DUAL_DELTA_RIGHT_POS_IDXS = slice(6, 9)
DUAL_DELTA_RIGHT_ROT_IDXS = slice(9, 12)


TCP_TORCH_STEP_2 = torch.tensor(
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

TCP_TORCH_STEP_3 = torch.tensor(
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
