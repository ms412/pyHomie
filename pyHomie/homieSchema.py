
homieSchema = {
  "$ref": "#/schema/homie",
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "schema": {
    "homie": {
      "type": "object",
      "additionalProperties": False,
      "patternProperties": {
        "^(?!-)[a-z0-9-]+$": {
          "type": "object",
          "$ref": "#/schema/device"
        }
      },
      "title": "homie"
    },
    "device": {
      "type": "object",
      "additionalProperties": False,
      "properties": {
        "topic": {
          "type": "string"
        },
        "name": {
          "type": "string"
        },
        "nodes": {
          "type": "array",
          "items": {
            "patternProperties": {
              "^(?!-)[a-z0-9-]+$": {
                "type": "object"
              }
            },
            "additionalProperties": False,
            "$ref": "#/schema/nodes"
          }
        }
      },
      "required": [
        "topic", "name","nodes"
      ],
      "title": "device"
    },
    "nodes": {
      "type": "object",
      "additionalProperties": False,
      "patternProperties": {
        "^(?!-)[a-z0-9-]+$": {
          "type": "object",
          "$ref": "#/schema/node"
        }
      },
      "title": "nodes"
    },
    "node": {
      "type": "object",
      "additionalProperties": False,
      "properties": {
        "type": {
          "type": "string"
        },
        "name": {
          "type": "string"
        },
        "properties": {
          "type": "array",
          "items": {
            "patternProperties": {
              "^(?!-)[a-z0-9-]+$": {
                "type": "object"
              }
            },
            "additionalProperties": False,
            "$ref": "#/schema/properties"
          }
        }
      },
      "required": [
        "name", "properties"
      ],
      "title": "node"
    },
    "properties": {
      "type": "object",
      "additionalProperties": False,
      "patternProperties": {
        "^(?!-)[a-z0-9-]+$": {
          "type": "object",
          "$ref": "#/schema/property"
        }
      },
      "title": "properties"
    },
    "property": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string"
        },
        "type": {
          "type": "string"
        },
        "datatype": {
          "enum": ["string", "float", "boolean", "integer", "datetime"]
        }
      },
      "required": [
        "name", "datatype"
      ]
    }
  }
}