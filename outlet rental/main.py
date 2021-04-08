import csv
from math import radians, cos, sin, asin, sqrt	

#file strucutre
OutletRentalfile = 'Outlet_Rental.csv'
lat_col,lon_col,rate_col,complex_col = 6,7,10,4 

OutletMasterfile = "../Outlet_Master.csv"
#Outlet ID	Outlet Name	Latitude 	Longitude	Premiumness	Office Area	PoI?	Junction

#Outlet ID,Outlet Name,Latitude ,Longitude,Premiumness,Office Area,PoI?,Junction

APIOutputfile = "../API_Output.csv"

average_rental = 76
def getOutputData():
	data = []
	with open(APIOutputfile,"r") as API_Output:
		API_Output = csv.reader(API_Output)
		data.append(next(API_Output))
		for line in API_Output:
			# print(line)
			data.append(line)
	return data

def getDegrees(dist):
	return dist*0.0000090909

def isInsideSquare(lat,lon,outlet_lat,outlet_lon,dist=500):
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
		if lon<lon_east_bound and lon>lon_west_bound:
			return True
	return False








def main():

	#lat,lon,prem
	result_data = getResult()
	# print(result_data)
	output_file_data = getOutputData()
	# print(output_data)
	output_file_data_fileds = output_file_data[0]
	print(output_file_data_fileds)
	output_file_data = output_file_data[1:]
	print(output_file_data)
	for i in range(len(result_data)):
		if len(output_file_data)<len(result_data):
			output_file_data.append(["","",result_data[i][0],result_data[i][1],result_data[i][2],"","","",""])
		else:
			output_file_data[i][4] = result_data[i][2]	
	with open(APIOutputfile,"w") as API_Output:
		API_Output = csv.writer(API_Output)
		API_Output.writerow(output_file_data_fileds)
		API_Output.writerows(output_file_data)







def getResult():
	global OutletMasterfile
	output_data = []
	with open(OutletMasterfile,"r") as OutletMasterfile:
		OutletMasterfile = csv.reader(OutletMasterfile)
		fields = next(OutletMasterfile)
		for line in OutletMasterfile:
			outlet_lat = float(line[2])
			outlet_lon = float(line[3])
			output_data.append([outlet_lat,outlet_lon,getScore(outlet_lat,outlet_lon)])	
	return output_data		
def getScore(outlet_lat,outlet_lon):
	global OutletRentalfile
	with open(OutletRentalfile,"r") as csvfile:
		csvreader = csv.reader(csvfile)
		fields = next(csvreader)
		min_distance = float('inf')
		price = 0
		# complex_name = ""

		#No Rental detail in vicinity : if flag is true
		data_insuf_flag = True

		for row in csvreader:
			lat = float(row[lat_col])
			lon = float(row[lon_col])
			if isInsideSquare(lat,lon,outlet_lat,outlet_lon):
					cur_distance = findDistance(lat,lon,outlet_lat,outlet_lon)
					if cur_distance<min_distance:
						min_distance = cur_distance
						price = row[rate_col]
						complex_name = row[complex_col]
					data_insuf_flag = False
		score = "Data Not Avaialable"
		if data_insuf_flag:
			return score
		else:
			price = int(price)
			if  price >= 4*average_rental:
				score = 20 
			elif price >=2*average_rental:
				score = 15
			elif price >= average_rental:
				score = 10
			else:
				score = 6
		return score






def findDistance(lat1,lon1, lat2, lon2):
	# The math module contains a function named
	# radians which converts from degrees to radians.
	lon1 = radians(lon1)
	lon2 = radians(lon2)
	lat1 = radians(lat1)
	lat2 = radians(lat2)
	# Haversine formula
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * asin(sqrt(a))
	# Radius of earth in kilometers. Use 3956 for miles
	r = 6371
	# calculate the result in meters
	return int(c * r*1000)

main()
