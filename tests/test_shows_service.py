def test_duration_min_param(shows_service):
    duration_min = 50
    shows = shows_service.get_list(duration_min=duration_min)
    assert all(show.duration >= duration_min for show in shows)


def test_duration_max_param(shows_service):
    duration_max = 50
    shows = shows_service.get_list(duration_max=duration_max)
    assert all(show.duration <= duration_max for show in shows)
