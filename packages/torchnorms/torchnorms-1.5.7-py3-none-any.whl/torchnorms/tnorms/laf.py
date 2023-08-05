import torch
from torch import nn, Tensor
from torchnorms.tnorms.base import BaseTNorm

class LearnableLatentTNorm(BaseTNorm):
    def __init__(self):
        super().__init__()
        
        params = torch.empty(12,1)
        torch.nn.init.xavier_normal_(params)
        self.params = nn.Parameter(params)
        self.softplus = nn.Softplus()
    
    def aggregate(self, a: Tensor, b: Tensor, powers: nn.Parameter) -> Tensor:
        res_1 =  torch.pow(a,powers[0]) + torch.pow(b, powers[0])
        res_2 =  torch.pow(res_1, powers[1])

        return res_2
        
    def __call__(self, a: Tensor,b: Tensor) -> Tensor:
        
        self.params.data[0:8] = self.softplus(self.params[0:8])

        l_1 = self.aggregate(a, b, self.params[0:2])
        l_1_rev = self.aggregate(1.0 - a, 1 - b, self.params[2:4])
        
        l_2 = self.aggregate(a, b, self.params[4:6])
        l_2_rev = self.aggregate(1.0 - a, 1 - b, self.params[6:8])
        
        # Aggregation scheme learned from https://www.ijcai.org/proceedings/2021/0398.pdf
        LAF = (self.params[8] * l_1 + self.params[9] * l_1_rev) / (self.params[10] * l_2 + self.params[11] * l_2_rev)
        
        res = torch.clamp(self.softplus(LAF), max=0.99)

        return res