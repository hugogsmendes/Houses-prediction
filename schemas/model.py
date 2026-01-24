from pydantic import BaseModel

class ModelSchemaPost (BaseModel):

    class config:
        from_attributes = True