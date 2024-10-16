import requests
import json
from bs4 import BeautifulSoup
# 打开并读取JSON文件
with open('config.json', 'r') as file:
    config = json.load(file)
# 使用配置数据
JSESSIONID = config['JSESSIONID']
def get_html(ZC,Z,LF):
    """
    :param ZC: 第几周
    :param Z:  周几
    :param LF: 教学楼编号   弘毅楼：114
    :param JSESSIONID: COOKIES
    :return: 空教室表格HTMl
    """
    cookies = {
      'JSESSIONID': JSESSIONID,
    }

    headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
      'Referer': 'http://jwgl.hist.edu.cn/kbbp/dykb.zrjckb.html?menucode=SB05',
      # 'Cookie': 'JSESSIONID=D9D40C2197F93684D470CA6C9B4A532B',
      'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
      'hidCXLX': 'ajsi',
      'hidZC': ZC,
      'hidZ': Z,
      'hidLF': LF,
      'xn': '2024',
      'xq_m': '0',
      'radioa': '3',
    }

    response = requests.post('http://jwgl.hist.edu.cn/kbbp/dykb.zrjckb_data.jsp', cookies=cookies, headers=headers, data=data)
    if "凭证已失效" in response.text:
        print("COOKIE失效")
        return None
    else:
        return response.text


def parser_html(html_content):
    """
    :param html_content:
    :return:
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    group_div = soup.find('div', {'group': 'group'})
    campus = group_div.find(string=lambda t: "校区：" in t).strip()
    building = group_div.find(string=lambda t: "楼房：" in t).strip()
    week_and_day = group_div.find(string=lambda t: "星期" in t).strip().replace("\t","").replace("\r","").replace("\n","")

    # 找到所有的表格行
    rows = soup.find_all('tr')

    # 准备一个空列表来存储结果
    locations_and_periods = []

    # 遍历每一行，提取地点和节次
    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 1:  # 确保行中有足够的列
            location = cols[0].text.strip()  # 获取地点
            period = cols[7].text.strip()  # 获取节次
            locations_and_periods.append((location, period))  # 将它们作为一个元组添加到列表中

    # 打印结果
    locations_and_periods.pop(0)
    # print(locations_and_periods)
    # for location, period in locations_and_periods:
    #     print(f"地点: {location}, 节次: {period}")
    # 初始化教室时间表字典
    timetable = {}
    # 遍历数据，更新教室时间表
    for room, time_period in locations_and_periods:
        # 解析时间段
        days, periods = time_period.split('[')
        periods = periods.replace(']', '')
        periods = periods.replace('节', '').split('-')
        start_period, end_period = int(periods[0]), int(periods[1])
        if room not in timetable:
            # 如果教室不在字典中，初始化为全False
            timetable[room] = [False] * 10  # 假设有10个时间段

        # 更新时间段状态为True
        for period in range(start_period, end_period + 1):
            timetable[room][period - 1] = True

    # 打印结果
    return timetable,campus,building,week_and_day
    # for room, periods in timetable.items():
    #     print(f'"{room}": {periods}')

def main(ZC,Z,LF):
    """
    :param ZC:
    :param Z:
    :param LF:
    :return: [timetable,campus,building,week_and_day]
    """
    html_content = get_html(ZC,Z,LF)
    if html_content:
        a = parser_html(html_content)
        return a
    else:
        return None
if __name__ == '__main__':
    a = main("4", "5", "114")
    print(a)


