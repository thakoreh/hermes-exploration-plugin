"""
JSON Schema definitions for discoveries (tools, APIs, models).
"""

from typing import Dict, List, Any
import jsonschema


# ── Tool ──────────────────────────────────────────────────────────────────────

TOOL_SCHEMA = {
    "type": "object",
    "required": ["name", "description", "category", "status", "added_by"],
    "properties": {
        "name":                          {"type": "string"},
        "description":                   {"type": "string", "minLength": 20},
        "category":                      {"type": "string"},
        "use_cases":                     {"type": "array",  "items": {"type": "string"}},
        "github_url":                    {"type": "string", "format": "uri"},
        "install_command":               {"type": "string"},
        "official_documentation_url":    {"type": "string", "format": "uri"},
        "pricing_model":                 {"type": "string", "enum": ["free", "freemium", "paid", "open-source", "unknown"]},
        "status":                        {"type": "string", "enum": ["verified", "unverified", "unreliable"]},
        "added_by":                      {"type": "string"},
        "tags":                          {"type": "array",  "items": {"type": "string"}},
        "last_verified":                 {"type": "string", "format": "date"},
    },
}

# ── API ────────────────────────────────────────────────────────────────────────

API_SCHEMA = {
    "type": "object",
    "required": ["name", "description", "category", "pricing_model", "status", "added_by"],
    "properties": {
        "name":                          {"type": "string"},
        "description":                   {"type": "string", "minLength": 20},
        "category":                      {"type": "string"},
        "base_url":                      {"type": "string", "format": "uri"},
        "documentation_url":             {"type": "string", "format": "uri"},
        "github_url":                    {"type": "string", "format": "uri"},
        "pricing_model":                 {"type": "string", "enum": ["free", "freemium", "paid", "open-source", "unknown"]},
        "free_tier_notes":               {"type": "string"},
        "status":                        {"type": "string", "enum": ["verified", "unverified", "unreliable"]},
        "added_by":                      {"type": "string"},
        "tags":                          {"type": "array",  "items": {"type": "string"}},
        "last_verified":                 {"type": "string", "format": "date"},
    },
}

# ── Model ──────────────────────────────────────────────────────────────────────

MODEL_SCHEMA = {
    "type": "object",
    "required": ["name", "description", "provider", "context_window", "status", "added_by"],
    "properties": {
        "name":                          {"type": "string"},
        "description":                   {"type": "string", "minLength": 20},
        "provider":                      {"type": "string"},
        "context_window":                {"type": "integer"},
        "input_price_per_mtok":          {"type": "number"},
        "output_price_per_mtok":         {"type": "number"},
        "release_date":                  {"type": "string"},
        "status":                        {"type": "string", "enum": ["verified", "unverified", "unreliable"]},
        "added_by":                      {"type": "string"},
        "tags":                          {"type": "array",  "items": {"type": "string"}},
        "last_verified":                 {"type": "string", "format": "date"},
        "strengths":                     {"type": "array",  "items": {"type": "string"}},
        "weaknesses":                     {"type": "array",  "items": {"type": "string"}},
    },
}

SCHEMAS = {"tool": TOOL_SCHEMA, "api": API_SCHEMA, "model": MODEL_SCHEMA}


class DiscoverySchema:
    """Helpers for validating and working with discovery records."""

    @staticmethod
    def get_tool_schema() -> Dict[str, Any]:
        return TOOL_SCHEMA

    @staticmethod
    def get_api_schema() -> Dict[str, Any]:
        return API_SCHEMA

    @staticmethod
    def get_model_schema() -> Dict[str, Any]:
        return MODEL_SCHEMA

    @staticmethod
    def validate(discovery_type: str, data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        Returns (is_valid, list_of_errors).
        """
        schema = SCHEMAS.get(discovery_type)
        if not schema:
            return False, [f"Unknown discovery type: {discovery_type}"]
        try:
            jsonschema.validate(instance=data, schema=schema)
            return True, []
        except jsonschema.ValidationError as e:
            return False, [e.message]

    @staticmethod
    def required_fields(discovery_type: str) -> List[str]:
        return list(SCHEMAS.get(discovery_type, {}).get("properties", {}).keys())
