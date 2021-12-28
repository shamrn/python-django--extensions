import sys
from io import BytesIO

from PIL import Image
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from portfolio.models import Work
from webp import WebPPicture, WebPConfig

FAIL = '\033[91m'
END = '\033[0m'


def make_image_webp(image):
    pil_image = Image.open(image)
    pic = WebPPicture.from_pil(pil_image)
    config = WebPConfig.new(quality=90, lossless=False)
    buffer_img = pic.encode(config).buffer()
    output = BytesIO(buffer_img)
    image = InMemoryUploadedFile(
        name=f'_.{settings.WEBP_FORMAT}',
        field_name='ImageField', charset=None,
        file=output, content_type=f'image/{settings.WEBP_FORMAT}',
        size=sys.getsizeof(output))
    return image


def run(work_):
    print('Object: ', work_, ' id: ', work_.id)

    try:
        if work_.image and not work_.image_webp:
            work_.image_webp = make_image_webp(work_.image)
            print('    Created image_webp')

        else:
            print('    Created already image_webp')  # NOQA

        if work_.image_tile_quad and not work_.image_tile_quad_webp:
            work_.image_tile_quad_webp = make_image_webp(work_.image_tile_quad)
            print('    Created image_tile_quad_webp')

        else:
            print('    Created already image_tile_quad_webp')  # NOQA

        if work_.image_tile_wide and not work_.image_tile_wide_webp:
            work_.image_tile_wide_webp = make_image_webp(work_.image_tile_wide)
            print('    Created image_tile_wide_webp')

        else:
            print('    Created already image_tile_wide_webp')  # NOQA

        work_.save(update_fields=['image_webp', 'image_tile_quad_webp', 'image_tile_wide_webp'])

    except Exception as exc:
        print(FAIL + '    Error: ', exc, END)


works = Work.objects.all()

for work in works:
    run(work)
