from skimage import segmentation, color
from skimage.future import graph
from skimage.io import imread, imsave

class filterMarcos:
    def __init__(self, imagem):
        self._path = imagem
        self._images = imread(imagem)

    def apply_filter(self, compactness=30, n_segments=400, start_label=1):
        # Apply the filter
        labels = segmentation.slic(self._imagem, compactness=30, n_segments=400, start_label=1)
        g = graph.rag_mean_color(self._imagem, labels, mode='similarity')
        labels2 = graph.cut_threshold(labels, g)
        # Save the image
        out2 = color.label2rgb(labels2, self._imagem, kind='avg', bg_label=0)
        imsave(self._path[:-4] + '_filter.png', out2)