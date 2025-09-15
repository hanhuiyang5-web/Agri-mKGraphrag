# -*- coding: utf-8 -*-
"""
Agri-mGraphrag V2 完整演示
集成ChatGPT API、Neo4j数据库和Embedding模型的智慧农业知识图谱问答系统演示
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import logging
import argparse
import json
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from src.core.agri_system_v2 import AgriMGraphragV2
except ImportError as e:
    print(f"Import error: {e}")
    print("请确保所有模块都已正确安装")
    sys.exit(1)




def display_banner():
    """显示系统banner"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    🌾 Agri-mGraphrag V2 🌾                  ║
║          智慧农业多模态知识图谱问答系统 完整演示                    ║
║                                                              ║
║  集成功能:                                                    ║
║    ✨ ChatGPT API (GPT-3.5/GPT-4)                            ║
║    📊 Neo4j 图数据库                                          ║
║    🔍 Embedding 向量搜索                                      ║
║    📝 多模态数据处理                                          ║
║    💡 智能问答系统                                            ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def demo_data_processing(system: AgriMGraphragV2):
    """演示数据处理功能"""
    print("\n" + "="*60)
    print("📊 数据处理演示")
    print("="*60)
    
    if not system.components_status['data_processing']:
        print("❌ 数据处理模块未初始化")
        return
    
    try:
        # 处理结构化数据
        print("\n1️⃣ 处理结构化数据 (CSV)...")
        if os.path.exists("data/raw/structured/agriculture_data.csv"):
            structured_result = system.process_agricultural_data("data/raw/structured/agriculture_data.csv", "structured")
            
            entities = structured_result.get('entities', [])
            relations = structured_result.get('relations', [])
            
            print(f"   ✓ 抽取实体: {len(entities)} 个")
            print("   示例实体:")
            for i, entity in enumerate(entities[:3]):
                print(f"     - {entity.get('name', 'N/A')} ({entity.get('type', 'N/A')})")
            
            print(f"   ✓ 抽取关系: {len(relations)} 个")
            print("   示例关系:")
            for i, relation in enumerate(relations[:3]):
                if isinstance(relation, (list, tuple)) and len(relation) >= 3:
                    print(f"     - {relation[0]} -> {relation[1]} -> {relation[2]}")
                elif isinstance(relation, dict):
                    src = relation.get('source') or relation.get('from') or relation.get('src')
                    rel = relation.get('type') or relation.get('relation')
                    dst = relation.get('target') or relation.get('to') or relation.get('dst')
                    if src and rel and dst:
                        print(f"     - {src} -> {rel} -> {dst}")
            
            return structured_result
        else:
            print("   ❌ 示例CSV文件不存在")
    
    except Exception as e:
        print(f"   ❌ 处理失败: {str(e)}")
        return None


def demo_text_processing(system: AgriMGraphragV2):
    """演示文本处理功能"""
    print("\n2️⃣ 处理非结构化文本...")
    
    try:
        if os.path.exists("data/raw/unstructured/agriculture_text.txt"):
            text_result = system.process_agricultural_data("data/raw/unstructured/agriculture_text.txt", "text")
            
            entities = text_result.get('entities', [])
            relations = text_result.get('relations', [])
            
            print(f"   ✓ 抽取实体: {len(entities)} 个")
            print("   示例实体:")
            for entity in entities[:3]:
                print(f"     - {entity.get('name', 'N/A')} ({entity.get('type', 'N/A')})")
            
            print(f"   ✓ 抽取关系: {len(relations)} 个")
            
            return text_result
        else:
            print("   ❌ 示例文本文件不存在")
    
    except Exception as e:
        print(f"   ❌ 处理失败: {str(e)}")
        return None


def demo_knowledge_graph(system: AgriMGraphragV2, processed_data_list: list):
    """演示知识图谱构建"""
    print("\n" + "="*60)
    print("🕸️  知识图谱构建演示")
    print("="*60)
    
    if not system.components_status['neo4j']:
        print("❌ Neo4j 图数据库未连接")
        print("💡 请确保Neo4j正在运行 (bolt://localhost:7687)")
        return
    
    try:
        total_entities = 0
        total_relations = 0
        
        # 构建知识图谱
        for i, data in enumerate(processed_data_list):
            if data:
                print(f"\n{i+1}️⃣ 构建知识图谱 - 数据集 {i+1}...")
                success = system.build_knowledge_graph(data)
                
                if success:
                    entities = len(data.get('entities', []))
                    relations = len(data.get('relations', []))
                    total_entities += entities
                    total_relations += relations
                    print(f"   ✓ 成功添加: {entities} 实体, {relations} 关系")
        
        # 获取图统计信息
        print(f"\n📈 知识图谱统计:")
        stats = system.get_system_status().get('graph_stats', {})
        if 'error' not in stats:
            print(f"   总节点数: {stats.get('total_nodes', 0)}")
            print(f"   总关系数: {stats.get('total_relationships', 0)}")
            
            # 实体类型分布
            entity_types = stats.get('entity_types', [])
            if entity_types:
                print("   实体类型分布:")
                for et in entity_types[:5]:
                    print(f"     - {et.get('type', 'N/A')}: {et.get('count', 0)} 个")
        else:
            print("   ❌ 无法获取图统计信息")
    
    except Exception as e:
        print(f"❌ 知识图谱构建失败: {str(e)}")


def demo_embedding_search(system: AgriMGraphragV2, processed_data_list: list):
    """演示向量搜索功能"""
    print("\n" + "="*60)  
    print("🔍 向量相似度搜索演示")
    print("="*60)
    
    if not system.components_status['embedding']:
        print("❌ Embedding模型未初始化")
        return
    
    try:
        # 添加实体embeddings
        all_entities = []
        for data in processed_data_list:
            if data and data.get('entities'):
                all_entities.extend(data['entities'])
        
        if all_entities:
            total = len(all_entities)
            print(f"\n1️⃣ 添加 {total} 个实体的向量...")
            batch_size = 200
            ok = True
            for start in range(0, total, batch_size):
                end = min(start + batch_size, total)
                print(f"   -> [{start+1}/{total}] 正在处理 {end - start} 个实体...")
                part = all_entities[start:end]
                success = system.add_embeddings(part)
                if not success:
                    ok = False
                    break
            if ok:
                print("   ✓ 向量添加成功")
            else:
                print("   ❌ 向量添加失败")
                return
        
        # 测试相似度搜索
        search_queries = [
            "粮食作物",
            "植物病害", 
            "害虫防治",
            "肥料施用"
        ]
        
        print(f"\n2️⃣ 相似度搜索测试:")
        for query in search_queries:
            print(f"\n🔎 搜索: '{query}'")
            similar_entities = system.search_similar_entities(query, k=3)
            
            if similar_entities:
                for i, entity in enumerate(similar_entities, 1):
                    name = entity.get('name', 'N/A')
                    entity_type = entity.get('type', 'N/A') 
                    similarity = entity.get('similarity', 0)
                    print(f"     {i}. {name} ({entity_type}) - 相似度: {similarity:.3f}")
            else:
                print("     未找到相关实体")
    
    except Exception as e:
        print(f"❌ 向量搜索演示失败: {str(e)}")


def demo_qa_system(system: AgriMGraphragV2):
    """演示问答系统"""
    print("\n" + "="*60)
    print("💬 智能问答系统演示")
    print("="*60)
    
    if not system.components_status['chatgpt']:
        print("❌ ChatGPT集成未配置")
        print("💡 请在 config/config_v2.yaml 中配置您的 OpenAI API密钥")
        return
    
    # 测试问题
    test_questions = [  ]
    
    try:
        print("\n🤖 AI问答测试:")
        for i, question in enumerate(test_questions, 1):
            print(f"\n❓ 问题 {i}: {question}")
            
            # 获取答案
            answer_result = system.answer_question(question, use_kg_context=True)
            
            if 'error' not in answer_result:
                answer = answer_result.get('answer', '无答案')
                print(f"💡 答案: {answer[:200]}{'...' if len(answer) > 200 else ''}")
            else:
                print(f"❌ 回答失败: {answer_result['error']}")
    
    except Exception as e:
        print(f"❌ 问答系统演示失败: {str(e)}")


def demo_system_status(system: AgriMGraphragV2):
    """显示系统状态"""
    print("\n" + "="*60)
    print("📊 系统状态总览")
    print("="*60)
    
    status = system.get_system_status()
    
    print(f"\n系统: {status['system_name']} v{status['version']}")
    
    print(f"\n组件状态:")
    components = {
        'data_processing': '数据处理',
        'embedding': '向量模型',
        'neo4j': 'Neo4j数据库', 
        'chatgpt': 'ChatGPT集成'
    }
    
    for key, name in components.items():
        status_icon = "✅" if status['components'].get(key, False) else "❌"
        print(f"  {status_icon} {name}")
    
    print(f"\n可用功能:")
    for feature in status['available_features']:
        print(f"  ✨ {feature}")
    
    # 图数据库统计
    if 'graph_stats' in status and 'error' not in status['graph_stats']:
        stats = status['graph_stats']
        print(f"\n知识图谱统计:")
        print(f"  📊 节点总数: {stats.get('total_nodes', 0)}")
        print(f"  🔗 关系总数: {stats.get('total_relationships', 0)}")


def interactive_qa_demo(system: AgriMGraphragV2):
    """交互式问答演示"""
    if not system.components_status['chatgpt']:
        return
        
    print("\n" + "="*60)
    print("🗣️  交互式问答 (输入 'quit' 退出)")
    print("="*60)
    
    while True:
        try:
            question = input("\n❓ 请输入您的农业问题: ").strip()
            
            if question.lower() in ['quit', 'exit', '退出', 'q']:
                print("👋 再见!")
                break
                
            if not question:
                continue
                
            print("🤖 AI正在思考...")
            
            answer_result = system.answer_question(question, use_kg_context=True)
            
            if 'error' not in answer_result:
                answer = answer_result.get('answer', '抱歉，我无法回答这个问题。')
                print(f"\n💡 答案:\n{answer}")
            else:
                print(f"❌ 回答失败: {answer_result['error']}")
                
        except KeyboardInterrupt:
            print("\n👋 再见!")
            break
        except Exception as e:
            print(f"❌ 发生错误: {str(e)}")


def main():
    """主演示函数"""
    display_banner()
    
    try:
        parser = argparse.ArgumentParser(description="Agri-mGraphrag V2 Demo")
        parser.add_argument("--mode", choices=["ingest", "query"], default="ingest", help="运行模式：导入或检索")
        parser.add_argument("--structured", default="data/raw/structured/agriculture_data.csv", help="结构化数据路径")
        parser.add_argument("--unstructured", default="data/raw/unstructured/agriculture_text.txt", help="非结构化文本路径")
        parser.add_argument("--processed_out_struct", default="data/processed/structured_result.json", help="结构化结果输出")
        parser.add_argument("--processed_out_text", default="data/processed/unstructured_result.json", help="文本结果输出")
        parser.add_argument("--embeddings_out", default="data/embeddings/index", help="向量索引前缀")
        parser.add_argument("--question", default="", help="单条检索问题（启用LLM回答）")
        parser.add_argument("--questions_file", default="", help="批量问题文件(每行一问)（启用LLM回答）")
        args = parser.parse_args()
        # 使用用户提供的数据文件
        print("📋 使用用户数据进行演示...")
        
        # 初始化系统
        print("\n🔧 初始化系统...")
        system = AgriMGraphragV2()
        
        # 初始化所有组件
        print("⚙️ 初始化组件...")
        components_status = system.initialize_all_components()
        
        # 显示系统状态
        demo_system_status(system)
        
        processed_data_list = []
        if args.mode == "ingest":
            # 处理并保存
            print("\n== 导入阶段 ==")
            if os.path.exists(args.structured):
                sd = system.process_agricultural_data(args.structured, "structured")
                processed_data_list.append(sd)
                try:
                    os.makedirs(os.path.dirname(args.processed_out_struct), exist_ok=True)
                    with open(args.processed_out_struct, 'w', encoding='utf-8') as f:
                        json.dump(sd, f, ensure_ascii=False)
                    print(f"已保存结构化处理结果: {args.processed_out_struct}")
                except Exception as e:
                    print(f"保存结构化结果失败: {e}")

            if os.path.exists(args.unstructured):
                td = system.process_agricultural_data(args.unstructured, "text")
                processed_data_list.append(td)
                try:
                    os.makedirs(os.path.dirname(args.processed_out_text), exist_ok=True)
                    with open(args.processed_out_text, 'w', encoding='utf-8') as f:
                        json.dump(td, f, ensure_ascii=False)
                    print(f"已保存文本处理结果: {args.processed_out_text}")
                except Exception as e:
                    print(f"保存文本结果失败: {e}")

            # 入图
            demo_knowledge_graph(system, processed_data_list)
        
            # 生成并保存向量索引
            if processed_data_list and system.components_status['embedding']:
                all_entities = []
                for d in processed_data_list:
                    all_entities.extend(d.get('entities', []))
                if all_entities:
                    print(f"\n生成向量索引，共 {len(all_entities)} 个实体...")
                    system.add_embeddings(all_entities)
                    try:
                        os.makedirs(os.path.dirname(args.embeddings_out), exist_ok=True)
                        system.embedding_manager.save_embeddings(args.embeddings_out)
                        print(f"已保存向量索引: {args.embeddings_out}(.index/.metadata)")
                    except Exception as e:
                        print(f"保存向量索引失败: {e}")

        else:  # query
            print("\n== 检索阶段 ==")
            # 加载处理结果
            cached = []
            for p in [args.processed_out_struct, args.processed_out_text]:
                if os.path.exists(p):
                    try:
                        with open(p, 'r', encoding='utf-8') as f:
                            cached.append(json.load(f))
                    except Exception as e:
                        print(f"加载 {p} 失败: {e}")
            if not cached:
                print("未找到已保存的处理结果，请先使用 --mode=ingest 运行。")
            else:
                # 加载向量索引
                if system.components_status['embedding']:
                    try:
                        system.embedding_manager.load_embeddings(args.embeddings_out)
                        print(f"已加载向量索引: {args.embeddings_out}")
                    except Exception as e:
                        print(f"加载向量索引失败: {e}")
                # 直接检索演示（不触发LLM）
                demo_embedding_search(system, cached)

                # LLM 辅助检索与回答（不重复数据处理）
                questions = []
                if args.question.strip():
                    questions.append(args.question.strip())
                if args.questions_file and os.path.exists(args.questions_file):
                    try:
                        with open(args.questions_file, 'r', encoding='utf-8', errors='ignore') as f:
                            questions.extend([q.strip() for q in f if q.strip()])
                    except Exception as e:
                        print(f"加载问题文件失败: {e}")

                if questions:
                    if not system.components_status['chatgpt']:
                        print("❌ ChatGPT未配置，无法进行LLM回答。")
                    else:
                        print("\n== LLM 辅助问答 ==")
                        for i, q in enumerate(questions, 1):
                            print(f"\n❓ 问题 {i}: {q}")
                            ans = system.answer_question(q, use_kg_context=True)
                            if 'error' not in ans:
                                print(f"💡 答案: {ans.get('answer', '')[:200]}{'...' if len(ans.get('answer',''))>200 else ''}")
                            else:
                                print(f"❌ 回答失败: {ans['error']}")
        
        # 交互式问答
        if system.components_status['chatgpt']:
            try_interactive = input("\n🤔 是否尝试交互式问答? (y/N): ").strip().lower()
            if try_interactive in ['y', 'yes', '是', 'Y']:
                interactive_qa_demo(system)
        
        print("\n" + "="*60)
        print("🎉 Agri-mGraphrag V2 演示完成!")
        print("="*60)
        
        # 清理资源
        system.cleanup()
        
    except KeyboardInterrupt:
        print("\n\n👋 演示被用户中断")
    except Exception as e:
        print(f"\n❌ 演示过程中发生错误: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()