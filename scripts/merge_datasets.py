from example_policies.data_ops.merge_lerobot import merge_datasets

if __name__ == "__main__":
    import pathlib

    path_step_1 = pathlib.Path("data/lerobot/step_1_tcp_one_hot")
    path_step_2 = pathlib.Path("data/lerobot/step_2_tcp_one_hot")
    path_step_3 = pathlib.Path("data/lerobot/step_3_tcp_one_hot")
    output_path = pathlib.Path("data/lerobot/step_1_2_3_tcp_one_hot")
    merge_datasets(
        [path_step_1, path_step_2, path_step_3],
        output_path,
    )
