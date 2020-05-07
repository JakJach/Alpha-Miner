from parsers.txt_parser import read
from miners.alpha import Alpha
from miners.aplha_plus import AlphaPlus
from miners.alpha_plus_plus import AlphaPlusPlus
from representation.petri_net import PetriNet
from subprocess import check_call
import os.path


file_path = r'logs\log8.txt'
log = read(file_path)

filename = os.getcwd() + r'\result'
alpha_model = AlphaPlusPlus(log)
alpha_model.generate_footprint(txtfile="{}_footprint.txt".format(filename))
pn = PetriNet()
pn.generate_with_alpha(alpha_model, dotfile="{}.dot".format(filename))
#check_call(["dot", "-Tpng", "{}.dot".format(filename),"-o", "{}.png".format(filename)])
#
# #print(alpha_model.l1l)
# #print(alpha_model.triangle)
# # print('---')
# # print(alpha_model.parallel)
# print(alpha_model.causal)
# # print(alpha_model.independent)
# print(alpha_model.direct_succession)
# print('---')
# print(alpha_model.xor_split)
# print(alpha_model.xor_join)
# print(alpha_model.indirect_succession)
# print(alpha_model.succession)
# print(log)

#print(alpha_model.xl)
#print(alpha_model.yl)
#for place in alpha_model.all_places:
#    print(place)
print('---')
print(alpha_model.w1)
print(alpha_model.w2_1)
print(alpha_model.w2_2)
print(alpha_model.w2)
print(alpha_model.w3)