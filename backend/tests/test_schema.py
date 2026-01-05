
import unittest
from backend.app.template_types import VARIABLE_TYPES

class TestVariableTypes(unittest.TestCase):
    def test_variable_types_exist(self):
        expected_keys = [
            "text", "select", "api_dynamic_select",
            "dify_kb_search", "summary_kb_search", "excel"
        ]
        for key in expected_keys:
            self.assertIn(key, VARIABLE_TYPES)

    def test_text_extension_schema(self):
        text_schema = VARIABLE_TYPES["text"]["extension_schema"]
        keys = [item["key"] for item in text_schema]
        self.assertIn("placeholder", keys)
        self.assertIn("max_length", keys)
        self.assertIn("is_textarea", keys)

    def test_api_dynamic_select_schema(self):
        schema = VARIABLE_TYPES["api_dynamic_select"]["extension_schema"]
        keys = [item["key"] for item in schema]
        self.assertIn("data_source_url", keys)
        self.assertIn("query_params", keys)
        self.assertNotIn("label_field", keys) # Should be removed

    def test_dify_kb_search_schema(self):
        schema = VARIABLE_TYPES["dify_kb_search"]["extension_schema"]
        keys = [item["key"] for item in schema]
        self.assertIn("base_url", keys)
        self.assertIn("search_method", keys)
        self.assertIn("top_k", keys)
        self.assertIn("name", keys)

    def test_summary_kb_search_schema(self):
        schema = VARIABLE_TYPES["summary_kb_search"]["extension_schema"]
        keys = [item["key"] for item in schema]
        self.assertIn("abstract_columns", keys)
        self.assertIn("score_threshold", keys)

    def test_excel_schema(self):
        schema = VARIABLE_TYPES["excel"]["extension_schema"]
        keys = [item["key"] for item in schema]
        self.assertIn("headers", keys)
        self.assertIn("placeholder", keys)

if __name__ == "__main__":
    unittest.main()
