import json
import yaml
import xmlschema
import xml.etree.ElementTree as ET
from data_validator.models import ValidateResponse
from fastapi import UploadFile, HTTPException
from jsonschema import validate as json_validate, ValidationError, SchemaError


def validate_json_string(data: str) -> ValidateResponse:
    """
    Validate JSON string syntax.
    """
    try:
        json.loads(data)
        return ValidateResponse(valid=True, message="Valid JSON", format="json")
    except json.JSONDecodeError as e:
        return ValidateResponse(valid=False, message="Invalid JSON", errors=str(e), format="json")

def validate_yaml_string(data: str) -> ValidateResponse:
    """
    Validate YAML string syntax (supports multi-document YAML).
    """
    try:
        docs = list(yaml.safe_load_all(data))
        return ValidateResponse(valid=True, message=f"Valid YAML ({len(docs)} document(s))", format="yaml")
    except yaml.YAMLError as e:
        return ValidateResponse(valid=False, message="Invalid YAML", errors=str(e), format="yaml")

def validate_xml_string(data: str) -> ValidateResponse:
    """
    Validate XML string syntax.
    """
    try:
        ET.fromstring(data)
        return ValidateResponse(valid=True, message="Valid XML", format="xml")
    except ET.ParseError as e:
        return ValidateResponse(valid=False, message="Invalid XML", errors=str(e), format="xml")

# --- Helper to read file content ---
async def read_file(file: UploadFile) -> str:
    """
    Read content from uploaded file as UTF-8 string.
    """
    try:
        content = await file.read()
        return content.decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read file: {str(e)}")

def validate_json_schema(data: str, schema: dict) -> ValidateResponse:
    """
    Validate JSON string against a JSON Schema.
    """
    try:
        obj = json.loads(data)
    except json.JSONDecodeError as e:
        return ValidateResponse(valid=False, message="Invalid JSON", errors=str(e), format="json")
    
    try:
        json_validate(instance=obj, schema=schema)
        return ValidateResponse(valid=True, message="Valid JSON (schema OK)", format="json")
    except ValidationError as e:
        return ValidateResponse(valid=False, message="JSON does not match schema", errors=str(e), format="json")
    except SchemaError as e:
        return ValidateResponse(valid=False, message="Invalid schema", errors=str(e), format="json")

def validate_yaml_schema(data: str, schema: dict) -> ValidateResponse:
    """
    Validate YAML string against a JSON Schema (applied to each document).
    """
    try:
        docs = list(yaml.safe_load_all(data))
    except yaml.YAMLError as e:
        return ValidateResponse(valid=False, message="Invalid YAML", errors=str(e), format="yaml")
    
    for i, doc in enumerate(docs):
        try:
            json_validate(instance=doc, schema=schema)
        except ValidationError as e:
            return ValidateResponse(
                valid=False,
                message=f"YAML document {i+1} does not match schema",
                errors=str(e),
                format="yaml"
            )
        except SchemaError as e:
            return ValidateResponse(valid=False, message="Invalid schema", errors=str(e), format="yaml")
    return ValidateResponse(valid=True, message=f"Valid YAML ({len(docs)} document(s), schema OK)", format="yaml")

def validate_xml_schema(data: str, xsd_file: str) -> ValidateResponse:
    """
    Validate XML string against an XSD schema.
    """
    try:
        schema = xmlschema.XMLSchema(xsd_file)
        schema.validate(data)
        return ValidateResponse(valid=True, message="Valid XML (XSD OK)", format="xml")
    except xmlschema.XMLSchemaException as e:
        return ValidateResponse(valid=False, message="XML does not match XSD", errors=str(e), format="xml")
