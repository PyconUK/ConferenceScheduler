import conference_scheduler


def test_version_type():
    assert type(conference_scheduler.__version__) is str
