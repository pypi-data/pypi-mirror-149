import requests
import json

urlClouds = "https://api.openground.bentley.com/api/v1.0/identity/clouds"
queryUrlTemplate = "https://api.{0}.openground.bentley.com/api/v1.0/data/query"

def getHeaders(contentType = None, accept = "*/*", accessToken = None, instanceId = None):

    # Returns standard headers which may have additional entries depending on the passed parameters.
    headers = {
        "Content-Type" : contentType,
        "User-Agent" : "openground-python-demo",
        "Accept" : accept,
        "Cache-Control" : "no-cache",
        "Accept-Encoding" : "gzip, deflate, br",
        "KeynetixCloud" : "U3VwZXJCYXRtYW5GYXN0",        
    }

    if (contentType != None):
        headers["Content-Type"] = contentType   

    if (accessToken != None):
        headers["Authorization"] = "Bearer " + accessToken
        
    if (instanceId != None):
        headers["InstanceId"] = instanceId

    return headers  

def getClouds(accessToken):

    # Query clouds for the user.
                  
    headers = getHeaders(accessToken = accessToken)
    cloudsResponse = requests.get(urlClouds, headers = headers)
    
    cloudsList = json.loads(cloudsResponse.text)
    
    return cloudsList

def getProjects(accessToken, cloud):
    
    query = {
                    
        "Projects": [],
        "Projections": [
            {
                "Group": "Project",
                "Header": "ProjectID"
            },
            {
                "Group": "Project",
                "Header": "ProjectTitle"
            }
        ],
        "Orderings": [
            {
                "Group": "Project",
                "Header": "ProjectID",
                "Ascending": "true"
            }
        ],
        "Group": "Project"

    }
           
    return runQuery(accessToken, cloud, query)

def getProjectLocations(accessToken, cloud, project) :

    # project = project instance identifier (GUID)
    
    query = {
                    
        "Projects": [ project ],
        "Projections": [
            {
                "Group": "LocationDetails",
                "Header": "LocationID"            
            },
            {
                "Group": "LocationDetails",
                "Header": "LatitudeNumeric"
            },
            {
                "Group": "LocationDetails",
                "Header": "LongitudeNumeric"
            }        
        ],
        "Orderings": [
            {
                "Group": "LocationDetails",
                "Header": "LocationID",
                "Ascending": "true"
            }
        ],
        "Group": "LocationDetails"

    }

    return runQuery(accessToken, cloud, query)

def runQuery(accessToken, cloud, query):
    # Performs a query for the specified cloud.
    cloudId = cloud["Id"]
    cloudRegion = cloud["Region"]
    
    queryUrl = queryUrlTemplate.format(cloudRegion)
        
    # Query to JSON.
    body = json.dumps(query)
    
    # POST request to /query endpoint and return response.
    headers = getHeaders("application/json", "application/json", accessToken, cloudId)                
    queryResponse = requests.post(queryUrl, headers = headers, data = body)    
       
    result = json.loads(queryResponse.text)
    
    return result