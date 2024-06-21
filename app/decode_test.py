import numpy as np
import imageio

# parameters
rawWidth = 4608
rawHeight = 2592
rawStride = int(rawWidth * 10 / 8)

thumbnailWidth = 512
thumbnailHeight = np.floor(thumbnailWidth * rawHeight / rawWidth).astype(int)

# Load raw image
rawImage = np.fromfile('/tmp/test.raw', dtype=np.uint8)
rawImage = rawImage.reshape((rawHeight, rawStride))

# Compute the average of each 2x2 block
print("rawImage.shape: ", rawImage.shape)

print(np.mean(rawImage[::2, ::5]))
print(np.mean(rawImage[1::2, ::5]))
print(np.mean(rawImage[::2, 1::5]))
print(np.mean(rawImage[1::2, 1::5]))

b = rawImage[::2, ::5]
g = rawImage[1::2, ::5]
r = rawImage[::2, 1::5]

# Create an image
img = np.zeros((r.shape[0], r.shape[1], 3), dtype=np.uint8)
img[:, :, 2] = b
img[:, :, 1] = g
img[:, :, 0] = r

# Save the image
imageio.imwrite('/tmp/capture.jpg', img)