#!/usr/bin/env python
from __future__ import absolute_import, division, print_function

import json
import time
from collections import OrderedDict
from glob import glob
import cv2
import requests
import os

def hasNumbers(inputString):
    state = False
    for character in inputString:
        if character.isdigit():
            state = True
    return state

def get_state_satutes(num):
    state_statues = ['A', 'AA', 'AB', 'ABG', 'ABI', 'AC', 'AE', 'AH', 'AIB', 'AIC', 'AK', 'ALF', 'ALZ', 'AM', 'AN', 'ANA', 'ANG', 'ANK', 'AO', 'AP', 'APD', 'ARN', 'ART', 'AS', 'ASL', 'ASZ', 
    'AT', 'AU', 'AUR', 'AW', 'AZ', 'AZE', 'B', 'BA', 'BAD', 'BAR', 'BB', 'BBG', 'BBL', 'BC', 'BCH', 'BD', 'BE', 'BED', 'BER', 'BF', 'BGD', 'BGL', 'BH', 'BI', 'BID', 'BIN', 'BIR', 'BIT', 'BIW', 
    'BK', 'BKS', 'BL', 'BLB', 'BLK', 'BM', 'BN', 'BNA', 'BO', 'BO', 'BOG', 'BOH', 'BOR', 'BOT', 'BP', 'BRA', 'BRB', 'BRG', 'BRK', 'BRL', 'BRV', 'BS', 'BSB', 'BSK', 'BT', 'BTF', 'BUD', 'BUL', 
    'BUR', 'BUS', 'BUZ', 'BW', 'BWL', 'BYL', 'BZ', 'C', 'CA', 'CAS', 'CB', 'CE', 'CHA', 'CLP', 'CLZ', 'CO', 'COC', 'COE', 'CR', 'CUX', 'CW', 'D', 'DA', 'DAH', 'DAN', 'DAU', 'DBR', 'DD', 'DE', 
    'DEG', 'DEL', 'DGF', 'DH', 'DI', 'DIL', 'DIN', 'DIZ', 'DKB', 'DL', 'DLG', 'DM', 'DN', 'DO', 'DON', 'DU', 'DUD', 'DUW', 'DW', 'DZ', 'E', 'EA', 'EB', 'EBE', 'EBN', 'EBS', 'ECK', 'ED', 'EE', 
    'EF', 'EG', 'EH', 'EI', 'EIC', 'EIL', 'EIN', 'EIS', 'EL', 'EM', 'EMD', 'EMS', 'EN', 'ER', 'ERB', 'ERH', 'ERK', 'ERZ', 'ES', 'ESB', 'ESW', 'EU', 'EW', 'F', 'FB', 'FD', 'FDB', 'FDS', 'FEU', 
    'FF', 'FFB', 'FG', 'FI', 'FKB', 'FL', 'FLO', 'FN', 'FO', 'FOR', 'FR', 'FRG', 'FRI', 'FRW', 'FS', 'FT', 'FTL', 'FU', 'FUS', 'FW', 'FZ', 'G', 'GA', 'GAN', 'GAP', 'GC', 'GD', 'GDB', 'GE', 'GEL', 
    'GEO', 'GER', 'GF', 'GG', 'GHA', 'GHC', 'GI', 'GK', 'GL', 'GLA', 'GM', 'GMN', 'GN', 'GNT', 'GO', 'GOA', 'GOH', 'GP', 'GR', 'GRA', 'GRH', 'GRI', 'GRM', 'GRZ', 'GS', 'GT', 'GTH', 'GU', 'GUB', 
    'GUN', 'GV', 'GVM', 'GW', 'GZ', 'H', 'HA', 'HAB', 'HAL', 'HAM', 'HAS', 'HB', 'HBN', 'HBS', 'HC', 'HCH', 'HD', 'HDH', 'HDL', 'HE', 'HEB', 'HEF', 'HEI', 'HEL', 'HER', 'HET', 'HF', 'HG', 'HGN', 
    'HGW', 'HH', 'HHM', 'HI', 'HIG', 'HIP', 'HK', 'HL', 'HM', 'HMU', 'HN', 'HO', 'HOG', 'HOH', 'HOL', 'HOM', 'HOR', 'HOS', 'HOT', 'HP', 'HR', 'HRO', 'HS', 'HSK', 'HST', 
    'HU', 'HV', 'HVL', 'HWI', 'HX', 'HY', 'HZ', 'IGB', 'IK', 'IL', 'ILL', 'IN', 'IZ', 'J', 'JE', 'JL', 'JUL', 'K', 'KA', 'KB', 'KC', 'KE', 'KEH', 'KEL', 'KEM', 'KF', 'KG', 
    'KH', 'KI', 'KIB', 'KK', 'KL', 'KLE', 'KLZ', 'KM', 'KN', 'KO', 'KON', 'KOT', 'KOZ', 'KR', 'KRU', 'KS', 'KT', 'KU', 'KUN', 'KUS', 'KW', 'KY', 'KYF', 'L', 'LA', 'LAN', 'LAU', 'LB', 'LBS', 'LBZ', 
    'LC', 'LD', 'LDK', 'LDS', 'LEO', 'LER', 'LEV', 'LF', 'LG', 'LH', 'LI', 'LIB', 'LIF', 'LIP', 'LL', 'LM', 'LN', 'LO', 'LOB', 'LOS', 'LP', 'LR', 'LRO', 'LSA', 'LSN', 'LSZ', 'LU', 'LUN', 'LUP', 'LWL', 
    'M', 'MA', 'MAB', 'MAI', 'MAK', 'MAL', 'MB', 'MC', 'MD', 'ME', 'MED', 'MEG', 'MEI', 'MEK', 'MEL', 'MER', 'MET', 'MG', 'MGH', 'MGN', 'MH', 'MHL', 'MI', 'MIL', 'MK', 'MKK', 'ML', 'MM', 'MN', 'MO', 'MOD', 
    'MOL', 'MON', 'MOS', 'MQ', 'MR', 'MS', 'MSE', 'MSH', 'MSP', 'MST', 'MTK', 'MTL', 'MU', 'MUB', 'MUR', 'MVL', 'MW', 'MY', 'MYK', 'MZ', 'MZG', 'N', 'NAB', 'NAI', 'NAU', 'NB', 'ND', 'NDH', 'NE', 'NEA', 
    'NEB', 'NEC', 'NEN', 'NES', 'NEW', 'NF', 'NH', 'NI', 'NK', 'NL', 'NM', 'NMB', 'NMS', 'NO', 'NOH', 'NOL', 'NOM', 'NOR', 'NP', 'NR', 'NRW', 'NT', 'NU', 'NVP', 'NW', 'NWM', 'NY', 'NZ', 'OA', 'OAL', 'OB', 
    'OBB', 'OBG', 'OC', 'OCH', 'OD', 'OE', 'OF', 'OG', 'OH', 'OHA', 'OHR', 'OHV', 'OHZ', 'OK', 'OL', 'OP', 'OPR', 'OS', 'OSL', 'OVI', 'OVL', 'OVP', 'OZ', 'P', 'PA', 'PAF', 'PAN', 'PAR', 'PB', 'PCH', 'PE', 
    'PEG', 'PF', 'PI', 'PIR', 'PL', 'PLO', 'PM', 'PN', 'PR', 'PRU', 'PS', 'PW', 'PZ', 'QFT', 'QLB', 'R', 'RA', 'RC', 'RD', 'RDG', 'RE', 'REG', 'REH', 'REI', 'RG', 'RH', 'RI', 'RID', 'RIE', 'RL', 'RM', 'RN', 
    'RO', 'ROD', 'ROF', 'ROK', 'ROL', 'ROS', 'ROT', 'ROW', 'RP', 'RPL', 'RS', 'RSL', 'RT', 'RU', 'RUD', 'RUG', 'RV', 'RW', 'RZ', 'S', 'SAB', 'SAD', 'SAL', 'SAN', 'SAW', 'SB', 'SBG', 'SBK', 'SC', 'SCZ', 'SDH', 
    'SDL', 'SDT', 'SE', 'SEB', 'SEE', 'SEF', 'SEL', 'SFB', 'SFT', 'SG', 'SGH', 'SH', 'SHA', 'SHG', 'SHK', 'SHL', 'SI', 'SIG', 'SIH', 'SIM', 'SK', 'SL', 'SLE', 'SLF', 'SLG', 'SLK', 'SLN', 'SLS', 'SLU', 'SLZ', 
    'SM', 'SMU', 'SN', 'SO', 'SOB', 'SOG', 'SOK', 'SOM', 'SON', 'SP', 'SPB', 'SPN', 'SR', 'SRB', 'SRO', 'ST', 'STA', 'STB', 'STD', 'STE', 'STL', 'SU', 'SUL', 'SUW', 'SW', 'SWA', 'SY', 'SZ', 'SZB', 'TBB', 'TDO', 'TE', 
    'TET', 'TF', 'TG', 'THL', 'THW', 'TIR', 'TO', 'TOL', 'TP', 'TR', 'TS', 'TT', 'TU', 'TUT', 'UE', 'UEM', 'UFF', 'UH', 'UL', 'UM', 'UN', 'USI', 'UB', 'V', 'VAI', 'VB', 'VEC', 'VER', 'VG', 'VIB', 'VIE', 'VIT', 'VK', 
    'VOH', 'VR', 'VS', 'W', 'WA', 'WAF', 'WAK', 'WAN', 'WAT', 'WB', 'WBS', 'WDA', 'WE', 'WEL', 'WEN', 'WER', 'WES', 'WF', 'WG', 'WHV', 'WI', 'WIL', 'WIN', 'WIS', 'WIT', 'WIV', 'WIZ', 'WK', 'WL', 'WLG', 'WM', 'WMS', 
    'WN', 'WND', 'WO', 'WOB', 'WOH', 'WOL', 'WOR', 'WOS', 'WR', 'WRN', 'WS', 'WSF', 'WST', 'WSW', 'WT', 'WTL', 'WTM', 'WU', 'WUG', 'WUM', 'WUN', 'WUR', 'WW', 'WZ', 'WZL', 'X', 'Y', 'Z', 'ZE', 'ZEL', 'ZI', 'ZIG', 
    'ZP', 'ZR', 'ZW', 'ZZ']
    state_number = ""
    state_number1 = ""
    state_number2 = ""
    state_number3 = ""
    number1 = num[:1]
    number2 = num[:2]
    number3 = num[:3]
    if number1 in state_statues :
        state_number1 = number1
        number = number1
    if number2 in state_statues :
        state_number2 = number2
        number = number2
    if number3 in state_statues :
        state_number3 = number3
        number = number3
    return number

def recognition_plate_number(path, frame):
    result = []
    with open(path, 'rb') as fp:
        response = requests.post(
                        'https://api.platerecognizer.com/v1/plate-reader/',
                        files=dict(upload=fp),
                        data=dict(regions='fr'),
                        headers={'Authorization': 'Token ' + '46569c6bbf83ec3257068d20a74113e420598687'})
    result.append(response.json(object_pairs_hook=OrderedDict))
    time.sleep(1)

    im=cv2.imread(path)
          
    resp_dict = json.loads(json.dumps(result, indent=2))

    for resp_dict_object in resp_dict[0]['results']:
        num=resp_dict_object['plate']
        num = num.upper()
        boxs=resp_dict_object['box']
        candidates = resp_dict_object['candidates']
        car_number = ""
        for candidate in candidates :
            if candidate['score'] > 0.85:
                car_number = candidate['plate']
        num = car_number.upper()
        xmins, ymins, ymaxs, xmaxs=boxs['xmin'],boxs['ymin'],boxs['ymax'],boxs['xmax']

        img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
        if hasNumbers(num) :
            # state_statue = get_state_satutes(num)
            edges = cv2.Canny(img,100,200)
            cv2.rectangle(frame, (xmins, ymins), (xmaxs, ymaxs), (255,0,0), 2)
            cv2.rectangle(edges, (xmins, ymins), (xmaxs, ymaxs), (255,0,0), 2)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, num, (xmins, ymins), font, 0.8, (255,0,0), 2, cv2.LINE_AA)
            cv2.destroyAllWindows()
