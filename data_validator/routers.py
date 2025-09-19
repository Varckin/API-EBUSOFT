from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Optional
import json
from data_validator.models import ValidateResponse
from data_validator.settings import CONFIG
from data_validator.service import (validate_json_string, read_file,
                                    validate_xml_string, validate_yaml_string,
                                    validate_json_schema, validate_xml_schema,
                                    validate_yaml_schema, validate_file)


router = APIRouter(prefix="/validator", tags=["validator"])


@router.get("/health", response_model=str)
async def health() -> str:
    """Health check specifically for the validator module."""
    return "ok"

@router.post("", response_model=ValidateResponse)
async def validate_string(
    format: str = Form(..., description="Data format: json, yaml, xml"),
    data: Optional[str] = Form(None, description="Data as a string"),
    file: Optional[UploadFile] = File(None, description="Optional file upload")
):
    """
    Validate raw data syntax for JSON, YAML, or XML.
    """
    if not data and not file:
        raise HTTPException(status_code=400, detail="Provide either 'data' or 'file' for validation")

    # Read file content if provided
    fmt = format.lower()
    if file:
        await validate_file(file, fmt)
        data = await read_file(file)

    if fmt == "json":
        return validate_json_string(data)
    elif fmt == "yaml":
        return validate_yaml_string(data)
    elif fmt == "xml":
        return validate_xml_string(data)
    else:
        raise HTTPException(status_code=400, detail="Format must be one of: json, yaml, xml")

@router.post("/schema", response_model=ValidateResponse)
async def validate_schema(
    format: str = Form(..., description="Data format: json, yaml, xml"),
    data: Optional[str] = Form(None, description="Data as a string"),
    file: Optional[UploadFile] = File(None, description="Optional file upload"),
    schema: Optional[UploadFile] = File(None, description="Schema file (JSON Schema for JSON/YAML, XSD for XML)")
):
    """
    Validate data against a schema (JSON Schema for JSON/YAML or XSD for XML).
    """
    if not data and not file:
        raise HTTPException(status_code=400, detail="Provide either 'data' or 'file' for validation")
    if file:
        data = await read_file(file)
    if not schema:
        raise HTTPException(status_code=400, detail="Schema file is required for schema validation")
    
    fmt = format.lower()

    if file:
        await validate_file(file, fmt)
        data = await read_file(file)

    if fmt in ["json", "yaml"]:
        await validate_file(schema, "json")
    elif fmt == "xml":
        await validate_file(schema, "xsd")
    else:
        raise HTTPException(status_code=400, detail="Format must be one of: json, yaml, xml")

    
    schema_content = await read_file(schema)
    
    if fmt in ["json", "yaml"]:
        try:
            schema_dict = json.loads(schema_content)
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail=f"Invalid JSON schema: {str(e)}")
        return validate_json_schema(data, schema_dict) if fmt == "json" else validate_yaml_schema(data, schema_dict)
    else:  # xml
        return validate_xml_schema(data, schema_content)
