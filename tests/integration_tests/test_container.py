import pytest
import subprocess
import numpy as np
from analysis import calculate_metrics as c_m

@pytest.mark.parametrize("gold_ctm, txtdir, wavdir, lang, baseline_values",[
    ("../kaldi-dir/alignment_test_data/martti_vainio_ctm/ctm",
    "../kaldi-dir/alignment_test_data/martti_vainio_txt",
    "../kaldi-dir/alignment_test_data/martti_vainio_16k",
    "fi",
    [13000, 1300, 1000, 4.3, 4.7, 0.016, 0.012, [19.4, 50.2, 86.7, 98.6, 21.1, 53.4, 82.8, 98.6]])
])

def test_g2p_finnish(source_corpus_file, reference_lexicon_file, g2p_mapping, tmp_path):

def test_finnish_mv_results(tmp_path, gold_ctm, txtdir, wavdir, lang, baseline_values):

    correct_token_frames        = baseline_values[0]
    correct_empty_frames        = baseline_values[1]
    incorrect_frames            = baseline_values[2]
    start_difference_accuracy   = baseline_values[3]
    end_difference_accuracy     = baseline_values[4]
    max_start_difference        = baseline_values[5]
    max_end_difference          = baseline_values[6]
    baseline_percentiles        = baseline_values[7]

    frame_buffer        = 100
    accuracy_sum_buffer = 0.5
    accuracy_max_buffer = 0.1
    statistics_buffer   = 0.005

    errors = []

    tmp_ctm_dir = tmp_path / "ctm_results/" + lang
    tmp_ctm_dir.mkdir(parents=True)

    kaldi_align_cmd = " ".join(["--txt", txtdir, "--wav", wavdir, "--lang", lang, str(tmp_ctm_dir)])
    rc = subprocess.call("kaldi-align" + " " + kaldi_align_cmd, shell=True)

    created_ctm = str(sorted(tmp_ctm_dir.rglob("ctm"))[0])
    gold_df, created_df = c_m.create_ctm_dfs(gold_ctm, created_ctm)

    frames = c_m.calculate_frame_wise_comparison(gold_df, created_df)

    if sum(frames[0]) > correct_token_frames:
        errors.append("Baseline model had more correct token frames, " +
        "baseline: {}, here: {}".format(correct_token_frames, frames[0]))
    if sum(frames[1]) > correct_empty_frames:
        errors.append("Baseline model had more correct empty frames, " +
        "baseline: {}, here: {}".format(correct_empty_frames, frames[1]))
    if sum(frames[2]) < incorrect_frames:
        errors.append("Baseline model had less incorrect frames, " +
        "baseline: {}, here: {}".format(incorrect_frames, frames[2]))

    mistakes = np.asarray(c_m.calculate_ctm_mistakes(gold_df, created_df))

    mistake_start_sum = sum(abs(mistakes[:,0]))
    if mistake_start_sum < start_difference_accuracy:
        errors.append("Baseline model had better accuracy on start differences, " +
        "baseline: {}, here: {}".format(correct_token_frames, mistake_start_sum))

    mistake_end_sum = sum(abs(mistakes[:,1]))
    if mistake_end_sum < end_difference_accuracy:
        errors.append("Baseline model had better accuracy on end differences, " +
        "baseline: {}, here: {}".format(correct_token_frames, mistake_end_sum))

    mistake_start_max = max(abs(mistakes[:,0]))
    if mistake_start_max < max_start_difference:
        errors.append("Baseline model had better accuracy on max start time, " +
        "baseline: {}, here: {}".format(correct_token_frames, mistake_start_max))

    mistake_end_max = max(abs(mistakes[:,1]))
    if mistake_end_max < max_end_difference:
        errors.append("Baseline model had better accuracy on max end time, " +
        "baseline: {}, here: {}".format(correct_token_frames, mistake_end_max))

    stats = c_m.calculate_statistics(mistakes)

    for baseline, new in zip(baseline_percentiles, stats[2]):
        if baseline - new > 0.0050:
            errors.append("baseline better in percentiles, " +
            "baseline: {}, here: {}".format(baseline, new))

    assert not errors, "errors occured:\n{}".format("\n".join(errors))

