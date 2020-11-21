# Copyright The PyTorch Lightning team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fairscale.nn.data_parallel.sharded_ddp import ShardedDataParallel


class LightningShardedDataParallel(ShardedDataParallel):

    def forward(self, *inputs, **kwargs):
        if self.enable_broadcast_buffers:
            self.sync_buffers()

        if self.base_model.training:
            outputs = self.base_model.training_step(*inputs, **kwargs)
        elif self.base_model.testing:
            outputs = self.base_model.test_step(*inputs, **kwargs)
        else:
            outputs = self.base_model.validation_step(*inputs, **kwargs)
        return outputs
