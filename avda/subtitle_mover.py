import os
import logging
import typing
import cchardet
from .helper import avid


class SubtitleMover:
    exts: typing.List[str] = [".srt", ".vtt", ".ass"]
    target_dir: str
    subtitle_dir: str
    dry_run: bool
    overwrite: bool = False

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def run(self):
        for relpath, _, files in os.walk(self.target_dir):
            for f in files:
                if not f.upper().endswith(".NFO"):
                    continue

                number = avid.get_avid_from_filename(f)
                if number is None:
                    logging.info(f"get number failed from {f}")
                    continue

                if not self.overwrite:
                    hasSrt = False
                    for ext in self.exts:
                        if os.path.exists(
                            os.path.join(self.target_dir, relpath, number + ext)
                        ):
                            hasSrt = True
                            break
                    if hasSrt:
                        continue

                full_path = os.path.join(self.target_dir, relpath, f)
                self.handle_nfo(number, full_path)

    def handle_nfo(self, number: str, full_path: str):
        subtitle_files = []
        for root, _, filenames in os.walk(self.subtitle_dir):
            for filename in filenames:
                if not filename.startswith(".") and filename.lower().startswith(
                    number.lower()
                ):
                    subtitle_files.append(os.path.join(root, filename))

        full_path = os.path.normpath(os.path.abspath(full_path))
        logging.info(f"====> handing {number} - {full_path}")
        logging.info(f"probable subtitles: {subtitle_files}")
        for file in subtitle_files:
            self.handle_subtitle(number, os.path.dirname(full_path), file)

    def handle_subtitle(
        self,
        number: str,
        target_dir: str,
        source_path: str,
    ):
        (_, rext) = os.path.splitext(source_path)
        if rext not in self.exts:
            return

        dst_path = os.path.join(target_dir, number + rext)

        with open(source_path, "rb") as original_file:
            content = original_file.read()
            detect_result = cchardet.detect(content)

            if not "UTF-8" in detect_result["encoding"].upper():
                result_content = content.decode(detect_result["encoding"], "ignore")
                logging.info(
                    f"copying [{source_path}] to [{dst_path}](transform from {detect_result['encoding']})"
                )
            else:
                result_content = content.decode()
                logging.info(f"copying [{source_path}] to [{dst_path}]")

            result_content = result_content.replace("\r\n", "\n")

            if self.dry_run:
                return
            try:
                with open(dst_path, "w", encoding="utf-8-sig", newline="\n") as out:
                    out.write(result_content)
            except Exception as e:
                logging.error(f"translate encoding error {str(e)}")
