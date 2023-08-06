#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
cookie 相关模块
"""
import traceback

from wpy.functools import clock
from wush.common.loggers import get_logger
from wush.common.constants import Constants

class Cookie(object):

    logger = get_logger('Cookie')

    @classmethod
    @clock(fmt = Constants.CLOCK_FMT, logger_func = logger.info)
    def get_browser_cookie(cls, *domains, browser='chrome'):
        """获取留来的 cookie
        :param list domains: 域名列表
        """
        chrome = None
        try:
            import browsercookie
            chrome = getattr(browsercookie, browser)()
        except :
            print('can not import browsercookie')
            traceback.print_exc()
            traceback.print_stack()
        res = {}
        if not chrome:
            return res
        try:
            for k, v in chrome._cookies.items():
                if k not in domains:
                    continue
                cookies = v.get("/")
                for ck, cv in cookies.items():
                    res[ck] = cv.value
        except Exception as e:
            print(e)
        return res

if __name__ == "__main__":
    res = Cookie.get_browser_cookie('.python.org')
    print(res)

