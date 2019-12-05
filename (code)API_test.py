import requests
import pygal
from pygal.style import LightColorizedStyle as LCS,LightenStyle as LS


url = 'https://api.github.com/search/repositories?q=language:python&sort=starts'
r = requests.get(url)
print('response:' ,r.status_code)

response_dict = r.json() #API的响应，并将响应存储在一个变量里
print('total_count:',response_dict['total_count'])

resp_dicts = response_dict['items']
print('responses return:',len(resp_dicts))

name,starts = [],[] #创建两个空列表，用以存储放在图表中的信息
for resp_dict in resp_dicts:
    name.append(resp_dict['name'])
    starts.append(resp_dict['stargazers_count'])

my_style = LS('#333366',base_style = LCS)
my_config = pygal.Config()
my_config.x_label_rotation = 45
my_config.show_legend = False
my_config.title_font_size = 24
my_config.label_font_size = 14
my_config.major_label_font_size = 19
my_config.truncate_label = 15
my_config.show_y_guides = False
my_config.width = 1000

chart = pygal.Bar(style = my_style, show_legend = False)
chart_title ='Most starts project in 2019-11'
chart.x_labels = name

chart.add('',starts)
path = 'D://python_github.svg'
chart.render_to_file(path)
print('保存成功！保存位置在:' + path)

#resp_dict = resp_dicts[0]
#print('\nkeys:',len(resp_dict))
#for key in sorted(resp_dict.keys()):  #提取resp_dict中一些键相关的值
#    print(key)

#print(response_dict.keys())
#


'''print('\nselect information about first dict')  #这是显示调用的API的信息部分，接下来用pygal库可视化展示
for resp_dict in resp_dicts:
    print('\nName:',resp_dict['name'])
    print('starts:',resp_dict['stargazers_count'])
    print('Owner:',resp_dict['owner']['login'])  
    print('Url:',resp_dict['html_url'])
    print('Created:',resp_dict['created_at'])
    print('Updated:',resp_dict['updated_at'])
    print('Description:',resp_dict['description'])
'''