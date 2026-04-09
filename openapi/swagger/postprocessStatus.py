#!/usr/bin/env python3

import json
import os
import sys
import re
from typing import List, Dict, Any, Optional


def walk(directory: str, file_list: Optional[List[str]] = None) -> List[str]:
    if file_list is None:
        file_list = []

    try:
        for entry in os.listdir(directory):
            full_path = os.path.join(directory, entry)
            if os.path.isdir(full_path):
                walk(full_path, file_list)
            elif os.path.isfile(full_path) and entry.endswith(".swagger.json"):
                file_list.append(full_path)
    except (OSError, PermissionError) as e:
        print(f"Error accessing directory {directory}: {e}", file=sys.stderr)

    return file_list

def rewrite_rpc_status(definitions: Optional[Dict[str, Any]]) -> bool:
    if not definitions or not isinstance(definitions, dict):
        return False

    status_def = definitions.get("rpcStatus")
    if not status_def or not isinstance(status_def, dict):
        return False

    # Ensure the definition is an object schema
    status_def["type"] = "object"
    if "properties" not in status_def:
        status_def["properties"] = {}

    # Overwrite properties to desired shape
    status_def["properties"] = {
        "status_id": {"type": "integer", "format": "int32"},
        "status_code": {"type": "string"},
        "message": {"type": "string"},
        "details": {"type": "array", "items": {"type": "object"}},
    }

    if "required" in status_def:
        del status_def["required"]

    definitions["rpcStatus"] = status_def
    return True


def process_file(file_path: str) -> bool:
    try:
        proto_path = file_path.replace("code/swagger/", "protos/").replace(".swagger.json", ".proto")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if data.get("info"):
            data.pop("info", None)    
        changed = rewrite_rpc_status(data.get("definitions"))
        
        if changed:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write("\n")
            return True

        return False

    except (OSError, json.JSONDecodeError, KeyError) as e:
        print(f"Failed to process {file_path}: {e}", file=sys.stderr)
        return False


def main() -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    files = walk(script_dir)
    for file_path in files:
        process_file(file_path)
    

if __name__ == "__main__":
    main()
