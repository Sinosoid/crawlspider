import urllib2,urllib
headers={
'Host': 'weixin.sogou.com',
'Connection': 'keep-alive',
'Accept': '*/*',
'X-Requested-With': 'XMLHttpRequest',
'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
'Referer': 'http://weixin.sogou.com/',
'Accept-Language': 'zh-CN,zh;q=0.8'
}
request=urllib2.Request(url='http://weixin.sogou.com/pcindex/pc/pc_3/1.html',headers=headers)
response=urllib2.urlopen(request)
print response.read()