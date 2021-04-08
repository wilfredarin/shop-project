import csv
import requests
import time


# api
api_nearest_road ="" 
api_gecoding = ""




#file structure of cornershop.csn
# outlet_lat | outlet_lon | is_corner
OutletMasterfile = "../Outlet_Master.csv"
APIOutputfile = "../API_Output.csv"


def getOutputData():
	data = []
	with open(APIOutputfile,"r") as API_Output:
		API_Output = csv.reader(API_Output)
		data.append(next(API_Output))
		for line in API_Output:
			# print(line)
			data.append(line)
	return data

def getResult():
	global OutletMasterfile
	output_data = []
	print("Reading outlet data.....")
	with open(OutletMasterfile,"r") as OutletMasterfile:
		OutletMasterfile = csv.reader(OutletMasterfile)
		fields = next(OutletMasterfile)
		for line in OutletMasterfile:
			outlet_lat = float(line[2])
			outlet_lon = float(line[3])
			time.sleep(1)
			output_data.append([outlet_lat,outlet_lon,isCorner(outlet_lat,outlet_lon)])
	return output_data

def writeData(APIOutputfile,fields,data):
	with open(APIOutputfile,'w') as filename:
		filename = csv.writer(filename)
		filename.writerow(fields)
		filename.writerows(data)
def main():

	output_data = getOutputData()
	output_data_fields = output_data[0]
	output_data = output_data[1:]

	result = getResult()
	print(result)
	print(output_data)
	for i in range(len(result)):
		if  len(output_data)<len(result):
			print("no")
			output_data.append(["","",result[i][1],result[i][1],"","",result[i][2]])
		else:
			print("notje")
			output_data[i][7] = result[i][2]
			
			
	writeData(APIOutputfile,output_data_fields,output_data)


def isCorner(lat,lon):
	#meters to move in four directions	
	distance = 10
	cord1 = [float(lat)+getDegrees(distance),lon]
	cord2 = [float(lat)-getDegrees(distance),lon]
	cord3 = [lat,float(lon)+getDegrees(distance)]
	cord4 = [lat,float(lon)-getDegrees(distance)]
	points = [cord1,cord2,cord3,cord4]
	roads = []
	for i in range(4):
		poss = points[i]
		lat = poss[0]
		lon = poss[1]
		road = getNearestRoads(lat,lon)
		if road and road not in roads:
			roads.append(road)
	if len(roads)>1:
		return True
	return False
	

def requestData(url):
	req = requests.get(url=url)
	response = req.json()
	return response
	

def getNearestRoads(lat,lon):
	url_nearest_road = "https://roads.googleapis.com/v1/nearestRoads?points="+str(lat)+","+str(lon)+"&key="+api_nearest_road
	response = requestData(url_nearest_road)
	if response:
		#we are getting place id of just one road 
		#if its two way there will be two place id's and but same name so we'll pick only first placeid 
		return response['snappedPoints'][0]['placeId']
	return False
		

def getRoadName(place_id):
	url_geocode = "https://maps.googleapis.com/maps/api/geocode/json?place_id="+place_id+"&key="+api_gecoding;
	response  = requestData(url_geocode)
	return response['results'][0]['formatted_address']


def getDegrees(meters):
	return  meters*0.0000090909;

main()

