shang_dic = {'健康': {'province_shang': 4.614931341259213, 'emotion_shang': 1.7425643297013043},'事业有成': {'province_shang': 4.6637099637881985, 'emotion_shang': 1.330961168845477},'发展机会': {'province_shang': 4.646693383284832, 'emotion_shang': 1.6815369339421364},'生活幸福': {'province_shang': 4.676081956069652, 'emotion_shang': 1.326266607438356},'有房': {'province_shang': 4.450996265928352, 'emotion_shang': 1.8512545823922906},'出名': {'province_shang': 4.60629078639634, 'emotion_shang': 1.7926907030973753},'家庭幸福': {'province_shang': 4.645193087395395, 'emotion_shang': 1.4111918296202708},'好工作': {'province_shang': 4.5806270617437725, 'emotion_shang': 1.699848118852902},'平等机会': {'province_shang': 4.535844884956961, 'emotion_shang': 1.8934531097785894},'白手起家': {'province_shang': 4.576773617415558, 'emotion_shang': 1.4671189161848104},'成为富人': {'province_shang': 4.610419305107782, 'emotion_shang': 1.806871317347328},'个体自由': {'province_shang': 3.8793067156561394, 'emotion_shang': 1.3132859350989219},'安享晚年': {'province_shang': 4.532088162152894, 'emotion_shang': 1.7959849012260913},'收入足够': {'province_shang': 4.44449133972484, 'emotion_shang': 1.8576476312107724},'个人努力': {'province_shang': 4.724085178174252, 'emotion_shang': 1.1191634015490641},'祖国强大': {'province_shang': 4.611218815596922, 'emotion_shang': 1.549148587597116},'中国经济持续发展': {'province_shang': 3.82186193262807, 'emotion_shang': 1.5304930567574826},'父辈更好': {'province_shang': 4.541929022026666, 'emotion_shang': 1.9182958340544896}}
keyword_list = ['健康','事业有成','发展机会','生活幸福','有房','出名','家庭幸福','好工作','平等机会','白手起家','成为富人','个体自由','安享晚年','收入足够','个人努力','祖国强大','中国经济持续发展','父辈更好']

province_data = []
emotion_data = []

for current_keyword in keyword_list:
    province_data.append(shang_dic[current_keyword]['province_shang'])
    emotion_data.append(shang_dic[current_keyword]['emotion_shang'])

print(province_data)
print(emotion_data)