from avda import subtitle_mover


def test_subtitle_mover():
    runner = subtitle_mover.SubtitleMover(
        dry_run=True,
        subtitle_dir="/the_subtitle_dir",
        target_dir="/the_video_dir",
    )
    runner.run()
