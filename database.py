from peewee import *
import datetime

from peewee import BackrefAccessor

database = SqliteDatabase('./database/test.db')


class BaseModel(Model):
    class Meta:
        database = database


class User(BaseModel):
    userId = IntegerField(primary_key=True)
    username = CharField(unique=True)
    password = CharField()
    firstName = CharField()
    lastName = CharField()
    email = CharField()


class UserArchive(BaseModel):
    archiveId = IntegerField(primary_key=True)
    archiveName = CharField(unique=True)
    creationTime = DateTimeField()
    lastUpdateTime = DateTimeField()
    typeOfArchive = CharField()
    userId = ForeignKeyField(User, backref='archives')

class ListOfArchive(BaseModel):
    listOfArchiveId = IntegerField(primary_key=True)
    archiveData = CharField()
    archiveId = ForeignKeyField(UserArchive, backref='docs')

class Database:
    def __init__(self):
        super(Database, self).__init__()

    def createDatabase(self):
        with database:
            database.create_tables([User, UserArchive, ListOfArchive])

    def connectDB(self):
        with database:
            database.connect()

    def login(self, username, password):
        with database:
            userList = User.select()
            for user in userList:
                if user.username == username and user.password == password:
                    return 'success'
            return 'ERROR: Username and Password did not match'

    def singin(self, username, password, first_name, last_name, email):
        with database:
            userList = User.select()
            if userList is not None:
                for user in userList:
                    if user.username == username:
                        print(user.username)
                        return 'ERROR: Username Taken'
            newUser = User()
            newUser.username = username
            newUser.password = password
            newUser.firstName = first_name
            newUser.lastName = last_name
            newUser.email = email
            newUser.save()
            return 'success'

    def printAllUser(self):
        with database:
            userList = User.select()
            for user in userList:
                print(user.username)

    def createArchive(self, archive_name, creation_time, last_update_time, type_of_archive, user, data):
        with database:
            newArchive = UserArchive()
            newArchive.archiveName = archive_name
            newArchive.creationTime = creation_time
            newArchive.lastUpdateTime = last_update_time
            newArchive.typeOfArchive = type_of_archive

            newArchive.userId = user.userId

            newArchive.save()
            self.saveDocTable(newArchive.archiveId, data)
            
    def getArchiveList(self, user):
        with database:
            return UserArchive.select().where(UserArchive.userId == user.userId)

# here
    def getArchiveByName(self, archive_name):
        with database:
            userArchive = UserArchive.select().where(UserArchive.archiveName == archive_name)
            # print(userArchive[0].archiveName)
            data = ListOfArchive.select().where(ListOfArchive.archiveId == userArchive[0].archiveId)
            return data[0].archiveData

    def saveArchive(self, archive_name, newData):
        with database:
            userArchive = UserArchive.select().where(UserArchive.archiveName == archive_name)
            data = ListOfArchive.select().where(ListOfArchive.archiveId == userArchive[0].archiveId)
            userArchive[0].lastUpdateTime = datetime.datetime.now()
            data[0].archiveData = newData
            userArchive[0].save()
            data[0].save()
            return 'success'
            
    
    def getUserObj(self, username):
        with database:
            userList = User.select()
            if userList is not None:
                for user in userList:
                    if user.username == username:
                        return user
                        break
    
    def isArchiveExist(self, archiveName):
        with database:
            archiveList = UserArchive.select()
            if archiveList is not None:
                for archive in archiveList:
                    if archive.archiveName == archiveName:
                        return True
            return False

    def saveDocTable(self, archiveId, data):
        with database:
            newArchive = ListOfArchive()
            newArchive.archiveData = data
            newArchive.archiveId = archiveId
            newArchive.save()


db = Database()
db.createDatabase()
# db.saveDocTable('haha')
# db.createArchive('test4', datetime.datetime.now(), datetime.datetime.now(), 'simple', User.select()[1], 'haha')
# print('done')
# db.getArchiveByName('sameep')
