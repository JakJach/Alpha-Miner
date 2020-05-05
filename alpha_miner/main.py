from parsers.txt_parser import read
from miners.alpha import Alpha
from miners.aplha_plus import AlphaPlus
from representation.petri_net import PetriNet
from subprocess import check_call
import os.path


file_path = r'logs\log7.txt'
log = read(file_path)

filename = os.getcwd() + r'\result'
alpha_model = AlphaPlus(log)
alpha_model.generate_footprint(txtfile="{}_footprint.txt".format(filename))
pn = PetriNet()
pn.generate_with_alpha(alpha_model, dotfile="{}.dot".format(filename))
#check_call(["dot", "-Tpng", "{}.dot".format(filename),"-o", "{}.png".format(filename)])
#print(alpha_model.l1l)
#print(alpha_model.triangle)
#print(alpha_model.romb)
print('---')
print(alpha_model.parallel)
print(alpha_model.causal)
print(alpha_model.direct_succession)
print(log)