from difflib import SequenceMatcher
import pytest

from data_preparation import change_lex_pho


@pytest.mark.parametrize("source_corpus_file, reference_lexicon_file, g2p_mapping",[
    ("tests/data/finnish_corpus.txt", "tests/data/finnish_lexicon.txt", "g2p_mappings/phone-finnish-finnish.csv"),
    ("tests/data/sami_corpus.txt", "tests/data/sami_lexicon.txt", "g2p_mappings/phone-sami-finnish.csv"),
    ("tests/data/estonian_corpus.txt", "tests/data/estonian_lexicon.txt", "g2p_mappings/phone-estonian-finnish.csv")
])

def test_g2p_finnish(source_corpus_file, reference_lexicon_file, g2p_mapping, tmp_path):
    with open(reference_lexicon_file, "r", encoding="utf-8") as baseline_lexicon_file:
        baseline_lexicon = baseline_lexicon_file.read()

    tmp_lexicon_file = tmp_path / "lexicon_tests/lexicon.txt"
    tmp_lexicon_file.parent.mkdir()
    change_lex_pho.main(source_corpus_file, g2p_mapping, str(tmp_lexicon_file))

    with open(str(tmp_lexicon_file), "r", encoding="utf-8") as testable_lexicon_file:
        testable_lexicon = testable_lexicon_file.read()

    seq_matcher = SequenceMatcher(None, baseline_lexicon, testable_lexicon)
    op_codes = seq_matcher.get_opcodes()
    assert len(op_codes) == 1 and op_codes[0][0] == "equal"






