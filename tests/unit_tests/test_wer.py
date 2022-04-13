import pytest
from finnish_forced_alignment.alignment import wer

@pytest.mark.parametrize("hypothesis, reference, wer_reference", [
    ("testi on",
    "testi ei",
    {'WER': 0.25, 'Cor': 6, 'Sub': 2, 'Ins': 0, 'Del': 0}),

    (['pitää', 'testata', 'myös', 'ääkkösiä'],
    ['pitääkö', 'testata', 'myös', 'ääkkösiä'],
    {'WER': 0.25, 'Cor': 3, 'Sub': 1, 'Ins': 0, 'Del': 0}),

    (['no', 'nyt', 'sitten', 'on', 'jo', 'on', 'hyvä'],
    ['no', 'nyt', 'sit', 'jo', 'hyvä'],
    {'WER': 0.429, 'Cor': 4, 'Sub': 1, 'Ins': 0, 'Del': 2}),

    #This should actually have one more corr, two less sub,  one more del and ins
    (['Suopma', 'lei', 'jieŋa', 'vuolde', 'maŋimus', 'jiekŋabaji', 'áigge'],
    ['jieŋa', 'vuolle', 'maŋimus', 'lei', 'jiekŋabaji'],
    {'WER': 0.714, 'Cor': 2, 'Sub': 3, 'Ins': 0, 'Del': 2})
])

def test_wer(hypothesis, reference, wer_reference):
    wer_results = wer.wer(hypothesis, reference)
    assert wer_results[0] == wer_reference
