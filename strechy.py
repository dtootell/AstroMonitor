
#
from PIL import Image
from numpy import asarray
import numpy as np
import matplotlib.pyplot as plt




class Stretch:

    def __init__(self, target_bkg = 0.25, shadows_clip = -1.25): #(default values were bkg = 0.25, clip = -1.25)
        self.shadows_clip = shadows_clip
        self.target_bkg = target_bkg

    def _get_avg_dev(self, data):
        """Return the average deviation from the median.

        Args:
            data (np.array): array of floats, presumably the image data
        """
        median = np.median(data)
        n = data.size
        median_deviation = lambda x: abs(x - median)
        avg_dev = np.sum( median_deviation(data) / n )
        return avg_dev


    def _mtf(self, m, x):
        """Midtones Transfer Function

        MTF(m, x) = {
            0                for x == 0,
            1/2              for x == m,
            1                for x == 1,

            (m - 1)x
            --------------   otherwise.
            (2m - 1)x - m
        }

        See the section "Midtones Balance" from
        https://pixinsight.com/doc/tools/HistogramTransformation/HistogramTransformation.html

        Args:
            m (float): midtones balance parameter
                       a value below 0.5 darkens the midtones
                       a value above 0.5 lightens the midtones
            x (np.array): the data that we want to copy and transform.
        """
        shape = x.shape
        x = x.flatten()
        zeros = x==0
        halfs = x==m
        ones = x==1
        others = np.logical_xor((x==x), (zeros + halfs + ones))

        x[zeros] = 0
        x[halfs] = 0.5
        x[ones] = 1
        x[others] = (m - 1) * x[others] / ((((2 * m) - 1) * x[others]) - m)
        return x.reshape(shape)


    def _get_stretch_parameters(self, data):
        """ Get the stretch parameters automatically.
        m (float) is the midtones balance
        c0 (float) is the shadows clipping point
        c1 (float) is the highlights clipping point
        """
        median = np.median(data)
        avg_dev = self._get_avg_dev(data)

        c0 = np.clip(median + (self.shadows_clip * avg_dev), 0, 1)
        m = self._mtf(self.target_bkg, median - c0)

        return {
            "c0": c0,
            "c1": 1,
            "m": m
        }


    def stretch(self, data):
        """ Stretch the image.

        Args:
            data (np.array): the original image data array.

        Returns:
            np.array: the stretched image data
        """

        # Normalize the data
        d = data / np.max(data)

        # Obtain the stretch parameters
        stretch_params = self._get_stretch_parameters(d)
        m = stretch_params["m"]
        c0 = stretch_params["c0"]
        c1 = stretch_params["c1"]

        # Selectors for pixels that lie below or above the shadows clipping point
        below = d < c0
        above = d >= c0

        # Clip everything below the shadows clipping point
        d[below] = 0

        # For the rest of the pixels: apply the midtones transfer function
        d[above] = self._mtf(m, (d[above] - c0)/(1 - c0))
        return d



# load the image
image = Image.open('kv/pix/Rosette.jpg')
print('image type is: ',type(image))
# convert image to numpy array
data = asarray(image)
print(type(data))
# summarize shape
print(data.shape)

# create Pillow image
#image2 = Image.fromarray(data)
# print(type(image2))


#rng = np.random.RandomState(10)  # deterministic random data
# a = np.hstack(data)
# _ = plt.hist(a, bins=255)  # arguments are passed to np.histogram
# plt.title("Histogram with 'auto' bins")
# Text(0.5, 1.0, "Histogram with 'auto' bins")
#
#
# hist, edges = np.histogram(data,bins=range(255))
# plt.figure(figsize=[10,8])
#
# plt.bar(edges[:-1], hist, width = 0.8, color='red')
# # plt.xlim(min(edges), max(edges))
# # plt.grid(axis='y', alpha=0.75)
# # plt.xlabel('Value',fontsize=15)
# # plt.ylabel('Frequency',fontsize=15)
# # plt.xticks(fontsize=15)
# # plt.yticks(fontsize=15)
# # plt.ylabel('Frequency',fontsize=15)
# # plt.title('Document Image Histogram',fontsize=15)
# plt.show()


# summarize image details
# print(image2.mode)
# print(image2.size)
# print(data)

stretch_data = Stretch()
new_image = stretch_data.stretch(data)
#
image_stretch = Image.fromarray((new_image * 255).astype(np.uint8))

# image_stretch = Image.fromarray(new_image)#
# print(new_image.shape)
# image2.show()

#
image_stretch.show()
# print(image_stretch)
# print('strectched image type is: ',type(image_stretch))
#
# hist, edges = np.histogram(image_stretch,bins=range(255))
# plt.figure(figsize=[10,8])
# print('hists size',hist.size)
# print(hist)
#
# plt.bar(edges[:-1], hist, width = 0.8, color='red')
# plt.show()