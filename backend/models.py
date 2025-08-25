from enum import Enum
import uuid
from tortoise import fields, models
import hashlib


def default_hash():
    return hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()


class Location(models.Model):
    id = fields.IntField(pk=True)
    pet = fields.ForeignKeyField("models.Pet", related_name="locations")
    latitude = fields.FloatField()
    longitude = fields.FloatField()
    timestamp = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pet_id}: ({self.latitude}, {self.longitude})"


class User(models.Model):
    id = fields.IntField(pk=True)
    first_name = fields.CharField(max_length=255)
    last_name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    phone = fields.CharField(max_length=255)
    full_address = fields.CharField(max_length=1024)
    recovery_bounty = fields.DecimalField(
        max_digits=10, decimal_places=2, null=True, default=None)
    hash = fields.CharField(max_length=64, unique=True,
                            null=False, index=True, default=default_hash)

    def __str__(self):
        return self.email


class PetType(str, Enum):
    CAT = "Cat"
    DOG = "Dog"
    LIZARD = "Lizard"
    HAMSTER = "Hamster"
    BIRD = "Bird"
    OTHER = "Other"


class Pet(models.Model):
    id = fields.IntField(pk=True)
    owner = fields.ForeignKeyField("models.User", related_name="pets")
    name = fields.CharField(max_length=255)
    pet_type = fields.CharEnumField(PetType, max_length=16)
    picture = fields.CharField(max_length=1024)
    notes = fields.TextField()

    def __str__(self):
        return self.name

    def generate_qr_code(self, base_url: str = "http://localhost:5173"):
        import qrcode
        import io

        qr_data = f"{base_url}/qrcode/scan/{self.owner.hash}|{self.id}"
        img = qrcode.make(qr_data)
        buf = io.BytesIO()
        img.save(buf, "PNG")
        buf.seek(0)
        return buf
