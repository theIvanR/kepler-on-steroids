import time
import torch
import torch.nn as nn
import torch.optim as optim

# -------------------------
class ResidualDeepNet(nn.Module):
    def __init__(self, in_dim, out_dim, hidden_dim=2048, alpha_init=1e-2):
        super().__init__()
        assert in_dim == out_dim, "Identity-init assumes in_dim == out_dim"
        self.linear_passthrough = nn.Linear(in_dim, out_dim)
        
        layers = [nn.Linear(in_dim, hidden_dim), nn.LayerNorm(hidden_dim), nn.GELU()]
        # first residual block
        for _ in range(16):
            layers += [nn.Linear(hidden_dim, hidden_dim), nn.LayerNorm(hidden_dim), nn.GELU()]
        layers.append(nn.Linear(hidden_dim, out_dim))
        
        self.residual_mlp = nn.Sequential(*layers)
        self.alpha = nn.Parameter(torch.tensor(float(alpha_init)))
        self._init_weights()

    def _init_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                if m.bias is not None:
                    nn.init.zeros_(m.bias)
            elif isinstance(m, nn.LayerNorm):
                nn.init.ones_(m.weight)
                nn.init.zeros_(m.bias)
        with torch.no_grad():
            self.linear_passthrough.weight.copy_(torch.eye(self.linear_passthrough.weight.shape[0]))
            if self.linear_passthrough.bias is not None:
                self.linear_passthrough.bias.zero_()
            final_lin = self.residual_mlp[-1]
            if isinstance(final_lin, nn.Linear):
                final_lin.weight.zero_()
                if final_lin.bias is not None:
                    final_lin.bias.zero_()

    def forward(self, x):
        return self.linear_passthrough(x) + self.alpha * self.residual_mlp(x)



# -------------------------
def main():
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    IN_DIM = 1024
    BATCH_SIZE = 32768  # push as much as your GPU memory allows

    print(f"Using device: {DEVICE}")

    # Single continuous batch in GPU memory
    xb = torch.randn(BATCH_SIZE, IN_DIM, device=DEVICE)
    yb = torch.randn(BATCH_SIZE, IN_DIM, device=DEVICE)

    model = ResidualDeepNet(IN_DIM, IN_DIM).to(DEVICE)
    if torch.cuda.device_count() > 1 and DEVICE.type == 'cuda':
        model = nn.DataParallel(model)

    optimizer = optim.AdamW(model.parameters(), lr=1e-4)
    criterion = nn.MSELoss()

    epoch = 0
    while True:  # hammer indefinitely
        epoch += 1
        start = time.time()
        optimizer.zero_grad()
        loss = criterion(model(xb), yb)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        print(f"Epoch {epoch} | MSE: {loss.item():.6f} | time: {time.time()-start:.1f}s")


if __name__ == "__main__":
    main()
