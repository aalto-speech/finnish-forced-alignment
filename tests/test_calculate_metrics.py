import numpy as np
import pytest
from analysis import calculate_metrics as c_m



@pytest.fixture
def dfs():
    gold_df, created_df = c_m.create_ctm_dfs("tests/data/gold.ctm", "tests/data/created.ctm")
    return gold_df, created_df


def test_create_ctm_dfs(dfs):
    errors = []
    gold_df, created_df = dfs
    if not gold_df.token[3] == "neljäs":
        errors.append("tokens not correct")
    start = gold_df.iloc[-1].start
    end = gold_df.iloc[-1].end
    duration = gold_df.iloc[-1].duration
    if not abs(start + duration - end) < 0.001:
        errors.append("timestamps not correct")

    assert not errors, "errors occured:\n{}".format("\n".join(errors))


def test_calculate_frame_wise_comparison(dfs):
    gold_df, created_df = dfs
    frames = c_m.calculate_frame_wise_comparison(gold_df, created_df)
    assert frames == [[316], [49], [56]]


def test_calculate_ctm_mistakes(dfs):
    correct_mistakes = [[-0.1, -0.1], [0.0, 0.0], [0.0, 0.1], [0.0, 0.0], [0.0, 0.1], [0.0, 0.0], [-0.1, -0.1], [0.0, 0.0]]
    errors = []

    gold_df, created_df = dfs
    mistakes = c_m.calculate_ctm_mistakes(gold_df, created_df)
    for i, (cm, m) in enumerate(zip(correct_mistakes, mistakes)):
        error_sum = abs(cm[0] - m[0]) + abs(cm[1] - m[1])
        if error_sum > 0.001:
            errors.append("mistakes in {} row".format(i))
    assert not errors, "errors occured in:\n{}".format("\n".join(errors))


def test_calculate_statistics(dfs):
    errors = []
    correct_stats = (0.0, 0.05, [75.0, 75.0, 75.0, 87.5, 50.0, 50.0, 50.0, 87.5])
    gold_df, created_df = dfs
    mistakes = c_m.calculate_ctm_mistakes(gold_df, created_df)
    np_mistakes = np.asarray(mistakes)
    stats = c_m.calculate_statistics(np_mistakes)
    if not abs(stats[0] - correct_stats[0]) < 0.001:
        errors.append("median start difference error")
    if not abs(stats[1] - correct_stats[1]) < 0.001:
        errors.append("median end difference error")
    for i, (cs, s) in enumerate(zip(correct_stats[2], stats[2])):
        error_sum = abs(cs - s)
        if error_sum > 0.001:
            errors.append("mistakes in percentiles, {} row".format(i))

    assert not errors, "errors occured:\n{}".format("\n".join(errors))


def test_calculate_time_from_ctms(dfs, capsys):
    gold_df, created_df = dfs
    c_m.calculate_time_from_ctms(gold_df, created_df)
    captured = capsys.readouterr()
    assert captured.out[:40] == "start is 0.4, end is 4.2 and total: 3.80"
