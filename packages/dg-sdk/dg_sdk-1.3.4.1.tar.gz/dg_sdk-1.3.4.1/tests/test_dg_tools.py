import unittest
from tests.conftest import *


class TestDGTools(unittest.TestCase):

    def setUp(self):

        print("setup")

    def tearDown(self):
        print("tearDown")

    def test_verfy_sign(self):
        data = {"resp_desc":"业务执行失败","req_seq_id":"202204181801142405249","req_date":"20220418","resp_code":"90000000","huifu_id":"6666000108854952"}
        sign = "CUWBV7RUGb0cvaxvnh97giA78Z5ZWKvlQOwTpNqLjigeKZSiWmp1EgPqjMZM/UnhNcpglLHZo/DFep3X05Ycdwsyqv7PkSnN/AXpi6UofQGsaxKaWNUokKfGN5TUWDsW6H843br0WNWMdRMAD1nmKj+B5pl8+HwjEv44hXUT6P+o/kPKZAlZLhBejT46L3mjoVSoiMxLpL7HSgUn43iWgCDEfWZLN6RNkn3/t/3UXtiwimc01Bqh+GbW/no95RN4BcYkJK18BjIhsLqtNvXHXkdcczofwpfa5EfEiR7h33cuqUvGGfpGbiSrxmqzoMF4kRGx242rD2nnSZZ6bIlnog=="
        result = dg_sdk.DGTools.verify_sign(data, sign)
        print(result)
