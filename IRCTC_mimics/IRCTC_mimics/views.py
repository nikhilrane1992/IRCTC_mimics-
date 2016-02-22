from models import UserDetail, Train, Station, DepartureDay, Reservation
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
import json
import re
import datetime

def validate_mobile(value):
	rule = re.compile(r'^(\+91[\-\s]?)?[0]?[1789]\d{9}$')
	if not rule.search(value):
		return False
	else:
		return value

def generate_prn_number(qry):
	currentDate = datetime.datetime.today().strftime('%d%m%Y')
	pnrNo = '10'+str(currentDate)+'{0:0{width}}'.format(qry.id, width=8)
	return pnrNo

def getCoachNo(train):
	## get seat availablity and return coach birth and seat no
	obj = {"coach": "5S", "seatNo": 25, "birth": "UPPER"}
	return obj

## search train on travel date, source, destination
def searchTrain(request):
	if request.user.is_authenticated():
		jsonObj = json.loads(request.body)
		travelDate = jsonObj['travelDate']
		source = jsonObj['source']
		destination = jsonObj['destination']

		kwargs = {}

		print source, destination, travelDate

		if len(source) != 0 or len(destination) != 0:
			kwargs['station__stationName__iexact'] = source.strip()
			kwargs['station__stationName__iexact'] = destination.strip()
			travelDate = datetime.datetime.fromtimestamp(travelDate/1000)
			weekday = travelDate.weekday()
			kwargs['departureday__depDay'] = weekday
		else:
			return HttpResponse(json.dumps({"validation": "Invalid parameter..!!", "status": False}), content_type = "application/json")

		trains = Train.objects.filter(**kwargs)
		print trains
		trainList = []
		for i in trains:
			sourceStation = Station.objects.get(train=i, stationName__iexact=source.strip())
			destinationStation = Station.objects.get(train=i, stationName__iexact=destination.strip())
			obj = {"trainNo": i.trainNo, "trainName": i.trainName, "sourceArrivalTime": sourceStation.arrivalTime.strftime('%I:%M %p'), "sourceDepartureTime": sourceStation.departureTime.strftime('%I:%M %p'), 
			"destinationArrivalTime": destinationStation.arrivalTime.strftime('%I:%M %p'), "destinationDepartureTime": destinationStation.departureTime.strftime('%I:%M %p'), "travelDate": travelDate.strftime('%b-%d-%Y'),
			"source": source.strip(), "destination": destination.strip()}
			trainList.append(obj)
		return HttpResponse(json.dumps({"trainList": trainList,"status":True}), content_type="application/json")
	else:
		return HttpResponse(json.dumps({"validation":"You are not logged in.Please login first.","status":False}), content_type="application/json")


## create view for seat reservation
@transaction.atomic
def seatReservation(request):
	if request.user.is_authenticated():
		jsonObj = json.loads(request.body)
		user = UserDetail.objects.get(user__id=request.user.id)
		
		if jsonObj['mobileNo'] != None:
			mobileNo = validate_mobile(str(jsonObj['mobileNo']))
			if mobileNo == False:
				return HttpResponse(json.dumps({"validation": "Invalid mobile number..!!", "status": False}), content_type = "application/json")
		else:
			return HttpResponse(json.dumps({"validation": "Enter mobile number..!!", "status": False}), content_type = "application/json")

		journeyDate = datetime.datetime.fromtimestamp(jsonObj['journeyDate']/1000)

		reservationQry = Reservation(firstName=jsonObj['firstName'], lastName=jsonObj['lastName'], age=jsonObj['age'], gender= jsonObj['genderId'],addressLine1=jsonObj['addressLine1'], addressLine2 = jsonObj['addressLine2'], 
			state=jsonObj['state'], city=jsonObj['city'], pinNo=jsonObj['pinNo'], mobileNo=mobileNo, journeyDate=journeyDate)

		reservationQry.userDetail = user
		train = Train.objects.get(id=jsonObj['trainId'])
		reservationQry.train = train
		reservationQry.coachAndSeatNo = json.dumps(getCoachNo(train))
		origin = Station.objects.get(id=jsonObj['originId'])
		destination = Station.objects.get(id=jsonObj['destinationId'])
		reservationQry.source = origin
		reservationQry.destination = destination
		pnrNo = generate_prn_number(train)
		reservationQry.save()
		return HttpResponse(json.dumps({"validation":"Your reservation process is completed Successfully.","status":True}), content_type="application/json")
	else:
		return HttpResponse(json.dumps({"validation":"You are not logged in.Please login first.","status":False}), content_type="application/json")
