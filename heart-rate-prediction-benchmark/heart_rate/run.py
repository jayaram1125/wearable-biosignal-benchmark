"""Run the heart-rate benchmark.
    python -m heart_rate.run --config configs/hr_dalia.yaml --method spectral
    python -m heart_rate.run --config configs/hr_dalia.yaml --method papagei --subjects S1,S2
Writes results/<dataset>_<method>_predictions.csv, results/<dataset>_<method>_summary.md and logs/<...>.json."""
from __future__ import annotations
import argparse, os, time
import numpy as np, pandas as pd, yaml
from common.quality import gate
from common.metrics import summarise
from common.loso import loso, ridge_fit, ridge_predict
from common.runlog import write_log
from heart_rate.dalia import load_all
from heart_rate.spectral import spectral_hr


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", required=True)
    ap.add_argument("--method", choices=["spectral", "papagei", "kidppg"], default="spectral")
    ap.add_argument("--subjects", default=None, help="comma-separated subset, e.g. S1,S2")
    ap.add_argument("--out", default="results")
    a = ap.parse_args(argv)
    cfg = yaml.safe_load(open(a.config))
    subjects = a.subjects.split(",") if a.subjects else cfg["subjects"]
    t0 = time.time()
    D = load_all(cfg["data_dir"], subjects, cfg)
    accepted, feats = gate(D["ppg"], D["acc"], cfg["quality"])
    if a.method == "spectral":
        pred = spectral_hr(D["ppg"], cfg["fs_ppg"], tuple(cfg["bandpass_hz"]), tuple(cfg["hr_range_bpm"]))
    elif a.method == "kidppg":
        from heart_rate.baselines import kidppg_hr
        pred = kidppg_hr(D["ppg"], D["acc"], cfg["fs_ppg"], cfg["fs_acc"])
    else:
        from heart_rate.embed_papagei import embed
        tag = "_".join(subjects) if a.subjects else "all"
        E = embed(D["ppg"], cfg["fs_ppg"], cfg["papagei"], cache=f"embeddings/{cfg['dataset']}_{tag}.npy")
        pred = loso(E, D["y"], D["subject"], ridge_fit(cfg["papagei"]["ridge_alpha"]), ridge_predict)
    names = {int(k): v for k, v in cfg["activities"].items()}
    df = pd.DataFrame({"subject": D["subject"], "activity": [names.get(int(x), str(x)) for x in D["activity"]],
                       "y": D["y"], "pred": pred, "accepted": accepted, **{k: v for k, v in feats.items()}})
    os.makedirs(a.out, exist_ok=True)
    stem = f"{cfg['dataset']}_{a.method}" + (f"_{'_'.join(subjects)}" if a.subjects else "")
    df.to_csv(os.path.join(a.out, stem + "_predictions.csv"), index=False)
    overall = summarise(df, "pred"); by_act = summarise(df, "pred", by="activity"); by_sub = summarise(df, "pred", by="subject")
    log = write_log(f"logs/{stem}_{time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())}.json", cfg,
                    {"method": a.method, "subjects": subjects, "n_windows": int(len(df)), "seconds": round(time.time() - t0, 1)})
    md = [f"# {cfg['dataset']} · {a.method} · leave-one-subject-out", "",
          f"Run {log['timestamp_utc']} · commit `{log['git_hash'][:12]}` · subjects {len(subjects)} · windows {len(df)}",
          "Preliminary, untuned. Protocol as in the PPG Heart-Rate Technical Architecture v0.2. MAE in bpm.", "",
          "## Overall", overall.round(3).to_markdown(), "", "## By activity", by_act.round(3).to_markdown(), "",
          "## By subject", by_sub.round(3).to_markdown(), ""]
    open(os.path.join(a.out, stem + "_summary.md"), "w").write("\n".join(md))
    print("\n".join(md[:8]))


if __name__ == "__main__":
    main()
