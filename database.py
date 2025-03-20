from peewee import *

# Initialize database connection
db = None

# Define models
class Kind(Model):
    kind_name = CharField()
    food = CharField()
    noise = CharField()

    class Meta:
        database = db


class Pet(Model):
    name = CharField()
    age = IntegerField()
    owner = CharField()
    kind = ForeignKeyField(Kind, backref="pets")

    class Meta:
        database = db


def initialize(database_file):
    global db, Kind, Pet
    db = SqliteDatabase(database_file)

    Kind._meta.database = db
    Pet._meta.database = db

    db.connect()
    db.create_tables([Pet, Kind])


def get_pets():
    pets = Pet.select().join(Kind)
    return list(pets)

def create_pet(data):
    print(data)
    kind = Kind.get_by_id(data["kind_id"])
    return Pet.create(name=data["name"], age=int(data["age"]), owner=data["owner"], kind=kind)

def get_pet(id):
    return Pet.get_or_none(Pet.id == id)

def delete_pet(id):
    return Pet.delete_by_id(id)
def update_pet(id, data):
    kind = Kind.get_by_id(data["kind_id"])
    return Pet.update({Pet.name: data["name"],
                Pet.age: int(data["age"]),
                Pet.owner: data["owner"],
                Pet.kind: kind}).where(Pet.id == id).execute()


def get_kind(id):
    return Kind.get_or_none(Kind.id == id)

def get_kinds():
    kinds = Kind.select()
    return list(kinds)

def create_kind(data):
    print(data)
    return Kind.create(kind_name=data["name"], food=data["food"], noise=data["sound"])
def update_kind(id, data):
     return Kind.update({Kind.kind_name: data["name"],
                     Kind.food: data["food"],
                     Kind.noise: data["sound"]}).where(Kind.id == id).execute()

def delete_kind(id):
    return Kind.delete_by_id(id)


def test_initialize():
    print("test initialize...")
    initialize("test_pets.db")
    assert db != None

def test_get_pets():
    print("test get_pets...")
    kind = Kind(kind_name = "dog",food="dog_food",noise="bark")
    kind.save()
    pet = Pet(name="Dorothy",age=10,owner="Greg",kind=kind)
    pet.save()
    pets = get_pets()
    assert type(pets) is list
    assert type(pets[0]) is Pet
    assert pets[0].name == "Dorothy"

def test_get_kinds():
    print("test get_kinds...")
    kind = Kind(kind_name="dog", food="dog_food", noise="bark")
    kinds = get_kinds()
    assert type(kinds) is list
    assert type(kinds[0]) is Kind
    assert kinds[0].kind_name == "dog"

def get_pet_by_id(id):
    # pet = Pet.get_by_id(id)
    pet = Pet.get_or_none(Pet.id == id)
    return pet

def test_get_pet_by_id():
    print("test get_pet_by_id...")
    pet = get_pet_by_id(1)
    assert type(pet) is Pet
    assert pet.id == 1
    pet = get_pet_by_id(3451)
    assert pet == None


def get_kind_by_id(id):
    # kind = Kind.get_by_id(id)
    kind = Kind.get_or_none(Kind.id == id)
    return kind


def test_get_kind_by_id():
    print("test get_kind_by_id...")
    kind = get_kind_by_id(1)
    assert type(kind) is Kind
    assert kind.id == 1
    kind = get_kind_by_id(3451)
    assert kind == None


if __name__ == "__main__":
    test_initialize()
    test_get_pets()
    test_get_kinds()
    test_get_pet_by_id()
    test_get_kind_by_id()
    print("done.")

