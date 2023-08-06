# -*- encoding=utf-8 *-*
"""
    author: Li Junxian
    function: cookie
"""
from urllib.parse import urlparse


class CookiesUtils(object):

    @staticmethod
    def __is_match(url, domain):
        """
        判断domain是否匹配host
        :param domain:
        :return:
        """
        parse_ret = urlparse(url)
        hostname = parse_ret.hostname
        if hostname is None:
            return False
        if hostname.endswith(domain):
            return True
        return False

    @staticmethod
    def merge_requests_to_selenium(session, driver):
        if session is None or driver is None:
            return driver
        url = driver.current_url
        for cookie in session.cookies:
            cookie_ = {"name": cookie.name, "value": cookie.value}
            if cookie.path is not None:
                cookie_["path"] = cookie.path
            if cookie.domain is not None:
                domain = cookie.domain
                if not CookiesUtils.__is_match(url, domain):
                    continue
                cookie_["domain"] = cookie.domain
            if cookie.secure is not None:
                cookie_["secure"] = cookie.secure
            if cookie.expires is not None:
                cookie_["expiry"] = cookie.expires
            driver.delete_cookie(cookie.name)
            driver.add_cookie(cookie_)
        return driver



