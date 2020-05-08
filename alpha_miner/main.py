from parsers.txt_parser import read
from miners.alpha import Alpha
from miners.aplha_plus import AlphaPlus
from miners.alpha_plus_plus import AlphaPlusPlus
from representation.petri_net import PetriNet
from subprocess import check_call
import os.path


file_path = r'logs\log6.txt'
log = read(file_path)

filename = os.getcwd() + r'\result'
alpha_model = AlphaPlusPlus(log)
alpha_model.generate_footprint(txtfile="{}_footprint.txt".format(filename))
pn = PetriNet()
pn.generate_with_alpha(alpha_model, dotfile="{}.dot".format(filename))
# check_call(["dot", "-Tpng", "{}.dot".format(filename),"-o", "{}.png".format(filename)])
