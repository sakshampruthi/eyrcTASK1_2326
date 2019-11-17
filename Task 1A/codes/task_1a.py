
import cv2
import numpy as np
import os


# To enhance the maze image
import image_enhancer


# Maze images in task_1a_images folder have cell size of 20 pixels
CELL_SIZE = 20


class Point(object):

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


dir4 = [Point(0, -CELL_SIZE), Point(0, CELL_SIZE),
        Point(CELL_SIZE, 0), Point(-CELL_SIZE, 0)]


def readImage(img_file_path):

    binary_img = None

    #############	Add your Code here	###############
    img = cv2.imread(img_file_path, 0)
    ret, binary_img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)
    ###################################################

    return binary_img


def solveMaze(original_binary_img, initial_point, final_point, no_cells_height, no_cells_width):

    shortestPath = []

    s = Point(initial_point[0], initial_point[1])
    e = Point(final_point[0], final_point[1])
    s.x = s.x * CELL_SIZE + int(CELL_SIZE/2 - 1)
    s.y = s.y * CELL_SIZE + int(CELL_SIZE/2 - 1)
    e.x = e.x * CELL_SIZE + int(CELL_SIZE/2 - 1)
    e.y = e.y * CELL_SIZE + int(CELL_SIZE/2 - 1)
    h = no_cells_height*CELL_SIZE
    w = no_cells_width*CELL_SIZE

    found = False
    queue = []

    v = [[0 for j in range(w)] for i in range(h)]
    parent = [[Point() for j in range(w)] for i in range(h)]

    queue.append(s)
    v[s.y][s.x] = 1
    while len(queue) > 0:
        p = queue.pop(0)
        for d in dir4:
            cell = p + d
            cx = np.sign(d.x)
            cy = np.sign(d.y)

            if (cell.x >= int(CELL_SIZE/2 - 1)
                and cell.x <= w-int(CELL_SIZE/2)
                and cell.y >= int(CELL_SIZE/2 - 1)
                and cell.y <= h-int(CELL_SIZE/2)
                and v[cell.y][cell.x] == 0
                    and (original_binary_img[cell.y - int(CELL_SIZE/2)*cy][cell.x - int(CELL_SIZE/2)*cx] != 0)):

                queue.append(cell)
                v[cell.y][cell.x] = v[p.y][p.x] + 1  # Later
                parent[cell.y][cell.x] = p
                if cell == e:
                    found = True
                    del queue[:]
                    break

    if found:

        p = e
        while p != s:
            shortestPath.append(p)
            p = parent[p.y][p.x]
        shortestPath.append(p)
        shortestPath.reverse()

        for a, b in enumerate(shortestPath):
            shortestPath[a] = ((int(b.y/CELL_SIZE), int(b.x/CELL_SIZE)))

        print("Path Found")

        return shortestPath

    ###################################################


#############	You can add other helper functions here		#############


#########################################################################

# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
#
# Function Name:	main
# Inputs:			None
# Outputs: 			None
# Purpose: 			the function first takes 'maze00.jpg' as input and solves the maze by calling readImage
# 					and solveMaze functions, it then asks the user whether to repeat the same on all maze images
# 					present in 'task_1a_images' folder or not
if __name__ == '__main__':

    curr_dir_path = os.getcwd()
    # path to directory of 'task_1a_images'
    img_dir_path = curr_dir_path + '/../task_1a_images/'

    file_num = 0
    img_file_path = img_dir_path + 'maze0' + \
        str(file_num) + '.jpg'		# path to 'maze00.jpg' image file

    print('\n============================================')

    print('\nFor maze0' + str(file_num) + '.jpg')

    try:

        original_binary_img = readImage(img_file_path)
        height, width = original_binary_img.shape

    except AttributeError as attr_error:

        print('\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
        exit()

    # number of cells in height of maze image
    no_cells_height = int(height/CELL_SIZE)
    # number of cells in width of maze image
    no_cells_width = int(width/CELL_SIZE)
    initial_point = (0, 0)											# start point coordinates of maze
    # end point coordinates of maze
    final_point = ((no_cells_height-1), (no_cells_width-1))

    try:

        shortestPath = solveMaze(
            original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

        if len(shortestPath) > 2:

            img = image_enhancer.highlightPath(
                original_binary_img, initial_point, final_point, shortestPath)

        else:

            print(
                '\n[ERROR] shortestPath returned by solveMaze function is not complete !\n')
            exit()

    except TypeError as type_err:

        print('\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
        exit()

    print('\nShortest Path = %s \n\nLength of Path = %d' %
          (shortestPath, len(shortestPath)))

    print('\n============================================')

    cv2.imshow('canvas0' + str(file_num), img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    choice = input(
        '\nWant to run your script on all maze images ? ==>> "y" or "n": ')

    if choice == 'y':

        file_count = len(os.listdir(img_dir_path))

        for file_num in range(file_count):

            img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

            print('\n============================================')

            print('\nFor maze0' + str(file_num) + '.jpg')

            try:

                original_binary_img = readImage(img_file_path)
                height, width = original_binary_img.shape

            except AttributeError as attr_error:

                print(
                    '\n[ERROR] readImage function is not returning binary form of original image in expected format !\n')
                exit()

            # number of cells in height of maze image
            no_cells_height = int(height/CELL_SIZE)
            # number of cells in width of maze image
            no_cells_width = int(width/CELL_SIZE)
            initial_point = (0, 0)											# start point coordinates of maze
            # end point coordinates of maze
            final_point = ((no_cells_height-1), (no_cells_width-1))

            try:

                shortestPath = solveMaze(
                    original_binary_img, initial_point, final_point, no_cells_height, no_cells_width)

                if len(shortestPath) > 2:

                    img = image_enhancer.highlightPath(
                        original_binary_img, initial_point, final_point, shortestPath)

                else:

                    print(
                        '\n[ERROR] shortestPath returned by solveMaze function is not complete !\n')
                    exit()

            except TypeError as type_err:

                print(
                    '\n[ERROR] solveMaze function is not returning shortest path in maze image in expected format !\n')
                exit()

            print('\nShortest Path = %s \n\nLength of Path = %d' %
                  (shortestPath, len(shortestPath)))

            print('\n============================================')

            cv2.imshow('canvas0' + str(file_num), img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    else:

        print('')
