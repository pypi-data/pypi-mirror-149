import mpld3
from http.server import HTTPServer
import time
import math
import numpy as np
import threading
from matplotlib.figure import Figure
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable


class NonBlockServer(HTTPServer):
    def __init__(self, server_address, handler, bind_and_activate=True):
        super().__init__(server_address, handler, bind_and_activate)

    def shutdown_thread(self):
        time.sleep(1)
        self.shutdown()

    def serve_forever(self, poll_interval=0.5):
        t = threading.Thread(target=self.shutdown_thread)
        t.start()
        super().serve_forever(poll_interval)
        t.join()


def vis_image(image):
    '''
    imshow a numpy array
    :param image: (H, W) or (H, W, C), when C is greater than 1, each channel is displayed separately.
    :return: None
    '''
    if type(image) is not np.ndarray:
        raise TypeError("image must be numpy.ndarray!")

    if len(image.shape) == 2:
        image = image[..., np.newaxis]

    n_channels = image.shape[-1]

    n_cols = 1
    if n_channels > 1:
        n_cols = 2
    n_rows = math.ceil(n_channels / 2)

    plt_fig = Figure(figsize=(n_cols * 6, n_rows * 6))
    plt_axis = plt_fig.subplots(nrows=n_rows, ncols=n_cols)
    if n_channels > 1:
        plt_axis = plt_axis.reshape(-1)

    c_map = LinearSegmentedColormap.from_list("RdWhGn", ["red", "white", "green"])

    for c_idx in range(n_channels):
        axis = plt_axis if n_channels == 1 else plt_axis[c_idx]
        heat_map = axis.imshow(image[:, :, c_idx], cmap=c_map)
        axis_separator = make_axes_locatable(axis)
        color_bar_axis = axis_separator.append_axes("bottom", size="5%", pad=0.1)
        plt_fig.colorbar(heat_map, orientation="horizontal", cax=color_bar_axis)

    mpld3.show(plt_fig, http_server=NonBlockServer)


if __name__ == '__main__':
    from torchvision.datasets import VOCSegmentation
    import torchvision.transforms as T
    import torch

    voc_ds = VOCSegmentation(
        '/Users/lujia/works/model_interp/lime/VOC',
        year='2012',
        image_set='train',
        download=False,
        transform=T.Compose([
            T.ToTensor(),
            T.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ]),
        target_transform=T.Lambda(
            lambda p: torch.tensor(p.getdata()).view(1, p.size[1], p.size[0])
        )
    )

    sample_idx = 439

    img, seg_mask = voc_ds[sample_idx]  # tensors of shape (channel, height, width)
    seg_ids = sorted(seg_mask.unique().tolist())
    feature_mask = seg_mask.clone()
    for i, seg_id in enumerate(seg_ids):
        feature_mask[feature_mask == seg_id] = i

    a = feature_mask.squeeze().numpy()[..., np.newaxis]
    b = np.concatenate([a, 2 * a, 3 * a, 4 * a], axis=2)

    vis_image(b)

    print('ok')
