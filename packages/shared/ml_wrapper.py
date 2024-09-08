import os

if os.environ.get('USE_MLX', 'false').lower() == 'true':
    import mlx.core as mx
    import mlx.nn as nn
else:
    import torch as mx
    import torch.nn as nn


class ModelWrapper:
    def __init__(self):
        pass

    def _create_model(self):
        pass

    def forward(self, nx):
        pass

    def train(self, data):
        pass
