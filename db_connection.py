import pymongo

class Mongo():
    dbname = "rent-a-room"
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[dbname]

    print(myclient.list_database_names())

    dblist = myclient.list_database_names()
    room = mydb["rooms"]
    customer = mydb["persons"]

    if dbname in dblist:
        print("The database has been found")

    def createLogin(name, firstname, email, password, telnr, address):
        mydict = {"name": name, "firstname": firstname, "password": password, "address": address, "email": email, "telnr": telnr}
        Mongo.customer.insert_one(mydict)
        return 1

    def getLogin(email):
        return Mongo.customer.find_one({"email": email}, {"email": 1, "name": 1, "password": 1})

    def createRoom(name, desc, address, room_amount, space, owner, owner_id):
        mydict = {"name": name, "beschreibung": desc, "address": address, "room_amount": room_amount, "space": space, "owner": owner, "owner_id": owner_id, "is_booked": False, "booker_id": "none"}
        result = Mongo.room.insert_one(mydict)
        return result.inserted_id

    def getRoom(filtername):
        return Mongo.room.find({"name": filtername}, {"_id": 1, "name": 1, "beschreibung": 1, "owner": 1})

    def getAllRoom(self):
        return Mongo.room.find({}, {"_id": 1, "name": 1, "beschreibung": 1, "address": 1, "owner": 1})

    def getRoomByOwner(owner, owner_id):
        return Mongo.room.find({"owner": owner, "owner_id": owner_id}, {"_id": 1, "name": 1, "beschreibung": 1, "address": 1})

    def getRoomById(id):
        return Mongo.room.find_one({"_id": id}, {})
    def getAllRooms(self):
        for x in Mongo.room.find({}, {}):
            print(x)
            return x

    def getByName(name):
        for x in Mongo.room.find({"name": name }, {}):
            print (x)
            return x
    def getByDesc(beschreibung):
        for x in Mongo.room.find({"beschreibung": beschreibung}, {}):
            print(x)
            return x

    def getByRoomAmount(room_amount):
        for x in Mongo.room.find({"room_amount": room_amount}, {}):
            print(x)
            return x

    def getBySpace(space):
        for x in Mongo.room.find({"space": space},{}):
            print(x)
            return x

    def deleteRoom(id):
        objToDelete = {"_id": id}
        Mongo.room.delete_one(objToDelete)
        return True

    def updateRoomById(id, newName, newDesc, newAdd):
        myquery = {"_id": id}
        newvalues = {"$set": {"name": newName, "beschreibung": newDesc,"address": newAdd}}
        Mongo.room.update_one(myquery, newvalues)
        return id

    def book_room(id, booker_id):
        myquery = {"_id": id}
        newvalues = {"$set": {"is_booked": True, "booker_id": booker_id}}
        Mongo.room.update_one(myquery, newvalues)
        return id

    def unbook_room(id):
        myquery = {"_id": id}
        newvalues = {"$set": {"is_booked": False, "booker_id": "None"}}
        Mongo.room.update_one(myquery, newvalues)
        return id





