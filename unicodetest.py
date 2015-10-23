#! *-* coding:utf-8 *-*
import chardet

def _smartcode(stream):
    """smart recove stram into UTF-8"""

    ustring = stream
##    codedetect = chardet.detect(ustring)["encoding"]
##    print(codetect)

    try:
##        print(ustring)
##        ustring = unicode(ustring,codedetect)
##        print(ustring)
        return "{}{}".format("",ustring.encode('utf-8'))
    except:
        return u"bad unicode encode try!"

if __name__ == "__main__":
    _smartcode('世界大同.html')
