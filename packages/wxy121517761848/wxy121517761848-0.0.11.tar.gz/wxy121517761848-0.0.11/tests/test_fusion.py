def test__get_canonical_root_url():
    from wxy121517761848.fusion import _get_canonical_root_url

    some_url = "https://fusion-api.jpmorgan.com/fusion/v1/a_given_resource"
    root_url = "https://fusion-api.jpmorgan.com"
    assert root_url == _get_canonical_root_url(some_url)


def test_FusionCredentials(example_creds_dict):
    from wxy121517761848.fusion import FusionCredentials

    FusionCredentials.from_dict(example_creds_dict)


def test_FusionCredentials_no_pxy(example_creds_dict_no_pxy):
    from wxy121517761848.fusion import FusionCredentials

    FusionCredentials.from_dict(example_creds_dict_no_pxy)


def test_FusionCredentials_empty_pxy(example_creds_dict_empty_pxy):
    from wxy121517761848.fusion import FusionCredentials

    FusionCredentials.from_dict(example_creds_dict_empty_pxy)
