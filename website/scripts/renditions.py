"""Write one downscaled copy of a photo master to stdout as JPEG.

Usage: renditions.py MASTER WIDTH

Called by the /media/w<width>/<file> endpoint. The master is only read: the copy keeps
its colour profile and proportions, and is never wider than the master.
"""

import io
import sys

from PIL import Image, ImageOps


def render(master: str, width: int) -> bytes:
    with Image.open(master) as image:
        # Browsers honour EXIF orientation on the master; bake it in so the copy matches.
        upright = ImageOps.exif_transpose(image)
        if width >= upright.width:
            raise ValueError(f"{width}px is not narrower than the {upright.width}px master")
        height = round(upright.height * width / upright.width)
        resized = upright.convert("RGB").resize((width, height), Image.Resampling.LANCZOS)
        out = io.BytesIO()
        icc = image.info.get("icc_profile")
        options = {"icc_profile": icc} if icc else {}
        resized.save(out, "JPEG", quality=85, optimize=True, progressive=True, **options)
        return out.getvalue()


def main() -> None:
    master, width = sys.argv[1], int(sys.argv[2])
    sys.stdout.buffer.write(render(master, width))


if __name__ == "__main__":
    main()
