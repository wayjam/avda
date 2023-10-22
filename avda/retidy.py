import os
import shutil
import logging
import typing
from .helper import get_avid_from_title
from .helper.nfo import NFO, NFOParseError
import enum


class VideoFilePathOpts:
    multi_actors_mode: str = "多人共演"
    unknown_actor: str = "佚名"
    format: str

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Video:
    actors: typing.List[str]
    avid: str
    title: str
    basename: str

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def generate_file_path(
        self, output: str, opts: VideoFilePathOpts, filename: str
    ) -> str:
        format = opts.format.replace("$(title)", self.title)
        format = format.replace("$(avid)", self.avid)

        if len(self.actors) == 0:
            format = format.replace("$(actor)", opts.unknown_actor)
        if len(self.actors) == 1:
            format = format.replace("$(actor)", self.actors[0])
        else:
            format = format.replace("$(actor)", opts.multi_actors_mode)

        if filename.find(self.basename) != -1:
            suffix = filename.replace(self.basename, "")
            result = f"{format}{suffix}"
        else:
            result = f"{format}-{filename}"

        result = os.path.join(output, result)
        return result


class RunMode(enum.Enum):
    FLAT = "flat"
    SEPARATED = "separated"


class RetidyFielsRunner:
    input_dir: str
    output_dir: str
    dry_run: bool
    # 一级目录模式,子目录模式
    run_mode: RunMode
    video_file_path_opts: VideoFilePathOpts

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def run(self):
        if not os.path.isdir(self.input_dir):
            logging.error(f"Input directory {self.input_dir} does not exist")
            return

        if not os.path.isdir(self.output_dir):
            logging.error(f"Output directory {self.output_dir} does not exist")
            return

        switcher = {
            RunMode.SEPARATED: self.run_separated_dir_mode,
            RunMode.FLAT: self.run_flat_dir_mode,
        }
        f = switcher.get(self.run_mode)
        if f is not None:
            f()
        else:
            logging.error(f"unknown run mode {self.run_mode}")

    def run_flat_dir_mode(self):
        for file in os.listdir(self.input_dir):
            if not file.endswith(".nfo"):
                continue

            video = self.parse_nfo_file(os.path.join(self.input_dir, file))
            if video is None:
                logging.error(f"file {file} parse to video fail")
                continue

            file_list = [
                os.path.join(self.input_dir, f)
                for f in os.listdir(self.input_dir)
                if f.startswith(video.basename)
            ]
            logging.info(f"===> handing {video.basename}")
            for item in file_list:
                target_path = video.generate_file_path(
                    self.output_dir,
                    self.video_file_path_opts,
                    os.path.basename(item),
                )
                self.move(item, target_path)

    def run_separated_dir_mode(self):
        dirs = os.listdir(self.input_dir)
        for item in dirs:
            full_path = os.path.join(self.input_dir, item)
            if os.path.isfile(full_path):
                continue
            self._run_separated_dir_mode(full_path)

    def _run_separated_dir_mode(self, dir_path):
        other_files = []
        nfo_file = ""
        for file in os.listdir(dir_path):
            if file.endswith(".nfo"):
                nfo_file = file
            else:
                other_files.append(file)
        if nfo_file == "":
            logging.error(f"not found nfo in {dir_path}")
            return

        video = self.parse_nfo_file(os.path.join(dir_path, nfo_file))
        if video is None:
            logging.error(f"file {nfo_file} parse to video fail")
            return

        logging.info(f"===> handing {dir_path}")
        for item in [*other_files, nfo_file]:
            target_path = video.generate_file_path(
                self.output_dir,
                self.video_file_path_opts,
                os.path.basename(item),
            )
            self.move(os.path.join(dir_path, item), target_path)

        self.clear(dir_path)

    def parse_nfo_file(self, file_path: str) -> typing.Optional[Video]:
        nfoData = NFO()
        try:
            nfoData.decode(file_path)
            avid = get_avid_from_title(nfoData.title)
        except NFOParseError:
            logging.error(f"Failed to parse {file_path} as XML")
            return None
        except AttributeError:
            logging.error(f"Failed to find necessary fields in {file_path}")
            return None
        except Exception as err:
            logging.error(
                f"Unexpected error occurred while processing {file_path}: {str(err)}"
            )
            return None
        video = Video(
            title=nfoData.title,
            avid=avid,
            actors=nfoData.actors,
            basename=os.path.basename(file_path).replace(".nfo", ""),
        )
        return video

    def move(self, source_path, target_path):
        try:
            logging.info(f"moving from [{source_path}] to [{target_path}]")

            if not self.dry_run:
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                shutil.move(source_path, target_path)
        except Exception as err:
            logging.error(
                f"Unexpected error occurred while moving file {source_path}: {str(err)}"
            )

    def clear(self, dir_path):
        if (
            (not self.dry_run)
            and self.run_mode.value == RunMode.SEPARATED
            and os.path.exists(dir_path)
            and len(os.listdir(dir_path)) == 0
        ):
            logging.info(f"{dir_path} is empty and removed")
            shutil.rmtree(dir_path)
