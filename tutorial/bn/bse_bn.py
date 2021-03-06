#
# Author: Henrique Pereira Coutada Miranda
# Run a BSE calculation using yambo
#
from __future__ import print_function
import sys
from yambopy import *
from qepy import *
import argparse

#parse options
parser = argparse.ArgumentParser(description='Test the yambopy script.')
parser.add_argument('-dg','--doublegrid', action="store_true", help='Use double grid')
parser.add_argument('-r', '--run',        action="store_true", help='Run BSE calculation')
parser.add_argument('-a', '--analyse',    action="store_true", help='plot the results')
args = parser.parse_args()

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)

yambo = "yambo"

if not os.path.isdir('database'):
    os.mkdir('database')

#check if the nscf cycle is present
if os.path.isdir('nscf/bn.save'):
    print('nscf calculation found!')
else:
    print('nscf calculation not found!')
    exit()

#check if the SAVE folder is present
if not os.path.isdir('database/SAVE'):
    print('preparing yambo database')
    os.system('cd nscf/bn.save; p2y > p2y.log')
    os.system('cd nscf/bn.save; yambo > yambo.log')
    os.system('mv nscf/bn.save/SAVE database')

#check if the SAVE folder is present
if args.doublegrid:
    if not os.path.isdir('database_double/SAVE'):
        print('preparing yambo database')
        os.system('cd nscf_double/bn.save; p2y > p2y.log')
        os.system('cd nscf_double/bn.save; yambo > yambo.log')
        os.system('mv nscf_double/bn.save/SAVE database_double')

if not os.path.isdir('bse'):
    os.mkdir('bse')
    os.system('cp -r database/SAVE bse')

#initialize the double grid
if args.doublegrid:
    print("creating double grid")
    f = open('bse/ypp.in','w')
    f.write("""kpts_map
    %DbGd_DB1_paths
    "../database_double"
    %""")
    f.close()
    os.system('cd bse; ypp')

if args.run:
    #create the yambo input file
    y = YamboIn('yambo -b -o b -k sex -y d -V all',folder='bse')

    y['FFTGvecs'] = [30,'Ry']
    y['NGsBlkXs'] = [1,'Ry']
    y['BndsRnXs'] = [1,30]
    y['BSEBands'] = [3,5]
    y['BEnSteps'] = 500
    y['BEnRange'] = [[0.0,10.0],'eV']

    y.arguments.append('WRbsWF')
    y.write('bse/yambo_run.in')

    print('running yambo')
    os.system('cd bse; %s -F yambo_run.in -J yambo'%yambo)

if args.analyse:
    #pack in a json file
    y = YamboOut('bse')
    y.pack()

    #get the absorption spectra
    a = YamboBSEAbsorptionSpectra('yambo',save='bse/SAVE',path='bse')
    excitons = a.get_excitons(min_intensity=0.0005,max_energy=6,Degen_Step=0.01)
    print( "nexcitons: %d"%len(excitons) )
    print( "excitons:" )
    print( excitons )
    a.get_wavefunctions(Degen_Step=0.01,repx=range(-1,2),repy=range(-1,2),repz=range(1))
    a.write_json()
