"""
*** Running the program: ***
In the order to run this python script, first verify that Python 3
is installed on your system.
Then, run the command "pip3 install Pillow" to install the "Pillow" library.
On the same directory where this file is contained, you should create two new
folders: "set1" and "set2". Each of those folders should contain image files
inside, and nothing else. The image files cannot be placed inside subfolders.
Finally, open a bash/terminal window, navigate to the current directory, and
run the command "python merge.py".
"""

# Import required libraries
from time import sleep

from PIL import Image
import os, sys
import gc

# Main function, responsible for manipulating data and calling
# the other functions
def main():
    # Load the image files from the directories "set1" and "set2"
    set1_imgs = get_imgs('Frames')
    set2_imgs = get_imgs('Images')
    # print(set1_imgs)

    # Ask user to input the X coordinate of the Set2 images
    pos_x = get_position(
        'Input the X position of the Set2 images\n'
        '(i.e. how many pixels away they are from the left corner of the Set1 images)\n'
    )
    
    # Print new line
    print()

    # Ask user to input the Y coordinate of the Set2 images
    pos_y = get_position(
        'Input the Y position of the Set2 images\n'
        '(i.e. how many pixels away they are from the top corner of the Set1 images)\n'
    )

    # For every image in Set1, combine that image with all the
    # images from Set2.
    # Save all of these combined images to a list variable named "combined_imgs"
    # combined_imgs = [combine_imgs(set1_img, set2_img, (pos_x, pos_y))
    #                 for set2_img in set2_imgs
    #                 for set1_img in set1_imgs]

    combined_imgs = []

    CURRENT_DIR = os.path.dirname(__file__)
    FRAMES_DIR = os.path.join(CURRENT_DIR, 'Frames')
    IMAGES_DIR = os.path.join(CURRENT_DIR, 'Images')

    for i, set1_img in enumerate(set1_imgs):
        for k, set2_img in enumerate(set2_imgs):
            final_image = combine_imgs(Image.open(os.path.join(FRAMES_DIR, set1_img)), Image.open(os.path.join(IMAGES_DIR, set2_img)), (pos_x, pos_y))
            combined_imgs.append(final_image)
            try:
                final_image.save(f'Merge/{set1_imgs[k].split(".")[0]}_{"%02d" % i}.png')
                final_image.close()
                gc.collect()
            except FileNotFoundError:
                print('\nMerge folder does not exist.')
                print('\nCreating Merge folder...')
                os.makedirs('Merge')
                final_image.save(f'Merge/{set1_imgs[k].split(".")[0]}_{"%02d" % i}.png')
                final_image.close()
                gc.collect()


# Function responsible for combining any two image files
def combine_imgs(foreground, background, offset):

    # Resize the background image (i.e. the image in the back layer)
    # so that it can fit inside the foreground image
    background.thumbnail(
        (
            int(foreground.size[0] - offset[0]),
            int(foreground.size[1] - offset[1])
        ),
        Image.ANTIALIAS
    )

    # Calculate the desired width and height of the combined image
    width = max(background.size[0], foreground.size[0])
    height = max(background.size[1], foreground.size[1])

    # Resize both the background and foreground images, so that
    # they can easily be merged together
    background = sized_up_RGBA_img(background, (width, height), offset)
    foreground = sized_up_RGBA_img(foreground, (width, height), (0, 0))

    # Merge the two images
    composite = Image.new('RGBA', (width, height))
    composite = Image.alpha_composite(composite, background)

    return Image.alpha_composite(composite, foreground)


# Function responsible for resizing an image file
def sized_up_RGBA_img(img, size, offset):
    width, height = size
    x, y = offset
    new_img = Image.new('RGBA', size)
    new_img.paste(img.convert('RGBA'), (x, y))
    return new_img

# Function responsible for loading all the images file
# contained inside a given directory


def get_imgs(folder_name):
    images = []
    for img in os.listdir(folder_name):
        if not img.endswith('.db'):
            images.append(img)
    return images


# Functionr responsible for prompting the user for a
# X or Y pixel coordinate
def get_position(message):
    while True:
        try:
            position = int(input(message))
            if position >= 0:
                return position
        except ValueError:
            pass
        print('\nThe value for the position should be a positive integer, or "0"\n')


# Code responsible for starting the program and handling
# potential errors/bugs
if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'\n\nThe following error has occured: \n {e}')
        print(type(e))
        print(e.args)
        print('\n Press Enter to exit program')
        input()
