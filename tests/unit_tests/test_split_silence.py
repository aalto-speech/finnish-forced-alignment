import numpy as np
import pytest
from analysis import split_silences



@pytest.fixture
def dfs():
    gold_df, created_df = c_m.create_ctm_dfs("tests/data/gold.ctm", "tests/data/created.ctm")
    return gold_df, created_df


def test_split_middle(dfs):
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


def test_calculate_time_from_ctms(dfs, capsys):
    gold_df, created_df = dfs
    c_m.calculate_time_from_ctms(gold_df, created_df)
    captured = capsys.readouterr()
    assert captured.out[:40] == "start is 0.4, end is 4.2 and total: 3.80"
