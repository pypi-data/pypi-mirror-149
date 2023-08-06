import os
from io import BytesIO
import tarfile
from matplotlib import gridspec
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
import tensorflow.compat.v1 as tf
import boto3
import tempfile


class ImageSegmentation(object):
    """Class to load model and run inference."""

    INPUT_TENSOR_NAME = 'ImageTensor:0'
    OUTPUT_TENSOR_NAME = 'SemanticPredictions:0'
    INPUT_SIZE = 513
    FROZEN_GRAPH_NAME = 'frozen_inference_graph'

    def __init__(self, tarball_path):
        print('Loading Image Segmentation model...')
        """Creates and loads pretrained model."""
        self.graph = tf.Graph()

        graph_def = None
        # Extract frozen graph from tar archive.
        tar_file = tarfile.open(tarball_path)
        for tar_info in tar_file.getmembers():
            if self.FROZEN_GRAPH_NAME in os.path.basename(tar_info.name):
                file_handle = tar_file.extractfile(tar_info)
                graph_def = tf.GraphDef.FromString(file_handle.read())
                break

        tar_file.close()

        if graph_def is None:
            raise RuntimeError('Cannot find inference graph in tar archive.')

        with self.graph.as_default():
            tf.import_graph_def(graph_def, name='')

        self.sess = tf.Session(graph=self.graph)
        print('Model loaded successfully!')

    def run(self, image):
        """Runs inference on a single image.

        Args:
            image: A PIL.Image object, raw input image.

        Returns:
            resized_image: RGB image resized from original input image.
            seg_map: Segmentation map of `resized_image`.
        """
        width, height = image.size
        resize_ratio = 1.0 * self.INPUT_SIZE / max(width, height)
        target_size = (int(resize_ratio * width), int(resize_ratio * height))
        resized_image = image.convert('RGB').resize(target_size, Image.ANTIALIAS)
        batch_seg_map = self.sess.run(
            self.OUTPUT_TENSOR_NAME,
            feed_dict={self.INPUT_TENSOR_NAME: [np.asarray(resized_image)]})
        seg_map = batch_seg_map[0]
        return resized_image, seg_map


def create_pascal_label_colormap():
    """Creates a label colormap used in PASCAL VOC segmentation benchmark.

    Returns:
    A Colormap for visualizing segmentation results.
    """
    colormap = np.zeros((256, 3), dtype=int)
    ind = np.arange(256, dtype=int)

    for shift in reversed(range(8)):
        for channel in range(3):
            colormap[:, channel] |= ((ind >> channel) & 1) << shift
    ind >>= 3

    return colormap


def label_to_color_image(label):
    """Adds color defined by the dataset colormap to the label.

    Args:
    label: A 2D array with integer type, storing the segmentation label.

    Returns:
    result: A 2D array with floating type. The element of the array
        is the color indexed by the corresponding element in the input label
        to the PASCAL color map.

    Raises:
    ValueError: If label is not of rank 2 or its value is larger than color
        map maximum entry.
    """
    if label.ndim != 2:
        raise ValueError('Expect 2-D input label')

    colormap = create_pascal_label_colormap()

    if np.max(label) >= len(colormap):
        raise ValueError('label value too large.')

    return colormap[label]


def run_visualization(image, seg_map, alpha=0.7) -> Image:
    """Visualizes input image, segmentation map and overlay view."""
    fig = plt.figure(figsize=(10, 5))
    grid_spec = gridspec.GridSpec(1, 2, width_ratios=[6, 2])
    seg_image = label_to_color_image(seg_map).astype(np.uint8)

    plt.subplot(grid_spec[0])
    plt.imshow(image)
    plt.imshow(seg_image, alpha=alpha)
    plt.axis('off')
    plt.title('Segmentation overlay')

    unique_labels = np.unique(seg_map)
    ax = plt.subplot(grid_spec[1])
    plt.imshow(
        FULL_COLOR_MAP[unique_labels].astype(np.uint8), interpolation='nearest')
    ax.yaxis.tick_right()
    plt.yticks(range(len(unique_labels)), LABEL_NAMES[unique_labels])
    plt.xticks([], [])
    ax.tick_params(width=0.0)
    plt.grid('off')
    buf = BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    image = Image.open(buf)
    return image



def decode_image(image_data) -> Image:
    """Decodes the image data."""
    image = Image.open(BytesIO(image_data))
    return image


def perform_segmentation(model, image) -> Image:
    print(f'running image segmentation on the image')
    resized_im, seg_map = model.run(image)
    image = run_visualization(resized_im, seg_map)
    print('Done!')
    return image

def save_image_to_s3(image: Image, name: str, bucket_name: str):
    s3 = boto3.client('s3')
    folder = name.split('/')
    if len(folder) > 1:
        if '.' in folder[0]:
            raise ValueError('invalid folder name, it can\'t contain a dot')
    else:
        raise ValueError('invalid image name, it needs to be in the format of /folder/image.png')
    
    filename = folder[-1].split('.')[0] + '.png'
    filename_path = folder[0] + '/' + filename
    with tempfile.TemporaryDirectory() as tmpdirname:
        os.mkdir(tmpdirname + '/' + folder[0])
        image.save(tmpdirname + '/' + filename_path)
        s3.upload_file(tmpdirname + '/' + filename_path, bucket_name, filename_path)
    print(f'image saved to s3 bucket')

LABEL_NAMES = np.asarray([
    'background',
    'aeroplane',
    'bicycle',
    'bird',
    'boat',
    'bottle',
    'bus',
    'car',
    'cat',
    'chair',
    'cow',
    'diningtable',
    'dog',
    'horse',
    'motorbike',
    'person',
    'pottedplant',
    'sheep',
    'sofa',
    'train',
    'tv'
])
# LABEL_NAMES = np.asarray([c['name'] for c in cats])
FULL_LABEL_MAP = np.arange(len(LABEL_NAMES)).reshape(len(LABEL_NAMES), 1)
FULL_COLOR_MAP = label_to_color_image(FULL_LABEL_MAP)