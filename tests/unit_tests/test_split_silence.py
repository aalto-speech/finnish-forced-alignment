import pytest
from finnish_forced_alignment.data_handling import split_silence
from finnish_forced_alignment.alignment import calculate_metrics as c_m


@pytest.fixture
def dfs():
    gold_df, created_df = c_m.create_ctm_dfs("tests/data/gold.ctm", "tests/data/created.ctm")
    return gold_df, created_df


def test_split_middle(dfs):
    pass
