import cv2 as cv
import numpy as np
import os
import glob
import random


def dim(image, degree=1, show=False, show_original=False):
    """
    A function to dim images and make it less contrast.

    image: The image you wish to dim. This should be the absolute path to the image.

    degree: The degree of darkness you want. Values range from 1 to 15 with 1=lowest darkness and 15=highest darkness.
    Default is set to 1.

    show: True to show the modified image using cv2.imshow, False to not show modified image. Defaults to False.

    show_original: True to show original image alonside modified image, False to not show original image. Defaults to False.
    """

    # read the image
    img = cv.imread(image)

    # check if the degree is within range else raise a ValueError
    if degree < 1 or degree > 10:
        raise ValueError("degree value must be within the range of 1 and 15")
    else:
        # create an np.array with dimensions corresponsing to the shape of the image
        divider = np.ones(img.shape, dtype="uint8") * degree

    # add the channels values of read in image
    # the adder array of 1s multiplied the value int(degree*100) is subtracted from the original image array
    # the new array results in a much brighter image th
    dim_img = cv.divide(img, divider)

    img = cv.resize(img, (400, 480))
    dim_img = cv.resize(dim_img, (400, 480))

    # if show is true then open a window with the modified image
    if show:
        # if show original is true then show both original and modified images
        if show_original:
            cv.imshow("Original", img)
            cv.imshow("Dim Modified", dim_img)
        else:
            # return the modified array if show is false
            cv.imshow("Dim Modified", dim_img)
    else:
        # return the new modified array
        return dim_img

    # destroy all windows window 0 is pressed
    cv.waitKey(0)
    cv.destroyAllWindows()


# dim all images and add to a newly created folder
def dim_to_folder(images_path, file_extension, folder_name="modified", lowest_degree=1, highest_degree=5, add_original=False, randomize=False):
    """
    This function returns a folder containing all images modified.

    images_path(required): The absolute path of the folder containing the images.

    file_extension(required): The extension name of the files in the folder, eg. jpg, png etc.... Must be a string value.

    folder_name: Name of the newly created folder that contains the modified images. Defaults to 'modified'.

    lowest_degree: The least value of degree of modification to apply to the images. Defaults to 1.

    highest_degree: The highest value of degree of modification to apply to the images. Defaults to 5. Limit is 10.

    add_original: True to add original images to modified ones in the folder, False to not. Defaults to False.

    randomize: True to mix up the modified and original images in the folder, False to not.
    """

    # initialize empty lists
    image_list = []
    dim_list = []

    # check for lowest and highest degree limits
    if lowest_degree < 1 or lowest_degree > 10:
        raise ValueError(
            "lowest degree value must be within the range of 1 and 10")
    elif highest_degree < 1 or highest_degree > 10:
        raise ValueError(
            "highest degree value must be within the range of 1 and 10")
    else:
        None

    # for every file in the image path provided having the extension provided
    # read the image and add to image_list
    for filename in glob.glob(images_path+"/*."+file_extension):
        img = cv.imread(filename)
        image_list.append(img)

    # loop through the image list and modify each one
    # append to the dim list when done
    for i in range(len(image_list)):
        random_degree = random.randint(lowest_degree, highest_degree)
        divisor = np.ones(image_list[i].shape, dtype="uint8") * random_degree
        dim_img = cv.divide(image_list[i], divisor)
        dim_list.append(dim_img)

    # if the folder name specified exists raise an error
    if os.path.exists(folder_name):
        raise FileExistsError(
            "{} folder already exists, please consider using something else.".format(folder_name))
    else:
        # if not create the folder
        os.mkdir(folder_name)

    # if add original, then add the dim list to the image list
    if add_original:
        image_list.extend(dim_list)
        # if randomize, shuffle the image list
        if randomize:
            image_list = random.sample(image_list, len(image_list))
        else:
            None

        # for all images in the image list write to the required folder
        for i in range(len(image_list)):
            img_path = os.path.join(folder_name, str(i)+"."+file_extension)
            cv.imwrite(img_path, image_list[i])
    else:
        # if add to original is false then write only the dim list images
        for i in range(len(dim_list)):
            img_path = os.path.join(folder_name, str(i)+"."+file_extension)
            cv.imwrite(img_path, dim_list[i])

    return None
