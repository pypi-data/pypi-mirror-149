import os

import large_image
import pytest
import requests
from server_thread import ServerDownError, ServerManager

from localtileserver.client import (
    DEMO_REMOTE_TILE_SERVER,
    RemoteTileClient,
    TileClient,
    get_or_create_tile_client,
)
from localtileserver.tileserver.utilities import get_clean_filename, get_tile_source

skip_pil_source = True
try:
    import large_image_source_pil  # noqa

    skip_pil_source = False
except ImportError:
    pass

TOLERANCE = 2e-2


def get_content(url):
    r = requests.get(url)
    r.raise_for_status()
    return r.content


def test_create_tile_client(bahamas_file):
    assert ServerManager.server_count() == 0
    tile_client = TileClient(bahamas_file, debug=True)
    assert tile_client.filename == get_clean_filename(bahamas_file)
    assert tile_client.server_port
    assert tile_client.server_base_url
    assert "bounds" in tile_client.metadata()
    assert tile_client.bounds()
    center = tile_client.center()
    assert center[0] == pytest.approx(24.5579, abs=TOLERANCE)
    assert center[1] == pytest.approx(-77.7668, abs=TOLERANCE)
    tile_url = tile_client.get_tile_url().format(z=8, x=72, y=110)
    r = requests.get(tile_url)
    r.raise_for_status()
    assert r.content
    tile_url = tile_client.get_tile_url(grid=True).format(z=8, x=72, y=110)
    r = requests.get(tile_url)
    r.raise_for_status()
    assert r.content
    tile_url = tile_client.create_url("api/tiles/debug/{z}/{x}/{y}.png".format(z=8, x=72, y=110))
    r = requests.get(tile_url)
    r.raise_for_status()
    assert r.content
    tile_url = tile_client.get_tile_url(palette="matplotlib.Plasma_6").format(z=8, x=72, y=110)
    r = requests.get(tile_url)
    r.raise_for_status()
    assert r.content
    path = tile_client.thumbnail()
    assert os.path.exists(path)
    tile_client.shutdown(force=True)


def test_create_tile_client_bad(bahamas_file):
    with pytest.raises(OSError):
        TileClient("foo.tif", debug=True)
    with pytest.raises(ValueError):
        TileClient(bahamas_file, port="0", debug=True)


def test_client_force_shutdown(bahamas):
    tile_url = bahamas.get_tile_url().format(z=8, x=72, y=110)
    r = requests.get(tile_url)
    r.raise_for_status()
    assert r.content
    assert ServerManager.server_count() == 1
    bahamas.shutdown(force=True)
    assert ServerManager.server_count() == 0
    with pytest.raises(requests.ConnectionError):
        r = requests.get(tile_url)
        r.raise_for_status()
    with pytest.raises(ServerDownError):
        bahamas.bounds()


def test_multiple_tile_clients_one_server(bahamas, blue_marble):
    assert ServerManager.server_count() == 1
    tile_url_a = bahamas.get_tile_url().format(z=8, x=72, y=110)
    tile_url_b = blue_marble.get_tile_url().format(z=8, x=72, y=110)
    assert get_content(tile_url_a) != get_content(tile_url_b)
    thumb_url_a = bahamas.create_url("api/thumbnail.png")
    thumb_url_b = blue_marble.create_url("api/thumbnail.png")
    assert get_content(thumb_url_a) != get_content(thumb_url_b)


def test_extract_roi_world(bahamas):
    # -78.047, -77.381, 24.056, 24.691
    path = bahamas.extract_roi(-78.047, -77.381, 24.056, 24.691)
    assert path.exists()
    source = get_tile_source(path)
    assert source.getMetadata()["geospatial"]


def test_extract_roi_pixel(bahamas):
    path = bahamas.extract_roi_pixel(100, 500, 300, 600)
    assert path.exists()
    source = get_tile_source(path)
    assert source.getMetadata()["geospatial"]


@pytest.mark.skipif(skip_pil_source, reason="`large-image-source-pil` not installed")
def test_extract_roi_pixel_pil(bahamas):
    path = bahamas.extract_roi_pixel(100, 500, 300, 600, encoding="PNG")
    assert path.exists()
    source = get_tile_source(path)
    assert "geospatial" not in source.getMetadata()


def test_caching_query_params(bahamas):
    thumb_url_a = bahamas.create_url("api/thumbnail.png")
    thumb_url_b = bahamas.create_url("api/thumbnail.png?band=1")
    assert get_content(thumb_url_a) != get_content(thumb_url_b)
    thumb_url_c = bahamas.create_url("api/thumbnail.png")
    assert get_content(thumb_url_a) == get_content(thumb_url_c)


def test_multiband(bahamas):
    # Create an RGB tile in several ways and make sure all same
    url_a = bahamas.get_tile_url(
        band=[1, 2, 3],
    ).format(z=8, x=72, y=110)
    url_b = bahamas.get_tile_url(
        band=[3, 2, 1],
        palette=["b", "g", "r"],
    ).format(z=8, x=72, y=110)
    url_c = bahamas.get_tile_url().format(z=8, x=72, y=110)
    assert get_content(url_a) == get_content(url_b) == get_content(url_c)
    # Check that other options are well handled
    url = bahamas.get_tile_url(
        band=[1, 2, 3],
        palette=["b", "g", "r"],
        vmin=0,
        vmax=300,
        nodata=0,
    ).format(z=8, x=72, y=110)
    assert get_content(url)  # just make sure it doesn't fail


@pytest.mark.xfail
def test_remote_client(remote_file_url):
    tile_client = RemoteTileClient(remote_file_url, host=DEMO_REMOTE_TILE_SERVER)
    assert tile_client.metadata()
    url = tile_client.get_tile_url(projection=None).format(z=0, x=0, y=0)
    assert get_content(url)


def test_launch_non_default_server(bahamas_file):
    default = TileClient(bahamas_file)
    diff = TileClient(bahamas_file, port=0)
    assert default.server != diff.server
    assert default.server_port != diff.server_port


def test_get_or_create_tile_client(bahamas_file, remote_file_url):
    tile_client, _ = get_or_create_tile_client(bahamas_file)
    same, created = get_or_create_tile_client(tile_client)
    assert not created
    assert tile_client == same
    diff, created = get_or_create_tile_client(bahamas_file)
    assert created
    assert tile_client != diff
    with pytest.raises(requests.HTTPError):
        _, _ = get_or_create_tile_client(__file__)
    tile_client = RemoteTileClient(remote_file_url, host=DEMO_REMOTE_TILE_SERVER)
    same, created = get_or_create_tile_client(tile_client)
    assert not created
    assert tile_client == same


def test_pixel(bahamas):
    pix = bahamas.pixel(0, 0)  # pixel space
    assert "bands" in pix
    pix = bahamas.pixel(
        24.56, -77.76, units="EPSG:4326", projection="EPSG:3857"
    )  # world coordinates
    assert "bands" in pix


def test_histogram(bahamas):
    hist = bahamas.histogram()
    assert len(hist)


def test_custom_palette(bahamas):
    palette = ["#006633", "#E5FFCC", "#662A00", "#D8D8D8", "#F5F5F5"]
    thumbnail = bahamas.thumbnail(
        band=1,
        palette=palette,
        scheme="discrete",
    )
    assert thumbnail  # TODO: check colors in produced image
    thumbnail = bahamas.thumbnail(
        band=1,
        cmap=palette,
        scheme="linear",
    )
    assert thumbnail  # TODO: check colors in produced image


def test_style_dict(bahamas):
    style = {
        "bands": [
            {"band": 1, "palette": ["#000", "#0f0"]},
        ]
    }
    thumbnail = bahamas.thumbnail(
        style=style,
    )
    assert thumbnail  # TODO: check colors in produced image


def test_pixel_space_tiles(pelvis):
    tile_url = pelvis.get_tile_url().format(z=0, x=0, y=0)
    assert "projection=none" in tile_url.lower()
    r = requests.get(tile_url)
    r.raise_for_status()
    assert r.content


def test_large_image_to_client(bahamas_file):
    src = large_image.open(bahamas_file)
    tile_client = TileClient(src)
    assert tile_client.filename == get_clean_filename(bahamas_file)
    assert "bounds" in tile_client.metadata()


def test_default_zoom(bahamas):
    assert bahamas.default_zoom == 8
