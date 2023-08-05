import torch
from torch import nn, Tensor
from torchnorms.tnorms.base import BaseTNorm

class LearnableSiameseLatentTNorm(BaseTNorm):
    def __init__(self, input_size: int = 100, hidden_dim: int = 200):
        super().__init__()
        self.mlp_1 = nn.Linear(in_features=input_size, out_features=hidden_dim)
        self.softplus = nn.Softplus()
        self.mlp_2 = nn.Linear(in_features=hidden_dim, out_features=input_size)
        
        params = torch.empty(12,1)
        torch.nn.init.xavier_normal_(params)
        self.params = nn.Parameter(params)

    
    def aggregate(self, a: Tensor, b: Tensor, powers: nn.Parameter) -> Tensor:
        res_1 =  torch.pow(a,powers[0]) + torch.pow(b, powers[0])
        res_2 =  torch.pow(res_1, powers[1])

        return res_2
        
    def __call__(self, a: Tensor,b: Tensor) -> Tensor:
        
        self.params.data[0:8] = self.softplus(self.params[0:8])

        latent_1 = self.mlp_1(a)
        latent_2 = self.mlp_1(b)
        
        latent_1 = torch.sigmoid(latent_1)
        latent_2 = torch.sigmoid(latent_2)
        

        l_1 = self.aggregate(latent_1, latent_2, self.params[0:2])
        l_1_rev = self.aggregate(1.0 - latent_1, 1 - latent_2, self.params[2:4])
        
        l_2 = self.aggregate(latent_1, latent_2, self.params[4:6])
        l_2_rev = self.aggregate(1.0 - latent_1, 1 - latent_2, self.params[6:8])
        
        # Aggregation scheme learned from https://www.ijcai.org/proceedings/2021/0398.pdf
        LAF = (self.params[8] * l_1 + self.params[9] * l_1_rev) / (self.params[10] * l_2 + self.params[11] * l_2_rev)
        
        res = self.mlp_2(LAF)
        res = torch.clamp(self.softplus(res), max=0.99)

        return res

