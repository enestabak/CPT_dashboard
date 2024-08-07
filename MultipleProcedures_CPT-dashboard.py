#!/usr/bin/env python
# coding: utf-8

# # Importing the modules




import numpy as np
import pandas as pd
import httpx
from enum import Enum
from scipy import interpolate
from bokeh.plotting import figure, show, output_file
from bokeh.models import Label, Div, ColorBar, LinearColorMapper
from bokeh.models import HoverTool, BoxSelectTool, TapTool, LassoSelectTool
from bokeh.models import ColumnDataSource
from bokeh.layouts import layout
from bokeh.transform import transform
from bokeh.models import FixedTicker
from bokeh.models import Image
from bokeh.models import ColumnDataSource, FixedTicker, LinearColorMapper, ColorBar, Label, HoverTool, BoxSelectTool, TapTool, LassoSelectTool
from bokeh.transform import transform
from bokeh.plotting import figure
from bokeh.models.widgets import Div
from bokeh.models.layouts import TabPanel, Tabs
from bokeh.layouts import row, column
from bokeh.models.widgets import DataTable, TableColumn
from bokeh.io import output_file, save
from bokeh.models import Span
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as tick
from matplotlib.lines import Line2D 
import pyproj


# # LINE DATA
# ## source: [Fellenius website](https://www.fellenius.net/papers.html) (file name: 365 cribsheet.xlsx)




# Robertson 2010 updated non normalized

k1 = np.array([0.1,0.1479324575221,0.1826745656148,0.2071390155102,0.2277237625334,0.2487995374042,0.2686918276626,0.3102152916836,0.354847986827,0.3913878028901,0.4330301330565,0.4776206112305,0.5219406114272,0.5637830751489,0.6066028983424,0.6531888741867,0.7150091601044,0.7581106384458,0.8075455575137,0.8482807119889,0.8924303675199,0.937447380543,0.9816638840219,1.0312076594646,1.0583383134772,1.1100991825378,1.1454726416729,1.1959080040289,1.2369179294774,1.2934142398713,1.3589189783343,1.4067127353586,1.461875519268,1.5384270706496,1.5816348801616,1.6298299066864,1.6702649799299,1.7076236414637,1.7294265049203])
l1 = np.array([10.230312945492,9.9006824507003,9.5816729665929,9.3338821623362,9.0246866645238,8.7666550915678,8.4841850565946,8.0209627027002,7.5617737533034,7.1288727320598,6.7207546916759,6.3360008409959,5.9509572830296,5.5893131129819,5.2792035773538,4.9769765213022,4.5749898846565,4.2889299879911,4.0282884723272,3.7905738132517,3.5802629823445,3.3689869031622,3.182066803508,2.9831020573679,2.8070652383997,2.6070381445084,2.4623929310419,2.2912106695749,2.1560032813925,1.9986258907269,1.8269122659963,1.6999077699824,1.5758230566051,1.4216874121592,1.3019763293622,1.1934616082085,1.1084173940964,1.0391114998296,0.1])

k2 = np.array([1.7071373112805,1.8672845611252,1.9785962914846,2.0739388681628,2.2892593398763,2.5347779940646,2.7850020301001,3.036123882029,3.3178377769574,3.5726220577659,3.8320033847798,4.1455487279346,4.3987203763523,4.7181369450972,4.9637316924882,5.2138958617159,5.4726297878829,5.7529682236772,6.0477420451033,6.2596342696324,6.4894796611167,6.8218223000935,7.0282633407073,7.2809593223966,7.5122757938287,7.7218344514991,7.9803029375273,8.196666153457,8.5036963315608,8.6935272730401,8.9359268600625,9.1508762075368,9.4353395293734,9.7511631770618,10])
l2 = np.array([1.1,1.1188381635832,1.1539268305401,1.1890027997888,1.2612050322646,1.3377917475822,1.4163759452801,1.5136745586735,1.599593952147,1.6967293452851,1.8065124730985,1.9126301357214,2.0249813331182,2.1519720661713,2.2826506376858,2.4303445096676,2.5731071435131,2.7344719704548,2.900522867008,3.0939798070689,3.2634873154594,3.4746440600904,3.6925461163083,3.8730403219936,4.1702024489705,4.4151673430074,4.6832785190078,4.9491113874502,5.2693327176939,5.5893131129819,5.9287243278545,6.1548434973643,6.5163896341753,6.9120976000041,7])

k3 = np.array([0.7133182967841,0.8260392199755,0.9082806018579,1.0041223855973,1.1083449227419,1.2406347142735,1.3483670983993,1.4699940089066,1.5828781797221,1.6782137805868,1.8579803690128,2.0822222529835,2.2837910188038,2.4045768234355,2.5258105847673,2.6490651873153,2.7804360875227,2.9229197347153,3.063159380963,3.2126156577049,3.3870785467568,3.5550045496151,3.6711083388854,3.8295215517607,3.9545908609687,4.1060286289272,4.3122182093629,4.5321877216311,4.7084873829139,4.8772641034944,4.9977745073976,5.1015886373912,5.2598178879531,5.3730701809504,5.5102009522552,5.6461755310756,5.7935802605516,5.9365477571305,6.0407374916975,6.1331312733367])
l3 = np.array([4.6050557865445,4.9583823875111,5.2545610227334,5.5840853226544,5.945391240066,6.2769878341274,6.6706306165985,7.095596190796,7.526476493023,7.9909961450946,8.6282997358977,9.6176046263883,10.482265636914,11.087631843247,11.7719391537,12.486790529673,13.282285950169,14.075675611939,14.944399236333,15.866738811845,17.309411727289,18.446632497818,19.603458659593,20.716192746562,22.01534768687,23.330388585746,25.499366779829,27.948338915416,30.489523469031,32.492671809299,34.433553822643,36.354041257022,38.887771731203,41.249232894707,43.590627252728,46.411062589953,50.583602202205,53.856502550898,57.394851184225,60.200351169498])

k4 = np.array([0.3004622026783,0.3431597673069,0.3870941742385,0.4181914305396,0.4713667315474,0.5337757882977,0.6007130058188,0.6744832365762,0.742762603942,0.82242755496,0.90500464234,0.9744899309887,1.0731396117873,1.1908861322925,1.3849762736614,1.5144231331177,1.6254619183304,1.7368305480831,1.8201850056924,1.9358272146924,2.0587910483158,2.1592292726637,2.2663506155699,2.3824751630502,2.4755813448432,2.5663542444859,2.6667289106036,2.7859258252759,2.8948345488956,3.0426529699868,3.1954041822003,3.3428908259195,3.4333962390731,3.5236209900907,3.613460867182,3.708417459533,3.7910843624163,3.8427291386067,3.8948603908038])
l4 = np.array([8.2416073697694,8.7339026047969,9.2642691156276,9.5548123453612,10.13502862605,10.760543098256,11.424663120518,12.107091555129,12.890454195339,13.660438604082,14.489969168676,15.39866485715,16.395001483769,17.636410019065,20.105058323786,21.749156960829,23.527702376627,24.839929891883,26.323691320393,27.896082144652,29.617774676875,31.475166079008,33.386496530755,35.413892584399,37.634770429543,39.994924079833,42.304689573425,45.168543625624,47.911404860288,52.121194386018,57.073508456604,62.379515034558,66.291462375589,70.448735958584,74.726737669097,79.413004668232,84.630404299236,90.106227840505,96.747721945201])

k5 = np.array([0.001,0.1428000809695,0.1768064154577,0.2086506507323,0.2357683846555,0.2631398718719,0.3026928099986,0.3275167710954,0.3475851714701,0.3746320586148,0.4022298924239,0.4282038998809,0.4565592534261,0.4852770168257,0.5178063216045,0.5503901828687,0.5777635148342,0.6592746459043,0.7721882605805,0.887872071396,0.9846191389949,1.0527458627797,1.1170378113097,1.1742877656254,1.2479191039415,1.3189619489654,1.3769432955903,1.4232620416754,1.4642526514814,1.5216634991313,1.5728309833232,1.6356746731743,1.6894083885588,1.7406408111344,1.8071964862263,1.8765526257294,1.9380914352943,1.9846498288625,2.0401389448018,2.0989738785892,2.1659802592985,2.2095471563486,2.2712960809942,2.3186766041944,2.3796965260989,2.4369238715359,2.4817534544403,2.5370602301552])
l5 = np.array([24.596048896911,27.022518296119,27.948338915416,28.770950707089,29.756674506385,30.575236041067,31.504632958413,32.492671809299,33.417752787339,34.530353907612,35.579974732566,36.558726532092,37.599569916554,38.778756352505,39.957516070471,41.056687473838,42.782409444587,46.194422498677,51.635741735444,56.807097618508,60.256710411052,65.001492262712,68.819792179613,72.862385628061,77.286956290794,82.287638234764,86.958459929547,90.021949780422,93.805812194669,97.840232249117,101.47681744579,106.73629178475,110.28993940939,116.11479622395,124.09135689958,129.91366537203,135.37428288472,141.19648844906,148.0982703701,153.45920918522,161.56400936163,167.25580408001,175.76001292965,183.14767458854,193.54352687168,201.11330448993,212.52892420964,226.70402202379])

k6 = np.array([0.1,0.1256341561978,0.1442946498559,0.1644508315822,0.1775233178893,0.1931278211188,0.2128921678388,0.232140260988,0.2502116995223,0.2970169787618,0.3741145927863,0.4600874690558,0.5387596164442,0.5688910453266,0.6050232842443,0.6340518786139,0.6680825310354,0.7001366639983,0.7246221900616,0.7501126558162,0.7794653717834,0.7975326446563,0.8192214171454,0.8414843803313,0.8596720844334,0.8816179783525,0.9020586380791,0.925746253841,0.9486201545761,0.9714086720316,0.9946399253952,0.995,1,0,0,0,0,0,0])
l6 = np.array([157.23861075228,162.16988090825,167.09936656128,171.6960197897,177.24648086004,182.63425064538,187.83392989005,194.08761912376,199.61338091948,215.73486972227,246.392954393,277.22597550472,321.09812349258,350.94995495508,372.95874650084,395.97704295366,420.80957554763,446.78113312878,481.06077412805,502.69024848485,530.23075515464,557.19061526316,581.69845973905,608.99147961704,638.16196019052,673.75462750443,707.34981692572,753.82239014262,798.85039913095,833.20752472215,882.97743923111,945.40166783377,1000,0,0,0,0,0,0])

k7 = np.array([])
l7 = np.array([])

k8 = np.array([1.4,1.4399199002537,1.4720353010086,1.5083874546543,1.5494834269669,1.5952645969783,1.6258186729123,1.6620802859549,1.6953109399558,1.7385663939353,1.78,1.8157340571461,1.85,1.9109338419911,1.9672482729831,2.0081603585995,2.0705715098841,2.126720773653,2.1791325414247,2.2347602639555,2.2899763955781,2.3520462999093,2.4139276812186,2.4715937641785,2.5446827128532,2.6302320402733,2.7120771734987,2.7835342354599,2.8948400176414,2.9709652871588,3.0754553968167,3.1808397366261,3.2644859073183,3.3583357874973,3.4465641831443,3.5397642518848,3.6044772327547,3.7129778652742,3.8042935356063,3.9379458439525,4.1109269843925,4.2252862502102,4.3258486754681,4.4528333125771,4.6121570690458,4.7658253136287,4.912967697453,5.0841530225573,5.2493811101346,5.4703666877764,5.7007257948404,5.996312012691,6.2877475047066,6.623206941339,6.955450238734,7.3836528655377,7.8264688737697,8.3468508222129,9.0342320380427,10])
l8 = np.array([1000,933.97068069057,883.80407791041,834.76834370716,769.50190490987,718.69221792006,678.81731639755,642.35583063995,602.19131723819,567,538,508,473.91193151349,447.61807285153,422.78306541774,395.60667813186,372.95874650084,350.29376170505,333.34467721986,313.08706934276,295.16327044606,277.74529338516,261.35517431091,247.31693790236,230.12379533137,212.52892420964,199.24015120018,186.43304525197,173.63487340806,163.6945186085,152.31469472585,143.86388184492,135.62787487056,126.67245861324,119.86846888871,113.85531044065,108.85449894537,105.34710258918,101.00313841827,94.510682520039,89.266985615655,85.02729936839,81.521217730379,78.306122475707,74.936810512378,72.318970512485,70.251244683372,68.562679368696,66.353524082347,64.637561415393,62.848243656273,61.051302469174,59.250269192903,58.643515167598,57.448583931942,56.700881807721,55.54553403282,55,54,53])

k9 = np.array([3.9132987146198,4.0121298203779,4.1099403758291,4.2065622761541,4.3148865192465,4.4219974489882,4.5205745789091,4.6304683545051,4.7369838358667,4.8474536530901,4.9331509487289,5])
l9 = np.array([95.667410904684,105.15012847178,116.98729945461,131.6268084567,151.17871617224,177.08069887226,212.13154548503,268.04254871489,365.35926931174,534.2149850884,793.63479288497,1000.0000000018])

k10 = np.array([])
l10 = np.array([])

df1990_1 = pd.DataFrame({'k1': k1, 'l1': l1})
df1990_2 = pd.DataFrame({'k2': k2, 'l2': l2})
df1990_3 = pd.DataFrame({'k3': k3, 'l3': l3})
df1990_4 = pd.DataFrame({'k4': k4, 'l4': l4})
df1990_5 = pd.DataFrame({'k5': k5, 'l5': l5})
df1990_6 = pd.DataFrame({'k6': k6, 'l6': l6})
df1990_8 = pd.DataFrame({'k8': k8, 'l8': l8})
df1990_9 = pd.DataFrame({'k9': k9, 'l9': l9})

# TO BE USED AS QC DETECTION BORDER: interpolation function from k1 and l1 
f = interpolate.interp1d(k1, l1)


# # User inputs




token = str(input("Enter your token: "))
project_ext_id_input = str(input("Enter your project external id: ")) # 20210119 for Moss
chosen_name = str(input("Enter the sounding name: ")) # eg: 07-163 (TOT, CPT and SA)


# # API




fmtoken = token
auth_header = {
    "Authorization": f"Bearer {fmtoken}",
}

fm_api: str = "https://api.fieldmanager.io/fieldmanager"


# To avoid further errors, go with previous variable name
project_external_id = project_ext_id_input

# optional backup project for approved CPTU data: 20190001
# Moss project for sample data "20210119"

def get_projects(url_projects, auth_header) -> pd.DataFrame:
    response_projects: httpx.Response = httpx.get(url_projects, headers=auth_header)
    projects_dict = response_projects.json()
    projects_df: pd.DataFrame = pd.DataFrame(projects_dict)
    return projects_df

class MethodStatusID(Enum):
    # ( PLANNED=1, READY=2, CONDUCTED=3, VOIDED=4, APPROVED=5, )
    approved = [3, 5]


piezometer_type_id = 5
cptu_type_id = 1
sampling_type_id = 4


def is_piezometer(method_type_id):
    return method_type_id == piezometer_type_id

def is_cptu(method_type_id):
    return method_type_id == cptu_type_id

def is_sampling(method_type_id):
    return method_type_id == sampling_type_id


def is_approved(status_id):
    return status_id in MethodStatusID.approved.value


def get_locations(url_locations, auth_header) -> pd.DataFrame:
    response_location: httpx.Response = httpx.get(
        url_locations, headers=auth_header, timeout=60
    )
    locations = response_location.json()

    #piezo_locations = [
    #     location
    #     for location in locations
    #     for method in location["methods"]
    #     if is_piezometer(method["method_type_id"])
    #     and is_approved(method["method_status_id"])
    # ]

    cpt_locations = [
         location
         for location in locations
         for method in location["methods"]
         if is_cptu(method["method_type_id"])
         and is_approved(method["method_status_id"])
     ]
    



    return pd.DataFrame(cpt_locations)


def get_methods(url_methods, auth_header) -> pd.DataFrame:
    response_method: httpx.Response = httpx.get(
        url_methods, headers=auth_header, timeout=60
    )
    locations = response_method.json()
    print(locations)


auth_header = {
    "Authorization": f"Bearer {fmtoken}",
}

fm_api: str = "https://api.fieldmanager.io/fieldmanager"

url_projects: str = f"{fm_api}/projects"

projects_df = pd.DataFrame(get_projects(url_projects, auth_header))

# Get the project ID for the specified project external ID
project_id = projects_df[projects_df["external_id"] == project_external_id][
    "project_id"
].iloc[0]

# Get the URL for sounding locations for the specified project ID
url_locations: str = f"{fm_api}/projects/{project_id}/locations?limit=1000"

# locations df
location_tot_rp_df = get_locations(url_locations, auth_header)





location_tot = location_tot_rp_df[location_tot_rp_df['name'].str.contains(chosen_name)]
location_tot = location_tot.reset_index(drop=True)


# ------------

# # Chosing a sample row to work on




chosen_row = location_tot_rp_df.loc[location_tot_rp_df['name'] == chosen_name]


# # Importing "sample data" and processing it




sample_df = pd.read_csv(r"sample processing\processed_FallCone_data.csv")
sample_df = sample_df[sample_df['Cufc'] != '-']
sample_df['St'] = sample_df['St'].astype(float)
sample_df['Cufrc'] = sample_df['Cufrc'].astype(float)

sample_df['NGF1974'] = 'no'  
sample_df['NVE2009'] = 'no'  

# Update 'NGF1974' column based on conditions
sample_df.loc[(sample_df['St'] >= 30) & (sample_df['Cufrc'] <= 0.5), 'NGF1974'] = 'NGF1974'

# Update 'NVE2009' column based on conditions
sample_df.loc[(sample_df['St'] >= 15) & (sample_df['Cufrc'] <= 2), 'NVE2009'] = 'NVE2009'


# 
# 
# If `St >= 30` and `Cufrc <= 0.5`, then QC according to 'NGF 1974'
# 
# 
# If `St >= 15` and `Cufrc <= 2`, then sensitive brittle clay according to 'NVE 2009' 
# 
# 

# # Defining the functions




def get_merged_df(location_tot_rp_df, chosen_name, fm_api, project_id, auth_header):
    chosen_row = location_tot_rp_df.loc[location_tot_rp_df['name'] == chosen_name]
    chosen_location_id = chosen_row['location_id'].values[0]
    chosen_method_id = chosen_row['methods'].values[0][0]['method_id']

    cpts: str = f"{fm_api}/projects/{project_id}/locations/{chosen_location_id}/methods/{chosen_method_id}"
    cpt_data: str = f"{fm_api}/projects/{project_id}/locations/{chosen_location_id}/methods/{chosen_method_id}/data"

    response_cpts = httpx.get(cpts, headers=auth_header)
    response_cpt_data = httpx.get(cpt_data, headers=auth_header)

    # This is an important step. If the function doesnt work, these two df should be printed to see if data is imported or not
    cpts_df = pd.DataFrame(response_cpts.json())
    cpt_data_df = pd.DataFrame(response_cpt_data.json())

    merged_df = pd.merge(cpt_data_df, cpts_df, on='method_id')
    merged_df['cone_area_ratio'] = merged_df['cone_area_ratio'].fillna(1)
    merged_df['cone_area_ratio'] = merged_df['cone_area_ratio'].infer_objects()
    print(chosen_name)


    if 'qc' in merged_df.columns:
        # The column exists, safe to proceed
        print(merged_df['qc'].value_counts())
    else:
        print("'qc' column not found in merged_df")

    # Optional: Debugging print statement to check the current columns in merged_df
    print(merged_df.columns)
    # Create 'qt' column
    merged_df['qt'] = merged_df['qc'] + ((merged_df['u2'] * merged_df['cone_area_ratio']) / 1000)



    # in may cases the water depth info is not available
    # if the water_depth is given, calculate the u0. if not consider it as 0:
    first_water_depth = cpts_df["water_depth"].iloc[0]
    if first_water_depth is None:
        merged_df['u0'] = 0
    else:
        merged_df['u0'] = merged_df['depth'].apply(lambda x: 10*(x - first_water_depth) if x >= first_water_depth else 0)

    unit_weight = 1.8 # kN/m3
    merged_df['tot_stress'] = merged_df['depth'] * unit_weight
    merged_df['eff_stress'] = merged_df['tot_stress'] - merged_df['u0']
    merged_df['F'] = 100 * (merged_df['fs'] / (merged_df['qt'] * 1000 - merged_df['tot_stress']))
    merged_df['Q'] = (merged_df['qt'] * 1000 - merged_df['tot_stress']) / merged_df['eff_stress']
    merged_df['Bq'] = (merged_df['u2'] - merged_df['u0']) / ((merged_df['qt'] * 1000) - merged_df['tot_stress'])
    merged_df['Ic'] = ((3 - np.log10(merged_df['Q'] * (1 - merged_df['Bq'])))**2 + (1.5 + 1.3 * np.log10(merged_df['F']))**2)**(1/2)
    merged_df['Rf'] = (merged_df['fs'] / (merged_df['qc'] * 1000)) * 100
    merged_df = merged_df[merged_df['Rf'] <= 10]
    merged_df['Isbt'] = np.sqrt(((3.47 - np.log10(merged_df['qc'] / 0.1))**2 + (np.log10(merged_df['Rf']) + 1.22)**2))
    filtered_df = merged_df[merged_df['depth'] == 12.0]
    
    print("np.log(filtered_df['qc'] / 0.1):", np.log10((filtered_df['qc'] / 0.1)))
    print("np.log(filtered_df['Rf']) + 1.22:", np.log10(filtered_df['Rf']) + 1.22)

    merged_df['qt/pa'] = merged_df['qc'] / 0.1

    def map_values(val):
        if val < 1.31:
            return 'Dense sand to gravelly sand (7)'
        elif 1.31 <= val < 2.05:
            return 'Sands (6)'
        elif 2.05 <= val < 2.60:
            return 'Sand mixtures (5)'
        elif 2.60 <= val < 2.95:
            return 'Silt mixtures (4)'
        elif 2.95 <= val < 3.60:
            return 'Clays (3)'
        else:
            return 'Clay - organic soil (2)'

    merged_df['SBT'] = merged_df['Isbt'].apply(map_values)
    
    def QC_detector(row):
        # Check if 'Rf' is within the range of k1
        if row['Rf'] < k1.min() or row['Rf'] > k1.max():
            return "False"
        
        # Get y-value on curve at x = row['Rf']
        y_on_curve = f(row['Rf'])
        
        # If row['qt/pa'] is less than y_on_curve, return "Quick/Sensitive Clay", else "False"
        return "Quick/Sensitive Clay" if row['qt/pa'] < y_on_curve else "False"    
    merged_df['QC'] = merged_df.apply(QC_detector, axis=1)


    
    if (sample_df['name'] == chosen_name).any():
        chosen_sampling = sample_df[sample_df['name'] == chosen_name]
        merged_df['depth'] = pd.to_numeric(merged_df['depth'], errors='coerce')
        chosen_sampling['depth'] = pd.to_numeric(chosen_sampling['depth'], errors='coerce')
        merged_df = pd.merge(merged_df, chosen_sampling[['depth', 'NGF1974', 'NVE2009']], on='depth', how='left')
    
    return merged_df


def get_thickest_layer(df):
    # Initialize variables
    in_layer = False
    start_depth = end_depth = thickness = 0
    max_start_depth = max_end_depth = max_thickness = 0

    # Iterate over the DataFrame
    for i, row in df.iterrows():
        if row['QC'] == 'Quick/Sensitive Clay':
            if not in_layer:
                # Start a new layer
                in_layer = True
                start_depth = end_depth = row['depth']
                thickness = 0
            else:
                # Update the current layer
                end_depth = row['depth']
                thickness = end_depth - start_depth
        elif in_layer:
            # End the current layer
            in_layer = False
            if thickness > max_thickness:
                # Update the thickest layer
                max_start_depth = start_depth
                max_end_depth = end_depth
                max_thickness = thickness

    # Check the last layer
    if in_layer and thickness > max_thickness:
        max_start_depth = start_depth
        max_end_depth = end_depth
        max_thickness = thickness

    return max_start_depth, max_end_depth, max_thickness

def get_total_thickness(df):
    # Initialize variables
    in_layer = False
    start_depth = end_depth = thickness = 0
    total_thickness = 0

    # Iterate over the DataFrame
    for i, row in df.iterrows():
        if row['QC'] == 'Quick/Sensitive Clay':
            if not in_layer:
                # Start a new layer
                in_layer = True
                start_depth = end_depth = row['depth']
                thickness = 0
            else:
                # Update the current layer
                end_depth = row['depth']
                thickness = end_depth - start_depth
        elif in_layer:
            # End the current layer
            in_layer = False
            total_thickness += thickness

    # Check the last layer
    if in_layer:
        total_thickness += thickness

    return total_thickness



merged_df = get_merged_df(location_tot_rp_df, chosen_name, fm_api, project_id, auth_header)


# $$ Rf = \frac{fs}{qc \times 1000} \times 100 $$

# $$ Isbt = \sqrt{(3.47 - \log{\frac{qc}{0.1}})^2 + (\log{Rf} + 1.22)^2} $$




# path to save and then load the stratigraphy
# saving at the code location
dashboards_path = f'{project_external_id}_{chosen_name}.html'
image_path_strat = f'{project_external_id}_{chosen_name}.png'


source = ColumnDataSource(merged_df)
nonselectionalphavalue = 0.01

def apply_plot_style(plot):
    plot.toolbar.logo = None
    plot.title.align = "center"
    plot.title.text_font_size = "20px"
    plot.title.text_font_style = "bold"
    plot.title.text_color = "black"
    plot.title.text_font = "times"
    plot.title.text_alpha = 1
    plot.title.background_fill_color = "white"
    plot.title.background_fill_alpha = 1
    plot.title.text_baseline = "middle"

def apply_image_style(plot):
    plot.axis.visible = False
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = None
    plot.outline_line_color = None
    plot.toolbar_location = None
    plot.toolbar.active_drag = None  
    plot.toolbar.active_scroll = None  

        







def plot_stratigraphy(merged_df, get_thickest_layer, project_external_id, chosen_name):
    color_dict = {
        'Dense sand to gravelly sand (7)': '#F79C9C',
        'Sands (6)': '#F7C79C',
        'Sand mixtures (5)': '#F7F79C',
        'Silt mixtures (4)': '#9CF79C',
        'Clays (3)': '#9CF7F7',
        'Clay - organic soil (2)': '#9C9CF7',
        'Quick/Sensitive Clay': 'black',
    }

    merged_df['color'] = merged_df['SBT'].map(color_dict)

    plt.figure(figsize=(0.35, 6), dpi=200)

    for category, color in color_dict.items():
        plt.scatter([0]*len(merged_df[merged_df['SBT'] == category]), 
                    merged_df[merged_df['SBT'] == category]['depth'], 
                    c=color, 
                    marker='_', 
                    s=1400, 
                    label=category)
    plt.gca().invert_yaxis()
    plt.gca().axes.get_xaxis().set_visible(False)
    plt.gca().yaxis.set_minor_locator(tick.AutoMinorLocator())
    formatter = tick.FuncFormatter(lambda x, pos: f'{x}m')
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.xlim(-0.1, 1)
    plt.ylim(merged_df['depth'].max(), merged_df['depth'].min())


    plt.scatter([-0.07]*len(merged_df[merged_df['QC'] == 'Quick/Sensitive Clay']), 
                merged_df[merged_df['QC'] == 'Quick/Sensitive Clay']['depth'], 
                c=color,  # Choose a color
                marker='_', 
                s=300, 
                label=category)

    legend_elements = [mpatches.Patch(color=color, label=category) for category, color in color_dict.items()]
    if (sample_df['name'] == chosen_name).any():
        plt.scatter([0.7]*len(merged_df[merged_df['NGF1974'] == 'NGF1974']), 
                    merged_df[merged_df['NGF1974'] == 'NGF1974']['depth'], 
                    c='none', 
                    marker='o',
                    edgecolors='#8e1313', linewidths=3,
                    s=100)

        
        plt.scatter([0.2]*len(merged_df[merged_df['NVE2009'] == 'NVE2009']), 
                    merged_df[merged_df['NVE2009'] == 'NVE2009']['depth'], 
                    c='none', 
                    marker='o',
                    edgecolors='#2a5576', linewidths=3,
                    s=100)


        ngf1974_symbol = Line2D([0], [0], marker='o', color='w', label='NGF1974',
                                markerfacecolor='none', markersize=10, markeredgewidth=2, markeredgecolor='#8e1313',
                                linestyle='None')

        nve2009_symbol = Line2D([0], [0], marker='o', color='w', label='NVE2009',
                                markerfacecolor='none', markersize=10, markeredgewidth=2, markeredgecolor='#2a5576',
                                linestyle='None')



        legend_elements.extend([ngf1974_symbol, nve2009_symbol, ])




    plt.legend(handles=legend_elements, bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.savefig(image_path_strat, bbox_inches='tight')




plot_stratigraphy(merged_df, get_thickest_layer, project_external_id, chosen_name)





def create_plot_and_text(merged_df, chosen_name, project_ext_id_input):

    p1990 = figure(x_range=(0.1, 10), y_range=(1, 1000), 
               width=800, height=600, 
               x_axis_label='Friction Ratio (%)', 
               y_axis_label='Normalized Cone Stress/athmospheric pressure, qt/pa', 
               title= f' Robertson (2010) - Updated non-normalized SBT chart\n Sounding Name: {chosen_name} - Project ID: {project_ext_id_input}',
               y_axis_type="log", x_axis_type="log",
               )
    p1990.toolbar.logo = None
    p1990.ygrid[0].ticker = FixedTicker(ticks=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100,
                                           200, 300, 400, 500, 600, 700, 800, 900, 1000])
    color_mapper = LinearColorMapper(palette='Magma256', high=min(merged_df['depth']), low=max(merged_df['depth']))
    p1990.scatter(y='qt/pa', x='Rf', color=transform('depth', color_mapper), source=source, nonselection_alpha=nonselectionalphavalue,)
    p1990.line(df1990_1['k1'], df1990_1['l1'], color='black')
    p1990.line(df1990_2['k2'], df1990_2['l2'], color='black')
    p1990.line(df1990_3['k3'], df1990_3['l3'], color='black')
    p1990.line(df1990_4['k4'], df1990_4['l4'], color='black')
    p1990.line(df1990_5['k5'], df1990_5['l5'], color='black')
    p1990.line(df1990_6['k6'], df1990_6['l6'], color='black')
    p1990.line(df1990_8['k8'], df1990_8['l8'], color='black')
    p1990.line(df1990_9['k9'], df1990_9['l9'], color='black')
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=12, location=(0,0), title='Depth (m)')
    p1990.add_layout(color_bar, 'left')
    p1990.add_layout(Label(x=0.2, y=2, text='1', text_color='grey', text_font_size='15pt'))
    p1990.add_layout(Label(x=9, y=2, text='2', text_color='grey', text_font_size='15pt'))
    p1990.add_layout(Label(x=9, y=9, text='3', text_color='grey', text_font_size='15pt'))
    p1990.add_layout(Label(x=0.7, y=5, text='4', text_color='grey', text_font_size='15pt'))
    p1990.add_layout(Label(x=0.2, y=20, text='5', text_color='grey', text_font_size='15pt'))
    p1990.add_layout(Label(x=0.2, y=90, text='6', text_color='grey', text_font_size='15pt'))
    p1990.add_layout(Label(x=0.2, y=600, text='7', text_color='grey', text_font_size='15pt'))
    p1990.add_layout(Label(x=3, y=670, text='8', text_color='grey', text_font_size='15pt'))
    p1990.add_layout(Label(x=9, y=200, text='9', text_color='grey', text_font_size='15pt'))
    text1990 = """<br><br><br><br><br><br><br><br><br><br><br><br>
    <b><font size="4">1 : </font></b>  Sensitive Fine-Grained<br>
    <b><font size="4">2 : </font></b>  Organic Soils and Peat<br>
    <b><font size="4">3 : </font></b>  Clays (Clay to Silty Clay)<br>
    <b><font size="4">4 : </font></b>  Silt Mixtures (Silty Clay to Clayey Silt)<br>
    <b><font size="4">5 : </font></b>  Sand Mixtures (Sandy Silt to Silty Sand)<br>
    <b><font size="4">6 : </font></b>  Sand (Silty Sand to Sand)<br>
    <b><font size="4">7 : </font></b>  Sand to Gravely Sand<br>
    <b><font size="4">8 : </font></b>  Sand/Clayey Sand to "very stiff" sand<br>
    <b><font size="4">9 : </font></b>  Very Stiff Fine-Grained, Overconsolidated or Cemented Soil<br>
    """
    text_box1990 = Div(text=text1990, width=200, height=100)
    hover1990 = HoverTool()
    hover1990.tooltips = [
        ("Friction Ratio", "@Rf"),
        ("Cone Stress", "@qt"),
        ("Sleeve Friction", "@fs"),
        ("Pore Pressure", "@u2"),
        ("Depth", "@depth"),
        ("Ic", "@Ic"),
        ("QC", "@QC"),
    ]
    p1990.tools.append(hover1990)
    p1990.tools.append(BoxSelectTool())
    p1990.add_tools(TapTool(), LassoSelectTool())
    apply_plot_style(p1990)
    return p1990, text_box1990

p1990, text_box1990 = create_plot_and_text(merged_df, chosen_name, project_ext_id_input)





def SBT_plot(merged_df, source, nonselectionalphavalue):
    p_Ic = figure(width=300, height=580, x_axis_label='Isbt', y_axis_label='Depth (m)', title="Soil Type Behavior Index", y_range=(max(merged_df['depth']), min(merged_df['depth'])))
    p_Ic.tools.append(BoxSelectTool())

    hoverSBT = HoverTool()
    hoverSBT.tooltips = [
        ("Friction Ratio", "@Rf"),
        ("Cone Stress", "@qc"),
        ("Sleeve Friction", "@fs"),
        ("Isbt", "@Isbt"),
        ("Pore Pressure", "@u2"),
        ("Depth", "@depth"),
        ("QC", "@QC"),]
    
    p_Ic.tools.append(hoverSBT)
    p_Ic.add_tools(TapTool(), LassoSelectTool())
    p_Ic.toolbar.logo = None

    for x in [0, 1.31, 2.05, 2.60, 2.95, 3.60, 4.0]:
        vline = Span(location=x, dimension='height', line_color='black', line_width=1)
        p_Ic.add_layout(vline)


    colors = ['#F79C9C', '#F7C79C', '#F7F79C', '#9CF79C', '#9CF7F7', '#9C9CF7']
    x_ranges = [(0.0, 1.31), (1.31, 2.05), (2.05, 2.60), (2.60, 2.95), (2.95, 3.60), (3.60, 4.0)]


    y_range = (0, merged_df['depth'].max())

    for color, x_range in zip(colors, x_ranges):

        p_Ic.rect(x=(x_range[0]+x_range[1])/2, y=(y_range[0]+y_range[1])/2, 
                  width=x_range[1]-x_range[0], height=y_range[1]-y_range[0], 
                  color=color, alpha=0.75)
    
    p_Ic.scatter('Isbt', 'depth', color='black', source=source, nonselection_alpha=nonselectionalphavalue)
    p_Ic.line('Isbt', 'depth', color='black', source=source)
    apply_plot_style(p_Ic)
    return p_Ic

p_Ic = SBT_plot(merged_df, source, nonselectionalphavalue)


# # A trial dashboard for the chosen name




merged_df = get_merged_df(location_tot_rp_df, chosen_name, fm_api, project_id, auth_header)
source = ColumnDataSource(merged_df)
get_thickest_layer(merged_df)
plot_stratigraphy(merged_df, get_thickest_layer, project_external_id, chosen_name)
p1990, text_box1990 = create_plot_and_text(merged_df, chosen_name, project_ext_id_input)
start_depth, end_depth, thickness = get_thickest_layer(merged_df)
thickness = round(thickness, 2) 
p_Ic = SBT_plot(merged_df, source, nonselectionalphavalue)
p = figure(x_range=(0,1), y_range=(0,1))
apply_image_style(p)
p.image_url(url=[image_path_strat], x=0, y=1, w=1, h=1)
output_file(dashboards_path)
columns = [TableColumn(field="depth", title="Depth (m)"), TableColumn(field="SBT", title="Soil Behavior Type")]
datatable = DataTable(source=source, columns=columns)
tab1 = TabPanel(child=column(row(p1990, text_box1990), row(p_Ic, p, datatable)), title="Stratigraphy & Soil Classification")
l = Tabs(tabs=[tab1])
show(l)





merged_df = get_merged_df(location_tot_rp_df, chosen_name, fm_api, project_id, auth_header)


# # Loop to apply the individual procedure to all CPTu locations




thickness_values = {}
TotalQC_values = {}
path_dash_values = {}
path_strat_values = {}
NGF1974_values = {}
NVE2009_values = {}

# Iterate over each unique name in the 'name' column
for chosen_name in location_tot_rp_df['name'].unique():
    merged_df = get_merged_df(location_tot_rp_df, chosen_name, fm_api, project_id, auth_header)
    if 'cone_area_ratio' in merged_df.columns:
        dashboards_path = f'{project_external_id}_{chosen_name}.html'
        image_path_strat = f'{project_external_id}_{chosen_name}.png'
        path_dash_values[chosen_name] = f"files/{dashboards_path}"  # Store the dashboard path in the dictionary
        path_strat_values[chosen_name] = f"files/{image_path_strat}"  # Store the stratigraphy image path in the dictionary

        
        # check if chosen_name is in sample_df 
        if chosen_name in sample_df['name'].values:
            # Filter the DataFrame for the specific chosen_name
            matched_rows = sample_df[sample_df['name'] == chosen_name]
            # Check if any of the rows have 'NGF1974' in the NGF1974 column
            if 'NGF1974' in matched_rows['NGF1974'].values:
                NGF1974_values[chosen_name] = 'yes'
            else:
                NGF1974_values[chosen_name] = 'no'

        if chosen_name in sample_df['name'].values:
            # Filter the DataFrame for the specific chosen_name
            matched_rows = sample_df[sample_df['name'] == chosen_name]
            # Check if any of the rows have 'NVE2009' in the NVE2009 column
            if 'NVE2009' in matched_rows['NVE2009'].values:
                NVE2009_values[chosen_name] = 'yes'
            else:
                NVE2009_values[chosen_name] = 'no'

        merged_df['depth'] = merged_df['depth'].round(2)
        source = ColumnDataSource(merged_df)
        get_thickest_layer(merged_df)
        plot_stratigraphy(merged_df, get_thickest_layer, project_external_id, chosen_name)
        p1990, text_box1990 = create_plot_and_text(merged_df, chosen_name, project_ext_id_input)
        start_depth, end_depth, thickness = get_thickest_layer(merged_df)
        thickness = round(thickness, 2)
        thickness_values[chosen_name] = thickness  # Store the thickness value in the dictionary
        total_QCthickness = get_total_thickness(merged_df)
        TotalQC = round(total_QCthickness, 2)
        TotalQC_values[chosen_name] = TotalQC
        p_Ic = SBT_plot(merged_df, source, nonselectionalphavalue)
        p = figure(x_range=(0,1), y_range=(0,1))
        apply_image_style(p)
        p.image_url(url=[image_path_strat], x=0, y=1, w=1, h=1)
        output_file(dashboards_path)
        columns = [TableColumn(field="depth", title="Depth (m)"), TableColumn(field="SBT", title="Soil Behavior Type")]
        datatable = DataTable(source=source, columns=columns)
        tab1 = TabPanel(child=column(row(p1990, text_box1990), row(p_Ic, p, datatable)), title="Stratigraphy & Soil Classification")
        l = Tabs(tabs=[tab1])
        save(l)
    else:
        continue

location_tot_rp_df['ThickestQC'] = location_tot_rp_df['name'].map(thickness_values)
location_tot_rp_df['TotalQC'] = location_tot_rp_df['name'].map(TotalQC_values)
location_tot_rp_df['pathDash'] = location_tot_rp_df['name'].map(path_dash_values)
location_tot_rp_df['pathStrat'] = location_tot_rp_df['name'].map(path_strat_values)
location_tot_rp_df['NGF1974'] = location_tot_rp_df['name'].map(NGF1974_values)
location_tot_rp_df['NVE2009'] = location_tot_rp_df['name'].map(NVE2009_values)

# location_tot_rp_df.to_csv("20210119_locations3.csv", index=False)


# # Coordinate system tranformation to  Norwegian CRS




wgs84 = pyproj.CRS("EPSG:4326")  # WGS84
etrs89 = pyproj.CRS("EPSG:25833")  # ETRS89 (UTM zone 33N)

# convert from WGS84 to ETRS89
transformer = pyproj.Transformer.from_crs(wgs84, etrs89, always_xy=True)
location_tot_rp_df['ETRS89_x'], location_tot_rp_df['ETRS89_y'] = transformer.transform(location_tot_rp_df['point_x_wgs84_web'].values, location_tot_rp_df['point_y_wgs84_web'].values)


# # Save the csv file to be imported to GIS




location_tot_rp_df.to_csv("20210119_locationsETRS89.csv", index=False)

