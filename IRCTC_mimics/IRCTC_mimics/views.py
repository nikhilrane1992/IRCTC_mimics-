from models import UserDetail, Location, Train, Station, DepartureDay, Reservation
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

@transaction.atomic
def seatReservation(request):
	# if request.user.is_authenticated():
	jsonObj = json.loads(request.body)
	id = 1
	user = UserDetail.objects.get(user__id=1)
	
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
	origin = Location.objects.get(id=jsonObj['originId'])
	destination = Location.objects.get(id=jsonObj['destinationId'])
	reservationQry.source = origin
	reservationQry.destination = destination
	pnrNo = generate_prn_number(train)
	reservationQry.save()
	return HttpResponse(json.dumps({"validation":"Your reservation process is completed Successfully.","status":True}), content_type="application/json")
	# else:
	# 	return HttpResponse(json.dumps({"validation":"You are not logged in.Please login first.","status":False}), content_type="application/json")
