import scipy.misc
import random
from skimage.transform import resize
from PIL import Image
import numpy as np
xs = []
ys = []

#points to the end of the last batch
train_batch_pointer = 0
val_batch_pointer = 0

#read data.txt
with open("driving_dataset/data.txt") as f:
    for line in f:
        xs.append("driving_dataset/" + line.split()[0])
        #the paper by Nvidia uses the inverse of the turning radius,
        #but steering wheel angle is proportional to the inverse of turning radius
        #so the steering wheel angle in radians is used as the output
        ys.append(float(line.split()[1]) * scipy.pi / 180)

#get number of images
num_images = len(xs)

#shuffle list of images
c = list(zip(xs, ys))
random.shuffle(c)
xs, ys = zip(*c)

train_xs = xs[:int(len(xs) * 0.8)]
train_ys = ys[:int(len(xs) * 0.8)]

val_xs = xs[-int(len(xs) * 0.2):]
val_ys = ys[-int(len(xs) * 0.2):]

num_train_images = len(train_xs)
num_val_images = len(val_xs)

# def LoadTrainBatch(batch_size):
#     global train_batch_pointer
#     x_out = []
#     y_out = []
#     for i in range(0, batch_size):
#         x_out.append(scipy.misc.imresize(scipy.misc.imread(train_xs[(train_batch_pointer + i) % num_train_images])[-150:], [66, 200]) / 255.0)
#         y_out.append([train_ys[(train_batch_pointer + i) % num_train_images]])
#     train_batch_pointer += batch_size
#     return x_out, y_out

def LoadTrainBatch(batch_size):
    global train_batch_pointer
    x_out = []
    y_out = []
    for i in range(0, batch_size):
        image_path = train_xs[(train_batch_pointer + i) % num_train_images]
        image = Image.open(image_path)
        image = image.crop((0, image.size[1] - 150, image.size[0], image.size[1]))  # Crop the bottom part
        image = image.resize((200, 66))  # Resize the image
        image = np.array(image) / 255.0  # Convert to numpy array and normalize
        x_out.append(image)
        y_out.append([train_ys[(train_batch_pointer + i) % num_train_images]])
    train_batch_pointer += batch_size
    return x_out, y_out

# def LoadValBatch(batch_size):
#     global val_batch_pointer
#     x_out = []
#     y_out = []
#     for i in range(0, batch_size):
#         x_out.append(scipy.misc.imresize(scipy.misc.imread(val_xs[(val_batch_pointer + i) % num_val_images])[-150:], [66, 200]) / 255.0)
#         y_out.append([val_ys[(val_batch_pointer + i) % num_val_images]])
#     val_batch_pointer += batch_size
#     return x_out, y_out

def LoadValBatch(batch_size):
    global val_batch_pointer
    x_out = []
    y_out = []
    for i in range(0, batch_size):
        image_path = val_xs[(val_batch_pointer + i) % num_val_images]
        image = Image.open(image_path)
        image = image.crop((0, image.size[1] - 150, image.size[0], image.size[1]))  # Crop the bottom part
        image = image.resize((200, 66))  # Resize the image
        image = np.array(image) / 255.0  # Convert to numpy array and normalize
        x_out.append(image)
        y_out.append([val_ys[(val_batch_pointer + i) % num_val_images]])
    val_batch_pointer += batch_size
    return x_out, y_out
