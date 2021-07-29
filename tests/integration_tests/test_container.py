import pytest
import subprocess
import numpy as np
from analysis import calculate_metrics as c_m


def test_finnish_mv_results(tmp_path):
    gold_ctm = "../kaldi-dir/alignment_test_data/martti_vainio_ctm/ctm"
    txtdir = "../kaldi-dir/alignment_test_data/martti_vainio_txt"
    wavdir = "../kaldi-dir/alignment_test_data/martti_vainio_16k"
    lang = "fi"

    tmp_ctm_dir = tmp_path / "ctm_results/finnish_mv"
    tmp_ctm_dir.mkdir(parents=True)

    kaldi_align_cmd = " ".join(["--txt", txtdir, "--wav", wavdir, "--lang", lang, str(tmp_ctm_dir)])
    rc = subprocess.call("kaldi-align" + " " + kaldi_align_cmd, shell=True)

    created_ctm = str(sorted(tmp_ctm_dir.rglob("ctm"))[0])
    gold_df, created_df = c_m.create_ctm_dfs(gold_ctm, created_ctm)

    frames = c_m.calculate_frame_wise_comparison(gold_df, created_df)

    assert sum(frames[0]) > 13000, "Baseline model had more correct token frames"
    assert sum(frames[1]) > 1300, "Baseline model had more correct empty frames"
    assert sum(frames[2]) < 1000, "Baseline model had less incorrect frames"

    mistakes = np.asarray(c_m.calculate_ctm_mistakes(gold_df, created_df))
    assert sum(abs(mistakes[:,0])) < 4.3, "Baseline model had better accuracy on start differences"
    assert sum(abs(mistakes[:,1])) < 4.7, "Baseline model had better accuracy on end differences"
     
    assert max(abs(mistakes[:,0])) < 0.016, "Baseline model had better accuracy on max start time"
    assert max(abs(mistakes[:,1])) < 0.012, "Baseline model had better accuracy on max end time"

    baseline_percentiles = [19.4, 50.2, 86.7, 98.6, 21.1, 53.4, 82.8, 98.6]

    errors = []
    stats = c_m.calculate_statistics(mistakes)
    for baseline, new in zip(baseline_percentiles, stats[2]):
        if baseline - new > 0.0050:
            errors.append("baseline better in percentiles")

    assert not errors, "errors occured:\n{}".format("\n".join(errors))

