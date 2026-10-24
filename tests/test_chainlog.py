import json, os, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import chainlog

class T(unittest.TestCase):
    def setUp(self):
        self.p = os.path.join(tempfile.mkdtemp(), "a.jsonl")
        for i in range(3):
            chainlog.append(self.p, {"i": i, "msg": "안녕"}, ts=i)
    def lines(self):
        return open(self.p, encoding="utf-8").read().splitlines()
    def write(self, ls):
        open(self.p, "w", encoding="utf-8").write("\n".join(ls) + "\n")
    def test_ok(self):
        self.assertEqual(chainlog.verify(self.p), (True, 3, None))
    def test_edit(self):
        ls = self.lines(); e = json.loads(ls[1]); e["data"]["i"] = 99; ls[1] = json.dumps(e); self.write(ls)
        self.assertEqual(chainlog.verify(self.p)[2], 2)
    def test_delete(self):
        ls = self.lines(); del ls[0]; self.write(ls)
        self.assertFalse(chainlog.verify(self.p)[0])
    def test_reorder(self):
        ls = self.lines(); ls[1], ls[2] = ls[2], ls[1]; self.write(ls)
        self.assertFalse(chainlog.verify(self.p)[0])
    def test_garbage(self):
        open(self.p, "a").write("not json\n")
        self.assertEqual(chainlog.verify(self.p), (False, 3, 4))
    def test_cli(self):
        self.assertEqual(chainlog.main(["verify", self.p]), 0)

if __name__ == "__main__":
    unittest.main()
