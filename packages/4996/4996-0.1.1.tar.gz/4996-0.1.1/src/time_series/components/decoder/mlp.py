# Copyright 2022 Jeremy Oldfather (github.com/theoldfather/time-series)
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
# Applies to:
#
# MLP
#
################################################################################


import torch.nn as nn
import numpy as np


class MLP(nn.Module):

    def __init__(self, input_size, hidden_size, output_size, num_layers=2, dropout=0.1, activation=nn.ReLU):
        """Multi-Layer Perceptron

        Allows for a variable number of layers (default=2).

        Args:
            input_size (int): inputs size of the first layer
            hidden_size (int): hidden size of the intermediate layers
            output_size (int): output size of the final layer
            num_layers (int): number of layers in the MLP
            dropout (float): dropout rate
            activation (nn.Module): an activation module that can be initialized
        """
        super(MLP, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.num_layers = num_layers
        self.dropout = dropout
        self.activation = activation()

        layers = []
        for k in np.arange(num_layers) + 1:
            input_size, output_size = self.hidden_size, self.hidden_size
            activation = self.activation

            if k == 1:
                input_size = self.input_size

            if k == self.num_layers:
                output_size = self.output_size
                activation = nn.Identity()

            layer = nn.Linear(input_size, output_size)
            layers.append(layer)
            layers.append(activation)
            layers.append(nn.Dropout(self.dropout))

        self.layers = nn.Sequential(*layers)

    def forward(self, x):
        """ Forward pass

        Args:
            x (nn.Tensor): a tensors of inputs

        Returns:
            a nn.Tensor with `output_size` number of outputs

        """

        return self.layers(x)
