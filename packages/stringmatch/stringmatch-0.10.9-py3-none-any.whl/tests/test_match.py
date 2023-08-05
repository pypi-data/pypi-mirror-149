from stringmatch.match import Match
from stringmatch.scorer import JaroScorer, JaroWinklerScorer, LevenshteinScorer, _Scorer


def test_match():
    assert Match().match("test", "test") is True
    assert Match().match("stringmatch", "something else") is False
    assert Match().match("stringmatch", "strngmach") is True
    assert (
        Match(latinise=True, remove_punctuation=True).match("séàr#.chlib", "searchlib")
        is True
    )
    assert Match(ignore_case=False).match("test", "TEST") is False
    assert Match(ignore_case=True).match("test", "TEST") is True
    assert Match(only_letters=True).match("test", "-- test --!<<><") is True
    assert Match().match("", "f") is False

    assert Match(latinise=True).match("séärçh", "search") is True
    assert Match(latinise=False).match("séärçh", "search") is False

    assert Match(remove_punctuation=True).match("test,---....", "test") is True
    assert Match(remove_punctuation=False).match("test,---....", "test") is False

    assert Match(only_letters=True).match("»»ᅳtestᅳ►", "test") is True
    assert Match(only_letters=False).match("»»ᅳtestᅳ►", "test") is False

    assert Match(scorer=LevenshteinScorer).match("test", "th test") is True
    assert Match(scorer=JaroWinklerScorer).match("test", "th test") is False

    assert (
        Match(include_partial=True).match("testbot testmann", "testbot", score=69)
        is True
    )
    assert (
        Match(include_partial=False).match("testbot testmann", "testbot", score=69)
        is False
    )


def test_match_with_ratio():
    assert Match().match_with_ratio("test", "test") == (True, 100)
    assert Match().match_with_ratio("test", "nope") == (False, 25)
    assert Match().match_with_ratio("searchlib", "srechlib") == (True, 82)
    assert Match(scorer=JaroWinklerScorer).match_with_ratio("test", "th test") == (
        False,
        60,
    )
    assert Match(ignore_case=True).match_with_ratio("Woosh", "woosh") == (True, 100)
    assert Match(include_partial=True).match_with_ratio(
        "testbot testmann", "testbot", score=69
    ) == (True, 75)
    assert Match(include_partial=False).match_with_ratio(
        "testbot testmann", "testbot"
    ) == (False, 61)
    assert Match(include_partial=True).match_with_ratio(
        "A string", "A string thats like really really long", score=55
    ) == (True, 69)
    assert Match(include_partial=False).match_with_ratio(
        "A string", "A string thats like really really long", score=55
    ) == (False, 35)

    class MyOwnScorer(_Scorer):
        def score(self, string1: str, string2: str) -> float:
            return 1

    assert Match(scorer=MyOwnScorer).match_with_ratio("anything", "whatever") == (
        True,
        100,
    )


def test_get_best_match():
    assert Match().get_best_match("test", ["test", "nope", "tset"]) == "test"
    assert Match().get_best_match("whatever", ["test", "nope", "tset"]) is None

    searches = ["stringmat", "strinma", "strings", "mtch", "whatever", "s"]
    assert Match().get_best_match("stringmatch", searches) == "stringmat"
    assert Match().get_best_matches("stringmatch", searches) == ["stringmat", "strinma"]

    assert Match().get_best_match("", ["f"]) is None

    assert (
        Match(remove_punctuation=True).get_best_match("....-", ["....-", "f"]) is None
    )

    assert (
        Match(
            ignore_case=True, include_partial=True, scorer=JaroWinklerScorer
        ).get_best_match("official", ["Africa", "「 Tournament Official 」"])
    ) == "Africa"
    assert (
        Match(
            ignore_case=True, include_partial=True, scorer=LevenshteinScorer
        ).get_best_match("official", ["Africa", "「 Tournament Official 」"], score=40)
    ) == "「 Tournament Official 」"
    assert (
        Match(
            ignore_case=True, include_partial=True, scorer=LevenshteinScorer
        ).get_best_match("official", ["Africa", "「 Tournament Official 」"], score=90)
    ) is None
    assert (
        Match(
            ignore_case=True,
            include_partial=True,
            scorer=LevenshteinScorer,
            only_letters=True,
        ).get_best_match("officia", ["Africa", "「 Tournament Official 」"])
    ) == "「 Tournament Official 」"
    assert (
        Match(
            ignore_case=True,
            include_partial=True,
            scorer=JaroScorer,
            only_letters=True,
        ).get_best_match("officia", ["Africa", "「 Tournament Official 」"])
    ) == "Africa"


def test_get_best_match_with_ratio():
    assert Match().get_best_match_with_ratio("test", ["test", "nope", "tset"]) == (
        "test",
        100,
    )
    assert (
        Match().get_best_match_with_ratio("whatever", ["test", "nope", "tset"]) is None
    )
    assert Match(ignore_case=True, include_partial=True).get_best_match_with_ratio(
        "official", ["Africa", "「 Tournament Official 」"], score=40
    ) == ("「 Tournament Official 」", 69)
    assert Match(include_partial=True, only_letters=True).get_best_match_with_ratio(
        "official", ["Africa", "「 Tournament Official 」"], score=40
    ) == ("「 Tournament Official 」", 66)
    assert Match(include_partial=True, latinise=True).get_best_match_with_ratio(
        "öfficiäl", ["Africa", "「 Tournament Official 」"], score=40
    ) == ("「 Tournament Official 」", 61)
    assert Match(include_partial=True, latinise=False).get_best_match_with_ratio(
        "öfficiäl", ["Africa", "「 Tournament Official 」"], score=40
    ) == ("「 Tournament Official 」", 52)


def test_get_best_matches():
    assert Match().get_best_matches("test", ["test", "nope", "tset"]) == [
        "test",
        "tset",
    ]

    searches = ["limit 5", "limit 4", "limit 3", "limit 2", "limit 1", "limit 0"]

    assert Match().get_best_matches("limit 5", searches, limit=2) == [
        "limit 5",
        "limit 4",
    ]

    assert Match().get_best_matches("limit 5", searches, limit=None) == searches

    assert Match().get_best_matches("", ["f"]) == []

    assert Match().get_best_matches("test", ["test", "nope", "tset"], limit=0) == [
        "test",
        "tset",
    ]

    assert Match(ignore_case=True, include_partial=True).get_best_matches_with_ratio(
        "official", ["Africa", "「 Tournament Official 」"], score=40
    ) == [("「 Tournament Official 」", 69), ("Africa", 57)]

    assert Match().get_best_matches("test", ["test", "nope", "tset"], limit=None) == [
        "test",
        "tset",
    ]

    assert Match(ignore_case=True).get_best_matches(
        "inc", ["Link", "Incineroar", "Pichu", "Sonic"], score=40, limit=25
    ) == ["Link", "Pichu", "Sonic", "Incineroar"]


def test_get_best_matches_with_ratio():
    assert Match().get_best_matches_with_ratio("test", ["test", "nope", "tset"]) == [
        ("test", 100),
        ("tset", 75),
    ]
    assert Match().get_best_matches_with_ratio(
        "limit 5",
        ["limit 5", "limit 4", "limit 3", "limit 2", "limit 1", "limit 0"],
        limit=2,
    ) == [("limit 5", 100), ("limit 4", 86)]

    assert (
        Match(
            ignore_case=True,
            include_partial=True,
            scorer=LevenshteinScorer,
            only_letters=True,
        ).get_best_matches_with_ratio(
            "officia", ["Africa", "「 Tournament Official 」"], score=50
        )
    ) == [("「 Tournament Official 」", 75), ("Africa", 62)]
    assert (
        Match(
            ignore_case=True,
            include_partial=True,
            scorer=JaroScorer,
            only_letters=True,
        ).get_best_matches_with_ratio(
            "officia", ["Africa", "「 Tournament Official 」"], score=50
        )
    ) == [("Africa", 75), ("「 Tournament Official 」", 75)]

    assert Match(include_partial=True).get_best_matches_with_ratio(
        "level 10", ["level 100", "level 10"]
    ) == [("level 10", 100), ("level 100", 97)]

    assert Match(include_partial=True).get_best_matches_with_ratio(
        "test", ["", None, "testo"], score=1  # type: ignore
    ) == [("testo", 97)]

    assert Match(include_partial=True).get_best_matches_with_ratio(
        "0", ["0", 0], score=0  # type: ignore
    ) == [("0", 100), (0, 0)]

    assert Match().get_best_matches_with_ratio("test", [5], score=0) == [(5, 0)]  # type: ignore

    assert Match().get_best_matches_with_ratio("test", [True], score=0) == [(True, 0)]  # type: ignore

    assert Match(latinise=True).get_best_matches_with_ratio(
        "test", [None, "nope", "tset"], score=0  # type: ignore
    ) == [("tset", 75), ("nope", 25), (None, 0)]
