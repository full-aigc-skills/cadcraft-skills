"""把毫米房间尺寸生成独立CADCraft新图命令计划。"""
import argparse
import json
import math
from pathlib import Path


def build_plan(data):
    if not isinstance(data,dict):raise ValueError('input must be an object')
    values=[data.get(k) for k in ('width','depth','door_start','door_width')]
    if any(type(v) not in (int,float) or abs(v)>1000000 or not math.isfinite(v) for v in values):
        raise ValueError('finite millimetre dimensions within one million required')
    width,depth,start,door=values
    if min(width,depth)<500 or door<100 or start<0 or start+door>width or door>depth:
        raise ValueError('invalid room or door outside room boundary')
    label=data.get('label')
    if not isinstance(label,str) or not label.strip() or len(label)>40 or any(ord(c)<32 or c in '\u2028\u2029' for c in label):
        raise ValueError('room label must contain1..40 single-line characters')
    offset=max(width,depth)*0.12;steps=[]
    def cmd(name,params):steps.append({'command':name,'params':params})
    def line(points):cmd('line',{'points':points})
    cmd('setvar',{'name':'INSUNITS','value':4});cmd('setvar',{'name':'DIMSCALE','value':max(width,depth)/50})
    cmd('layer.new',{'name':'WALLS','color':7,'current':True})
    if start>0:line([[0,0],[start,0]])
    if start+door<width:line([[start+door,0],[width,0]])
    line([[width,0],[width,depth],[0,depth],[0,0]])
    cmd('layer.new',{'name':'DOOR','color':1,'current':True});line([[start,0],[start,door]])
    cmd('arc',{'center':[start,0],'radius':door,'start':0,'end':90})
    cmd('layer.new',{'name':'LABELS','color':7,'current':True});cmd('text',{'at':[width*0.35,depth*0.5],'text':label,'height':min(width,depth)/20})
    cmd('layer.new',{'name':'DIMENSIONS','color':7,'current':True})
    cmd('dimlinear',{'p1':[0,0],'p2':[width,0],'at':[width/2,-offset]})
    cmd('dimlinear',{'p1':[width,0],'p2':[width,depth],'at':[width+offset,depth/2]})
    return {'schema':'cadcraft-room-plan/v1','newDocumentOnly':True,'unit':'mm','steps':steps,'geometry':{'width':width,'depth':depth,'doorGap':[start,start+door],'hinge':[start,0],'swingRadius':door},'checks':['Reopen DXF and measure actual endpoints and two dimensions','Inspect door gap, leaf and swing arc; no wall through opening','Render label and dimensions for overlap and font coverage'],'boundary':'Single-line room diagram only; no wall thickness, windows, services, structural or construction design'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();plan=build_plan(json.loads(a.input.read_text(encoding='utf-8')))
    with a.output.open('x',encoding='utf-8') as f:json.dump(plan,f,ensure_ascii=False,indent=2);f.write('\n')
if __name__=='__main__':main()
