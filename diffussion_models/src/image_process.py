import PIL

def download_image(image):
      image = PIL.ImageOps.exif_transpose(image)\
        .convert("RGB")
      return image