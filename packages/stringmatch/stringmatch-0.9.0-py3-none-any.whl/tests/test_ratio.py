import pytest

from stringmatch.ratio import Ratio
from stringmatch.scorer import JaroScorer, JaroWinklerScorer, LevenshteinScorer, _Scorer


def test_ratio():
    assert Ratio().ratio("test", "test") == 100
    assert Ratio().ratio("bla", "nope") == 0
    assert Ratio().ratio("stringmatch", "strngmach") == 90
    assert Ratio().ratio("stringmatch", "eh") == 15

    assert Ratio(scorer=JaroWinklerScorer).ratio("searchlib", "srechlib") == 93
    assert Ratio(scorer=LevenshteinScorer).ratio("test", "th test") == 73
    assert Ratio(scorer=JaroWinklerScorer).ratio("test", "th test") == 60
    assert Ratio(scorer=JaroScorer).ratio("test", "th test") == 60

    with pytest.raises(TypeError):
        assert Ratio(scorer="nope").ratio("searchlib", "srechlib") == 82  # type: ignore

    with pytest.raises(NotImplementedError):
        assert Ratio(scorer=_Scorer).ratio("searchlib", "srechlib") == 82

    assert Ratio().ratio("", "f") == 0
    assert Ratio(LevenshteinScorer).ratio_list("test", ["th test", "hwatever"]) == [
        73,
        33,
    ]
    assert Ratio(JaroWinklerScorer).ratio_list("test", ["th test", "hwatever"]) == [
        60,
        58,
    ]

    assert Ratio().ratio("ジャパニーズ", "ziyapanizu", latinise=True) == 100
    # for the explanation: the skintone emojis are the yellow emojis + a tone modifier
    assert Ratio().ratio("👍", "👍🏻") == 67


def test_ratio_list():
    assert Ratio().ratio_list("test", ["test", "nope"]) == [100, 25]
    assert Ratio().ratio_list(
        "srechlib", ["searchlib", "slib", "searching library", "spam"]
    ) == [82, 67, 56, 17]
    assert Ratio().ratio_list("test", ["th TEST", "hwatever", "*"]) == [18, 33, 0]
    assert Ratio().ratio_list(
        "test", ["th TEST", "hwatever", "*"], ignore_case=True, only_letters=True
    ) == [73, 33, 0]
    assert Ratio(JaroWinklerScorer).ratio_list(
        "test", ["th TEST", "hwatever", "*"], ignore_case=True, only_letters=True
    ) == [60, 58, 0]


def test_partial_ratio():
    assert Ratio().partial_ratio("test124", "93210") == 20
    assert Ratio().partial_ratio("93210", "test124") == 20
    assert Ratio().partial_ratio("testbot test", "testbot") == 80
    assert Ratio().partial_ratio("TESTbot test", "testbot", ignore_case=True) == 80
    assert Ratio().partial_ratio("TESTbot test", "testbot", ignore_case=False) == 42
    assert Ratio().partial_ratio("a", "this is a test") == 13
    assert Ratio().partial_ratio("a test", "this is a test") == 60
    assert Ratio().partial_ratio("this", "this is a test") == 60
    assert Ratio().partial_ratio("this is a test", "this this this") == 71
