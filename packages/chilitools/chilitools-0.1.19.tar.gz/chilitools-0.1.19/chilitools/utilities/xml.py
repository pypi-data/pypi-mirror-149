from chilitools.utilities.errors import ErrorHandler
from xml.etree.ElementTree import Element, SubElement, tostring

def unescapeXML(xml: str) -> str:
    from xml.sax.saxutils import unescape
    return unescape(xml)

def parseXML(xml: str):
    import xmltodict
    return xmltodict.parse(xml)

def createDatasourceXML(dataSourceID: str, data: list[dict]) -> str:
    numChildren = len(data)
    root = Element('dataSource', {'dataSourceID':dataSourceID, 'hasContent':'true', 'numRows':str(numChildren)})
    for r in range(numChildren):
        row = SubElement(root, 'row', {'rowNum':str(r+1)})
        c = 1
        for key, value in data[r].items():
            col = SubElement(row, 'col'+str(c), {'varName':key})
            col.text = str(value)
            c += 1
    return tostring(root, encoding='unicode')

def taskWasSuccessfull(task) -> bool:
    if task['task']['@succeeded'] == "True":
        return True
    return False

def getTaskResultURL(task) -> str:
    if taskWasSuccessfull(task=task):
        result = task['task']['@result']
        result = unescapeXML(result)
        result = parseXML(result)
        return result['result']['@url']
    return ErrorHandler().getError(errorName="TASKNOTSUCCEEDED")