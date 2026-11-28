"""Frozen PaPaGei-S encoder (Pillai et al., ICLR 2025) used as a feature extractor.
Weights: Zenodo record 13983110 (papagei_s.pt); code: github.com/Nokia-Bell-Labs/papagei-foundation-model.
This wrapper resamples each window to the model rate and pads/crops to the model segment
length. VERIFY the sampling rate, segment length and model constructor against the
repository README before reporting any number; they are read from the config, not assumed."""
from __future__ import annotations
import os, sys
import numpy as np
from common.signal import resample, zscore


def _load_model(cfg: dict):
    import torch
    sys.path.insert(0, cfg["repo"])
    from models.resnet import ResNet1DMoE                       # module path per the PaPaGei repo
    from utilities import load_model_without_module_prefix
    model_config = {"base_filters": 32, "kernel_size": 3, "stride": 2, "groups": 1, "n_block": 18,
                    "n_classes": 512, "n_experts": 3}            # PaPaGei-S quick-start configuration
    model = ResNet1DMoE(in_channels=1, **model_config)
    model = load_model_without_module_prefix(model, cfg["weights"])
    model.eval()
    return model


def embed(ppg_win: np.ndarray, fs_in: float, cfg: dict, batch: int = 256, cache: str | None = None) -> np.ndarray:
    """ppg_win: (n, len) at fs_in. Returns (n, 512) embeddings. Cached to disk if `cache` given."""
    if cache and os.path.exists(cache):
        return np.load(cache)
    import torch
    model = _load_model(cfg)
    x = resample(ppg_win, fs_in, cfg["fs_model"])
    L = int(cfg["segment_s"] * cfg["fs_model"])
    if x.shape[-1] < L:                                           # centre-pad by edge reflection
        pad = L - x.shape[-1]
        x = np.pad(x, ((0, 0), (pad // 2, pad - pad // 2)), mode="reflect")
    x = zscore(x[:, :L])
    out = []
    with torch.no_grad():
        for i in range(0, len(x), batch):
            xb = torch.tensor(x[i:i + batch], dtype=torch.float32).unsqueeze(1)
            emb = model(xb)
            emb = emb[0] if isinstance(emb, (tuple, list)) else emb
            out.append(emb.cpu().numpy())
    E = np.concatenate(out)
    if cache:
        os.makedirs(os.path.dirname(cache) or ".", exist_ok=True)
        np.save(cache, E)
    return E
