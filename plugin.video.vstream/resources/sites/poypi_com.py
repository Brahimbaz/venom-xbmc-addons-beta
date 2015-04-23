#-*- coding: utf-8 -*-
#Venom.
from resources.lib.gui.hoster import cHosterGui #system de recherche pour l'hote
from resources.lib.handler.hosterHandler import cHosterHandler #system de recherche pour l'hote
from resources.lib.gui.gui import cGui #system d'affichage pour xbmc
from resources.lib.gui.guiElement import cGuiElement #system d'affichage pour xbmc
from resources.lib.handler.inputParameterHandler import cInputParameterHandler #entrer des parametres
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler #sortis des parametres
from resources.lib.handler.requestHandler import cRequestHandler #requete url
from resources.lib.config import cConfig #config
from resources.lib.parser import cParser #recherche de code
from resources.lib.util import cUtil
import urllib2,urllib,re
import xbmcgui
import unicodedata,htmlentitydefs
 
 
SITE_IDENTIFIER = 'poypi_com'
SITE_NAME = 'Poypi.com'
SITE_DESC = 'Film en streaming'
 
#pour tous
ACCEUILPATTERN  = ''#non utilisé
FILMPATTERN = '<div class="article-content"><p style="text-align: center;"><img src="(.+?)" border.+?histoire.+?center;">(.+?)<\/p>'
#pour Poypi
URL_MAIN = 'http://www.poypi.com/rgc/'
SEARCHPATTERN = '<fieldset><div><a href="\/rgc\/(.+?)">(.+?)<\/a><\/div><\/fieldset>'
NORMALPATTERN = '<span style="list-style-type:none;" >.+? href="\/rgc\/(.+?)">(.+?)<\/a><\/span>'
NEXTPAGEPATTERN = '<span class="pagenav">[0-9]+<.span><.li><li><a title=".+?" href="\/rgc\/(.+?)" class="pagenav">'
FRAMEPATTERN = '<iframe src="\/rgc\/(.+?)" width='
# #pour zopap
# URL_MAIN = 'http://www.zopap.com/paq/'
# SEARCHPATTERN = '<fieldset><div><a href="\/paq\/(.+?)">(.+?)<\/a><\/div><\/fieldset>'
# NORMALPATTERN = '<span style="list-style-type:none;" >.+? href="\/paq\/(.+?)">(.+?)<\/a><\/span>'
# NEXTPAGEPATTERN = '<span class="pagenav">[0-9]+<.span><.li><li><a title=".+?" href="\/paq\/(.+?)" class="pagenav">'
# FRAMEPATTERN = '<iframe src="\/paq\/(.+?)" width='
# #pour zaloux
# URL_MAIN = 'http://www.zaloux.com/glpl/'
# SEARCHPATTERN = '<fieldset><div><a href="\/glpl\/(.+?)">(.+?)<\/a><\/div><\/fieldset>'
# NORMALPATTERN = '<span style="list-style-type:none;" >.+? href="\/glpl\/(.+?)">(.+?)<\/a><\/span>'
# NEXTPAGEPATTERN = '<span class="pagenav">[0-9]+<.span><.li><li><a title=".+?" href="\/glpl\/(.+?)" class="pagenav">'  
# FRAMEPATTERN = '<iframe src="\/glpl\/(.+?)" width='
 
 
#pour l'addon
MOVIE_NEWS = (URL_MAIN, 'showMovies')
MOVIE_GENRES = (True, 'showGenre') 
URL_SEARCH = (URL_MAIN + 'index.php?ordering=&searchphrase=all&Itemid=1&option=com_search&searchword=', 'showMovies')
FUNCTION_SEARCH = 'showMovies'
 
 
def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)
 
 
def load():
    oGui = cGui()
 
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films Nouveaute', 'films.png', oOutputParameterHandler)
   
    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, 'showGenre', 'Films Genres', 'genres.png', oOutputParameterHandler)
           
    oGui.setEndOfDirectory()
 
def showSearch():
    oGui = cGui()
 
    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = URL_MAIN + 'index.php?ordering=&searchphrase=all&Itemid=1&option=com_search&searchword=' + sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return  
   
   
def showGenre():
    oGui = cGui()

    liste = []
    liste.append( ['Action',URL_MAIN + 'index.php?option=com_content&view=category&id=1'] )
    liste.append( ['Aventure',URL_MAIN + 'index.php?option=com_content&view=category&id=4'] )
    liste.append( ['Comedie',URL_MAIN + 'index.php?option=com_content&view=category&id=6'] )
    liste.append( ['Drame',URL_MAIN + 'index.php?option=com_content&view=category&id=7'] )
    liste.append( ['Epouvante Horreur',URL_MAIN + 'index.php?option=com_content&view=category&id=9'] ) 
    liste.append( ['Fantastique',URL_MAIN + 'index.php?option=com_content&view=category&id=8'] )  
    liste.append( ['Policier',URL_MAIN + 'index.php?option=com_content&view=category&id=10'] )
    liste.append( ['Science Fiction',URL_MAIN + 'index.php?option=com_content&view=category&id=11'] )
    liste.append( ['Thriller',URL_MAIN + 'index.php?option=com_content&view=category&id=12'] )
    liste.append( ['Animation',URL_MAIN + 'index.php?option=com_content&view=category&id=2'] )
    liste.append( ['Documentaires',URL_MAIN + 'index.php?option=com_content&view=category&id=26'] )  
    liste.append( ['Spectacle',URL_MAIN + 'index.php?option=com_content&view=category&id=3'] ) 
                
    for sTitle,sUrl in liste:
        
        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)
       
    oGui.setEndOfDirectory() 
 
def showMovies(sSearch = ''):
    oGui = cGui()
 
    if sSearch :
        sUrl = sSearch
        sPattern = SEARCHPATTERN
    else :
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')
        sPattern = NORMALPATTERN
        # if (sUrl == URL_MAIN) :
            # sPattern = NORMALPATTERN
        # else:
            # sPattern = NORMALPATTERN
   
    #print sUrl
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
   
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
   
    #print aResult
   
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
       
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
           
            sTitle2 = aEntry[1]
            sUrl2 = aEntry[0]
           
            #not found better way
            #sTitle = unicode(sTitle, errors='replace')
            #sTitle = sTitle.encode('ascii', 'ignore').decode('ascii')
           
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', str(URL_MAIN) + str(sUrl2))
            oOutputParameterHandler.addParameter('sMovieTitle', str(sTitle2))
 
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sTitle2, '', '', '', oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
           
        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addDir(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', 'next.png', oOutputParameterHandler)
            #Ajoute une entrer pour le lien Next | pas de addMisc pas de poster et de description inutile donc
 
    if not sSearch:
        oGui.setEndOfDirectory()
   
def __checkForNextPage(sHtmlContent):
    sPattern = NEXTPAGEPATTERN
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return str(URL_MAIN) + aResult[1][0]
 
    return False
 
def showHosters():
    oGui = cGui()
   
    sLink = ''
    sThumb = ''
    sComm = ''
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
   
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
   
    oParser = cParser()
    sPattern = FILMPATTERN
    aResult = oParser.parse(sHtmlContent, sPattern)
       
    sThumb = aResult[1][0][0]
    sComm = unescape(aResult[1][0][1])
 
    #sPattern = 'proxy.link=(.+?)&autostart=true'
    #aResult = oParser.parse(sHtmlContent, sPattern)
 
    sHtmlContent = sHtmlContent.replace('\r','')
   
    sPattern = 'class="jwts_tabbertab" title="(.+?)">.+?' + FRAMEPATTERN
    aResult = oParser.parse(sHtmlContent, sPattern)
 
    #Si il n'a pas de selection de qualitee
    if (aResult[0] == False):
        sPattern = FRAMEPATTERN
        aResult = oParser.parse(sHtmlContent, sPattern)
 
        if (aResult[0] == True):
            print aResult[1][0]
            aResult[1][0] = ('???',aResult[1][0])
 
    if (aResult[0] == True):
        total = len(aResult[1])
        dialog = cConfig().createDialog(SITE_NAME)
       
        for aEntry in aResult[1]:
            cConfig().updateDialog(dialog, total)
            if dialog.iscanceled():
                break
           
            sLink = str(URL_MAIN) + urllib.unquote(aEntry[1]).decode('utf8')
           
            Squality = str(aEntry[0])
           
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sLink)
            oOutputParameterHandler.addParameter('sMovieTitle', sMovieTitle)
 
            oGui.addMovie(SITE_IDENTIFIER, 'showHostersLink', '[COLOR teal][' + Squality + '][/COLOR] ' + sMovieTitle, sThumb, sThumb, sComm, oOutputParameterHandler)
 
        cConfig().finishDialog(dialog)
       
    oGui.setEndOfDirectory()
   
def showHostersLink():
    #En fait ici, tout leur lien sont sur le meme hebergeur d'ou le lien deja traduit
    oGui = cGui()
   
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')  
   
    #recuperation urls
    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
   
    #fh = open('c:\\test.txt', "w")
    #fh.write(sHtmlContent)
    #fh.close()
   
    url = re.findall('"file":"(.+?)", "label":"(.+?)",', sHtmlContent)
   
    #dialogue final
   
    if (url):
        for aEntry in url:
 
            sTitle = '[COLOR teal][' + str(aEntry[1]) + '][/COLOR] ' + sMovieTitle
            sUrl = aEntry[0]
 
            sHosterUrl = str(sUrl)
            oHoster = cHosterGui().checkHoster(sHosterUrl)
           
            if (oHoster != False):
                oHoster.setDisplayName(sTitle)
                oHoster.setFileName(sTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, '')
           
        oGui.setEndOfDirectory()
      
