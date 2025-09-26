from tortoise.contrib.pydantic import pydantic_model_creator
from models import Pet


# Pydantic model for reading/writing Pet instances.
# PetIn excludes readonly fields (like id) so it can be used for create/update inputs.
PetIn = pydantic_model_creator(Pet, name="PetIn", exclude_readonly=True)

# PetOut is the response model used by FastAPI routes. It includes all fields.
PetOut = pydantic_model_creator(Pet, name="PetOut")
