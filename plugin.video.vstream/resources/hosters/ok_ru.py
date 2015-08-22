from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.config import cConfig
from resources.hosters.hoster import iHoster
import re,urllib2, urllib
import xbmcgui
import time
import random

class cHoster(iHoster):

    def __init__(self):
        self.__sDisplayName = 'Ok.ru'
        self.__sFileName = self.__sDisplayName
        self.__sHD = ''

    def getDisplayName(self):
        return  self.__sDisplayName

    def setDisplayName(self, sDisplayName):
        self.__sDisplayName = sDisplayName + ' [COLOR skyblue]'+self.__sDisplayName+'[/COLOR] [COLOR khaki]'+self.__sHD+'[/COLOR]'

    def setFileName(self, sFileName):
        self.__sFileName = sFileName

    def getFileName(self):
        return self.__sFileName

    def getPluginIdentifier(self):
        return 'ok_ru'

    def setHD(self, sHD):
        self.__sHD = ''

    def getHD(self):
        return self.__sHD

    def isDownloadable(self):
        return True

    def isJDownloaderable(self):
        return True

    def getPattern(self):
        return '';
        
    def getHostAndIdFromUrl(self, sUrl):
        sPattern = 'http:\/\/((?:(?:ok)|(?:odnoklassniki))\.ru)\/.+?\/([0-9]+)'
        oParser = cParser()
        aResult = oParser.parse(sUrl, sPattern)
        if (aResult[0] == True):
            return aResult[1][0]
        return ''

    def setUrl(self, sUrl):
        self.__sUrl = str(sUrl)

    def checkUrl(self, sUrl):
        return True

    def __getUrl(self, media_id):
        return ''

    def getMediaLink(self):
        return self.__getMediaLinkForGuest()

    def __getMediaLinkForGuest(self):

        v = self.getHostAndIdFromUrl(self.__sUrl)
        sId = v[1]
        sHost = v[0]
        web_url = 'http://' + sHost + '/dk?cmd=videoPlayerMetadata&mid=' + sId
        
        #bidouille en plus
        a = int(time.time())
        b = random.random()
        web_url = web_url + '&rnd=' + str(a) + str(b)
        
        #print web_url
        
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0'
        headers = {'User-Agent': UA ,
                   'Host' : sHost,
                   #'Referer': 'http://www.voirfilms.org/batman-unlimited-monstrueuse-pagaille.htm',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Content-Type': 'text/html; charset=utf-8'}
        
        #oRequest = cRequestHandler(web_url)
        #sHtmlContent = oRequest.request()
        
        req = urllib2.Request( 'http://ok.ru/video/' + str(sId),None,headers)
        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError, e:
            print e.read()
            print e.reason
        
        print web_url
        

        
        req = urllib2.Request(web_url,None,headers)
        try:
            response = urllib2.urlopen(req)
        except urllib2.URLError, e:
            print e.read()
            print e.reason
            
        sHtmlContent = response.read()
        response.close()
        
        sHtmlContent = sHtmlContent.decode('unicode-escape')
        sHtmlContent = sHtmlContent.encode("utf-8")
        
        sPattern = '"name":"([^"]+?)","url":"(.+?)"'
        oParser = cParser()
        aResult = oParser.parse(sHtmlContent, sPattern)
        
        #print aResult
        
        api_call = False

        if (aResult[0] == True):
            #initialisation des tableaux
            url=[]
            qua=[]
            
            #Replissage des tableaux
            for i in aResult[1]:
                url.append(str(i[1]))
                qua.append(str(i[0]))
                
            #Si au moins 1 url
            if (url):
            #Afichage du tableau
                dialog2 = xbmcgui.Dialog()
                ret = dialog2.select('Select Quality',qua)
                if (ret > -1):
                    api_call = url[ret]
                    
        
        #time.sleep( 5 )        
                    
        print api_call
        #api_call = 'http://217.20.157.207/?sig=1840c53829262bb9b14d50010b73f1722d2ec7e4&ct=0&expires=1439657212454&clientType=0&id=51659082303&type=1'
        
        UA = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'
        api_call = api_call + '|User-Agent=' + UA
        
        if (api_call):
            return True,api_call
            
        return False, False

        
#http://www.tubeoffline.com/download-Odnoklassniki-videos.php#.Vc4giJf-QZQ

