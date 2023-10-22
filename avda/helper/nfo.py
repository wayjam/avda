import xml.etree.ElementTree as ET
from lxml import etree
import typing


class NFOParseError(etree.ParseError):
    pass


class NFO:
    ext = ".nfo"
    title: str
    number: str
    actors: typing.List[str]
    tag: typing.List[str]
    genre: typing.List[str]
    studio: str
    director: str
    mpaa: str
    year: str
    runtime: str
    premiered: str
    release_date: str
    release: str
    website: str
    label: str

    def __init__(self):
        pass

    def encode(self, video: dict):
        """encode video info as nfo format (XML)

        return bytes that encode using nfo format

        NFO is appliable in Jellyfin / Emby.
        """

        nfo_movie = ET.Element("movie")
        ET.SubElement(nfo_movie, "title").text = video.get("title")
        ET.SubElement(nfo_movie, "originaltitle").text = (
            video.get("title").lstrip(video.get("designatio")).lstrip()
        )
        ET.SubElement(nfo_movie, "set")
        ET.SubElement(nfo_movie, "studio").text = video.get("maker")
        ET.SubElement(nfo_movie, "year").text = video.get("date")[:4]
        ET.SubElement(nfo_movie, "mpaa").text = video.get("mpaa")
        ET.SubElement(nfo_movie, "rating").text = video.get("review")
        ET.SubElement(nfo_movie, "outline").text = video.get("outline")
        ET.SubElement(nfo_movie, "plot").text = video.get("outline")
        ET.SubElement(nfo_movie, "runtime").text = video.get("length")
        ET.SubElement(nfo_movie, "director").text = video.get("director")
        ET.SubElement(nfo_movie, "poster").text = video.get("poster_path")
        ET.SubElement(nfo_movie, "thumb").text = video.get("thumb_path")
        ET.SubElement(nfo_movie, "fanart").text = video.get("fanart_path")
        for actor in video.get("cast"):
            nfo_actor = ET.SubElement(nfo_movie, "actor")
            ET.SubElement(nfo_actor, "name").text = actor
        ET.SubElement(nfo_movie, "maker").text = video.get("maker")
        ET.SubElement(nfo_movie, "label").text = video.get("label")
        for serie in video.get("series"):
            ET.SubElement(nfo_movie, "tag").text = serie
        for genre in video.get("genres"):
            ET.SubElement(nfo_movie, "genre").text = genre
        ET.SubElement(nfo_movie, "num").text = video.get("designatio")
        ET.SubElement(nfo_movie, "premiered").text = video.get("date")
        ET.SubElement(nfo_movie, "releasedate").text = video.get("date")
        ET.SubElement(nfo_movie, "tagline").text = "配信開始日 " + video.get("date")
        ET.SubElement(nfo_movie, "cover").text = video.get("cover_url")
        ET.SubElement(nfo_movie, "website").text = video.get("video_url")

        nfo = ET.ElementTree(nfo_movie).getroot()

        return ET.tostring(nfo, encoding="utf8", method="xml")

    def decode(self, path: str):
        try:
            movie = etree.parse(path).getroot()

            self.title = (
                movie.find("title").text if movie.find("title") is not None else ""
            )
            self.runtime = (
                movie.find("runtime").text if movie.find("runtime") is not None else ""
            )
            self.mpaa = (
                movie.find("mpaa").text if movie.find("mpaa") is not None else ""
            )
            self.director = (
                movie.find("director").text
                if movie.find("director") is not None
                else ""
            )
            self.year = (
                movie.find("year").text if movie.find("year") is not None else ""
            )
            self.studio = (
                movie.find("studio").text if movie.find("studio") is not None else ""
            )
            self.release_date = (
                movie.find("releasedate").text
                if movie.find("releasedate") is not None
                else ""
            )
            self.number = (
                movie.find("num").text if movie.find("num") is not None else ""
            )
            self.release = (
                movie.find("release").text if movie.find("release") is not None else ""
            )
            self.label = (
                movie.find("label").text if movie.find("label") is not None else ""
            )
            self.website = (
                movie.find("website").text if movie.find("website") is not None else ""
            )

            actors = []
            actors_elements = movie.findall("actor")
            for elem in actors_elements:
                actor = elem.find("name").text if elem.find("name") is not None else ""
                if actor:
                    actors.append(actor)
            self.actors = actors

            for item in self.actors:
                if "素人" in item:
                    self.actors.remove(item)

            self.tag = [item.text for item in movie.findall("tag")]
            self.genre = [item.text for item in movie.findall("genre")]

        except etree.ParseError:
            raise NFOParseError
