# -*- coding: utf-8 -*-
"""
Agri-mGraphrag V2 基础演示
展示核心功能，无需外部API和数据库
"""

import os
import sys
import json
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def display_banner():
    """显示系统banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                🌾 Agri-mGraphrag V2 基础演示 🌾                ║
║          智慧农业多模态知识图谱问答系统 核心功能展示          ║
║                                                              ║
║  演示内容:                                                    ║
║    📊 数据处理能力                                           ║
║    🕸️  知识图谱构建                                          ║
║    🔍 知识检索                                               ║
║    💡 系统架构展示                                           ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


class MockAgriDataProcessor:
    """模拟农业数据处理器"""
    
    def __init__(self):
        # 农业实体类型
        self.entity_types = {
            'crop': '作物',
            'disease': '病害', 
            'pest': '虫害',
            'fertilizer': '肥料',
            'pesticide': '农药',
            'soil': '土壤',
            'climate': '气候',
            'technology': '技术',
            'equipment': '设备'
        }
        
        # 关系类型
        self.relation_types = {
            'grows_in': '生长在',
            'infected_by': '感染',
            'damaged_by': '危害',
            'uses': '使用',
            'prevents': '防治',
            'suitable_for': '适用于'
        }
        
        # 农业知识规则
        self.knowledge_rules = {
            '水稻': {'type': 'crop', 'diseases': ['稻瘟病'], 'pests': ['稻飞虱'], 'fertilizers': ['尿素']},
            '小麦': {'type': 'crop', 'diseases': ['小麦锈病'], 'pests': ['蚜虫'], 'fertilizers': ['磷酸二铵']},
            '玉米': {'type': 'crop', 'diseases': ['玉米螟'], 'pests': ['玉米螟'], 'fertilizers': ['复合肥']},
            '稻瘟病': {'type': 'disease', 'affects': ['水稻'], 'preventions': ['三环唑']},
            '三环唑': {'type': 'pesticide', 'prevents': ['稻瘟病']},
            '尿素': {'type': 'fertilizer', 'used_for': ['水稻', '小麦']},
            '水田': {'type': 'soil', 'suitable_for': ['水稻']},
            '温带': {'type': 'climate', 'suitable_for': ['水稻', '小麦']}
        }
    
    def extract_entities_from_text(self, text: str):
        """从文本中抽取实体"""
        entities = []
        relations = []
        
        # 简单的关键词匹配
        for entity_name, info in self.knowledge_rules.items():
            if entity_name in text:
                entity = {
                    'id': f"{info['type']}_{len(entities)+1:03d}",
                    'name': entity_name,
                    'type': info['type'],
                    'description': f"{self.entity_types.get(info['type'], '未知类型')}: {entity_name}"
                }
                entities.append(entity)
                
                # 生成关系
                if 'diseases' in info:
                    for disease in info['diseases']:
                        if disease in text:
                            relations.append((entity_name, 'infected_by', disease))
                
                if 'prevents' in info:
                    for prevented in info['prevents']:
                        if prevented in text:
                            relations.append((entity_name, 'prevents', prevented))
                
                if 'used_for' in info:
                    for crop in info['used_for']:
                        if crop in text:
                            relations.append((entity_name, 'uses', crop))
        
        return {
            'entities': entities,
            'relations': relations,
            'text_length': len(text),
            'processing_method': 'rule_based_extraction'
        }
    
    def process_structured_data(self, data_dict):
        """处理结构化数据"""
        entities = []
        relations = []
        
        for record in data_dict.get('records', []):
            # 为每个字段创建实体
            for field, value in record.items():
                if value and value.strip():
                    # 推断实体类型
                    entity_type = self._infer_entity_type(field, value)
                    entity = {
                        'id': f"{entity_type}_{len(entities)+1:03d}",
                        'name': value,
                        'type': entity_type,
                        'description': f"{self.entity_types.get(entity_type, '未知')}: {value}",
                        'source_field': field
                    }
                    entities.append(entity)
            
            # 生成关系
            if len(entities) > 1:
                # 作物与病害的关系
                crop_entities = [e for e in entities if e['type'] == 'crop']
                disease_entities = [e for e in entities if e['type'] == 'disease']
                
                for crop in crop_entities:
                    for disease in disease_entities:
                        relations.append((crop['name'], 'infected_by', disease['name']))
        
        return {
            'entities': entities,
            'relations': relations,
            'record_count': len(data_dict.get('records', [])),
            'processing_method': 'structured_data_mapping'
        }
    
    def _infer_entity_type(self, field, value):
        """推断实体类型"""
        field_lower = field.lower()
        value_lower = value.lower()
        
        if 'crop' in field_lower or '作物' in field_lower:
            return 'crop'
        elif 'disease' in field_lower or '病' in field_lower:
            return 'disease'
        elif 'pest' in field_lower or '虫' in field_lower:
            return 'pest'
        elif 'fertilizer' in field_lower or '肥' in field_lower:
            return 'fertilizer'
        elif 'soil' in field_lower or '土' in field_lower:
            return 'soil'
        elif 'climate' in field_lower or '气候' in field_lower:
            return 'climate'
        elif any(keyword in value_lower for keyword in ['病', '疫', '霉']):
            return 'disease'
        elif any(keyword in value_lower for keyword in ['虫', '螟', '蚜']):
            return 'pest'
        elif any(keyword in value_lower for keyword in ['肥', '素']):
            return 'fertilizer'
        else:
            return 'crop'  # 默认为作物


class MockKnowledgeGraph:
    """模拟知识图谱"""
    
    def __init__(self):
        self.entities = {}
        self.relations = []
        self.stats = {'node_count': 0, 'relation_count': 0}
    
    def add_entity(self, entity):
        """添加实体"""
        entity_id = entity['id']
        self.entities[entity_id] = entity
        self.stats['node_count'] = len(self.entities)
    
    def add_relation(self, relation):
        """添加关系"""
        self.relations.append(relation)
        self.stats['relation_count'] = len(self.relations)
    
    def build_from_data(self, processed_data):
        """从处理数据构建图谱"""
        # 添加实体
        for entity in processed_data.get('entities', []):
            self.add_entity(entity)
        
        # 添加关系
        for relation in processed_data.get('relations', []):
            self.add_relation(relation)
        
        return True
    
    def search_entities(self, query, limit=5):
        """搜索实体"""
        results = []
        query_lower = query.lower()
        
        for entity_id, entity in self.entities.items():
            # 简单的文本匹配
            if (query_lower in entity['name'].lower() or 
                query_lower in entity.get('description', '').lower() or
                query_lower in entity['type'].lower()):
                
                # 计算简单相似度分数
                score = 0
                if query_lower in entity['name'].lower():
                    score += 10
                if query_lower in entity.get('description', '').lower():
                    score += 5
                if query_lower in entity['type'].lower():
                    score += 3
                    
                results.append({
                    'entity': entity,
                    'score': score
                })
        
        # 按分数排序
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:limit]
    
    def get_neighbors(self, entity_name):
        """获取实体邻居"""
        neighbors = []
        
        for relation in self.relations:
            if len(relation) >= 3:
                source, rel_type, target = relation[0], relation[1], relation[2]
                
                if source == entity_name:
                    neighbors.append({
                        'entity': target,
                        'relation': rel_type,
                        'direction': 'outgoing'
                    })
                elif target == entity_name:
                    neighbors.append({
                        'entity': source, 
                        'relation': rel_type,
                        'direction': 'incoming'
                    })
        
        return neighbors
    
    def get_stats(self):
        """获取统计信息"""
        entity_type_counts = {}
        for entity in self.entities.values():
            entity_type = entity['type']
            entity_type_counts[entity_type] = entity_type_counts.get(entity_type, 0) + 1
        
        return {
            'total_entities': len(self.entities),
            'total_relations': len(self.relations),
            'entity_types': entity_type_counts
        }


class MockQASystem:
    """模拟问答系统"""
    
    def __init__(self, knowledge_graph):
        self.kg = knowledge_graph
        
        # 预定义问答模板
        self.qa_templates = {
            '什么是': self._answer_definition,
            '如何防治': self._answer_prevention,
            '什么病': self._answer_diseases,
            '用什么': self._answer_usage,
            '怎么办': self._answer_solution
        }
    
    def answer_question(self, question):
        """回答问题"""
        question_lower = question.lower()
        
        # 寻找匹配的模板
        for pattern, handler in self.qa_templates.items():
            if pattern in question_lower:
                return handler(question)
        
        # 默认搜索回答
        return self._answer_search(question)
    
    def _answer_definition(self, question):
        """定义类问题"""
        # 提取问题中的实体
        entities = self._extract_entities_from_question(question)
        if entities:
            entity = entities[0]['entity']
            return f"{entity['name']}是一种{entity.get('description', '农业相关事物')}。"
        return "抱歉，我无法理解您询问的具体内容。"
    
    def _answer_prevention(self, question):
        """防治类问题"""
        entities = self._extract_entities_from_question(question)
        if entities:
            entity_name = entities[0]['entity']['name']
            neighbors = self.kg.get_neighbors(entity_name)
            
            preventions = [n for n in neighbors if n['relation'] == 'prevents' and n['direction'] == 'incoming']
            if preventions:
                prevention_names = [p['entity'] for p in preventions]
                return f"{entity_name}可以使用{', '.join(prevention_names)}进行防治。"
            else:
                return f"目前知识库中暂无{entity_name}的具体防治方案，建议咨询农业专家。"
        return "请明确您要防治的具体病害或虫害。"
    
    def _answer_diseases(self, question):
        """病害类问题"""
        entities = self._extract_entities_from_question(question)
        if entities:
            entity_name = entities[0]['entity']['name']
            neighbors = self.kg.get_neighbors(entity_name)
            
            diseases = [n for n in neighbors if n['relation'] == 'infected_by' and n['direction'] == 'outgoing']
            if diseases:
                disease_names = [d['entity'] for d in diseases]
                return f"{entity_name}常见的病害包括：{', '.join(disease_names)}。"
            else:
                return f"知识库中暂无{entity_name}的病害信息。"
        return "请明确您询问的作物名称。"
    
    def _answer_usage(self, question):
        """使用类问题"""
        entities = self._extract_entities_from_question(question)
        if entities:
            entity_name = entities[0]['entity']['name']
            neighbors = self.kg.get_neighbors(entity_name)
            
            uses = [n for n in neighbors if n['relation'] == 'uses' and n['direction'] == 'incoming']
            if uses:
                use_names = [u['entity'] for u in uses]
                return f"{entity_name}可以使用{', '.join(use_names)}。"
            else:
                return f"知识库中暂无{entity_name}的使用信息。"
        return "请明确您询问的具体内容。"
    
    def _answer_solution(self, question):
        """解决方案类问题"""
        return self._answer_prevention(question)
    
    def _answer_search(self, question):
        """基于搜索的回答"""
        # 搜索相关实体
        search_results = self.kg.search_entities(question, limit=3)
        
        if search_results:
            entity = search_results[0]['entity']
            return f"根据知识库，与您的问题相关的是：{entity['name']}({entity.get('description', '相关农业信息')})。"
        else:
            return "抱歉，我在知识库中没有找到相关信息，建议您咨询农业专家或查阅专业资料。"
    
    def _extract_entities_from_question(self, question):
        """从问题中提取实体"""
        results = []
        for entity_id, entity in self.kg.entities.items():
            if entity['name'] in question:
                results.append({
                    'entity': entity,
                    'score': len(entity['name'])
                })
        
        results.sort(key=lambda x: x['score'], reverse=True)
        return results


def demo_data_processing():
    """演示数据处理"""
    print("\n" + "="*60)
    print("📊 数据处理演示")
    print("="*60)
    
    processor = MockAgriDataProcessor()
    
    # 文本数据处理
    print("\n1️⃣ 非结构化文本处理:")
    sample_text = """
    水稻是重要的粮食作物，容易感染稻瘟病。稻瘟病是由真菌引起的病害，
    会导致叶片出现病斑。防治稻瘟病可以使用三环唑农药。水稻生长需要
    充足的水分，适合在水田中种植。在温带气候条件下生长良好。
    """
    
    print(f"   输入文本: {sample_text.strip()[:100]}...")
    text_result = processor.extract_entities_from_text(sample_text)
    
    print(f"   ✓ 抽取实体: {len(text_result['entities'])} 个")
    for entity in text_result['entities']:
        print(f"     - {entity['name']} ({entity['type']})")
    
    print(f"   ✓ 抽取关系: {len(text_result['relations'])} 个")
    for relation in text_result['relations']:
        print(f"     - {relation[0]} -> {relation[1]} -> {relation[2]}")
    
    # 结构化数据处理
    print("\n2️⃣ 结构化数据处理:")
    sample_data = {
        'records': [
            {'crop_name': '水稻', 'disease': '稻瘟病', 'fertilizer': '尿素', 'soil': '水田'},
            {'crop_name': '小麦', 'disease': '小麦锈病', 'fertilizer': '磷酸二铵', 'soil': '旱地'},
            {'crop_name': '玉米', 'disease': '玉米螟', 'fertilizer': '复合肥', 'soil': '旱地'}
        ]
    }
    
    print(f"   输入记录: {len(sample_data['records'])} 条")
    structured_result = processor.process_structured_data(sample_data)
    
    print(f"   ✓ 抽取实体: {len(structured_result['entities'])} 个")
    entity_types = {}
    for entity in structured_result['entities']:
        entity_types[entity['type']] = entity_types.get(entity['type'], 0) + 1
    for etype, count in entity_types.items():
        type_name = processor.entity_types.get(etype, etype)
        print(f"     - {type_name}: {count} 个")
    
    return text_result, structured_result


def demo_knowledge_graph(text_result, structured_result):
    """演示知识图谱构建"""
    print("\n" + "="*60)
    print("🕸️  知识图谱构建演示")
    print("="*60)
    
    kg = MockKnowledgeGraph()
    
    # 构建知识图谱
    print("\n1️⃣ 构建知识图谱...")
    kg.build_from_data(text_result)
    kg.build_from_data(structured_result)
    
    stats = kg.get_stats()
    print(f"   ✓ 总实体数: {stats['total_entities']}")
    print(f"   ✓ 总关系数: {stats['total_relations']}")
    
    print("   实体类型分布:")
    for entity_type, count in stats['entity_types'].items():
        type_name = MockAgriDataProcessor().entity_types.get(entity_type, entity_type)
        print(f"     - {type_name}: {count} 个")
    
    # 实体搜索演示
    print("\n2️⃣ 实体搜索演示:")
    search_queries = ["水稻", "病害", "肥料"]
    
    for query in search_queries:
        print(f"\n   🔎 搜索: '{query}'")
        results = kg.search_entities(query, limit=3)
        
        if results:
            for i, result in enumerate(results, 1):
                entity = result['entity']
                score = result['score']
                print(f"     {i}. {entity['name']} ({entity['type']}) - 得分: {score}")
        else:
            print("     未找到相关实体")
    
    # 关系查询演示
    print("\n3️⃣ 关系查询演示:")
    if stats['total_entities'] > 0:
        sample_entity = list(kg.entities.values())[0]['name']
        print(f"   查询实体 '{sample_entity}' 的关系:")
        
        neighbors = kg.get_neighbors(sample_entity)
        if neighbors:
            for neighbor in neighbors:
                direction = "→" if neighbor['direction'] == 'outgoing' else "←"
                print(f"     {direction} {neighbor['relation']} {neighbor['entity']}")
        else:
            print("     该实体暂无关系")
    
    return kg


def demo_qa_system(kg):
    """演示问答系统"""
    print("\n" + "="*60)
    print("💬 智能问答系统演示")
    print("="*60)
    
    qa_system = MockQASystem(kg)
    
    # 测试问题
    test_questions = [
        "水稻容易得什么病？",
        "如何防治稻瘟病？",
        "什么是水稻？",
        "水稻用什么肥料？",
        "稻瘟病怎么办？"
    ]
    
    print("\n🤖 问答测试:")
    for i, question in enumerate(test_questions, 1):
        print(f"\n❓ 问题 {i}: {question}")
        answer = qa_system.answer_question(question)
        print(f"💡 答案: {answer}")


def demo_system_architecture():
    """演示系统架构"""
    print("\n" + "="*60)
    print("🏗️  系统架构演示")
    print("="*60)
    
    architecture = {
        "系统层次": {
            "1. 数据接入层": ["结构化数据处理", "非结构化文本处理", "图像数据处理"],
            "2. 知识抽取层": ["实体识别", "关系抽取", "属性抽取"],
            "3. 知识存储层": ["Neo4j图数据库", "向量数据库", "缓存系统"],
            "4. 知识推理层": ["图推理", "向量检索", "规则推理"],
            "5. 应用服务层": ["问答接口", "搜索接口", "管理接口"],
            "6. 用户界面层": ["Web界面", "API接口", "移动端"]
        },
        "核心技术": {
            "大语言模型": ["ChatGPT API", "本地模型", "Prompt工程"],
            "知识图谱": ["Neo4j", "图算法", "知识推理"],
            "向量检索": ["Sentence Transformers", "FAISS", "相似度搜索"],
            "数据处理": ["多模态融合", "实体链接", "知识融合"]
        },
        "Windows优化": {
            "环境兼容": ["Python 3.11/3.12", "依赖管理", "路径处理"],
            "性能优化": ["内存管理", "并发控制", "缓存策略"],
            "部署支持": ["一键安装", "配置管理", "错误处理"]
        }
    }
    
    for category, items in architecture.items():
        print(f"\n📋 {category}:")
        for key, values in items.items():
            print(f"   {key}:")
            for value in values:
                print(f"     • {value}")


def main():
    """主演示函数"""
    display_banner()
    
    try:
        # 数据处理演示
        text_result, structured_result = demo_data_processing()
        
        # 知识图谱演示
        kg = demo_knowledge_graph(text_result, structured_result)
        
        # 问答系统演示
        demo_qa_system(kg)
        
        # 系统架构演示
        demo_system_architecture()
        
        print("\n" + "="*60)
        print("🎉 Agri-mGraphrag V2 基础演示完成!")
        print("="*60)
        
        print("\n📝 接下来的步骤:")
        print("1. 配置OpenAI API密钥启用ChatGPT集成")
        print("2. 安装并启动Neo4j数据库")
        print("3. 安装sentence-transformers启用向量搜索")
        print("4. 运行完整演示: python demo_v2.py")
        
        print("\n📖 详细部署指南请查看: WINDOWS_SETUP_GUIDE.md")
        
    except Exception as e:
        print(f"\n❌ 演示过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()