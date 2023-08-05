import requests
import datetime

def downloadAnnotations(url, token, classname, verify=True, timeout=60):
    ''' 
    url : IoT.own Server Address
    token : IoT.own API Token
    classname : Image Class ex) car, person, airplain
    '''
    apiaddr = url + "/api/v1.0/nn/images?labels=" + classname
    header = {'Accept':'application/json', 'token':token}
    try:
        r = requests.get(apiaddr, headers=header, verify=verify, timeout=timeout)
        if r.status_code == 200:
            return r.json()
        else:
            print(r)
            return None
    except Exception as e:
        print(e)
        return None

def storage(url, token, nid, date_from , date_to, lastKey="", group_id=None, verify=True, timeout=60):
    '''
    url : IoT.own Server Address
    token : IoT.own API Token
    nid : Node ID
    date_from : UTC string ex) "2018-11-02T13:00:00Z" 
    '''
                    
    header = {'Accept':'application/json','token':token}

    # only for administrators
    if group_id is not None:
        header['grpid'] = group_id

    apiaddr = url + "/api/v1.0/storage?nid=" + nid + "&from=" + date_from + "&to=" + date_to
    result = None
    
    while True:
        try:
            uri = apiaddr if lastKey == "" else apiaddr + "&lastKey=" + lastKey
            r = requests.get(uri, headers=header, verify=verify, timeout=timeout)
        except Exception as e:
            print(e)
            return None
    
        if r.status_code == 200:
            if result is None:
                result = r.json()
                if 'lastKey' in result.keys():
                    del result['lastKey']
            else:
                result['data'] += r.json()['data']

            if 'lastKey' in r.json().keys():
                lastKey = r.json()['lastKey']
                print(f"lastKey:{lastKey}, #Received:{len(result['data'])}")
            else:
                print(f"#TotalReceived:{len(result['data'])}")
                return result
        else:
            print(r)
            return None
def downloadImage(url, token, imageID, verify=True, timeout=60):
    ''' 
    url : IoT.own Server Address
    token : IoT.own API Token
    imageID : IoT.own imageID ( using annotation's 'id' not '_id' ) 
    '''
    apiaddr = url + "/nn/dataset/img/" + imageID
    header = {'Accept':'application/json', 'token':token}
    try:
        r = requests.get(apiaddr, headers=header, verify=verify, timeout=timeout)
        if r.status_code == 200:
            return r.content
        else:
            print(r)
            return None
    except Exception as e:
        print(e)
        return None
