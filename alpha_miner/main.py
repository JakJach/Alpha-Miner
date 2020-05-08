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
# # 1
# print(alpha_model.all_events)
# # 2
# print(alpha_model.l1l)
# # 3
# print(alpha_model.t_prim)
# # 4
# print(alpha_model.xw)
# # 5
# print(alpha_model.lw)
# # 6 i 7
# print(alpha_model.w_l1l)
# # 8
# print(alpha_model.idw1)
# # 9
# for place in alpha_model.pw_l1l:
#     print(place)
# print(alpha_model.tw_l1l)
# 10 i 11
# print(alpha_model.idw2)
# 12
for place in alpha_model.xw_12:
    print(place)
# 13
for place in alpha_model.yw:
    print(place)