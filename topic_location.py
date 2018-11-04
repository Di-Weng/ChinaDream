# -*- coding:UTF-8 -*-

'''

@author: diw

@contact: di.W@hotmail.com

@file: topic_location

@time: 2018/9/29 2:37

@desc:

'''

weibofilefolder = '/Volumes/新加卷/chinadream/data'


import topic_sta1
from numba import jit
from topic_sta1 import topic

north_city = ['北京','天津','内蒙古','新疆','河北','甘肃','宁夏','山西','陕西','青海','山东','河南','安徽','辽宁','吉林','黑龙江']
south_city = ['江苏','浙江','上海','湖北','湖南','四川','重庆','贵州','云南','广西','江西','福建','广东','海南','西藏','台湾','香港','澳门']
def process_statics():
    file_path_list = topic_sta1.getAllFile(weibofilefolder)
    topic_sta1.topic_location(file_path_list)

@jit
def list_add(a,b):
    c = []
    for i in range(len(a)):
        c.append(a[i]+b[i])
    return c

@jit
def add_data(output, input_list, keyword):
    if(keyword not in output.keys()):
        output[keyword] = input_list
    else:
        output[keyword] = list_add(output[keyword],input_list)
    return output

@jit
def calc_sum(topic_list):
    sum = 0
    for temp in topic_list:
        sum += temp
    return sum

def get_echartsdata(output):
    region_list = []
    series_dic = {}
    for region in output.keys():
        region_list.append(region)
    for topic_label in topic:
        current_list = []
        index = topic.index(topic_label)
        for region in region_list:
            current_region_list = output[region]
            if (index <= len(current_region_list) - 1):
                current_list.append(current_region_list[index])
            else:
                current_list.append(0)
        series_dic[topic_label] = current_list

    for series, series_list in series_dic.items():
        print(series)
        print(series_list)
        print('______________')
    # xAisx
    print(region_list)
    print(output)

def province_percent(calc_dic):
    output_dic = {}
    for location_detailed,current_list in calc_dic.items():
        province_list = location_detailed.split()
        if(len(province_list) == 0):
            continue
        province = province_list[0]
        output_dic[province] = []
        sum = calc_sum(current_list)
        temp_list = []
        for i in range(len(current_list)):
            temp_list.append(float(current_list[i])/sum)
        output_dic[province] = temp_list
    return output_dic

def region_calc(output_dic):
    output = {}
    for location_str, count_list in output_dic.items():
        location_list = location_str.split()
        # 抛弃未知地理位置的数据
        if(len(location_list) == 0):
            continue

        city = location_list[0]
        if(city == '其他'):
            output = add_data(output, count_list, '其他')
        elif(city == '海外'):
            output = add_data(output, count_list, '海外')
        elif (city in north_city):
            output = add_data(output, count_list, '北方')
        elif (city in south_city):
            output = add_data(output, count_list, '南方')
        else:
            print(city)

    percent_output = {}
    #pecent_list
    for region, current_list in output.items():
        sum = calc_sum(current_list)
        temp_list = []
        for i in range(len(current_list)):
            temp_list.append(float(current_list[i])/sum)
        percent_output[region] = temp_list
    return percent_output

if __name__ == '__main__':
    output_dic = {'广西 河池': [12481, 4337, 340, 4555, 19196, 5395, 178], '海外 澳大利亚': [48199, 19525, 1458, 20695, 54290, 27122, 553], '上海 黄浦区': [84711, 21210, 3796, 40664, 166304, 52472, 1374], '北京 朝阳区': [169830, 45509, 8689, 75880, 328959, 93899, 3151], '香港': [45464, 12592, 1016, 17107, 92177, 16563, 432], '福建 福州': [115790, 31148, 4514, 45470, 183620, 51013, 1577], '北京 西城区': [52083, 15500, 2336, 22951, 79250, 27668, 1148], '台湾 台北市': [50299, 17320, 1514, 19811, 90491, 21715, 623], '陕西 宝鸡': [24833, 7588, 601, 7841, 31755, 9670, 277], '山东 潍坊': [64056, 20715, 1733, 23443, 88059, 27072, 778], '湖南 岳阳': [18989, 5310, 663, 6236, 34551, 8192, 250], '安徽 宣城': [12651, 3365, 398, 4082, 19873, 4933, 131], '广西 百色': [12519, 4060, 372, 4611, 20127, 5237, 120], '上海': [138913, 36440, 5315, 57276, 249335, 63818, 2067], '河南': [54988, 15242, 1341, 18967, 87320, 24773, 799], '吉林 辽源': [20006, 8403, 348, 7284, 48931, 7694, 169], '北京': [271019, 61859, 9000, 98762, 414348, 129288, 3778], '海南 其他': [38649, 13929, 872, 14382, 55068, 16428, 396], '山西 太原': [53347, 13569, 2620, 20675, 101407, 29729, 875], '广西 南宁': [75070, 20118, 2764, 28601, 146228, 36419, 1065], '吉林 长春': [73598, 17949, 2953, 24548, 131977, 31826, 964], '广东 惠州': [50603, 14019, 1421, 17303, 85596, 20420, 516], '广东 深圳': [290282, 74365, 10846, 128523, 539711, 148600, 3792], '重庆 双桥区': [10944, 2651, 135, 3458, 14775, 3226, 87], '澳门 其他': [96681, 36861, 1919, 37080, 123195, 43019, 1028], '广东 广州': [406728, 98823, 17411, 164809, 943075, 222904, 5444], '辽宁 大连': [73104, 17384, 3836, 26232, 165367, 170566, 1244], '山东 泰安': [20410, 5323, 816, 6700, 35889, 8166, 312], '新疆 克拉玛依': [9266, 3260, 278, 3488, 14284, 4010, 116], '浙江 杭州': [220820, 50588, 7540, 81843, 444765, 106352, 2733], '上海 杨浦区': [30101, 7110, 1790, 10763, 53350, 11573, 629], '江苏 苏州': [138079, 31954, 5986, 51063, 246118, 54816, 1793], '陕西 渭南': [23870, 7769, 499, 7530, 29989, 9044, 262], '河北 石家庄': [96014, 22570, 3286, 32495, 146682, 38109, 1149], '北京 通州区': [22722, 6654, 824, 8622, 34194, 10475, 336], '山东 青岛': [95616, 23240, 4571, 38296, 180635, 41403, 1742], '广东 东莞': [82784, 22950, 2862, 38028, 167180, 39867, 866], '河南 新乡': [29451, 9719, 934, 11944, 44284, 12853, 351], '辽宁 沈阳': [100204, 24681, 4927, 36013, 214657, 42799, 1495], '河北 邯郸': [29076, 8330, 919, 11017, 51277, 12909, 387], '湖南 长沙': [116455, 30583, 5057, 42735, 223265, 65917, 1965], '其他': [1450061, 328898, 59001, 478421, 3292079, 586408, 22302], '辽宁': [36525, 11047, 1238, 13222, 68561, 32702, 497], '天津 红桥区': [9047, 3016, 362, 3549, 16453, 4311, 125], '山西 吕梁': [14247, 4643, 358, 5464, 22562, 6678, 162], '四川 成都': [225204, 54205, 10104, 80522, 392678, 96388, 3574], '北京 昌平区': [22340, 6054, 1021, 9208, 40153, 10400, 406], '贵州 贵阳': [40009, 10326, 1703, 14349, 73041, 18010, 609], '北京 东城区': [269231, 73352, 9413, 108002, 478814, 163943, 4681], '河北 保定': [32486, 8808, 1536, 12715, 59843, 14650, 500], '河北 唐山': [38456, 11964, 1330, 14109, 68108, 16774, 518], '江苏 无锡': [74759, 17784, 2679, 27832, 127979, 29877, 974], '江西': [35140, 12088, 769, 12154, 58698, 14335, 399], '重庆 九龙坡区': [11478, 2898, 512, 4233, 22582, 4703, 167], '北京 怀柔区': [10720, 3621, 254, 4396, 17692, 4978, 114], '黑龙江 黑河': [11604, 4141, 272, 4329, 18917, 5100, 119], '浙江 台州': [37269, 9621, 1320, 13964, 66376, 16462, 506], '湖北 武汉': [160869, 35854, 8221, 59412, 318914, 106250, 2790], '重庆 沙坪坝区': [20278, 3778, 1149, 5913, 52200, 6269, 344], '山东 东营': [23935, 8158, 726, 8187, 34302, 11848, 343], '北京 海淀区': [121102, 28630, 7749, 53900, 235169, 84077, 2894], '海外 美国': [70794, 17667, 5652, 36222, 153104, 33212, 1665], '安徽': [36240, 10626, 1045, 15722, 72048, 15929, 457], '重庆 涪陵区': [9660, 4019, 223, 3182, 11162, 3637, 85], '海外 加拿大': [23686, 6882, 1297, 10156, 47041, 10404, 486], '江苏 南京': [171547, 37654, 8859, 58257, 303236, 76995, 3101], '浙江 宁波': [104594, 22440, 3755, 34224, 161839, 43356, 1469], '北京 丰台区': [34881, 8906, 1682, 13726, 59866, 15745, 586], '安徽 六安': [13732, 4179, 442, 5416, 22645, 6725, 206], '广东 中山': [41640, 12559, 1371, 17076, 79380, 18892, 444], '青海 西宁': [24807, 7311, 676, 8718, 37526, 11701, 294], '河北 秦皇岛': [28001, 9335, 928, 10343, 42957, 11057, 344], '山东 济南': [100657, 23760, 4296, 35487, 169475, 52708, 1644], '山东 威海': [21839, 6155, 756, 8508, 35993, 10274, 302], '湖南 邵阳': [15749, 5137, 418, 5820, 24893, 6281, 164], '上海 浦东新区': [77052, 18737, 4102, 31549, 138643, 40637, 1505], '香港 东区': [1211, 326, 60, 583, 3737, 639, 36], '上海 徐汇区': [49813, 14293, 2653, 23931, 97815, 23567, 905], '宁夏 银川': [45270, 13942, 1161, 15891, 66350, 28888, 502], '北京 崇文区': [18347, 5904, 658, 6142, 24472, 7454, 185], '贵州 黔西南': [14842, 5246, 343, 5569, 25091, 6370, 130], '江苏 常州': [47639, 14142, 2013, 18409, 75720, 23455, 601], '福建 莆田': [36702, 15345, 1068, 13022, 53445, 15194, 378], '海外 韩国': [16321, 5446, 952, 8421, 45113, 6658, 263], '辽宁 盘锦': [14059, 4483, 384, 5316, 24343, 6012, 160], '湖北 宜昌': [25998, 7249, 1044, 9451, 40352, 11600, 410], '陕西 榆林': [18508, 6247, 424, 6705, 29103, 10237, 221], '江苏 泰州': [25560, 6484, 725, 8202, 40955, 9845, 411], '重庆': [56626, 19569, 1932, 21951, 119501, 23743, 936], '上海 闵行区': [32716, 8682, 1651, 13824, 60401, 15248, 676], '浙江 温州': [75125, 19372, 2497, 30457, 131681, 33301, 868], '广东 汕头': [106543, 24661, 2274, 33350, 132524, 35872, 769], '江苏 盐城': [27729, 7782, 896, 10684, 43598, 11321, 376], '天津': [47323, 12243, 1868, 16582, 86709, 23001, 730], '贵州 遵义': [24764, 7872, 747, 9551, 40373, 10656, 297], '上海 嘉定区': [18164, 4674, 680, 6541, 30029, 7259, 222], '广东 江门': [46706, 12277, 1402, 16583, 120921, 28051, 502], '福建': [59606, 21985, 1927, 21978, 92715, 25645, 672], '浙江 绍兴': [39156, 10866, 1435, 14193, 66711, 15819, 466], '黑龙江 哈尔滨': [87083, 19803, 3742, 28212, 162291, 33547, 1287], '广东 河源': [25409, 8380, 595, 9115, 43949, 10431, 233], '天津 武清区': [8941, 2878, 241, 3242, 15029, 3654, 95], '福建 漳州': [39387, 11794, 1180, 14215, 63359, 16055, 483], '广东': [153166, 42344, 4188, 63272, 289761, 76693, 1729], '河北 张家口': [16956, 5359, 565, 6342, 31563, 7393, 243], '北京 石景山区': [14841, 4434, 651, 6000, 25486, 7252, 224], '江苏': [74009, 19174, 2437, 27117, 151175, 30600, 1035], '山东 烟台': [36932, 8440, 1451, 13778, 64354, 16944, 594], '内蒙古 包头': [20421, 6601, 807, 7447, 33739, 9073, 294], '湖南 娄底': [12959, 4111, 351, 4713, 21792, 5530, 117], '西藏 林芝': [14269, 5402, 268, 5546, 24051, 6405, 153], '西藏 拉萨': [18297, 6629, 433, 6928, 29260, 8151, 244], '山东': [72084, 21606, 2061, 28812, 113402, 33354, 937], '山西 运城': [18473, 5359, 612, 7543, 30626, 8555, 233], '新疆 哈密': [9751, 3569, 254, 3638, 14554, 4436, 131], '海南 海口': [63765, 20431, 2126, 24797, 111683, 31606, 909], '青海 玉树': [15476, 5862, 292, 5904, 20660, 6803, 160], '广西 柳州': [33753, 11265, 987, 12965, 58067, 13656, 492], '湖南': [36430, 11254, 1077, 13792, 81922, 18810, 635], '湖北': [49698, 15646, 1346, 18879, 79919, 25244, 576], '重庆 渝中区': [18095, 5697, 573, 7115, 28103, 8065, 233], '安徽 合肥': [82643, 21329, 3254, 31082, 155614, 40776, 1195], '安徽 阜阳': [17520, 4341, 504, 6274, 29301, 6908, 221], '上海 长宁区': [26642, 7202, 1389, 12396, 50508, 13408, 524], '海外 其他': [72454, 14526, 4797, 27519, 174073, 29935, 1476], '河南 安阳': [21109, 6090, 821, 7703, 34080, 10348, 341], '宁夏 吴忠': [29632, 11092, 567, 11350, 44397, 13172, 316], '浙江 嘉兴': [44068, 12173, 1594, 15324, 79517, 18966, 547], '北京 大兴区': [20166, 7464, 737, 7967, 30753, 9843, 281], '上海 静安区': [24283, 6524, 1007, 9783, 42807, 11663, 553], '黑龙江 绥化': [13571, 4252, 366, 4806, 21542, 5563, 165], '广东 珠海': [43735, 13532, 1481, 17313, 79707, 20342, 605], '山东 菏泽': [16474, 4362, 467, 8207, 25189, 7373, 291], '河北': [47431, 13408, 2037, 16253, 83602, 23639, 838], '四川 宜宾': [11936, 3428, 455, 4170, 21344, 5108, 158], '江西 宜春': [23914, 7516, 685, 8593, 40907, 10085, 303], '陕西 西安': [151811, 36874, 6413, 54827, 268029, 66413, 2239], '河南 开封': [21025, 6048, 600, 6782, 33082, 7700, 390], '海外 荷兰': [1619, 392, 205, 596, 4077, 830, 37], '海外 马来西亚': [11570, 4201, 520, 4590, 32670, 4993, 154], '江苏 淮安': [20991, 6218, 796, 7706, 34578, 9197, 256], '山东 滨州': [96217, 38454, 1811, 37930, 119982, 41256, 882], '浙江 金华': [40493, 10924, 1390, 16129, 70130, 19078, 447], '海外': [90068, 22813, 4170, 35687, 203692, 102534, 1272], '新疆 昌吉': [11737, 3539, 300, 3920, 17763, 4307, 106], '福建 厦门': [108370, 28972, 4809, 41118, 175253, 46862, 1267], '广西 贵港': [11677, 3827, 331, 4351, 19240, 4925, 143], '上海 普陀区': [34461, 10669, 1415, 13930, 50154, 14147, 452], '福建 泉州': [72210, 19123, 2600, 25951, 119173, 29264, 843], '黑龙江 鹤岗': [13209, 5062, 253, 4885, 17536, 5590, 128], '辽宁 丹东': [16113, 4480, 517, 5354, 26098, 6259, 213], '贵州 安顺': [14723, 4994, 344, 5954, 21780, 6699, 170], '香港 其他': [120931, 42429, 2713, 45638, 175939, 63128, 1250], '天津 东丽区': [8445, 2791, 245, 3171, 14322, 3856, 97], '江西 上饶': [19282, 5656, 598, 6648, 32913, 7855, 260], '浙江': [67285, 17516, 1904, 25961, 125684, 33155, 955], '甘肃 白银': [12470, 4671, 249, 4606, 17707, 4936, 133], '四川 雅安': [8890, 2857, 307, 3187, 17865, 3698, 109], '云南 大理': [14614, 3784, 473, 5088, 20803, 5257, 142], '江苏 徐州': [42362, 12036, 1713, 14715, 66373, 17112, 608], '海外 新加坡': [16383, 4695, 729, 5990, 36260, 7184, 287], '澳门': [13524, 4445, 269, 4704, 20602, 5185, 140], '北京 宣武区': [20582, 7528, 776, 7128, 30938, 9292, 310], '黑龙江': [30301, 11810, 771, 10968, 46638, 16204, 325], '云南': [30929, 9330, 767, 10106, 46838, 12776, 341], '内蒙古 呼和浩特': [28275, 7814, 1157, 10766, 53359, 15515, 442], '福建 南平': [28185, 9470, 737, 10577, 43973, 12003, 395], '河南 郑州': [146441, 33588, 5811, 57551, 251144, 71748, 2600], '青海 海东': [17318, 5729, 299, 5888, 22447, 6539, 124], '山西 阳泉': [14692, 4672, 581, 5302, 23436, 6497, 187], '江西 新余': [19843, 7312, 403, 6392, 22490, 7578, 165], '香港 九龙城区': [3322, 1019, 143, 2273, 9870, 2854, 53], '山东 临沂': [31050, 10212, 1027, 10511, 55651, 14820, 496], '河南 平顶山': [17509, 5442, 492, 9149, 29568, 7397, 424], '河南 洛阳': [42347, 12294, 1361, 14182, 64877, 15822, 535], '天津 西青区': [14317, 4807, 621, 5846, 28361, 6049, 184], '上海 卢湾区': [13687, 4201, 566, 5451, 47291, 6131, 204], '四川 泸州': [12131, 3307, 432, 4229, 22672, 4806, 168], '广西 来宾': [2201, 611, 67, 944, 5440, 834, 27], '山东 枣庄': [47221, 18008, 969, 18890, 64114, 20203, 470], '新疆 乌鲁木齐': [34249, 8617, 1508, 11725, 63443, 14314, 619], '西藏 阿里': [15961, 6156, 347, 6415, 21737, 7276, 167], '台湾 台中市': [3776, 712, 113, 939, 7443, 1188, 43], '北京 房山区': [19208, 6270, 542, 6771, 36282, 8641, 234], '上海 金山区': [12349, 3733, 384, 4412, 18659, 6888, 183], '湖北 咸宁': [13223, 4524, 341, 4951, 20519, 5699, 156], '辽宁 朝阳': [14167, 4475, 336, 4981, 21390, 5647, 144], '新疆 巴音郭楞': [9710, 3303, 212, 3639, 16960, 4195, 116], '浙江 舟山': [23711, 6910, 500, 6774, 29630, 11559, 351], '重庆 南岸区': [14459, 3502, 861, 5190, 43970, 6717, 267], '甘肃 兰州': [41373, 11344, 3605, 14295, 67234, 16901, 830], '澳门 花地玛堂区': [2723, 806, 136, 1157, 9570, 1341, 37], '北京 顺义区': [14962, 3993, 465, 4762, 24587, 6234, 178], '甘肃 酒泉': [10332, 3552, 257, 3829, 15107, 4362, 130], '天津 河东区': [12754, 3635, 508, 4788, 22285, 5492, 183], '云南 临沧': [8263, 2994, 173, 3519, 11971, 3487, 74], '宁夏 固原': [30318, 11465, 610, 11643, 40924, 13247, 292], '陕西 汉中': [17631, 5586, 462, 6268, 28434, 7628, 197], '河北 廊坊': [23762, 6470, 874, 9038, 42659, 10397, 312], '天津 和平区': [30707, 9073, 1371, 11457, 55694, 15534, 484], '山东 德州': [22060, 6651, 591, 7536, 30046, 9746, 250], '安徽 亳州': [11505, 3748, 308, 4140, 18589, 5327, 173], '湖南 株洲': [19975, 6540, 632, 7268, 31807, 8195, 228], '上海 松江区': [20223, 5439, 848, 7069, 33827, 8542, 300], '山西 临汾': [18375, 5835, 486, 7091, 29021, 8176, 215], '黑龙江 大庆': [18206, 5167, 703, 6893, 34695, 7991, 288], '天津 宝坻区': [7692, 3214, 182, 2763, 10617, 3574, 92], '四川 绵阳': [22864, 4765, 862, 6836, 36395, 7763, 359], '河南 信阳': [17938, 4636, 546, 5843, 29113, 7175, 364], '辽宁 辽阳': [12558, 4293, 408, 4549, 20196, 5473, 171], '海外 德国': [5489, 1349, 629, 2192, 8549, 2526, 148], '山东 济宁': [24695, 7189, 820, 9194, 40971, 11292, 320], '湖北 随州': [11942, 4157, 264, 4654, 19859, 5162, 128], '河南 漯河': [23833, 9505, 490, 8633, 32221, 12553, 267], '江西 南昌': [84837, 28491, 2862, 29873, 127822, 35292, 1147], '香港 中西区': [8504, 2921, 416, 4424, 19352, 4821, 158], '新疆 塔城': [7866, 2946, 164, 2962, 12113, 3513, 110], '吉林 松原': [16460, 5698, 413, 6314, 24397, 8086, 187], '山西': [28044, 8363, 865, 10273, 52551, 12784, 295], '海外 法国': [18511, 6098, 853, 7106, 37580, 7760, 295], '广东 梅州': [26448, 8561, 819, 9226, 54633, 11416, 252], '湖南 常德': [15788, 4575, 527, 6497, 27404, 6936, 222], '天津 河北区': [11461, 3029, 393, 4073, 16701, 4421, 141], '广西 桂林': [27582, 8957, 1573, 10039, 53872, 11326, 395], '四川 南充': [15503, 4156, 535, 5223, 27253, 13857, 231], '上海 崇明县': [9107, 3295, 202, 2917, 11695, 4297, 93], '海外 英国': [27580, 7355, 2172, 11361, 57466, 11646, 557], '陕西 安康': [15098, 4987, 390, 5499, 22677, 6228, 191], '北京 平谷区': [10784, 4022, 230, 3972, 15511, 5201, 149], '吉林 吉林': [27364, 8902, 890, 10015, 48582, 10657, 334], '广东 佛山': [89483, 25245, 3508, 36217, 157644, 41752, 1007], '北京 密云县': [9811, 3607, 275, 3594, 15393, 4695, 112], '河北 衡水': [15910, 5098, 400, 6248, 28505, 6845, 166], '江苏 宿迁': [16844, 5526, 399, 6488, 27550, 9038, 206], '四川 凉山': [8010, 2454, 216, 2889, 13133, 3393, 84], '四川': [46975, 13605, 1581, 17646, 80397, 20539, 559], '广西': [37104, 11807, 1068, 13560, 63640, 15379, 471], '辽宁 鞍山': [22102, 6851, 770, 7948, 37991, 9111, 293], '重庆 江北区': [16182, 4305, 627, 6585, 28796, 6952, 237], '云南 保山': [9206, 3329, 217, 3479, 13248, 3912, 100], '贵州 毕节': [14260, 4756, 349, 5237, 22185, 6042, 163], '湖北 荆州': [20443, 5382, 637, 7033, 33711, 8539, 303], '陕西 咸阳': [21967, 6911, 645, 7603, 33242, 10919, 295], '云南 昆明': [59270, 14192, 2450, 21701, 104732, 27397, 1002], '上海 虹口区': [23766, 6763, 1388, 9385, 42430, 10774, 479], '辽宁 铁岭': [12171, 4017, 454, 4725, 24463, 5277, 153], '江苏 扬州': [33135, 7923, 1296, 10765, 53322, 13539, 524], '吉林': [26419, 8600, 735, 9157, 47950, 11809, 301], '重庆 万州区': [23231, 6780, 734, 6326, 41913, 7501, 345], '山西 长治': [16059, 4900, 446, 5916, 26782, 6630, 213], '黑龙江 牡丹江': [14401, 4729, 449, 5360, 28416, 6356, 202], '河南 鹤壁': [10338, 3651, 265, 3692, 15321, 7022, 112], '四川 阿坝': [7274, 2502, 152, 2613, 10915, 3043, 62], '湖北 孝感': [16394, 5415, 358, 5787, 22954, 6712, 168], '浙江 衢州': [18690, 5575, 542, 6595, 31066, 7504, 180], '广东 肇庆': [31483, 9413, 896, 10730, 100973, 12330, 16404], '湖北 襄阳': [20872, 5354, 570, 7810, 33272, 8273, 262], '安徽 滁州': [13749, 4149, 445, 4770, 24149, 5819, 196], '安徽 淮北': [11544, 3686, 313, 4364, 19517, 5428, 156], '云南 怒江': [8114, 3112, 167, 3151, 12422, 3667, 73], '江苏 南通': [37552, 9038, 1438, 14700, 64626, 15023, 515], '广东 湛江': [31307, 9348, 989, 11677, 56708, 12883, 336], '四川 乐山': [13559, 4176, 438, 4597, 21332, 5511, 164], '甘肃 天水': [13894, 4663, 345, 4804, 22538, 11612, 174], '重庆 渝北区': [13349, 3446, 573, 5072, 24262, 5734, 205], '福建 宁德': [20490, 6193, 681, 7448, 33667, 8439, 248], '江西 景德镇': [17481, 6300, 446, 6373, 28079, 7346, 195], '安徽 黄山': [13702, 4323, 442, 4601, 23050, 5950, 189], '天津 津南区': [7954, 2971, 241, 2968, 12535, 3613, 104], '湖南 永州': [13077, 4304, 327, 4850, 30647, 9421, 190], '湖北 十堰': [16473, 4675, 508, 6102, 26144, 6857, 238], '河南 商丘': [17471, 4763, 517, 6043, 27076, 7065, 215], '安徽 蚌埠': [18066, 5917, 578, 6731, 33237, 7543, 609], '黑龙江 佳木斯': [12895, 4323, 363, 4689, 23609, 5625, 172], '福建 三明': [35755, 11428, 970, 12156, 48787, 14196, 399], '黑龙江 伊春': [11805, 3998, 228, 4162, 17381, 4923, 135], '青海 海西': [14050, 5305, 251, 5364, 21184, 6356, 148], '辽宁 抚顺': [18695, 7098, 706, 6748, 26086, 8807, 242], '湖北 黄冈': [15121, 4568, 470, 5823, 25436, 6283, 174], '河南 焦作': [17022, 5155, 589, 6302, 31882, 7520, 278], '海外 日本': [35118, 10843, 2156, 16520, 55842, 18429, 666], '甘肃 甘南': [8116, 3120, 147, 3070, 11525, 3401, 76], '海外 瑞士': [1634, 310, 132, 548, 4668, 9093, 44], '江西 鹰潭': [12993, 4577, 328, 5112, 21172, 5832, 152], '吉林 延边朝鲜族自治州': [16338, 5661, 499, 6380, 26630, 7238, 202], '云南 玉溪': [11106, 3663, 298, 4087, 17294, 4568, 127], '贵州 六盘水': [14921, 5302, 394, 5786, 24331, 6634, 165], '新疆': [20208, 6455, 471, 6970, 48267, 8452, 281], '河南 濮阳': [15830, 4455, 487, 5418, 26049, 6810, 305], '江西 萍乡': [17670, 5963, 374, 6116, 25070, 8611, 194], '陕西 铜川': [16799, 6216, 300, 5757, 19196, 6570, 163], '台湾 台南市': [1395, 381, 45, 488, 3198, 524, 26], '广东 云浮': [9591, 3007, 349, 3522, 18093, 4013, 148], '四川 内江': [9654, 3138, 325, 3547, 18748, 3965, 115], '广西 防城港': [10012, 3513, 194, 3845, 15786, 4379, 98], '河南 许昌': [16177, 4334, 438, 6296, 26162, 7482, 293], '黑龙江 七台河': [10162, 3909, 247, 3876, 15086, 4345, 121], '内蒙古 鄂尔多斯': [15136, 4952, 415, 6337, 24665, 7022, 237], '新疆 克孜勒苏': [7216, 2742, 123, 2770, 9923, 3249, 75], '陕西': [36342, 11064, 996, 12852, 62228, 16429, 436], '河南 三门峡': [12222, 3834, 380, 4399, 21906, 5014, 145], '山东 日照': [15656, 4537, 508, 5523, 27683, 10678, 208], '安徽 芜湖': [25857, 7362, 906, 8819, 42285, 10668, 380], '山西 忻州': [13254, 4710, 331, 5563, 20906, 6128, 200], '浙江 湖州': [30223, 10407, 907, 10748, 47629, 13377, 355], '湖南 张家界': [11672, 3798, 280, 4188, 18018, 4880, 129], '西藏 昌都': [15935, 5912, 289, 6106, 24119, 7129, 175], '福建 龙岩': [27255, 9170, 752, 10351, 49184, 11616, 350], '安徽 马鞍山': [18812, 6018, 538, 6271, 25646, 10045, 267], '江西 吉安': [19129, 7030, 491, 7760, 28011, 8403, 1392], '安徽 池州': [10634, 3354, 309, 3928, 16602, 4694, 172], '浙江 丽水': [23434, 6368, 623, 9380, 46869, 8842, 246], '香港 沙田区': [1170, 387, 76, 623, 4162, 549, 26], '北京 门头沟区': [9753, 3149, 297, 3377, 14986, 4490, 133], '陕西 商洛': [12925, 4463, 303, 4493, 17950, 5712, 187], '广西 玉林': [15331, 4262, 452, 6094, 24055, 6228, 190], '内蒙古 通辽': [15520, 5304, 373, 5662, 22950, 6381, 211], '新疆 伊犁': [12236, 4234, 315, 4357, 16096, 5283, 178], '云南 德宏': [9019, 3283, 182, 3531, 14030, 4072, 106], '西藏': [15717, 5279, 342, 7222, 51545, 6500, 177], '天津 北辰区': [9306, 3093, 352, 3572, 15152, 3874, 133], '重庆 綦江县': [3645, 1209, 121, 1395, 5425, 1496, 47], '天津 河西区': [17345, 4714, 793, 6301, 32420, 7324, 330], '天津 蓟县': [6554, 2302, 165, 2471, 10083, 2855, 60], '江西 抚州': [14694, 4908, 409, 5456, 23945, 6433, 228], '江苏 镇江': [23210, 6343, 934, 8419, 38565, 9350, 315], '河南 南阳': [23475, 5809, 735, 7804, 38012, 10034, 405], '甘肃 陇南': [12964, 4972, 308, 4315, 15832, 6944, 155], '安徽 安庆': [17542, 4733, 637, 5851, 31255, 7705, 270], '贵州 黔南': [13997, 5436, 339, 5102, 20387, 5905, 148], '广西 钦州': [11601, 3621, 306, 4268, 19462, 4921, 144], '云南 曲靖': [12211, 3824, 317, 4662, 17935, 5198, 193], '四川 德阳': [13752, 3829, 575, 4713, 23568, 5534, 214], '贵州 黔东南': [19512, 5440, 416, 5592, 23250, 6550, 153], '新疆 吐鲁番': [7586, 2906, 186, 3010, 10739, 3327, 98], '河南 周口': [15086, 4268, 381, 5389, 28356, 6251, 217], '宁夏': [18621, 6412, 331, 6807, 32360, 7777, 163], '香港 油尖旺区': [1289, 588, 35, 891, 2523, 889, 19], '广东 揭阳': [53219, 20089, 1147, 21565, 91815, 22304, 349], '广东 潮州': [38282, 10699, 866, 13804, 64116, 14696, 280], '贵州': [26717, 6864, 576, 8278, 38612, 9497, 274], '海外 俄罗斯': [8700, 3380, 336, 3155, 14280, 3584, 136], '山西 朔州': [12159, 4589, 307, 4570, 18357, 5559, 158], '重庆 江津市': [4294, 1355, 128, 1535, 7147, 1820, 46], '吉林 通化': [20883, 7950, 454, 8397, 27499, 12194, 214], '重庆 合川区': [4706, 1445, 166, 1741, 8396, 1878, 86], '天津 滨海新区': [5544, 1527, 260, 2001, 9779, 2977, 126], '山东 淄博': [31175, 7970, 1085, 9637, 46555, 12307, 431], '甘肃 定西': [9368, 3230, 190, 3564, 13257, 4224, 95], '河北 沧州': [25092, 6716, 720, 8723, 43988, 10145, 284], '内蒙古 巴彦淖尔盟': [13789, 4155, 264, 4452, 17094, 5304, 153], '山东 莱芜': [10563, 3448, 329, 3900, 16064, 4494, 138], '上海 奉贤区': [12103, 3761, 398, 4534, 20037, 5094, 175], '内蒙古 呼伦贝尔': [14058, 4472, 438, 5434, 24116, 6353, 210], '内蒙古 锡林郭勒盟': [10915, 3898, 255, 4235, 16852, 4874, 125], '台湾 其他': [33379, 12729, 791, 12666, 51742, 14743, 348], '内蒙古 乌海': [15686, 6352, 308, 5723, 19365, 6460, 139], '重庆 大足县': [3412, 1233, 105, 1284, 5613, 1453, 40], '广东 阳江': [24802, 8776, 612, 10800, 44136, 10412, 223], '新疆 博尔塔拉': [8069, 3043, 202, 3127, 11949, 3513, 108], '台湾 台东县': [2099, 299, 18, 1190, 4799, 958, 12], '河北 邢台': [27791, 7236, 666, 8509, 37412, 9619, 283], '山西 晋城': [16031, 4835, 415, 5825, 25287, 6818, 246], '江西 赣州': [42327, 10527, 1069, 13118, 62221, 15095, 533], '青海 黄南': [15235, 5905, 269, 5901, 21169, 6762, 152], '青海 果洛': [15515, 5522, 272, 5925, 22118, 6716, 141], '宁夏 石嘴山': [36747, 11837, 586, 11960, 43026, 14091, 346], '天津 塘沽区': [10837, 3011, 421, 4085, 17946, 4418, 147], '云南 文山': [9312, 3212, 260, 3469, 13474, 3965, 99], '重庆 黔江区': [3527, 1194, 76, 1247, 5461, 1491, 41], '广西 北海': [16913, 5071, 386, 5241, 21952, 6292, 149], '四川 达州': [11267, 3470, 367, 4172, 20081, 4480, 137], '甘肃 庆阳': [10341, 3525, 223, 3888, 15370, 4492, 101], '湖北 荆门': [13646, 4564, 341, 5207, 22680, 6140, 154], '云南 红河': [11806, 3895, 282, 4468, 17198, 5512, 148], '西藏 那曲': [15372, 5670, 292, 5684, 22453, 6610, 147], '上海 南汇区': [9396, 3370, 259, 3704, 14327, 3925, 118], '安徽 宿州': [13795, 4165, 333, 4973, 36730, 6113, 148], '台湾 嘉义市': [1034, 287, 25, 372, 2133, 428, 11], '广东 韶关': [34312, 12766, 870, 11517, 54540, 13259, 276], '辽宁 营口': [14520, 4513, 577, 5533, 25083, 6520, 191], '江西 九江': [26947, 9846, 726, 9836, 39834, 10562, 298], '湖南 湘西土家族苗族自治州': [10773, 3670, 302, 3968, 16136, 4559, 100], '四川 甘孜': [8590, 2571, 240, 2576, 12585, 3334, 78], '云南 迪庆': [10680, 3284, 183, 3063, 13149, 3439, 78], '上海 青浦区': [12402, 3993, 422, 4576, 22484, 5144, 154], '江苏 连云港': [24262, 6458, 605, 8966, 35032, 9373, 229], '甘肃 武威': [11352, 3417, 199, 3677, 13920, 4138, 89], '吉林 白山': [16838, 5269, 345, 5867, 31220, 6647, 173], '吉林 白城': [15735, 5646, 346, 6800, 23704, 6628, 179], '湖南 湘潭': [22770, 8107, 531, 7653, 28577, 8049, 225], '天津 静海县': [7700, 2678, 222, 2954, 11247, 3135, 74], '海外 巴西': [7400, 3228, 333, 3317, 11232, 3277, 82], '湖北 恩施土家族苗族自治州': [14770, 4225, 318, 4830, 19974, 5436, 148], '广东 清远': [26177, 8779, 739, 9271, 48833, 11158, 244], '广东 茂名': [27852, 8969, 897, 11594, 56087, 12023, 298], '重庆 巴南区': [5696, 1772, 210, 2031, 9314, 2456, 89], '湖北 鄂州': [10633, 3728, 240, 4118, 24050, 4747, 139], '安徽 巢湖': [10483, 3149, 235, 3537, 14616, 4038, 125], '山东 聊城': [18794, 5391, 770, 6251, 27028, 8222, 203], '辽宁 葫芦岛': [13964, 4561, 401, 5010, 22638, 5907, 179], '湖南 益阳': [11974, 3962, 371, 4557, 19757, 5017, 156], '海外 蒙古': [428, 85, 33, 156, 1026, 216, 14], '甘肃 嘉峪关': [16845, 6584, 243, 5366, 19988, 9173, 132], '广西 贺州': [11566, 3971, 231, 4089, 16723, 4655, 116], '辽宁 本溪': [16373, 6335, 531, 5604, 21914, 6384, 130], '香港 湾仔区': [1431, 320, 56, 739, 3181, 873, 22], '海南 三亚': [48327, 17068, 1073, 17946, 78794, 22463, 526], '重庆 石柱土家族自治县': [3250, 1218, 67, 1306, 4542, 1338, 39], '青海 海南': [17347, 6162, 309, 6361, 22171, 7145, 155], '辽宁 阜新': [11880, 4262, 357, 4538, 19368, 4932, 134], '台湾': [16230, 5099, 443, 5721, 32519, 6938, 204], '湖南 衡阳': [21654, 6996, 714, 7581, 36569, 8796, 254], '海外 西班牙': [2025, 475, 306, 727, 5160, 836, 28], '湖南 郴州': [15700, 4931, 486, 5857, 29544, 6486, 190], '上海 宝山区': [22591, 5396, 1020, 7834, 36744, 8953, 390], '重庆 荣昌县': [3575, 1265, 92, 1298, 5553, 1505, 35], '贵州 铜仁': [15218, 5598, 369, 6117, 23562, 6936, 141], '四川 攀枝花': [8630, 2751, 210, 3270, 13812, 3690, 98], '辽宁 锦州': [16375, 4875, 524, 6012, 27393, 6675, 220], '云南 西双版纳': [10552, 3423, 274, 3834, 15598, 4399, 120], '青海': [18863, 5709, 290, 6728, 42670, 7710, 172], '重庆 酉阳土家族苗族自治县': [3200, 1192, 69, 1218, 4903, 1500, 31], '上海 闸北区': [17742, 5572, 836, 7291, 35438, 8622, 309], '海外 泰国': [61874, 7029, 622, 6601, 34545, 6715, 144], '湖北 天门': [1698, 561, 44, 1523, 4184, 810, 21], '安徽 铜陵': [10934, 3402, 365, 4061, 18564, 5074, 161], '黑龙江 齐齐哈尔': [19196, 6378, 606, 7033, 38356, 8152, 259], '吉林 四平': [19269, 6706, 515, 7045, 32975, 8399, 229], '山西 大同': [17466, 5706, 575, 6560, 33580, 7635, 239], '甘肃 金昌': [15372, 6390, 279, 5607, 19929, 6000, 133], '内蒙古 兴安盟': [11168, 3922, 244, 4298, 17137, 5004, 149], '新疆 石河子': [1900, 424, 97, 757, 4871, 928, 64], '四川 遂宁': [9335, 3104, 297, 3457, 16433, 3967, 104], '内蒙古 赤峰': [19900, 7803, 584, 7310, 27513, 8151, 188], '黑龙江 大兴安岭': [9069, 3297, 282, 3505, 13647, 3998, 124], '西藏 山南': [16667, 5581, 225, 5579, 21884, 6223, 142], '山西 晋中': [17313, 5740, 531, 6686, 30912, 7673, 210], '新疆 阿克苏': [9053, 2985, 200, 3272, 13020, 4214, 98], '天津 南开区': [20587, 5577, 1038, 7844, 42900, 9037, 348], '重庆 璧山县': [3525, 1153, 99, 1285, 5377, 1527, 37], '广西 梧州': [15179, 5100, 419, 5687, 24054, 6249, 156], '重庆 梁平县': [3300, 1161, 75, 1284, 4628, 1443, 30], '台湾 高雄市': [34589, 13807, 669, 13205, 44542, 15012, 337], '广东 汕尾': [24240, 8421, 563, 8921, 42605, 9955, 176], '海南': [24117, 9026, 517, 8776, 50398, 9784, 235], '重庆 忠县': [3353, 1203, 77, 1435, 4922, 1387, 28], '云南 丽江': [12123, 3851, 312, 4323, 19687, 8251, 143], '内蒙古 阿拉善盟': [9537, 3760, 177, 4339, 13107, 4412, 112], '甘肃 临夏': [8521, 3189, 210, 3182, 12710, 4144, 72], '重庆 长寿区': [3633, 1240, 111, 1246, 6249, 1672, 43], '湖南 怀化': [14651, 4437, 501, 5276, 25564, 5962, 161], '四川 广元': [9857, 2899, 305, 4385, 19151, 4007, 122], '天津 大港区': [7914, 2612, 238, 2848, 12317, 3553, 97], '甘肃 张掖': [9203, 3475, 218, 3571, 13808, 4185, 118], '重庆 云阳县': [3259, 1117, 83, 1236, 5296, 1526, 39], '新疆 和田': [8031, 3056, 148, 2960, 11040, 3298, 86], '四川 眉山': [9685, 2995, 343, 3594, 15329, 4156, 101], '重庆 彭水苗族土家族自治县': [3344, 1158, 133, 1205, 4693, 1563, 33], '黑龙江 鸡西': [19755, 7620, 311, 6444, 21778, 6848, 149], '甘肃 平凉': [9914, 3424, 214, 3755, 17691, 4359, 82], '四川 资阳': [8754, 2862, 251, 3304, 17455, 3746, 96], '澳门 氹仔': [911, 281, 66, 565, 3862, 629, 19], '香港 离岛区': [15361, 1759, 149, 2434, 40338, 2191, 277], '海外 瑞典': [1204, 277, 79, 582, 2715, 547, 28], '四川 自贡': [9969, 2902, 313, 3708, 17200, 4190, 140], '陕西 延安': [15156, 5218, 383, 5732, 23603, 6862, 171], '安徽 淮南': [15924, 4886, 481, 5588, 26688, 6624, 211], '青海 海北': [15923, 5374, 276, 5642, 21552, 6337, 183], '台湾 彰化县': [1121, 370, 112, 411, 4431, 506, 17], '海外 越南': [7206, 3100, 179, 2518, 10699, 3074, 89], '云南 楚雄': [9098, 3280, 271, 3413, 14393, 3835, 116], '海外 菲律宾': [7732, 2752, 194, 2437, 9397, 2948, 90], '海外 印尼': [7313, 3150, 141, 2787, 10393, 3408, 83], '海外 挪威': [1195, 276, 69, 363, 3724, 4750, 28], '西藏 日喀则': [16378, 6062, 308, 6134, 21974, 7065, 199], '天津 汉沽区': [6299, 2378, 152, 2482, 9533, 2785, 57], '台湾 新北市': [1176, 333, 104, 560, 4675, 519, 19], '海外 匈牙利': [353, 97, 25, 121, 1120, 184, 12], '重庆 巫山县': [2087, 744, 36, 747, 3397, 958, 21], '重庆 奉节县': [3453, 1148, 80, 1283, 7640, 1539, 37], '台湾 南投县': [927, 345, 35, 375, 7104, 459, 13], '重庆 大渡口区': [6635, 2271, 165, 2114, 9774, 2523, 68], '海外 土耳其': [601, 100, 32, 172, 1259, 5438, 13], '海外 希腊': [1110, 247, 65, 348, 3482, 517, 24], '河南 驻马店': [13368, 4079, 393, 4952, 24045, 5730, 217], '云南 普洱': [9732, 3411, 241, 3516, 16374, 4150, 100], '重庆 北碚区': [6267, 1720, 283, 2278, 12926, 15326, 87], '黑龙江 双鸭山': [12645, 4790, 305, 4799, 21909, 5376, 127], '海外 乌克兰': [371, 108, 19, 124, 1144, 243, 17], '内蒙古 乌兰察布市': [10524, 3779, 218, 4138, 16168, 4730, 115], '内蒙古': [24484, 8211, 708, 8537, 45998, 10337, 351], '海外 意大利': [3572, 636, 261, 1057, 7687, 1197, 55], '海外 爱尔兰': [1649, 298, 82, 538, 4396, 738, 23], '海外 沙特阿拉伯': [1672, 254, 132, 512, 3326, 602, 49], '海外 印度': [6879, 3015, 182, 2859, 9472, 3208, 93], '河南 济源': [1937, 590, 40, 742, 3596, 945, 43], '香港 北区': [577, 206, 24, 405, 1952, 310, 12], '湖北 仙桃': [2687, 801, 51, 986, 4856, 1142, 31], '重庆 潼南县': [3157, 1210, 100, 1480, 5689, 1403, 45], '海外 埃及': [645, 175, 37, 172, 2101, 225, 13], '重庆 永川区': [5034, 1487, 192, 1679, 8286, 2059, 58], '云南 昭通': [9400, 3010, 228, 3400, 14211, 4057, 104], '河北 承德': [16209, 5288, 456, 6226, 27862, 7574, 219], '湖北 神农架': [1859, 696, 25, 654, 4129, 772, 28], '重庆 城口县': [2922, 1107, 45, 1135, 4038, 1325, 24], '海外 哥伦比亚': [387, 93, 19, 153, 1313, 256, 14], '海外 丹麦': [1052, 205, 64, 338, 2641, 506, 32], '新疆 阿勒泰': [7855, 2890, 213, 2946, 11327, 3757, 104], '湖北 黄石': [14788, 4526, 464, 5522, 25477, 7339, 211], '台湾 新竹县': [932, 340, 50, 407, 2898, 512, 6], '重庆 武隆县': [3157, 1134, 81, 1197, 4704, 1331, 33], '海外 新西兰': [4277, 1883, 140, 2411, 6959, 3270, 76], '北京 延庆县': [8326, 2640, 282, 2719, 10860, 3311, 81], '重庆 垫江县': [3225, 1075, 84, 1200, 4641, 1452, 41], '香港 观塘区': [830, 293, 39, 438, 2775, 591, 16], '新疆 喀什': [8831, 3181, 184, 3397, 15860, 3919, 108], '重庆 丰都县': [3471, 1240, 89, 1258, 5076, 1399, 36], '四川 广安': [9639, 3255, 275, 3607, 15729, 4015, 95], '宁夏 中卫': [2589, 742, 49, 867, 5196, 1031, 26], '天津 保税区': [1086, 380, 16, 756, 2754, 594, 11], '天津 宁河县': [6623, 2482, 125, 2554, 9357, 3035, 66], '重庆 铜梁县': [3573, 1252, 96, 1307, 5524, 1450, 43], '广西 崇左': [2059, 597, 40, 827, 3795, 810, 18], '四川 巴中': [8236, 2737, 240, 3045, 13148, 3362, 92], '重庆 开县': [3837, 1235, 108, 1453, 5848, 1659, 36], '海外 芬兰': [929, 180, 76, 309, 2111, 352, 18], '甘肃': [25044, 7633, 520, 11687, 50467, 10178, 305], '海外 墨西哥': [236, 53, 14, 111, 828, 151, 7], '重庆 南川区': [3248, 1227, 82, 2115, 5001, 1369, 45], '台湾 基隆市': [928, 282, 29, 345, 2244, 365, 14], '台湾 新竹市': [1241, 367, 32, 416, 2502, 536, 12], '海外 比利时': [640, 180, 40, 214, 1747, 489, 20], '海外 阿根廷': [526, 108, 120, 160, 1555, 196, 9], '海外 南非': [392, 67, 23, 122, 1214, 223, 10], '香港 西贡区': [831, 189, 30, 337, 2500, 347, 24], '香港 深水埗区': [495, 186, 68, 287, 3450, 346, 11], '香港 黄大仙区': [2266, 193, 35, 323, 2467, 413, 14], '澳门 大堂区': [605, 229, 30, 416, 2814, 410, 8], '湖北 潜江': [4441, 606, 65, 719, 4495, 878, 24], '台湾 台中县': [1021, 350, 37, 434, 3971, 486, 14], '重庆 秀山土家族苗族自治县': [3163, 1198, 66, 1283, 4609, 1435, 30], '重庆 巫溪县': [3057, 1119, 60, 1173, 4310, 1392, 27], '重庆 万盛区': [5534, 1327, 78, 1142, 5607, 1435, 27], '澳门 风顺堂区': [503, 241, 24, 366, 2472, 633, 11], '澳门 路环': [577, 202, 24, 335, 2356, 340, 8], '香港 屯门区': [565, 200, 38, 285, 2007, 291, 8], '香港 元朗区': [903, 418, 39, 516, 2515, 539, 13], '台湾 花莲县': [381, 89, 23, 136, 1146, 141, 12], '香港 荃湾区': [706, 241, 27, 330, 1837, 352, 11], '海外 奥地利': [717, 172, 36, 242, 1816, 342, 19], '海外 伊朗': [342, 78, 25, 171, 958, 245, 14], '台湾 桃园县': [818, 225, 44, 346, 2774, 397, 19], '海外 白俄罗斯': [268, 58, 21, 99, 1463, 246, 5], '台湾 屏东县': [351, 113, 13, 208, 1391, 206, 5], '香港 大埔区': [340, 142, 22, 204, 1427, 210, 11], '香港 葵青区': [599, 198, 34, 292, 2157, 319, 13], '台湾 嘉义县': [199, 156, 6, 203, 1284, 194, 4], '海外 葡萄牙': [368, 80, 45, 81, 1170, 163, 6], '香港 南区': [435, 135, 27, 219, 1831, 250, 6], '澳门 望德堂区': [455, 150, 29, 324, 2533, 281, 6], '台湾 高雄县': [297, 108, 25, 169, 1239, 174, 4], '澳门 圣安多尼堂区': [650, 239, 35, 412, 2772, 397, 13], '台湾 宜兰县': [359, 133, 15, 176, 1243, 186, 8], '台湾 苗栗县': [5117, 407, 68, 487, 5820, 398, 17], '海外 古巴': [483, 105, 26, 170, 1230, 239, 13], '海外 波兰': [470, 114, 20, 150, 1153, 198, 5], '台湾 云林县': [239, 187, 14, 150, 1218, 165, 4], '台湾 台南县': [240, 71, 9, 133, 1094, 168, 6], '台湾 澎湖县': [945, 337, 36, 435, 4986, 532, 8], '': [58, 22, 4, 16, 159, 21, 2]}
    # percent_output = region_calc(output_dic)

    percent_output = province_percent(output_dic)
    get_echartsdata(percent_output)

    #

