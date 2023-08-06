import unittest
import gammalearn.data.nets as nets
import torch
import torchvision.models as models


class TestNets(unittest.TestCase):

    def setUp(self) -> None:
        self.input = torch.rand(10, 2, 55, 55)

        self.resnet18 = {
            'model': models.resnet18,
            'parameters':
                {
                    'output_size': (7, 7),
                    'num_channels': 2
                }
        }
        self.mobilenet_v2 = {
            'model': models.mobilenet_v2,
            'parameters':
                {
                    'output_size': (9, 9),
                    'num_channels': 2
                }
        }
        self.mobilenet_v3 = {
            'model': models.mobilenet_v3_large,
            'parameters':
                {
                    'output_size': (9, 9),
                    'num_channels': 2
                }
        }
        self.efficient_net = {
            'model': models.efficientnet_b7,
            'parameters':
                {
                    'output_size': (9, 9),
                    'num_channels': 2
                }
        }

    def test_resnet18(self):
        net = nets.TorchModel(self.resnet18)
        output = net(self.input)
        assert net.num_features == 512
        assert output.shape[1] == 512
        assert output.shape[2:] == self.resnet18['parameters']['output_size']
        assert net.n_pixels == torch.prod(torch.tensor(output.shape[2:]))

    def test_mobilenet_v2(self):
        net = nets.TorchModel(self.mobilenet_v2)
        output = net(self.input)
        assert net.num_features == 1280
        assert output.shape[1] == 1280
        assert output.shape[2:] == self.mobilenet_v2['parameters']['output_size']
        assert net.n_pixels == torch.prod(torch.tensor(output.shape[2:]))

    def test_mobilenet_v3(self):
        net = nets.TorchModel(self.mobilenet_v3)
        output = net(self.input)
        assert net.num_features == 960
        assert output.shape[1] == 960
        assert output.shape[2:] == self.mobilenet_v3['parameters']['output_size']
        assert net.n_pixels == torch.prod(torch.tensor(output.shape[2:]))

    def test_efficient_net(self):
        net = nets.TorchModel(self.efficient_net)
        output = net(self.input)
        assert net.num_features == 2560
        assert output.shape[1] == 2560
        assert output.shape[2:] == self.efficient_net['parameters']['output_size']
        assert net.n_pixels == torch.prod(torch.tensor(output.shape[2:]))
