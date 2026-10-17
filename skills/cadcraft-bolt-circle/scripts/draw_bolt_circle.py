#!/usr/bin/env python3
"""以真实CADCraft CLI绘制新孔位图并回读几何，不覆盖已有输出。"""
import argparse
import json
import math
from pathlib import Path
import subprocess
import tempfile


def plan(count, pitch, hole, outer, bore, start=0, center=(0, 0)):
    if type(count) is not int or not 3 <= count <= 360:
        raise ValueError('count must be an integer between 3 and 360')
    values=[pitch,hole,outer,bore,start,*center]
    if len(center)!=2 or any(type(v) not in (int,float) or not math.isfinite(v) for v in values):
        raise ValueError('all coordinates and sizes must be finite numbers')
    if min(pitch,hole,outer)<=0 or bore<0:
        raise ValueError('invalid radius')
    if pitch+hole>=outer or pitch-hole<=bore or pitch*math.sin(math.pi/count)<=hole:
        raise ValueError('holes touch or intersect each other or a boundary')
    return [[center[0]+pitch*math.cos(math.radians(start+360*i/count)),
             center[1]+pitch*math.sin(math.radians(start+360*i/count))] for i in range(count)]


def inspect_lines(text):
    return [json.loads(line) for line in text.splitlines() if line.lstrip().startswith('{')]


def verify(drawing, centers, radius):
    holes=[e for e in drawing['entities'] if e['layer']=='BOLT_HOLES']
    if len(holes)!=len(centers):raise AssertionError('wrong hole count')
    remaining=list(holes)
    for x,y in centers:
        matches=[e for e in remaining if e['type']=='Circle' and
                 math.isclose(e['geometry']['center']['x'],x,abs_tol=1e-7) and
                 math.isclose(e['geometry']['center']['y'],y,abs_tol=1e-7) and
                 math.isclose(e['geometry']['radius'],radius,abs_tol=1e-7)]
        if len(matches)!=1:raise AssertionError('hole center/radius or duplicate hole mismatch')
        remaining.remove(matches[0])
    return len(holes)


def draw(cli, output, count=6, pitch=40, hole=3, outer=55, bore=15, start=0, center=(0,0)):
    centers=plan(count,pitch,hole,outer,bore,start,center)
    output=Path(output).resolve()
    if output.suffix.lower()!='.dxf':raise ValueError('output must be a new .dxf')
    targets=[output,output.with_suffix('.png'),output.with_suffix('.svg')]
    if any(p.exists() for p in targets):raise FileExistsError('output or derivative already exists')
    output.parent.mkdir(parents=True,exist_ok=True)
    calls=[]
    def run(*args):
        calls.append(list(args));p=subprocess.run([str(cli),*map(str,args)],capture_output=True,text=True,encoding='utf-8',timeout=120)
        if p.returncode:raise RuntimeError(p.stderr or p.stdout)
        return p.stdout
    def cmd(name,args):return name+' '+json.dumps(args,ensure_ascii=True,separators=(',',':'))
    with tempfile.TemporaryDirectory(prefix='cad-bolt-') as temp:
        seed=Path(temp)/'seed.dxf'
        initial=['run','--metric','--cmd',cmd('setvar',{'name':'INSUNITS','value':4}),
                 '--cmd',cmd('layer.new',{'name':'OUTLINE','color':7,'current':True}),
                 '--cmd',cmd('circle',{'center':center,'radius':outer})]
        if bore:initial+=['--cmd',cmd('circle',{'center':center,'radius':bore})]
        initial+=['--cmd',cmd('layer.new',{'name':'BOLT_HOLES','color':7,'current':True}),
                  '--cmd',cmd('circle',{'center':centers[0],'radius':hole}),
                  '--cmd',cmd('drawing.inspect',{'entities':True,'limit':2000}),'--save',str(seed)]
        initial_drawing=next(x for x in inspect_lines(run(*initial)) if 'entities' in x)
        verify(initial_drawing,[centers[0]],hole)
        handle=next(e['handle'] for e in initial_drawing['entities'] if e['layer']=='BOLT_HOLES')
        label=[center[0]+outer+15,center[1]-10]
        array=['run',str(seed),'--cmd',cmd('arraypolar',{'handles':[handle],'center':center,'count':count,'angle':360,'rotate':True,'associative':False}),
               '--cmd',cmd('layer.new',{'name':'PITCH_GUIDE','color':8,'current':True}),
               '--cmd',cmd('circle',{'center':center,'radius':pitch}),
               '--cmd',cmd('setvar',{'name':'DIMSCALE','value':0.5}),
               '--cmd',cmd('layer.new',{'name':'DIMENSIONS','color':7,'current':True}),
               '--cmd',cmd('dimradius',{'handle':handle,'at':label}),
               '--save',str(output)]
        run(*array)
    reopened=next(x for x in inspect_lines(run('run',str(output),'--cmd',cmd('drawing.inspect',{'entities':True,'limit':2000}))) if 'entities' in x)
    verify(reopened,centers,hole)
    for target in targets[1:]:
        run('convert',str(output),str(target))
        if target.stat().st_size<100:raise AssertionError('empty export')
    return {'result':'PASS','scope':'native new drawing and reopened hole geometry; no host-sync or manufacturing acceptance',
            'output':str(output),'holes':count,'seedHandle':handle,'centers':centers,'nativeProcesses':len(calls),'calls':calls}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--cli',required=True);p.add_argument('--output',required=True)
    p.add_argument('--count',type=int,default=6);p.add_argument('--pitch-radius',type=float,default=40)
    p.add_argument('--hole-radius',type=float,default=3);p.add_argument('--outer-radius',type=float,default=55)
    p.add_argument('--bore-radius',type=float,default=15);p.add_argument('--start-angle',type=float,default=0)
    p.add_argument('--center',type=float,nargs=2,default=[0,0]);a=p.parse_args()
    print(json.dumps(draw(a.cli,a.output,a.count,a.pitch_radius,a.hole_radius,a.outer_radius,a.bore_radius,a.start_angle,a.center),ensure_ascii=True))
