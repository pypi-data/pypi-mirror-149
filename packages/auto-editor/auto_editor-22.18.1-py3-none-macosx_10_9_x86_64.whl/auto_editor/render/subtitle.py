import os
import re

from typing import List, Tuple
from auto_editor.utils.log import Log
from auto_editor.ffwrapper import FileInfo


class SubtitleParser:
    def __init__(self):
        self.supported_codecs = ("ass", "webvtt", "mov_text")

    def parse(self, text, fps: float, codec: str):

        if codec not in self.supported_codecs:
            raise ValueError(f"codec {codec} not supported.")

        self.fps = fps
        self.codec = codec
        self.contents = []

        if codec == "ass":
            time_code = re.compile(r"(.*)(\d+:\d+:[\d.]+)(.*)(\d+:\d+:[\d.]+)(.*)")
        if codec == "webvtt":
            time_code = re.compile(r"()(\d+:[\d.]+)( --> )(\d+:[\d.]+)(\n.*)")
        if codec == "mov_text":
            time_code = re.compile(r"()(\d+:\d+:[\d,]+)( --> )(\d+:\d+:[\d,]+)(\n.*)")

        i = 0
        for reg in re.finditer(time_code, text):
            i += 1
            if i == 1:
                self.header = text[: reg.span()[0]]

            self.contents.append(
                [
                    self.to_frame(reg.group(2)),
                    self.to_frame(reg.group(4)),
                    reg.group(1),
                    reg.group(3),
                    reg.group(5) + "\n",
                ]
            )

        if i == 0:
            self.header = ""
            self.footer = ""
        else:
            self.footer = text[reg.span()[1] :]

    def edit(self, chunks: List[Tuple[int, int, float]]) -> None:
        for cut in reversed(chunks):
            the_speed = cut[2]
            speed_factor = 1 if the_speed == 99999 else 1 - (1 / the_speed)

            new_content = []
            for content in self.contents:
                if cut[0] <= content[1] and cut[1] > content[0]:

                    diff = int(
                        (min(cut[1], content[1]) - max(cut[0], content[0]))
                        * speed_factor
                    )
                    if content[0] > cut[0]:
                        content[0] -= diff
                        content[1] -= diff

                    content[1] -= diff

                elif content[0] >= cut[0]:
                    diff = int((cut[1] - cut[0]) * speed_factor)

                    content[0] -= diff
                    content[1] -= diff

                if content[0] != content[1]:
                    new_content.append(content)

        self.contents = new_content

    def write(self, file_path: str):
        with open(file_path, "w") as file:
            file.write(self.header)
            for item in self.contents:
                file.write(
                    "{before}{start_time}{middle}{end_time}{after}".format(
                        before=item[2],
                        start_time=self.to_timecode(item[0]),
                        middle=item[3],
                        end_time=self.to_timecode(item[1]),
                        after=item[4],
                    )
                )
            file.write(self.footer)

    def to_frame(self, text: str) -> int:
        if self.codec == "mov_text":
            time_format = r"(\d+):?(\d+):([\d,]+)"
        else:
            time_format = r"(\d+):?(\d+):([\d.]+)"

        nums = re.match(time_format, text)
        assert nums is not None

        hours, minutes, seconds = nums.groups()
        seconds = seconds.replace(",", ".", 1)
        return round(
            (int(hours) * 3600 + int(minutes) * 60 + float(seconds)) * self.fps
        )

    def to_timecode(self, frame: int) -> str:
        seconds = frame / self.fps

        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)

        sig_fig = 2 if self.codec == "ass" else 3

        str_s = str(round(s, sig_fig)).zfill(2)
        del s

        if self.codec == "webvtt":
            if int(h) == 0:
                return f"{int(m):02d}:{str_s}"
            time_format = "{:02d}:{:02d}:{}"
        elif self.codec == "mov_text":
            str_s = str_s.replace(".", ",", 1)
            time_format = "{:02d}:{:02d}:{}"
        else:
            time_format = "{:d}:{:02d}:{}"

        return time_format.format(int(h), int(m), str_s)


def cut_subtitles(
    ffmpeg,
    inp: FileInfo,
    chunks: List[Tuple[int, int, float]],
    temp: str,
    log: Log,
) -> None:
    for s, sub in enumerate(inp.subtitles):
        file_path = os.path.join(temp, f"{s}s.{sub.ext}")
        new_path = os.path.join(temp, f"new{s}s.{sub.ext}")

        parser = SubtitleParser()

        if sub.codec in parser.supported_codecs:
            with open(file_path) as file:
                parser.parse(file.read(), inp.gfps, sub.codec)
        else:
            convert_path = os.path.join(temp, f"{s}s_convert.vtt")
            ffmpeg.run(["-i", file_path, convert_path])
            with open(convert_path) as file:
                parser.parse(file.read(), inp.gfps, "webvtt")

        parser.edit(chunks)
        parser.write(new_path)
