from example_policies.data_ops.merge_lerobot import merge_datasets

if __name__ == "__main__":
    import pathlib

    path_step_1 = pathlib.Path("data/lerobot/mh2_step_1_tcp")
    path_step_2 = pathlib.Path("data/lerobot/mh2_step_2_tcp")
    path_step_3 = pathlib.Path("data/lerobot/mh2_step_3_tcp")
    output_path = pathlib.Path("data/lerobot/mh2_step_1_2_3_tcp")
    merge_datasets(
        [path_step_1, path_step_2, path_step_3],
        output_path,
    )
