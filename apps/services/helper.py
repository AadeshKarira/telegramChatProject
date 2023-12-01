def convert_image_to_base64(image):
    # Convert the image to base64 string
    base64_image = None
    try:
        with Image.open(image) as img:
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG")
            base64_image = buffered.getvalue()
    except Exception as e:
        print(f"Error converting image to base64: {e}")
    return base64_image