from datetime import datetime

def search_algorithm(dataset, searchtext, skipfields=[]):
    searchtext=searchtext.upper()
    searcharray=searchtext.split()
    if not searcharray: return False

    searchresults=[]
    hitlist=[]
    #creates hitlimit for searching
    #purpose of hitlimit is to shorten the result list
    hitlimit=0
    for i in searcharray: 
        if i!="": hitlimit+=1
    
    #keeps hitlimit from being too large so we are able to get a favorable size of results
    if hitlimit>1:  hitlimit-=1
    else:           hitlimit=0

    for dataindex in range(len(dataset)):
        datapoint = dataset[dataindex]
        hits=0

        for searchkey in searcharray:
            for idx, data in enumerate(datapoint):
                if idx in skipfields: continue
                if searchkey in str(data).upper(): hits+=1

        if hits>hitlimit: hitlist.append([datapoint,hits])
    
    #sorts from high number of hits to low hits
    hitlist=sorted(hitlist,key=lambda tup:tup[1],reverse=True)
    for hitdata in hitlist: searchresults.append(hitdata[0])
    return searchresults

def sortResults(sortby, dataset):
    if sortby=='-----':
        dataset.sort(key=lambda i: i[10], reverse=True)
    else:
        if 'date' in sortby.lower():
            dataset.sort(key=lambda i: datetime.strptime(i[6], "%m%d%y"), reverse=True)
    return dataset
