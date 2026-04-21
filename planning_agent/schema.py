from __future__ import annotations


def build_schema() -> dict:
    text_item = {
        "type": "object",
        "properties": {
            "label": {"type": "string"},
            "value": {"type": "string"},
        },
        "required": ["label", "value"],
        "additionalProperties": False,
    }

    classification_option = {
        "type": "object",
        "properties": {
            "label": {"type": "string"},
            "checked": {"type": "boolean"},
            "note": {"type": "string"},
        },
        "required": ["label", "checked", "note"],
        "additionalProperties": False,
    }

    classification_group = {
        "type": "object",
        "properties": {
            "category": {"type": "string"},
            "options": {
                "type": "array",
                "items": classification_option,
            },
        },
        "required": ["category", "options"],
        "additionalProperties": False,
    }

    tool_item = {
        "type": "object",
        "properties": {
            "category": {"type": "string"},
            "system": {"type": "string"},
            "used": {"type": "boolean"},
            "purpose": {"type": "string"},
        },
        "required": ["category", "system", "used", "purpose"],
        "additionalProperties": False,
    }

    parameter_item = {
        "type": "object",
        "properties": {
            "system": {"type": "string"},
            "name": {"type": "string"},
            "value": {"type": "string"},
        },
        "required": ["system", "name", "value"],
        "additionalProperties": False,
    }

    flow_block = {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "actors": {
                "type": "array",
                "items": {"type": "string"},
            },
            "steps": {
                "type": "array",
                "items": {"type": "string"},
            },
            "outputs": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": ["title", "actors", "steps", "outputs"],
        "additionalProperties": False,
    }

    architecture_component = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "roles": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": ["name", "roles"],
        "additionalProperties": False,
    }

    implementation_step = {
        "type": "object",
        "properties": {
            "stage": {"type": "string"},
            "details": {
                "type": "array",
                "items": {"type": "string"},
            },
        },
        "required": ["stage", "details"],
        "additionalProperties": False,
    }

    work_process = {
        "type": "object",
        "properties": {
            "sample_flow_document": {"type": "string"},
            "sharepoint_link": {"type": "string"},
            "file_naming": {
                "type": "array",
                "items": {"type": "string"},
            },
            "as_is": flow_block,
            "to_be": flow_block,
            "implementation_architecture": {
                "type": "array",
                "items": architecture_component,
            },
            "implementation_steps": {
                "type": "array",
                "items": implementation_step,
            },
        },
        "required": [
            "sample_flow_document",
            "sharepoint_link",
            "file_naming",
            "as_is",
            "to_be",
            "implementation_architecture",
            "implementation_steps",
        ],
        "additionalProperties": False,
    }

    return {
        "name": "planning_document",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "background": {"type": "array", "items": {"type": "string"}},
                "purpose": {"type": "array", "items": {"type": "string"}},
                "writing_notes": {"type": "array", "items": {"type": "string"}},
                "toc": {"type": "array", "items": {"type": "string"}},
                "overview": {"type": "array", "items": text_item},
                "classification": {"type": "array", "items": classification_group},
                "work_process": work_process,
                "tools": {"type": "array", "items": tool_item},
                "parameters": {"type": "array", "items": parameter_item},
                "considerations": {"type": "array", "items": {"type": "string"}},
                "assumptions": {"type": "array", "items": {"type": "string"}},
            },
            "required": [
                "title",
                "background",
                "purpose",
                "writing_notes",
                "toc",
                "overview",
                "classification",
                "work_process",
                "tools",
                "parameters",
                "considerations",
                "assumptions",
            ],
            "additionalProperties": False,
        },
    }
