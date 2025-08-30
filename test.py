from bs4 import BeautifulSoup

html = ('<div><h1 class="heading" itemprop="name">Маленький взрослый – большой малыш</h1></div>');

src = 'чудо.html'

with open(src, 'rb') as read_file:
    index = read_file.read()

pars = BeautifulSoup(index, 'lxml')

creators = pars.select('[class*=badge-rating] .badge-text')
print(creators)

# data_post = {}
# data_post['name_ff'] = pars.body.find(("h1", {"class": "heading"})).text
#
# data_post['creators'] = {}

# i = 0
# for creators in pars.find_all('div', {'class': 'creator-info'}):
#
#     for work in creators.i:
#         data_post['creators'][i] = {}
#         data_post['creators'][i]['worker'] = work.text
#
#     for create in creators.find_all("a", {"class": "creator-username"}):
#         data_post['creators'][i]['name'] = create.text
#     i += 1
#
# post = f"<b>{data_post['name_ff']}<b><br>"
#
# for i in data_post['creators']:
#     post += data_post['creators'][i]['worker'] + ": " + data_post['creators'][i]['name']
#
# print(post);