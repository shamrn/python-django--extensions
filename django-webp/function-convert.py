
### Convert images to webp format, using the webp library ( https://github.com/anibali/pywebp )


import sys
from io import BytesIO
from uuid import uuid4

from PIL import Image
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from webp import WebPPicture, WebPConfig


def get_filename(file: 'InMemoryUploadedFile') -> str:
    """Function returns the name of the file without format"""

    file_name = file.name
    re_index = file_name.rfind('.')

    name = file_name if re_index == -1 else file_name[:re_index]
    if not name: name = uuid4().hex  # NOQA

    return name


def convert_image_webp(image: 'InMemoryUploadedFile', quality: int = settings.WEBP_QUALITY,
                       lossless: bool = False) -> 'InMemoryUploadedFile':
    """The function returns the image in memory that was converted to webp format."""

    pil_image = Image.open(image)

    if pil_image.format.lower() != settings.WEBP_FORMAT:
        pic = WebPPicture.from_pil(pil_image)
        config = WebPConfig.new(quality=quality, lossless=lossless)
        buffer_img = pic.encode(config).buffer()

        output = BytesIO(buffer_img)

        image = InMemoryUploadedFile(name=f'{get_filename(image)}.{settings.WEBP_FORMAT}',
                                     field_name='ImageField', charset=None,
                                     file=output, content_type=f'image/{settings.WEBP_FORMAT}',
                                     size=sys.getsizeof(output))

    return image
