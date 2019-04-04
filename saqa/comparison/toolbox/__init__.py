
def cropping_images(image_filename_a, image_filename_b):
    o_width, o_height = image_filename_a.shape[:2]
    a_width, a_height = image_filename_b.shape[:2]
    f_width = min(o_width, a_width)
    f_height = min(o_height, a_height)
    image_filename_a_cropped = image_filename_a[0:f_width, 0:f_height]
    image_filename_b_cropped = image_filename_b[0:f_width, 0:f_height]

    return image_filename_a_cropped, image_filename_b_cropped
