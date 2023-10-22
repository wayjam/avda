from avda.retidy import RetidyFielsRunner, RunMode, VideoFilePathOpts


def test_retidy():
    runner = RetidyFielsRunner(
        dry_run=True,
        input_dir="/mnt/disk/porn",
        output_dir="/mnt/disk/porn",
        video_file_path_opts=VideoFilePathOpts(
            format="$(actor)/$(avid)/$(avid)",
        ),
        run_mode=RunMode.FLAT,
    )
    runner.run()
