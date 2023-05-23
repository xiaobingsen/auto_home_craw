# encoding=utf-8
import requests
import re
from bs4 import BeautifulSoup
import string
import time
from tqdm import tqdm
class crawlCar(object):
    def __init__(self):
        # self.src_page_lst = [f"http://www.autohome.com.cn/grade/carhtml/{value}.html" for value in list(string.ascii_uppercase)]
        self.src_page_lst = list(string.ascii_uppercase) # A-Z
        # self.src_page_lst = ['A'] # A
        self.source_page = 'http://car.autohome.com.cn'
        self.image_save_file = open('./image_list.txt','w', encoding='utf-8')
        self.brand_sub_brand_file = open('./brand_sub_brand_file.txt','w', encoding='utf-8')
        self.res_info = {}
        self.brand_sbrand_info = {} # 用于存储品牌、子品牌以及对应的网址
        self.start()
        self.end()
    def write(self, writer, line):
        writer.write(line)
        writer.flush()
    def beautiful_soup(self, url):
        source = requests.get(url).text
        soup = BeautifulSoup(source, 'lxml')
        return soup
    def sub_brand_next_page(self, url, value, brand):
        # IN: 子品牌目录 https://car.autohome.com.cn/price/brand-33.html#pvareaid=2042362
        # OUT: ('https://www.autohome.com.cn/5998/#pvareaid=6834145', '奥迪A7L'), ('https://www.autohome.com.cn/6336/#pvareaid=6834145', '奥迪Q5 e-tron')
        sub_soup = self.beautiful_soup(url)
        sub_pattern = '<a class="font-bold" href="(.*?)" target="_blank">(.*?)</a'
        sub_groups = re.findall(sub_pattern, str(sub_soup))

        for subbrand_info in sub_groups:
            sub_brand_url, sub_brand = subbrand_info[0], subbrand_info[1]
            pattern = 'https://www.autohome.com.cn/(.*?)/#pvareaid'
            subrand_id = re.findall(pattern, sub_brand_url)[
                0]  # 读取5998: https://www.autohome.com.cn/5998/#pvareaid=6834145
            sub_brand_url = f'http://car.autohome.com.cn/pic/series/{subrand_id}.html'
            if sub_brand not in self.res_info[value][brand]['sub_brand']:
                self.res_info[value][brand]['sub_brand'][sub_brand] = {}
            self.res_info[value][brand]['sub_brand'][sub_brand]['url'] = sub_brand_url
            line = f'{brand}___{sub_brand}___{sub_brand_url}\n'
            self.write(self.brand_sub_brand_file, line)
        pass

    def get_brand_sbrand_info(self):
        for value in tqdm(self.src_page_lst):
            if value not in self.brand_sbrand_info:
                self.res_info[value] = {}
            url     = f"http://www.autohome.com.cn/grade/carhtml/{value}.html"
            soup = self.beautiful_soup(url)
            # width="50"/></a><div><a href="//car.autohome.com.cn/price/brand-33.html#pvareaid=2042362">奥迪</a></div></dt>
            pattern    = '</a><div><a href="(.*?)">(.*?)</a></div></dt>'
            brand_matchs = re.findall(pattern, str(soup))

            for brand_match in brand_matchs:
                # 品牌名字
                brand     = brand_match[1]
                brand_url = f'http:{brand_match[0]}'

                if brand not in self.res_info[value]:
                    self.res_info[value][brand] = {}
                self.res_info[value][brand]['url'] = brand_url
                self.res_info[value][brand]['sub_brand'] = {}
                self.sub_brand_next_page(brand_url, value, brand)

                # 查看是否需要翻页
                sub_soup = self.beautiful_soup(brand_url)
                pre_next_pattern = '上一页(.*?)下一页'
                next_page_groups = re.findall(pre_next_pattern, str(sub_soup))  # [('/pic/series/16-1-p2.html', '2')]
                if len(next_page_groups)  != 0:
                    next_pattern = '<a href="(.*?)">(.*?)</a>'
                    next_page_groups = re.findall(next_pattern, next_page_groups[0])
                    if not next_page_groups.__len__() == 0:
                        for npg in next_page_groups:
                            next_page_url = self.source_page + npg[0]
                            self.sub_brand_next_page(next_page_url, value, brand)

    def get_sbrand_full_image(self, url, brand, sub_brand):
        soup = self.beautiful_soup(url)
        # <a href="/photo/series/55229/1/7346033.html" title="上汽奥迪 奥迪A7L 2022款 45 TFSI quattro S-line 见远型曜黑套装" target="_blank"><img src=
        pattern = '<li><a href="(.*?)" target="_blank" title="(.*?)"><img alt="(.*?)"'
        groups = re.findall(pattern, str(soup))
        # out: [('/photo/series/55229/1/7346033.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI quattro S-line 见远型曜黑套装', '2022款 45 TFSI quattro S-line 见远型曜黑套装'), ('/photo/series/55229/1/7346032.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI quattro S-line 见远型曜黑套装', '2022款 45 TFSI quattro S-line 见远型曜黑套装'), ('/photo/series/55229/1/7346031.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI quattro S-line 见远型曜黑套装', '2022款 45 TFSI quattro S-line 见远型曜黑套装'), ('/photo/series/55229/1/7346030.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI quattro S-line 见远型曜黑套装', '2022款 45 TFSI quattro S-line 见远型曜黑套装'), ('/photo/series/55229/1/7346029.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI quattro S-line 见远型曜黑套装', '2022款 45 TFSI quattro S-line 见远型曜黑套装'), ('/photo/series/55229/1/7346028.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI quattro S-line 见远型曜黑套装', '2022款 45 TFSI quattro S-line 见远型曜黑套装'), ('/photo/series/55229/1/7346027.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI quattro S-line 见远型曜黑套装', '2022款 45 TFSI quattro S-line 见远型曜黑套装'), ('/photo/series/56686/1/8648818.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI quattro S-line 圣骑士', '2022款 45 TFSI quattro S-line 圣骑士'), ('/photo/series/56686/1/8648817.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI quattro S-line 圣骑士', '2022款 45 TFSI quattro S-line 圣骑士'), ('/photo/series/56686/1/8648816.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI quattro S-line 圣骑士', '2022款 45 TFSI quattro S-line 圣骑士'), ('/photo/series/56686/1/8648815.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI quattro S-line 圣骑士', '2022款 45 TFSI quattro S-line 圣骑士'), ('/photo/series/56686/1/8648814.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI quattro S-line 圣骑士', '2022款 45 TFSI quattro S-line 圣骑士'), ('/photo/series/56686/1/8648813.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI quattro S-line 圣骑士', '2022款 45 TFSI quattro S-line 圣骑士'), ('/photo/series/56686/1/8648812.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI quattro S-line 圣骑士', '2022款 45 TFSI quattro S-line 圣骑士'), ('/photo/series/62615/1/8624779.html', '上汽奥迪 奥迪A7L 2023款 45 TFSI quattro S-line 黑武士版', '2023款 45 TFSI quattro S-line 黑武士版'), ('/photo/series/62615/1/8624778.html', '上汽奥迪 奥迪A7L 2023款 45 TFSI quattro S-line 黑武士版', '2023款 45 TFSI quattro S-line 黑武士版'), ('/photo/series/62615/1/8624777.html', '上汽奥迪 奥迪A7L 2023款 45 TFSI quattro S-line 黑武士版', '2023款 45 TFSI quattro S-line 黑武士版'), ('/photo/series/62615/1/8624776.html', '上汽奥迪 奥迪A7L 2023款 45 TFSI quattro S-line 黑武士版', '2023款 45 TFSI quattro S-line 黑武士版'), ('/photo/series/62615/1/8624775.html', '上汽奥迪 奥迪A7L 2023款 45 TFSI quattro S-line 黑武士版', '2023款 45 TFSI quattro S-line 黑武士版'), ('/photo/series/62615/1/8624774.html', '上汽奥迪 奥迪A7L 2023款 45 TFSI quattro S-line 黑武士版', '2023款 45 TFSI quattro S-line 黑武士版'), ('/photo/series/62615/1/8624773.html', '上汽奥迪 奥迪A7L 2023款 45 TFSI quattro S-line 黑武士版', '2023款 45 TFSI quattro S-line 黑武士版'), ('/photo/series/53486/1/8483377.html', '上汽奥迪 奥迪A7L 2022款 55 TFSI quattro S-line 志远型曜黑套装', '2022款 55 TFSI quattro S-line 志远型曜黑套装'), ('/photo/series/53486/1/8483376.html', '上汽奥迪 奥迪A7L 2022款 55 TFSI quattro S-line 志远型曜黑套装', '2022款 55 TFSI quattro S-line 志远型曜黑套装'), ('/photo/series/53486/1/8483375.html', '上汽奥迪 奥迪A7L 2022款 55 TFSI quattro S-line 志远型曜黑套装', '2022款 55 TFSI quattro S-line 志远型曜黑套装'), ('/photo/series/53486/1/8483374.html', '上汽奥迪 奥迪A7L 2022款 55 TFSI quattro S-line 志远型曜黑套装', '2022款 55 TFSI quattro S-line 志远型曜黑套装'), ('/photo/series/53486/1/8483373.html', '上汽奥迪 奥迪A7L 2022款 55 TFSI quattro S-line 志远型曜黑套装', '2022款 55 TFSI quattro S-line 志远型曜黑套装'), ('/photo/series/53486/1/8483372.html', '上汽奥迪 奥迪A7L 2022款 55 TFSI quattro S-line 志远型曜黑套装', '2022款 55 TFSI quattro S-line 志远型曜黑套装'), ('/photo/series/53486/1/8483371.html', '上汽奥迪 奥迪A7L 2022款 55 TFSI quattro S-line 志远型曜黑套装', '2022款 55 TFSI quattro S-line 志远型曜黑套装'), ('/photo/series/57203/1/8172553.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI S-line 筑梦未来版', '2022款 45 TFSI S-line 筑梦未来版'), ('/photo/series/57203/1/8172552.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI S-line 筑梦未来版', '2022款 45 TFSI S-line 筑梦未来版'), ('/photo/series/57203/1/8172551.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI S-line 筑梦未来版', '2022款 45 TFSI S-line 筑梦未来版'), ('/photo/series/57203/1/8172549.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI S-line 筑梦未来版', '2022款 45 TFSI S-line 筑梦未来版'), ('/photo/series/57203/1/8172547.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI S-line 筑梦未来版', '2022款 45 TFSI S-line 筑梦未来版'), ('/photo/series/57203/1/8172545.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI S-line 筑梦未来版', '2022款 45 TFSI S-line 筑梦未来版'), ('/photo/series/57203/1/8172543.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI S-line 筑梦未来版', '2022款 45 TFSI S-line 筑梦未来版'), ('/photo/series/56685/1/8149200.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI quattro S-line 风骑士', '2022款 45 TFSI quattro S-line 风骑士'), ('/photo/series/56685/1/8149199.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI quattro S-line 风骑士', '2022款 45 TFSI quattro S-line 风骑士'), ('/photo/series/56685/1/8149198.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI quattro S-line 风骑士', '2022款 45 TFSI quattro S-line 风骑士'), ('/photo/series/56685/1/8149197.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI quattro S-line 风骑士', '2022款 45 TFSI quattro S-line 风骑士'), ('/photo/series/56685/1/8149196.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI quattro S-line 风骑士', '2022款 45 TFSI quattro S-line 风骑士'), ('/photo/series/56685/1/8149195.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI quattro S-line 风骑士', '2022款 45 TFSI quattro S-line 风骑士'), ('/photo/series/58422/1/8141511.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI S-line 筑梦新生版', '2022款 45 TFSI S-line 筑梦新生版'), ('/photo/series/58422/1/8141510.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI S-line 筑梦新生版', '2022款 45 TFSI S-line 筑梦新生版'), ('/photo/series/58422/1/8141509.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI S-line 筑梦新生版', '2022款 45 TFSI S-line 筑梦新生版'), ('/photo/series/58422/1/8141508.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI S-line 筑梦新生版', '2022款 45 TFSI S-line 筑梦新生版'), ('/photo/series/58422/1/8141507.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI S-line 筑梦新生版', '2022款 45 TFSI S-line 筑梦新生版'), ('/photo/series/58422/1/8141506.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI S-line 筑梦新生版', '2022款 45 TFSI S-line 筑梦新生版'), ('/photo/series/58422/1/8141505.html', '上汽奥迪 奥迪A7L 2022款 45 TFSI S-line 筑梦新生版', '2022款 45 TFSI S-line 筑梦新生版'), ('/photo/series/53490/1/7481205.html', '上汽奥迪 奥迪A7L 2022款 55 TFSI quattro S-line edition executive先见版', '2022款 55 TFSI quattro S-line edition executive先见版'), ('/photo/series/53490/1/7481204.html', '上汽奥迪 奥迪A7L 2022款 55 TFSI quattro S-line edition executive先见版', '2022款 55 TFSI quattro S-line edition executive先见版'), ('/photo/series/53490/1/7481203.html', '上汽奥迪 奥迪A7L 2022款 55 TFSI quattro S-line edition executive先见版', '2022款 55 TFSI quattro S-line edition executive先见版'), ('/photo/series/53490/1/7481202.html', '上汽奥迪 奥迪A7L 2022款 55 TFSI quattro S-line edition executive先见版', '2022款 55 TFSI quattro S-line edition executive先见版'), ('/photo/series/53490/1/7481201.html', '上汽奥迪 奥迪A7L 2022款 55 TFSI quattro S-line edition executive先见版', '2022款 55 TFSI quattro S-line edition executive先见版'), ('/photo/series/53490/1/7481200.html', '上汽奥迪 奥迪A7L 2022款 55 TFSI quattro S-line edition executive先见版', '2022款 55 TFSI quattro S-line edition executive先见版'), ('/photo/series/53490/1/7481199.html', '上汽奥迪 奥迪A7L 2022款 55 TFSI quattro S-line edition executive先见版', '2022款 55 TFSI quattro S-line edition executive先见版'), ('/photo/series/53483/1/7480246.html', '上汽奥迪 奥迪A7L 2022款 55 TFSI quattro S-line 境远型曜黑套装', '2022款 55 TFSI quattro S-line 境远型曜黑套装'), ('/photo/series/53483/1/7480245.html', '上汽奥迪 奥迪A7L 2022款 55 TFSI quattro S-line 境远型曜黑套装', '2022款 55 TFSI quattro S-line 境远型曜黑套装'), ('/photo/series/53483/1/7480244.html', '上汽奥迪 奥迪A7L 2022款 55 TFSI quattro S-line 境远型曜黑套装', '2022款 55 TFSI quattro S-line 境远型曜黑套装'), ('/photo/series/53483/1/7480243.html', '上汽奥迪 奥迪A7L 2022款 55 TFSI quattro S-line 境远型曜黑套装', '2022款 55 TFSI quattro S-line 境远型曜黑套装'), ('/photo/series/53483/1/7480242.html', '上汽奥迪 奥迪A7L 2022款 55 TFSI quattro S-line 境远型曜黑套装', '2022款 55 TFSI quattro S-line 境远型曜黑套装')]
        for pg in groups:
            # print(pg)
            sub_url = self.source_page + pg[0]
            sub_name = pg[1]
            sub_soup = self.beautiful_soup(sub_url)
            sub_pic_pattern = ' src="//car(.*?).autoimg.cn/(.*?)" width'  # 第一个(.*?)有些是car2有些是car3
            # 145: <img id="img" onside="-1" src="//car3.autoimg.cn/cardfs/product/g29/M0B/70/8A/1400x0_1_q95_autohomecar__ChwFk2HmlwqAelGbACJxDP9Mxeg639.jpg" width="1024"/>
            subsub_pic_groups = re.findall(sub_pic_pattern, str(sub_soup))
            for sub_pg in subsub_pic_groups:
                sub_pg_url = f'http://car{sub_pg[0]}.autoimg.cn/{sub_pg[1]}'
                line = f'{brand}___{sub_brand}___{sub_name}___{sub_pg_url}\n'
                self.write(self.image_save_file, line)



    def get_brand_sbrand_pic_url(self):
        for k in self.res_info:
            for brand in self.res_info[k]:
                for sub_brand in self.res_info[k][brand]['sub_brand']:
                    url = self.res_info[k][brand]['sub_brand'][sub_brand]['url']
                    sub_pic_soup = self.beautiful_soup(url)
                    sub_pic_pattern = '<div class="uibox-title"><a href="(.*?)">(.*?)<'
                    sub_pic_groups = re.findall(sub_pic_pattern, str(sub_pic_soup))
                    # class_list = ['车身外观', '中控方向盘', '车厢座椅', '其它细节', '评测']
                    class_list = ['车身外观']
                    for ssscng in sub_pic_groups:
                        if ssscng[1] in class_list:
                            sub_pic_url = self.source_page + ssscng[0]

                            # 当前页面所有图片爬取
                            self.get_sbrand_full_image(sub_pic_url, brand, sub_brand)

                            # 查看是否需要翻页
                            sub_soup = self.beautiful_soup(sub_pic_url)
                            pre_next_pattern = '上一页(.*?)下一页'
                            next_page_groups = re.findall(pre_next_pattern, str(sub_soup))  # [('/pic/series/16-1-p2.html', '2')]
                            if len(next_page_groups)  != 0:
                                next_pattern = '<a href="(.*?)">(.*?)</a>'
                                next_page_groups = re.findall(next_pattern, next_page_groups[0])
                                if not next_page_groups.__len__() == 0:
                                    for npg in next_page_groups:
                                        next_page_url = self.source_page + npg[0]
                                        self.get_sbrand_full_image(next_page_url, brand, sub_brand)
        print("get brand name and url end")
    def start(self):
        print("get brand name and url")
        self.get_brand_sbrand_info()
        self.get_brand_sbrand_pic_url()

    def end(self):
        self.image_save_file.close()
        self.brand_sub_brand_file.close()
if __name__ == "__main__":
    crawlCar()

