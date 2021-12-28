### An example of functionality

### Does not save the downloaded file, it saves only the converted file in webp format

def generate_webp_images(self):
    image_fields = {
        'image': self.data.get('image'),
        'image_tile_quad': self.data.get('image_tile_quad'),
        'image_tile_wide': self.data.get('image_tile_wide')
    }

    for field, value in image_fields.items():
        if value and value not in (getattr(self.instance, field), '__delete__', '__update__'):
            self.data[field] = convert_image_webp(value, quality=90)


# --------------------------------------------------------------------------------------------------

### Saves the original and assigns the converted image to the other fields

def make_webp_images(self):
    image_fields = ('image', 'image_tile_quad', 'image_tile_wide')

    for field in image_fields:
        field_webp = f'{field}_webp'

        if (hasattr(self.Meta.model, field_webp) and field_webp not in self.changed_data and
                field in self.changed_data):

            setattr(self.instance, field_webp,
                    convert_image_webp(getattr(self.instance, field), settings.WEBP_QUALITY))