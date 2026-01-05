
VARIABLE_TYPES = {
    # 1. Basic Text
    "text": {
        "label": "纯文本输入",
        "description": "用户手动输入一段文本",
        "extension_schema": [
            { "key": "placeholder", "label": "输入框提示语", "type": "string", "default": "请输入..." },
            { "key": "max_length", "label": "最大字数限制", "type": "number", "default": 1000 },
            { "key": "is_textarea", "label": "是否允许输入多行文本", "type": "boolean", "default": False }
        ]
    },

    # 2. Static Select
    "select": {
        "label": "静态下拉选项",
        "description": "管理员预设固定的选项列表",
        "extension_schema": [
            { "key": "options", "label": "选项列表(回车添加)", "type": "list_string", "default": ["选项1", "选项2"] },
            { "key": "allow_multiple", "label": "是否多选", "type": "boolean", "default": False }
        ]
    },

    # 3. API Dynamic Select
    "api_dynamic_select": {
        "label": "API 动态选项-查询多选列表",
        "description": "选项内容通过调用外部接口实时获取。API返回应为JSON列表，若不符合label/value格式，将默认使用label_example:value_example格式。",
        "extension_schema": [
            {
                "key": "data_source_url",
                "label": "数据接口地址",
                "type": "string",
                "default": "/api/external/list_items",
                "tips": "填写后端代理层的路径或允许跨域的完整URL"
            },
            {
                "key": "query_params",
                "label": "查询参数列表(逗号分隔)",
                "type": "list_string",
                "default": [],
                "tips": "若API需要参数，在此配置参数名，运行态将显示对应输入框"
            },
            { "key": "allow_multiple", "label": "是否多选", "type": "boolean", "default": False }
        ]
    },

    # 4. Dify KB Search
    "dify_kb_search": {
        "label": "Dify知识库检索和选择",
        "description": "根据用户输入自动检索知识库内容并进行选择",
        "extension_schema": [
            { "key": "base_url", "label": "关联知识库查询url", "type": "string", "default": "" },
            { "key": "name", "label": "名称", "type": "string", "default": "" },
            { "key": "api_key", "label": "API Key", "type": "string", "default": "" },
            { "key": "dataset_id", "label": "Dataset ID", "type": "string", "default": "" },
            {
                "key": "search_method",
                "label": "检索模式",
                "type": "select",
                "options": ["hybrid_search", "semantic_search", "full_text_search"],
                "default": "hybrid_search"
            },
            { "key": "vector_weight", "label": "向量权重 (0-1)", "type": "number", "default": 0.7 },
            { "key": "top_k", "label": "引用片段数量", "type": "number", "default": 3 },
            { "key": "score_threshold", "label": "相似度阈值", "type": "number", "default": 0.6 }
        ]
    },

    # 5. Summary KB Search
    "summary_kb_search": {
        "label": "摘要知识库检索和详细内容映射",
        "description": "根据用户输入自动检索知识库内容得到摘要并进行选择，点击确认得到最终结果",
        "extension_schema": [
            { "key": "base_url", "label": "查询接口地址", "type": "string", "default": "/knowledge/getCaseKnow" },
            { "key": "name", "label": "名称", "type": "string", "default": "摘要检索" },
            {
                "key": "abstract_columns",
                "label": "摘要显示列名(逗号分隔)",
                "type": "list_string",
                "default": ["module", "name", "code"],
                "tips": "配置abstract中需要显示的字段"
            },
            { "key": "score_threshold", "label": "自动勾选阈值", "type": "number", "default": 0.6 }
        ]
    },

    # 6. Excel Input
    "excel": {
        "label": "Excel表格输入",
        "description": "允许粘贴Excel数据，自动转换为Markdown表格",
        "extension_schema": [
            { "key": "default_rows", "label": "默认行数", "type": "number", "default": 5 },
            { "key": "default_cols", "label": "默认列数", "type": "number", "default": 3 },
            { "key": "placeholder", "label": "占位提示", "type": "string", "default": "请从Excel复制并粘贴数据..." },
            {
                "key": "headers",
                "label": "表头配置(逗号分隔)",
                "type": "list_string",
                "default": ["列1", "列2", "列3"],
                "tips": "配置每一列的名称"
            }
        ]
    }
}
