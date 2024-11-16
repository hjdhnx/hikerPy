#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File  : 胖虎.py
# Author: DaShenHan&道长-----先苦后甜，任凭晚风拂柳颜------
# Author's Blog: https://blog.csdn.net/qq_32394351
# Date  : 2024/11/10

import sys

sys.path.append('..')

try:
    from base.spider import BaseSpider
    from base.htmlParser import jsoup
except ImportError:
    from t4.base.spider import BaseSpider
    from t4.base.htmlParser import jsoup

import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
import json
import re
from urllib.parse import quote_plus


class Spider(BaseSpider):  # 元类 默认的元类 type
    module = None
    t = str(int(time.time()))
    host = "http://sm.physkan.top:3389"
    jsp = jsoup(host)

    def getDependence(self):
        return ['base_spider']
        # return []

    def getName(self):
        return "胖虎"

    def init_headers(self):
        self.headers = {
            "User-Agent": "okhttp/3.14.9",
            "app-version-code": "402",
            "app-ui-mode": "light",
            "app-user-device-id": "25f869d32598d3d3089a929453dff0bb7",
            "app-api-verify-time": self.t,
            "app-api-verify-sign": self.aes("encrypt", self.t),
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        }

    def init(self, extend=""):
        print(f"============依赖列表:{extend}============")
        ext = self.extend
        print(f"============ext:{ext}============")
        # 装载模块，这里只要一个就够了
        if isinstance(extend, list):
            for lib in extend:
                if '.Spider' in str(type(lib)):
                    self.module = lib
                    break

        self.init_headers()
        print(self.headers)

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    @staticmethod
    def body2data(body):
        data = {}
        for _b in body.split('&'):
            data[_b.split('=')[0]] = '='.join(_b.split('=')[1:])
        return data

    def homeContent(self, filter):
        r = self.fetch(f"{self.host}/api.php/getappapi.index/initV119", headers=self.headers)
        data = r.text
        data1 = json.loads(data)["data"]
        data2 = self.aes("decrypt", data1)
        dy = {
            "class": "类型",
            "area": "地区",
            "lang": "语言",
            "year": "年份",
            "letter": "字母",
            "by": "排序",
            "sort": "排序",
        }
        filters = {}
        classes = []
        json_data = json.loads(data2)["type_list"]
        self.home_data = json.loads(data2)["banner_list"]
        for item in json_data:
            if item["type_name"] == "全部":
                continue
            has_non_empty_field = False
            jsontype_extend = json.loads(item["type_extend"])
            jsontype_extend["sort"] = "最新,最热,最赞"
            classes.append({"type_name": item["type_name"], "type_id": item["type_id"]})
            for key in dy:
                if key in jsontype_extend and jsontype_extend[key].strip() != "":
                    has_non_empty_field = True
                    break
            if has_non_empty_field:
                filters[str(item["type_id"])] = []
                for dkey in jsontype_extend:
                    if dkey in dy and jsontype_extend[dkey].strip() != "":
                        values = jsontype_extend[dkey].split(",")
                        value_array = [
                            {"n": value.strip(), "v": value.strip()}
                            for value in values
                            if value.strip() != ""
                        ]
                        filters[str(item["type_id"])].append(
                            {"key": dkey, "name": dy[dkey], "value": value_array}
                        )
        result = {}
        result["class"] = classes
        result["filters"] = filters
        return result

    def homeVideoContent(self):
        result = {"list": self.home_data}
        # result = self.module.homeVideoContent()
        return result

    def categoryContent(self, tid, pg, filter, extend):
        body = f"area={extend.get('area', '全部')}&year={extend.get('year', '全部')}&type_id={tid}&page={pg}&sort={extend.get('sort', '最新')}&lang={extend.get('lang', '全部')}&class={extend.get('class', '全部')}"
        data = self.body2data(body)
        result = {}
        url = "{0}/api.php/getappapi.index/typeFilterVodList".format(self.host)
        data = self.post(url, headers=self.headers, data=data).text
        data1 = json.loads(data)["data"]
        data2 = self.aes("decrypt", data1)
        result["list"] = json.loads(data2)["recommend_list"]
        result["page"] = pg
        result["pagecount"] = 9999
        result["limit"] = 90
        result["total"] = 999999
        return result

    def detailContent(self, array):
        tid = array[0]
        url = f"{self.host}/api.php/getappapi.index/vodDetail"
        data = {
            "vod_id": tid
        }
        data = self.post(url, headers=self.headers, data=data).text
        data1 = json.loads(data)["data"]
        data2 = json.loads(self.aes("decrypt", data1))
        vod = data2["vod"]
        play = []
        names = []
        for itt in data2["vod_play_list"]:
            a = []
            names.append(itt["player_info"]["show"])
            parse = itt["player_info"]["parse"]
            for it in itt["urls"]:
                if re.search(r"mp4|m3u8", it["url"]):
                    a.append(f"{it['name']}${it['url']}")
                elif re.search(r"www.yemu.xyz", it["parse_api_url"]):
                    a.append(f"{it['name']}${it['parse_api_url']}")
                else:
                    a.append(
                        f"{it['name']}${'parse_api=' + parse + '&url=' + self.aes('encrypt', it['url']) + '&token=' + it['token']}")
            play.append("#".join(a))
        vod["vod_play_from"] = "$$$".join(names)
        vod["vod_play_url"] = "$$$".join(play)
        result = {"list": [vod]}
        return result

    def searchContent(self, key, quick=False, pg=1):
        body = f"keywords={key}&type_id=0&page={pg}"
        url = f"{self.host}/api.php/getappapi.index/searchList"
        data = self.body2data(body)
        data = self.post(url, headers=self.headers, data=data).text
        data1 = json.loads(data)["data"]
        data2 = self.aes("decrypt", data1)
        result = {"list": json.loads(data2)["search_list"]}
        return result

    def playerContent(self, flag, id, vipFlags):
        def edu(str):
            def replacer(match):
                return match.group(1) + quote_plus(match.group(2)) + match.group(3)

            return re.sub(r"(url=)(.*?)(&token)", replacer, str)

        url = id
        p = 0
        if "m3u8" not in url and "mp4" not in url:
            try:
                body = edu(url)
                data = self.body2data(body)
                data = self.post("{0}/api.php/getappapi.index/vodParse".format(self.host), headers=self.headers,
                                 data=data).text
                data1 = json.loads(data)["data"]
                data2 = json.loads(self.aes("decrypt", data1))["json"]
                url = json.loads(data2)["url"]
            except Exception as e:
                url = id
                p = 1
                if not url.startswith("https://www.yemu.xyz"):
                    url = "https://www.yemu.xyz/?url={0}".format(id)
        result = {}
        headers = self.headers.copy()
        del headers["Content-Type"]
        result["parse"] = p
        result["playUrl"] = ""
        result["url"] = url
        result["header"] = headers
        return result

    def localProxy(self, params):
        return [200, "video/MP2T", ""]

    def aes(self, operation, text):
        key = "ihIwTbt2YAe9TGea".encode("utf-8")
        iv = key
        if operation == "encrypt":
            cipher = AES.new(key, AES.MODE_CBC, iv)
            ct_bytes = cipher.encrypt(pad(text.encode("utf-8"), AES.block_size))
            ct = b64encode(ct_bytes).decode("utf-8")
            return ct
        elif operation == "decrypt":
            cipher = AES.new(key, AES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(b64decode(text)), AES.block_size)
            return pt.decode("utf-8")


def main():
    from base.loader import t3_spider_init

    spider = Spider()
    log = spider.log
    t3_spider_init(spider)

    log(spider.homeContent(True))
    log(spider.homeVideoContent())
    log(spider.categoryContent('21', 1, True, {}))
    log(spider.detailContent(['144311']))
    log(spider.playerContent('暴风', 'https://c1.7bbffvip.com/video/jiehunbabendana/第01集/index.m3u8', None))
    log(spider.searchContent('朋友'))


if __name__ == '__main__':
    main()
