# -*- coding: utf-8 -*-
import sys
import dns.resolver
import urllib
import urllib.request
#import urlparse
from urllib.parse import urlparse

class CdnCheck(object):
    CDN=None
    def __init__(self, url):
        super(CdnCheck, self).__init__()
        self.cdninfo()
        self.url = url
        self.cnames = []
        self.headers = []

    def get_cnames(self): # get all cname
        furl = urlparse(self.url)
        url = furl.netloc
        #print url

        rsv = dns.resolver.Resolver()
        # rsv.nameservers = ['114.114.114.114']
        try:
            answer = dns.resolver.query(url,'CNAME')
        except Exception as e:
            self.cnames = None
            # print "ERROR: %s" % e
        else:
            cname = [_.to_text() for _ in answer][0]
            self.cnames.append(cname)
            self.get_cname(cname)

    def get_cname(self,cname): # get cname
        try:
            answer = dns.resolver.query(cname,'CNAME')
            cname = [_.to_text() for _ in answer][0]
            self.cnames.append(cname)
            self.get_cname(cname)
        except dns.resolver.NoAnswer:
            pass

    def get_headers(self): # get header
        try:
            resp = urllib.request.urlopen(self.url)
        except Exception as e:
            self.headers = None
            # print "ERROR: %s" % e
        else:
            headers = str(resp.headers).lower()
            self.headers = headers

    def matched(self, context, *args): # Matching string 
        if not isinstance(context, str):
            context = str(context)

        func = lambda x, y: y in x
        # if any(func(context, pattern) for pattern in args):
        #     return True
        # else:
        #     return False
        for pattern in args:
            if func(context,pattern):
                return pattern
        return False

    def check(self):
        flag = None
        self.get_cnames()
        self.get_headers()
        if self.cnames:
            print (self.cnames)
            flag = self.matched(self.cnames,*self.cdn['cname'])
            #print flag
            if flag:
                return {'Status':True, 'CDN':self.cdn['cname'].get(flag)}
        if not flag and self.headers:
            flag = self.matched(self.headers,*self.cdn['headers'])
            if flag:
                return {'Status':True, 'CDN':'unknown'}
        return {'Status':False, 'CNAME':self.cnames, 'Headers':self.headers}

    def cdninfo(self):
        self.cdn = {
            'headers': set([
                'via',
                'x-via',
                'by-360wzb',
                'by-anquanbao',
                'cc_cache',
                'cdn cache server',
                'cf-ray',
                'chinacache',
                'powered-by-chinacache',
                'verycdn'
                'webcache',
                'x-cacheable',
                'x-fastly',
                'yunjiasu',
                'x-amz-cf-id',
                'X-CDN-Provider',
                'SkyparkCDN',

            ]),
            'cname':{
                'tbcache.com':u'Alibaba Cloud',# 阿里巴巴云
                'alicdn.com':u'Alibaba Cloud',#阿里巴巴云
                'tcdn.qq.com':u'tcdn.qq.com', # 腾讯
                '00cdn.com':u'XYcdn', # 星域cdn
                '21cvcdn.com':u'21Vianet', # 世纪互联
                '21okglb.cn':u'21Vianet', # 世纪互联
                '21speedcdn.com':u'21Vianet', # 世纪互联
                '21vianet.com.cn':u'21Vianet', # 世纪互联
                '21vokglb.cn':u'21Vianet', # 世纪互联
                '360wzb.com':u'360', # 360网站卫士
                '51cdn.com':u'ChinaCache', # 网宿科技
                'acadn.com':u'Dnion', # 帝联科技
                'aicdn.com':u'UPYUN', # 又拍云
                'akadns.net':u'Akamai', # Akamai
                'akamai-staging.net':u'Akamai', # Akamai
                'akamai.com':u'Akamai', # Akamai
                'akamai.net':u'Akamai', # Akamai
                'akamaitech.net':u'Akamai', # 易通锐进
                'akamaized.net':u'Akamai', # Akamai
                'alicloudlayer.com':u'ALiyun', # 阿里云
                'alikunlun.com':u'ALiyun', # 阿里云
                'aliyun-inc.com':u'ALiyun', # 阿里云
                'alicloudsec.com':u'ALiyun',# 阿里云
                'aliyuncs.com':u'ALiyun', # 阿里云
                'amazonaws.com':u'Amazon Cloudfront', # 亚马逊
                'anankecdn.com.br':u'Ananke', # Ananke
                'aodianyun.com':u'VOD', # 奥点云
                'aqb.so':u'AnQuanBao', # 安全宝
                'awsdns':u'KeyCDN', # KeyCDN
                'azioncdn.net':u'Azion', # Azion
                'azureedge.net':u'Azure CDN', # Microsoft Azure
                'bdydns.com':u'Baiduyun', # 百度云
                'bitgravity.com':u'Tata Communications', # 待定
                'cachecn.com':u'CnKuai', # 快网
                'cachefly.net':u'Cachefly', # Cachefly
                'ccgslb.com':u'ChinaCache', # 蓝汛科技
                'ccgslb.net':u'ChinaCache', # 蓝汛科技
                'ccgslb.com.cn':'ChinaCache',
                'cdn-cdn.net':u'', # 待定
                'cdn.cloudflare.net':u'CloudFlare', # CloudFlare
                'cdn.dnsv1.com':u'Tengxunyun', # 腾讯云
                'cdn.ngenix.net':u'', # 待定
                'cdn20.com':u'ChinaCache', # 网宿科技
                'cdn77.net':u'CDN77', # CDN77
                'cdn77.org':u'CDN77', # CDN77
                'cdnetworks.net':u'CDNetworks', # 同兴万点
                'cdnify.io':u'CDNify', # CDNify
                'cdnnetworks.com':u'CDNetworks', # 同兴万点
                'cdnsun.net':u'CDNsun', # CDNsun
                'cdntip.com':u'QCloud', # 腾讯云
                'cdnudns.com':u'PowerLeader', # 宝腾互联
                'cdnvideo.ru':u'CDNvideo', # CDNvideo
                'cdnzz.net':u'SuZhi', # 速致
                'chinacache.net':u'ChinaCache', # 蓝汛科技
                'chinaidns.net':u'LineFuture', # 澜景网络
                'chinanetcenter.com':u'ChinaCache', # 网宿科技
                'cloudcdn.net':u'CnKuai', # 快网
                'cloudfront.net':u'Amazon Cloudfront', # Amazon
                'customcdn.cn':u'ChinaCache', # 网宿科技
                'customcdn.com':u'ChinaCache', # 网宿科技
                'dnion.com':u'Dnion', # 帝联科技
                'dnspao.com':u'', # 待定
                'edgecastcdn.net':u'EdgeCast', # EdgeCast
                'edgesuite.net':u'Akamai', # Akamai
                'ewcache.com':u'Dnion', # 帝联科技
                'fastcache.com':u'FastCache', # 速网科技
                'fastcdn.cn':u'Dnion', # 帝联科技
                'fastly.net':u'Fastly', # Fastly
                'fastweb.com':u'CnKuai', # 快网
                'fastwebcdn.com':u'CnKuai', # 快网
                'footprint.net':u'Level3', # Level3
                'fpbns.net':u'Level3', # Level3
                'fwcdn.com':u'CnKuai', # 快网
                'fwdns.net':u'CnKuai', # 快网
                'globalcdn.cn':u'Dnion', # 帝联科技
                'hacdn.net':u'CnKuai', # 快网
                'hadns.net':u'CnKuai', # 快网
                'hichina.com':u'WWW', # 万网
                'hichina.net':u'WWW', # 万网
                'hwcdn.net':u'Highwinds', # Highwinds
                'incapdns.net':u'Incapsula', # Incapsula
                'internapcdn.net':u'Internap', # Internap
                'jiashule.com':u'Jiasule', # 加速乐
                'kunlun.com':u'ALiyun', # 阿里云
                'kunlunar.com':u'ALiyun', # 阿里云
                'kunlunca.com':u'ALiyun', # 阿里云
                'kxcdn.com':u'KeyCDN', # KeyCDN
                'lswcdn.net':u'Leaseweb', # Leaseweb
                'lxcdn.com':u'ChinaCache', # 网宿科技
                'mwcloudcdn.com':u'QUANTIL', # QUANTIL
                'netdna-cdn.com':u'MaxCDN', # MaxCDN
                'okcdn.com':u'21Vianet', # 世纪互联
                'okglb.com':u'21Vianet', # 世纪互联
                'ourwebcdn.net':u'ChinaCache', # 网宿科技
                'ourwebpic.com':u'ChinaCache', # 网宿科技
                'presscdn.com':u'Presscdn', # Presscdn
                'qingcdn.com':u'', # 待定
                'qiniudns.com':u'QiNiu', # 七牛云
                'skyparkcdn.net':u'', # 待定
                'speedcdns.com':u'QUANTIL', # QUANTIL
                'sprycdn.com':u'PowerLeader', # 宝腾互联
                'tlgslb.com':u'Dnion', # 帝联科技
                'txcdn.cn':u'CDNetworks', # 同兴万点
                'txnetworks.cn':u'CDNetworks', # 同兴万点
                'ucloud.cn':u'UCloud', # UCloud
                'unicache.com':u'LineFuture', # 澜景网络
                'verygslb.com':u'VeryCloud', # 云端网络
                'vo.llnwd.net':u'Limelight', # Limelight
                'wscdns.com':u'ChinaNetCenter', # 网宿科技
                'wscloudcdn.com':u'ChinaNetCenter', # 网宿科技
                'xgslb.net':u'Webluker', # WebLuker
                'ytcdn.net':u'Akamai', # Akamai
                'yunjiasu-cdn':u'Baiduyun', # 百度云加速
                'cloudfront':'CloudFront',#AWS CloudFront亚马逊云
                'kunlun.com':u'Alibaba Cloud',#阿里巴巴云
                'ccgslb':u'ChinaCache',#蓝汛
                'edgekey':u'Akamai',#CDN加速
                'fastly':u'Fastly',
                'chinacache':u'ChinaCache',
                'edgekey':u'Akamai',
                'akamai':u'Akamai',
                'fastly':u'Fastly',
                'edgecast':u'EdgeCast',
                'azioncdn':u'Azion',
                'cachefly':u'CacheFly',
                'cdn77':u'CDN77',
                'cdnetworks':u'CDNetworks',
                'cdnify':u'CDNify',
                'wscloudcdn':u'ChinaNetCenter',
                'speedcdns':u'ChinaNetCenter/Quantil',
                'mwcloudcdn':u'ChinaNetCenter/Quantil',
                'cloudflare':u'CloudFlare',
                'hwcdn':u'HighWinds',
                'kxcdn':u'KeyCDN',
                'awsdns':u'KeyCDN',
                'fpbns':u'Level3',
                'footprint':u'Level3',
                'llnwd':u'LimeLight',
                'netdna':u'MaxCDN',
                'bitgravity':u'Tata CDN',
                'azureedge':u'Azure CDN',
                'anankecdn':u'Anake CDN',
                'presscdn':u'Press CDN',
                'telefonica':u'Telefonica CDN',
                'dnsv1':u'Tecent CDN',
                'cdntip':u'Tecent CDN',
                'skyparkcdn':u'Sky Park CDN',
                'ngenix':u'Ngenix',
                'lswcdn':u'LeaseWeb',
                'internapcdn':u'Internap',
                'incapdns':u'Incapsula',
                'cdnsun':u'CDN SUN',
                'cdnvideo':u'CDN Video',
                'clients.turbobytes.net':u'TurboBytes',
                'clients.turbobytes.net':u'TurboBytes',
                'turbobytes-cdn.com':u'TurboBytes',
                'afxcdn.net':u'afxcdn.net',
                'akamai.net':u'Akamai',
                'akamaiedge.net':u'Akamai',
                'akadns.net':u'Akamai',
                'akamaitechnologies.com':u'Akamai',
                'gslb.tbcache.com':u'Alimama',
                'cloudfront.net':u'Amazon Cloudfront',
                'anankecdn.com.br':u'Ananke',
                'att-dsa.net':u'AT&T',
                'azioncdn.net':u'Azion',
                'belugacdn.com':u'BelugaCDN',
                'bluehatnetwork.com':u'Blue Hat Network',
                'systemcdn.net':u'EdgeCast',
                'cachefly.net':u'Cachefly',
                'cdn77.net':u'CDN77',
                'cdn77.org':u'CDN77',
                'panthercdn.com':u'CDNetworks',
                'cdngc.net':u'CDNetworks',
                'gccdn.net':u'CDNetworks',
                'gccdn.cn':u'CDNetworks',
                'cdnify.io':u'CDNify',
                'ccgslb.com':u'ChinaCache',
                'ccgslb.net':u'ChinaCache',
                'c3cache.net':u'ChinaCache',
                'chinacache.net':u'ChinaCache',
                'cncssr.chinacache.net':u'ChinaCache',
                'c3cdn.net':u'ChinaCache',
                'lxdns.com':u'ChinaNetCenter',
                'speedcdns.com':u'QUANTIL/ChinaNetCenter',
                'mwcloudcdn.com':u'QUANTIL/ChinaNetCenter',
                'cloudflare.com':u'Cloudflare',
                'cloudflare.net':u'Cloudflare',
                'edgecastcdn.net':u'EdgeCast',
                'adn.':u'EdgeCast',
                'wac.':u'EdgeCast',
                'wpc.':u'EdgeCast',
                'fastly.net':u'Fastly',
                'fastlylb.net':u'Fastly',
                'google.':u'Google',
                'googlesyndication.':u'Google',
                'youtube.':u'Google',
                'googleusercontent.com':u'Google',
                'l.doubleclick.net':u'Google',
                'hiberniacdn.com':u'Hibernia',
                'hwcdn.net':u'Highwinds',
                'incapdns.net':u'Incapsula',
                'inscname.net':u'Instartlogic',
                'insnw.net':u'Instartlogic',
                'internapcdn.net':u'Internap',
                'kxcdn.com':u'KeyCDN',
                'lswcdn.net':u'LeaseWeb CDN',
                'footprint.net':u'Level3',
                'llnwd.net':u'Limelight',
                'lldns.net':u'Limelight',
                'netdna-cdn.com':u'MaxCDN',
                'netdna-ssl.com':u'MaxCDN',
                'netdna.com':u'MaxCDN',
                'stackpathdns.com':u'StackPath',
                'mncdn.com':u'Medianova',
                'instacontent.net':u'Mirror Image',
                'mirror-image.net':u'Mirror Image',
                'cap-mii.net':u'Mirror Image',
                'rncdn1.com':u'Reflected Networks',
                'simplecdn.net':u'Simple CDN',
                'swiftcdn1.com':u'SwiftCDN',
                'swiftserve.com':u'SwiftServe',
                'gslb.taobao.com':u'Taobao',
                'cdn.bitgravity.com':u'Tata communications',
                'cdn.telefonica.com':u'Telefonica',
                'vo.msecnd.net':u'Windows Azure',
                'ay1.b.yahoo.com':u'Yahoo',
                'yimg.':u'Yahoo',
                'zenedge.net':u'Zenedge',
                'cdnsun.net.':u'CDNsun',
            }
        }


if __name__ == '__main__':
    # url = "http://www.reber-9.com"
    urlS= sys.argv[1]
    for line in open(urlS):
            url="http://www."+(line.replace("\n",""))
            line=line.replace("\n","")
            cdn = CdnCheck(url)
            cdnUsed=""
            cname=""
            
            data=cdn.check()
            print(data)
            cdnUsed=data['Status']
            
            if 'CNAME' in data: 
                print(data)
                cname=data['CNAME']                                                        
                
            if 'CNAME' not in data:
                cname='unknow'
                print(data)
            if 'CDN' in data:
                cdn.CDN=data['CDN']
            cdnData={'domain':line,'cdnUse':cdnUsed,'cname':cname,'CDN':cdn.CDN}
            with open('domainCDN.json','a+')as f:
                f.write(str(cdnData)+'\n')
            print(cdnData)