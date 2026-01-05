# Prompt Template Configuration System

## Overview
This system allows configuring and running dynamic prompt templates with various input types.

## Supported Variable Types

### 1. Basic Text (`text`)
- **Description**: Manual text input.
- **Configuration**:
    - `placeholder`: Input hint.
    - `max_length`: Character limit.
    - `is_textarea`: Toggle for multi-line input.

### 2. Static Select (`select`)
- **Description**: Pre-defined dropdown options.
- **Configuration**:
    - `options`: List of strings.
    - `allow_multiple`: Enable multi-selection.

### 3. API Dynamic Select (`api_dynamic_select`)
- **Description**: Options fetched from an external API.
- **Configuration**:
    - `data_source_url`: URL to fetch options from.
    - `query_params`: List of parameters to query (runtime input).
    - `allow_multiple`: Enable multi-selection.
- **Runtime**: Automatically maps response fields to label/value. Default fallback logic used if standard fields (`label`/`value` or `name`/`id`) are missing.

### 4. Dify Knowledge Base Search (`dify_kb_search`)
- **Description**: Search a Dify Knowledge Base and select content.
- **Configuration**:
    - `base_url`: Knowledge Base query URL.
    - `name`: Configuration name.
    - `api_key`: API Key.
    - `dataset_id`: Dataset ID.
    - `search_method`: `hybrid_search`, `semantic_search`, or `full_text_search`.
    - `top_k`, `score_threshold`, `vector_weight`.

### 5. Summary Knowledge Base Search (`summary_kb_search`)
- **Description**: Search for summaries, view in a table, select multiple, and fill detailed content.
- **Configuration**:
    - `base_url`: Search endpoint.
    - `abstract_columns`: Columns to display in the result table.
    - `score_threshold`: Auto-selection threshold.

### 6. Excel Input (`excel`)
- **Description**: Paste Excel/TSV data to convert to Markdown table.
- **Configuration**:
    - `headers`: Define column headers for display/validation.
    - `placeholder`, `default_rows`, `default_cols`.

## Usage
1. **Editor**: Create templates and configure parameters using the above types.
2. **Runner**: Fill in parameters. Dynamic fields will fetch data or allow searching external sources.
