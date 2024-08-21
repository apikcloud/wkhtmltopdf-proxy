from app.main import parse_args


class BaseClass:
    args = []
    dict_args = {}
    output = ""
    bodies = []
    cookies = []

    def test_01_keys_count(self):
        res = parse_args(self.args)
        assert len(list(self.dict_args.keys())) == len(res["dict_args"].keys())

    def test_02_keys(self):
        res = parse_args(self.args)
        assert set(self.dict_args.keys()) == set(res["dict_args"].keys())

    def test_03_values_count(self):
        res = parse_args(self.args)
        assert len(list(self.dict_args.values())) == len(res["dict_args"].values())

    def test_04_values(self):
        res = parse_args(self.args)
        for key, value in self.dict_args.items():
            assert value == res["dict_args"].get(key)

    def test_05_bodies_count(self):
        res = parse_args(self.args)
        assert len(self.bodies) == len(res["bodies"])

    def test_06_bodies(self):
        res = parse_args(self.args)
        assert set(self.bodies) == set(res["bodies"])

    def test_07_output(self):
        res = parse_args(self.args)
        assert self.output == res["output"]

    def test_08_cookies(self):
        if not self.cookies:
            return
        res = parse_args(self.args)

        assert isinstance(res["dict_args"].get("cookie"), list)
        assert len(self.cookies) == len(res["dict_args"]["cookie"])
