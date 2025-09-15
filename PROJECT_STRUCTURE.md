# Agri-mGraphrag 项目结构说明

## 📁 整理后的项目结构

```
project/
├── README.md                    # 项目说明文档
├── WINDOWS_SETUP_GUIDE.md       # Windows部署指南
├── PROJECT_STRUCTURE.md         # 项目结构说明(本文件)
├── requirements.txt             # Python依赖包
├── setup_windows.bat           # Windows一键安装脚本
├── entrypoint.sh               # Linux/macOS启动脚本
│
├── demo_v2.py                  # 完整功能演示(需要API配置)
├── demo_basic.py               # 基础功能演示(无需API)
│
├── config/
│   └── config.yaml             # 统一配置文件
│
├── data/                       # 数据目录
│   ├── raw/                    # 原始数据
│   │   ├── structured/         # 结构化数据(CSV)
│   │   ├── unstructured/       # 非结构化文本
│   │   └── images/             # 图像数据
│   └── processed/              # 处理后数据
│
├── src/                        # 核心源码
│   ├── core/                   # 系统核心
│   │   ├── agri_system_v2.py   # 主系统控制器
│   │   ├── config.py           # 配置管理
│   │   └── logger.py           # 日志系统
│   │
│   ├── data_processing/        # 数据处理模块
│   │   ├── base.py             # 基础数据处理类
│   │   ├── structured.py       # 结构化数据处理
│   │   ├── unstructured.py     # 文本处理
│   │   └── image.py            # 图像处理
│   │
│   ├── knowledge_graph/        # 知识图谱模块
│   │   ├── base.py             # 图谱基础类
│   │   ├── builder.py          # 图谱构建器
│   │   ├── ontology.py         # 农业本体定义
│   │   ├── networkx_store.py   # NetworkX图存储
│   │   └── neo4j_client.py     # Neo4j数据库客户端
│   │
│   ├── llm_integration/        # 大语言模型集成
│   │   ├── base.py             # LLM基础类
│   │   ├── openai_client.py    # OpenAI API客户端
│   │   └── local_llm.py        # 本地模型接口
│   │
│   └── embeddings/             # 向量嵌入模块
│       └── embedding_manager.py # 嵌入模型管理器
│
└── tests/                      # 测试脚本
    └── test_basic_functionality.py # 基础功能测试
```

## 🔧 核心模块说明

### 1. 系统核心 (src/core/)
- **agri_system_v2.py**: 系统主控制器，协调各模块工作
- **config.py**: 统一配置管理，支持YAML配置文件
- **logger.py**: 日志系统，支持多级别日志记录

### 2. 数据处理 (src/data_processing/)
- **base.py**: 数据处理基础类，定义统一接口
- **structured.py**: 处理CSV、JSON等结构化数据
- **unstructured.py**: 处理文本数据，提取实体关系
- **image.py**: 图像分析和描述生成

### 3. 知识图谱 (src/knowledge_graph/)
- **base.py**: 图谱操作基础接口
- **builder.py**: 知识图谱构建和融合逻辑
- **ontology.py**: 农业领域本体定义
- **networkx_store.py**: 基于NetworkX的内存图存储
- **neo4j_client.py**: Neo4j图数据库客户端

### 4. LLM集成 (src/llm_integration/)
- **base.py**: LLM集成基础接口
- **openai_client.py**: OpenAI ChatGPT API客户端
- **local_llm.py**: 本地模型集成接口

### 5. 向量嵌入 (src/embeddings/)
- **embedding_manager.py**: 管理多种嵌入模型，支持语义搜索

## 🔌 API和数据库接口位置

### 必须配置的接口:
1. **OpenAI API**: `src/llm_integration/openai_client.py` (第15-30行)
2. **Neo4j数据库**: `src/knowledge_graph/neo4j_client.py` (第20-40行)
3. **主配置**: `config/config.yaml` (全文件)

### 配置示例:
```yaml
# config/config_v2.yaml
openai:
  api_key: "your-openai-api-key"
  model: "gpt-3.5-turbo"

neo4j:
  uri: "bolt://localhost:7687"
  username: "neo4j"
  password: "your-password"

embeddings:
  model_type: "sentence-transformers"
  model_name: "all-MiniLM-L6-v2"
```

## 🚀 使用方法

### 立即体验 (无需配置):
```bash
python demo_basic.py
```

### 完整功能 (需要配置API):
1. 编辑 `config/config.yaml` 添加API密钥
2. 运行 `python demo_v2.py`

### 安装依赖:
```bash
# Windows
setup_windows.bat

# Linux/macOS
pip install -r requirements.txt
```

## 📊 项目统计

- **总文件数**: 34个核心文件
- **Python模块**: 22个
- **配置文件**: 1个
- **演示脚本**: 2个
- **文档文件**: 3个
- **代码总量**: 约8000行Python代码

项目结构清晰、模块化程度高，易于维护和扩展。