from unittest import TestCase

import numpy as np
import pandas as pd

from km3astro.time import np_to_datetime
from km3astro.random import (
    second_from_interval,
    equidistant_from_interval,
    random_date,
)


class TestTime(TestCase):
    def test_np_datetime(self):
        cur = np.datetime64("2017-03-07T15:05:54.117605")
        assert np.alltrue(cur == np_to_datetime([cur]))
        assert np.alltrue(cur == np_to_datetime(cur))

    def test_rand(self):
        randtime = random_date(n=100)
        np_to_datetime(randtime)

    def test_dataframe(self):
        df = pd.DataFrame({"time": random_date(n=100)})
        np_to_datetime(df.time)
