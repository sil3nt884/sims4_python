version = '2.0beta'
class ErrorHandler:

    def error(self, exception):
        raise exception

    def fatalError(self, exception):
        raise exception

    def warning(self, exception):
        print(exception)

class ContentHandler:

    def __init__(self):
        self._locator = None

    def setDocumentLocator(self, locator):
        self._locator = locator

    def startDocument(self):
        pass

    def endDocument(self):
        pass

    def startPrefixMapping(self, prefix, uri):
        pass

    def endPrefixMapping(self, prefix):
        pass

    def startElement(self, name, attrs):
        pass

    def endElement(self, name):
        pass

    def startElementNS(self, name, qname, attrs):
        pass

    def endElementNS(self, name, qname):
        pass

    def characters(self, content):
        pass

    def ignorableWhitespace(self, whitespace):
        pass

    def processingInstruction(self, target, data):
        pass

    def skippedEntity(self, name):
        pass

class DTDHandler:

    def notationDecl(self, name, publicId, systemId):
        pass

    def unparsedEntityDecl(self, name, publicId, systemId, ndata):
        pass

class EntityResolver:

    def resolveEntity(self, publicId, systemId):
        return systemId
