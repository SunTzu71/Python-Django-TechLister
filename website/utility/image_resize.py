from PIL import Image

def image_resize(orig_image, file_name, img_height=300, img_width=300):
    if orig_image.height > img_height or orig_image.width > img_width:

        orig_image.thumbnail((img_height, img_width))

        # Create a BytesIO object to temporarily hold the resized image
        from io import BytesIO
        output_io = BytesIO()

        # Save the resized image to the BytesIO object
        orig_image.save(output_io, format=orig_image.format)

        # Get the file name and extension from the original image
        file_name = file_name.name
        file_ext = file_name.split('.')[-1].lower()

        # Create a new InMemoryUploadedFile with the resized image data
        from django.core.files.uploadedfile import InMemoryUploadedFile
        resized_image = InMemoryUploadedFile(output_io, None, file_name, f'image/{file_ext}',
                                             output_io.tell(), None)

        return resized_image