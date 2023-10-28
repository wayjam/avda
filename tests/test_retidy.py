from avda import retidy


def test_retidy():
    runner = retidy.RetidyFilesRunner(
        dry_run=True,
        input_dir="/mnt/disk/porn",
        output_dir="/mnt/disk/porn",
        video_file_path_opts=retidy.VideoFilePathOpts(
            format="$(actor)/$(avid)/$(avid)",
        ),
        run_mode=retidy.RunMode.FLAT,
    )
    runner.run()
