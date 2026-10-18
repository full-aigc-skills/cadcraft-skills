import importlib.util
from pathlib import Path
import unittest
s=importlib.util.spec_from_file_location('room_plan',Path(__file__).parents[1]/'scripts/room_plan.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
class RoomPlanTests(unittest.TestCase):
    def data(self):return dict(width=5000,depth=4000,door_start=2000,door_width=1000,label='会议室')
    def test_geometry(self):
        p=m.build_plan(self.data());self.assertEqual(p['geometry']['doorGap'],[2000,3000]);self.assertEqual([c['params']['value'] for c in p['steps'] if c['command']=='setvar'],[4,100]);self.assertEqual(len([c for c in p['steps'] if c['command']=='dimlinear']),2)
    def test_label_preserved(self):self.assertEqual(next(c for c in m.build_plan(self.data())['steps'] if c['command']=='text')['params']['text'],'会议室')
    def test_edges_skip_zero_length_wall(self):
        d=self.data();d['door_start']=0;p=m.build_plan(d)
        for c in p['steps']:
            if c['command']=='line':self.assertNotEqual(c['params']['points'][0],c['params']['points'][1])
    def test_reject_invalid_opening(self):
        for start,door in [(-1,1000),(4500,1000),(0,4500),(0,0)]:
            d=self.data();d.update(door_start=start,door_width=door)
            with self.subTest(start=start,door=door),self.assertRaises(ValueError):m.build_plan(d)
    def test_reject_nonfinite_and_bool(self):
        for value in [True,float('nan'),float('inf'),10**1000]:
            d=self.data();d['width']=value
            with self.subTest(value=repr(value)[:30]),self.assertRaises(ValueError):m.build_plan(d)
    def test_reject_label_break(self):
        d=self.data();d['label']='A\nB'
        with self.assertRaises(ValueError):m.build_plan(d)
if __name__=='__main__':unittest.main()
