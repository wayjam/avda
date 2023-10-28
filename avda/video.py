import os
import typing


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
