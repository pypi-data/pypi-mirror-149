import requests
import json

urlClouds = "https://api.openground.bentley.com/api/v1.0/identity/clouds"
queryUrlTemplate = "https://api.{0}.openground.bentley.com/api/v1.0/data/query"
logUrlTemplate = "https://api.{0}.openground.bentley.com/api/v1.0/reports/projects/{1}/locations/{2}/quicklog"


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
    
def query(accessToken, cloud, group, projects = [], projections = [], groupings = [], filters = [], orderings = []) :

    filterGroup = {
        "Filters": filters,
        "And": True
    }

    query = {
        "Projects": projects,
        "Projections": projections,
        "Orderings": orderings,
        "Groupings": groupings,
        "FilterGroup": filterGroup,
        "Group": group
    }
    
    results = runQuery(accessToken, cloud, query)
    
    convertedResults = []
    
    for result in results:
        
        # Dictionary per entry.
        values = dict()

        values["Id"] = result["Id"]

        # Copy entries in DataFields.
        for field in result["DataFields"]:                        
            values[field["Header"]] = field["Value"]
                                
        convertedResults.append(values)
                                   
    return convertedResults
    

def generateLog(accessToken, cloud, project, location, path) :
    cloudId = cloud["Id"]
    cloudRegion = cloud["Region"]
    
    # Prepare address and headers.
    logUrl = logUrlTemplate.format(cloudRegion, project, location)    
    headers = getHeaders(None, "application/pdf", accessToken, cloudId)                
    
    # Perform the request and stream response to file. (Assumes a 200 responses for demo purposes.)
    with requests.get(logUrl, headers = headers, stream = True) as request :
        request.raise_for_status()
        
        with open(path, 'wb') as file :
            for chunk in request.iter_content(chunk_size = 8192) :
                file.write(chunk)


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