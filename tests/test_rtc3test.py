#
# License: See LICENSE.md file
# GitHub: https://github.com/Baekalfen/PyBoy
#

import os.path
from pathlib import Path

import PIL
import pytest

from pyboy import PyBoy, WindowEvent

OVERWRITE_PNGS = False


# https://github.com/aaaaaa123456789/rtc3test
@pytest.mark.skip("RTC is too unstable")
@pytest.mark.parametrize("subtest", [0, 1, 2])
def test_rtc3test(subtest, rtc3test_file):
    pyboy = PyBoy(rtc3test_file, window_type="headless")
    pyboy.set_emulation_speed(0)
    for _ in range(59):
        pyboy.tick(True)

    for _ in range(25):
        pyboy.tick(True)

    for n in range(subtest):
        pyboy.button("down")
        pyboy.tick(2, True)

    pyboy.button("a")
    pyboy.tick(2, True)

    while True:
        # Continue until it says "(A) Return"
        if pyboy.tilemap_background()[6:14, 17] == [193, 63, 27, 40, 55, 56, 53, 49]:
            break
        pyboy.tick(True)

    png_path = Path(f"tests/test_results/{rtc3test_file}_{subtest}.png")
    image = pyboy.screen().screen_image()
    if OVERWRITE_PNGS:
        png_path.parents[0].mkdir(parents=True, exist_ok=True)
        image.save(png_path)
    else:
        old_image = PIL.Image.open(png_path)
        diff = PIL.ImageChops.difference(image, old_image)
        if diff.getbbox() and not os.environ.get("TEST_CI"):
            image.show()
            old_image.show()
            diff.show()
        assert not diff.getbbox(), f"Images are different! {rtc3test_file}_{subtest}"

    pyboy.stop(save=False)
