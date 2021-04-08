import csv
import requests


#enter api key

api_distanceMatrix = "" 

#set search distance in meters 
dist = 1000

#set poi max allowed distance from outlet
lower_dist = upper_dist = 100

#file strucutre
# poi_file = 'poi.csv' poi_name = 2 lat_col = 3 lon_col = 4 type_col = 9

OutletMasterfile = "../Outlet_Master.csv"
APIOutputfile = "../API_Output.csv"
def writeData(APIOutputfile,fields,data):
	with open(APIOutputfile,'w') as filename:
		filename = csv.writer(filename)
		filename.writerow(fields)
		filename.writerows(data)
	 
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
	with open(OutletMasterfile,"r") as OutletMasterfile:
		OutletMasterfile = csv.reader(OutletMasterfile)
		fields = next(OutletMasterfile)
		for line in OutletMasterfile:
			outlet_lat = float(line[2])
			outlet_lon = float(line[3])
			output_data.append([outlet_lat,outlet_lon,isPoi(outlet_lat,outlet_lon)])
	return output_data		
def main():
	data = getOutputData()
	output_fields = data[0]
	output_data = data[1:]
	result = getResult()
	print(result)
	for i in range(len(result)):
		print(output_data,len(output_data))
		if  len(output_data)<len(result):
			print("no")
			output_data.append(["","",result[i][0],result[i][1],"",result[i][2][0],result[i][2][1],"",""])
		else:
			print("notje")
			output_data[i][5] = result[i][2][0]
			output_data[i][6] = result[i][2][1]	
			
	writeData(APIOutputfile,output_fields,output_data)

def isInsideSquare(dist,lat,lon,outlet_lat,outlet_lon):
	#point in mid  <---  . ---->
	lat = float(lat)
	lon = float(lon)
	sq_len = dist/2  
	move_degree = 0.0000090909*sq_len
	
	lon_west_bound = float(outlet_lon)-move_degree;
	lon_east_bound = float(outlet_lon)+move_degree;
	
	lat_north_bound = float(outlet_lat)+ move_degree;
	lat_south_bound = float(outlet_lat)- move_degree;

	if lat<lat_north_bound and lat>lat_south_bound:
		# print("hiiii")
		if lon<lon_east_bound and lon>lon_west_bound:
			return True
	return False

	 


def isType1(givenType):
	if givenType in ["hotel","shopping_mall","train_station","bus_station"]:
		return True
	return False

def isType2(givenType):
	if givenType in ["corporate_office","corporate_campus"]:
		return True
	return False



def isPoi(outlet_lat,outlet_lon):
	poifile = "poi_data.csv"
	type1Flag = False
	type2Flag = False	
	origin = str(outlet_lat)+","+str(outlet_lon)
	url_begin ="https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins="
	destination = ""
	with open(poifile,"r") as poifile:
		poifile = csv.reader(poifile)
		fields = next(poifile)
		# print(fields)
		destinationType1 = ""
		destinationType2 = ""
		for line in poifile:
			lat = float(line[3])
			lon = float(line[4])
			givenType = line[9]
			if isInsideSquare(15000,lat,lon,outlet_lat,outlet_lon):
				if isType1(givenType):
					if destinationType1 == "":
						destinationType1 +=str(lat)+"%2C"+str(lon)
					else:
						destinationType1+="%7C"+str(lat)+"%2C"+str(lon)
				if isType2(givenType):
					if destinationType2 == "":
						destinationType2 +=str(lat)+"%2C"+str(lon)
					else:
						destinationType2+="%7C"+str(lat)+"%2C"+str(lon)
	if destinationType1:
		url =  url_begin + origin+"&destinations="+destinationType1+"&key="+api_distanceMatrix
		response1 = requestData(url)
		type1Flag = getTravelDistance(response1,lower_dist,upper_dist)
	if destinationType2:
		url =  url_begin + origin+"&destinations="+destinationType2+"&key="+api_distanceMatrix
		response2 = requestData(url)
		type2Flag=getTravelDistance(response2,lower_dist,upper_dist)
	return [type1Flag,type2Flag]

	
def requestData(url):
	req = requests.get(url=url)
	return req.json()

def getTravelDistance(response,lower_dist,upper_dist):
	if response['status']=="OK":
		places = response['rows'][0]['elements']
		min_dist = float("inf")
		for i in range(len(places)):
			min_dist = min(min_dist,places[i]['distance']['value'])
		print("Min Distance from POI is : ",min_dist,"meters")
		if min_dist<=lower_dist:
			print("$$$$$  Passed POI  $$$$$")
			return True
		elif min_dist>lower_dist and min_dist<upper_dist:
			print("!!!!  Manual Intervention Required   !!!!!")
			return True
		else:
			print("XXXXX Failed POI  XXXXX")
			return False
	else:
		print("XXXXX Failed POI XXXXX")
		return False


main()