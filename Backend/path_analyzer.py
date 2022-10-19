import os

class PathAnalyzer:
    rev_indicators = ['REV', '_R', ' R']

    def findDwgNumPath(folderpath):
        basename = os.path.splitext(folderpath)[0]
        for rev_tag in PathAnalyzer.rev_indicators:
            basename = basename.replace(rev_tag.upper(),' ')
            basename = basename.replace(rev_tag.lower(),' ')
        basename = basename.split(' ')[0]
        return PathAnalyzer.number_finder(basename)

    def findSubstationPath(folderaddress):
        if "SUBSTATION" not in folderaddress: return ''
        try:
            path_elements = (folderaddress.upper()).split('\\')
            sub_index = path_elements.index('SUBSTATION')+1
            if path_elements[sub_index] == 'COMPLETED PROJECTS': sub_index+=1
            return (path_elements[sub_index].replace('SUBSTATION', '')).strip()
        except: return ''

    def findJobOrderPath(folderaddress):
        if 'JO' not in folderaddress: return ''
        return PathAnalyzer.number_finder(folderaddress,'JO')

    def findRevPath(folderpath):
        base=os.path.basename(folderpath)
        rtext=(os.path.splitext(base)[0]).upper()
        rt = '1'
        for revi in PathAnalyzer.rev_indicators:
            if revi in rtext: 
                rt = PathAnalyzer.number_finder(rtext, revi)
                break
        if rt == '': rt='1'
        return rt

    def findSheetPath(folderpath):
        base=os.path.basename(folderpath)
        stext=(os.path.splitext(base)[0]).upper()
        sheet_indicators = ['_SHEET','SHEET', '_S', ' SH']
        st = ''
        for shi in sheet_indicators:
            if shi in stext: 
                st = PathAnalyzer.number_finder(stext, shi)
                break
        return st

    def number_finder(basename, separator = None):
        if separator!=None: basename = basename.split(separator)[1]
        ntext = ''
        for n in basename:
            if not PathAnalyzer.is_int(n):
                if ntext != '': break
                continue
            ntext += n
        return ntext

    def is_int(number):
        try: 
            int(number)
            return True
        except: return False

if __name__ == '__main__':
    example_file = 'G:\PGE\SUBSTATION\COMPLETED PROJECTS\METCALF SUBSTATION\Metcalf-2008\ref download\111708\934-004.met'
    print(PathAnalyzer.findSubstationPath(example_file))

    