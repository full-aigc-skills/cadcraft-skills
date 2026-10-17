"""孔位参数与实际实体检查的正反例。"""
import importlib.util
import math
from pathlib import Path
import unittest
s=importlib.util.spec_from_file_location('bolt',Path(__file__).resolve().parents[1]/'skills/cadcraft-bolt-circle/scripts/draw_bolt_circle.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class BoltTests(unittest.TestCase):
    def test_count_includes_seed_and_no_duplicate_endpoint(self):
        p=m.plan(6,40,3,55,15)
        self.assertEqual(len(p),6);self.assertEqual(p[0],[40,0]);self.assertAlmostEqual(p[3][0],-40)
        self.assertEqual(len({(round(x,7),round(y,7)) for x,y in p}),6)
    def test_offset_and_start_angle(self):
        p=m.plan(4,40,3,55,15,90,(100,50));self.assertAlmostEqual(p[0][0],100);self.assertAlmostEqual(p[0][1],90)
    def test_reject_invalid_sizes_and_counts(self):
        for args in [(True,40,3,55,15),(6,math.nan,3,55,15),(6,40,3,43,15),(6,40,3,55,37),(60,40,3,55,15),(6,40,True,55,15)]:
            with self.subTest(args=args),self.assertRaises(ValueError):m.plan(*args)
    def test_wrong_radius_and_duplicate_rejected(self):
        e={'layer':'BOLT_HOLES','type':'Circle','geometry':{'center':{'x':40,'y':0},'radius':3}}
        self.assertEqual(m.verify({'entities':[e]},[[40,0]],3),1)
        with self.assertRaises(AssertionError):m.verify({'entities':[e,e]},[[40,0],[40,0]],3)
        with self.assertRaises(AssertionError):m.verify({'entities':[e]},[[40,0]],4)
if __name__=='__main__':unittest.main()
