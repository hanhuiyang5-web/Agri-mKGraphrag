# Agri-mKGraphrag: 智慧农业多模态知识图谱问答系统

基于大模型与多模态知识图谱技术融合的智慧农业问答系统，支持结构化文本、非结构化文本和图片三种数据类型。

## 系统特性

- 🌾 **农业领域专业化**: 专门针对农业领域设计的本体和知识抽取
- 🤖 **ChatGPT集成**: 支持OpenAI GPT-3.5/GPT-4 API
- 📊 **Neo4j图数据库**: 企业级图数据库存储和查询
- 🧠 **智能Embedding**: 支持语义相似度搜索和向量检索
- 💻 **Windows原生支持**: 针对Windows系统优化，一键部署
- 🔗 **多模态融合**: 统一处理文本、图像和结构化数据

## 环境要求

- Windows 10/11 (64位)
- Python 3.11 或 3.12
- 8GB+ RAM, 10GB+ 存储

## 快速开始

### 1. 安装依赖
```bash
# Windows一键安装
setup_windows.bat

# 或手动安装
pip install -r requirements.txt
```

### 2. 配置API密钥
编辑 `config/config_v2.yaml`:
```yaml
openai:
  api_key: "your-openai-api-key"
  
neo4j:
  password: "your-neo4j-password"
```

### 3. 运行演示（快速）
```bash
# 完整功能演示(需要API配置)
python demo_v2.py

# 基础功能演示(无需API)
python demo_basic.py
```

### 4. 数据导入、向量化与检索（推荐）

系统将“数据导入(ingest)”与“检索(query)”解耦，避免每次检索都重复跑数据处理与LLM抽取。

1) 准备数据与配置

- 目录结构（建议）
  - 结构化: `data/raw/structured/agriculture_data.csv`
  - 文本: `data/raw/unstructured/agriculture_text.txt`
- 在 `config/config_v2.yaml` 配置：
  - 向量模型：`embedding.model_type` 为 `ollama` 或 `sentence_transformers`
  - 文本LLM抽取开关：`data_processing.text.llm_extraction.enabled: true/false`
  - 结构化列映射与关系规则：`data_processing.structured.column_entity_map` 与 `relation_rules`

2) 导入阶段（处理→入图→向量化→落盘）

```bash
python demo_v2.py --mode=ingest \
  --structured data/raw/structured/agriculture_data.csv \
  --unstructured data/raw/unstructured/agriculture_text.txt \
  --processed_out_struct data/processed/structured_result.json \
  --processed_out_text data/processed/unstructured_result.json \
  --embeddings_out data/embeddings/index
```

完成后将生成：
- 处理结果：`data/processed/structured_result.json`、`data/processed/unstructured_result.json`
- 向量索引：`data/embeddings/index.index`、`data/embeddings/index.metadata`

3) 检索阶段（加载→检索→可选LLM回答）

```bash
# 直接检索（相似实体查询，不触发数据处理/抽取）
python demo_v2.py --mode=query \
  --processed_out_struct data/processed/structured_result.json \
  --processed_out_text data/processed/unstructured_result.json \
  --embeddings_out data/embeddings/index

# 带LLM回答（单问）
python demo_v2.py --mode=query --question "如何防治稻瘟病？"

# 带LLM回答（批量问题，每行一问）
python demo_v2.py --mode=query --questions_file questions.txt
```

- 交互式问答：在 `--mode=query` 运行后，提示“是否尝试交互式问答?(y/N)”输入 `y`，按提示直接提问。
- 注意：LLM回答需要在 `config/config_v2.yaml` 正确配置 `openai.api_key` 与 `base_url`（如使用代理）。

4) 性能与规模优化

- 仅一次性向量化：导入阶段落盘索引；检索阶段只加载，不重复向量化。
- 减少向量规模：
  - `data_processing.structured.deduplicate: true` 启用去重。
  - 在实体入向量前仅保留关键类型（如 crop/disease/pest）。
- 向量模型：
  - 本地 `sentence_transformers`（如 `all-MiniLM-L6-v2`，384维）速度更快；
  - `ollama` 速度取决于本机模型与并发；可按需调整。

## 项目结构

```
project/
├── src/                    # 核心源码
│   ├── core/              # 系统核心
│   ├── data_processing/   # 数据处理
│   ├── knowledge_graph/   # 知识图谱
│   ├── llm_integration/   # LLM集成
│   └── embeddings/        # 向量嵌入
├── config/                # 配置文件
├── data/                  # 数据存储
├── tests/                 # 测试脚本
├── demo_v2.py            # 主演示程序
├── demo_basic.py         # 基础演示
└── setup_windows.bat     # Windows安装脚本
```

## 核心功能

1. **多模态数据处理**: 智能处理结构化、非结构化文本和图像数据
2. **知识图谱构建**: 自动构建农业领域知识图谱
3. **语义搜索**: 基于向量嵌入的智能搜索
4. **智能问答**: ChatGPT驱动的农业问答系统
5. **图谱可视化**: Neo4j支持的图谱查询和可视化

## API接口位置

- **ChatGPT API**: `src/llm_integration/openai_client.py`
- **Neo4j连接**: `src/knowledge_graph/neo4j_client.py`
- **Embedding配置**: `src/embeddings/embedding_manager.py`

## 技术栈

- **深度学习**: PyTorch, SentenceTransformers
- **图数据库**: Neo4j, NetworkX
- **大语言模型**: OpenAI GPT-3.5/4
- **向量存储**: FAISS
- **数据处理**: Pandas, PIL

## 许可证

MIT License
