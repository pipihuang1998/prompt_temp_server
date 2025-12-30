
VARIABLE_TYPES = {
    # 1. Basic Text
    "text": {
        "label": "纯文本输入",
        "description": "用户手动输入一段文本",
        "extension_schema": [
            { "key": "placeholder", "label": "输入框提示语", "type": "string", "default": "请输入..." },
            { "key": "max_length", "label": "最大字数限制", "type": "number", "default": 100 },
            { "key": "is_textarea", "label": "是否多行文本", "type": "boolean", "default": False }
        ]
    },

    # 2. Static Select
    "select": {
        "label": "静态下拉选项",
        "description": "管理员预设固定的选项列表",
        "extension_schema": [
            # type: list_string means frontend should provide a tag input component
            { "key": "options", "label": "选项列表(回车添加)", "type": "list_string", "default": ["选项1", "选项2"] },
            { "key": "allow_multiple", "label": "是否多选", "type": "boolean", "default": False }
        ]
    },

    # 3. API Dynamic Select
    "api_dynamic_select": {
        "label": "API 动态选项",
        "description": "选项内容通过调用外部接口实时获取（如：获取用户列表、获取知识库列表）",
        "extension_schema": [
            {
                "key": "data_source_url",
                "label": "数据接口地址",
                "type": "string",
                "default": "/api/external/list_items",
                "tips": "填写后端代理层的路径或允许跨域的完整URL"
            },
            {
                "key": "label_field",
                "label": "显示字段名(Key)",
                "type": "string",
                "default": "name",
                "tips": "API返回JSON中用于显示的字段，如 'username'"
            },
            {
                "key": "value_field",
                "label": "值字段名(Key)",
                "type": "string",
                "default": "id",
                "tips": "API返回JSON中用于实际传输的字段，如 'user_id'"
            },
            { "key": "allow_multiple", "label": "是否多选", "type": "boolean", "default": False }
        ]
    },

    # 4. KB Search (Interactive)
    "kb_search": {
        "label": "知识库检索引用",
        "description": "根据用户输入自动检索知识库内容并填充",
        "extension_schema": [
            { "key": "kb_id", "label": "关联知识库ID", "type": "string", "default": "" },
            { "key": "top_k", "label": "引用片段数量", "type": "number", "default": 3 },
            { "key": "score_threshold", "label": "相似度阈值", "type": "number", "default": 0.6 }
        ]
    },

    # 5. Excel Input
    "excel": {
        "label": "Excel表格输入",
        "description": "允许粘贴Excel数据，自动转换为Markdown表格",
        "extension_schema": [
            { "key": "default_rows", "label": "默认行数", "type": "number", "default": 5 },
            { "key": "default_cols", "label": "默认列数", "type": "number", "default": 3 },
            { "key": "placeholder", "label": "占位提示", "type": "string", "default": "请从Excel复制并粘贴数据..." }
        ]
    }
}
