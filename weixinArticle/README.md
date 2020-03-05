# Scrapy爬取微信公众号文章

1. 二十次幂网站：[https://www.ershicimi.com/](https://www.ershicimi.com/)

2. 需要手动获取二十次幂的cookie

   ![](https://i.loli.net/2020/03/06/qau49UWC7hmLfrX.png)

设置`COOKIES_ENABLED = False`，并且添加下面请求头，主要是cookie

```python
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Cookie': 'Hm_lvt_ea5245057e456d6e5fe2fa739275b9dc=1581948850,1582024518,1583159670,1583399342; remember_token=820|bccb5ef3d5babaf6c943ce4a628f98e8e388e4c70fd2e50a76f4716741d957c1e8c4fe1e886e224b88126aa28c5238ad73918e48aab674ae15177477beece897; session=.eJwlj0FqBDEMBP_i8x5sWZas_cxiSW0SAgnM7J5C_p4hgb5WUf1dHvvA-Vbuz-OFW3m8Z7mXGETCrpwNq0mQos2pg5kIudMAck0b0Z1A1Z0ZBF6a2zzimpkRRSIXuNfdhatKI4SJr4GoTHo5-0TjmqMqtq8-Wop7K7cS57Efz68PfF49WlWbi1md6R4yMGws8ykai_siATz_uNeJ4__EpFp-fgGXAEBu.XmEk-A.lepbK3X_Bv7o8PczsbZF2ZqNSi0; Hm_lpvt_ea5245057e456d6e5fe2fa739275b9dc=1583425528',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'

}
```

