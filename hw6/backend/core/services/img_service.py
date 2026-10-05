from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile

from PIL import Image, ImageOps, UnidentifiedImageError


def convert_to_jpeg(uploaded_file) -> ContentFile:
    try:
        uploaded_file.seek(0)

        with Image.open(uploaded_file) as image:

            image = ImageOps.exif_transpose(image)

            if image.mode in ("RGBA", "LA") or (
                image.mode == "P" and "transparency" in image.info
            ):
                image_with_alpha = image.convert("RGBA")

                background = Image.new(
                    mode="RGB",
                    size=image_with_alpha.size,
                    color="white",
                )

                background.paste(
                    image_with_alpha,
                    mask=image_with_alpha.getchannel("A"),
                )

                image = background
            else:
                image = image.convert("RGB")

            buffer = BytesIO()

            image.save(
                buffer,
                format="JPEG",
                quality=90,
                optimize=True,
            )

    except (UnidentifiedImageError, OSError) as error:
        raise ValueError("Надісланий файл не є коректним зображенням.") from error

    buffer.seek(0)

    original_name = Path(uploaded_file.name).stem

    return ContentFile(
        buffer.read(),
        name=f"{original_name}.jpg",
    )