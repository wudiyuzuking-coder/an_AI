# 校园食堂 AI 助手

## 项目简介

本项目基于"大模型 + RAG（Retrieval-Augmented Generation）"技术，开发一个面向校园食堂反馈场景的微信小程序 AI 助手。学生可通过小程序提交食堂相关问题、建议与投诉，AI助手结合知识库进行智能回复，实现校园公共服务智能化。

---

## 技术栈

| 模块 | 技术 |
|---|---|
| 前端 | 微信小程序（WXML + WXSS + JavaScript） |
| 后端 | Python + FastAPI |
| 大模型 | Qwen3-1.7B（通过 Ollama 本地部署） |
| 向量数据库 | ChromaDB |
| Embedding模型 | BAAI/bge-small-zh-v1.5 |
| 文本处理 | LangChain |
| 数据通信 | REST API |

---

## 项目结构

```
an_AI/
├── backend/                  # Python后端
│   ├── app.py                # FastAPI主服务
│   ├── model/
│   │   └── llm_client.py     # Ollama大模型客户端
│   ├── prompt/
│   │   └── templates.py      # Prompt模板
│   ├── rag/
│   │   └── vector_service.py # RAG向量化与检索
│   ├── test_rag_pipeline.py  # RAG全链路测试
│   ├── test_classify.py      # 反馈分类测试
│   └── test_feedback_classify.py  # 反馈分类批量测试
│
├── miniapp/                  # 微信小程序前端
│   ├── app.js                # 小程序入口
│   ├── app.json              # 全局配置（含tabBar）
│   ├── project.config.json   # 项目配置
│   ├── images/               # tabBar图标
│   └── pages/
│       ├── index/            # 智能问答页面
│       │   ├── index.js
│       │   ├── index.wxml
│       │   ├── index.wxss
│       │   └── index.json
│       └── feedback/         # 意见反馈页面
│           ├── feedback.js
│           ├── feedback.wxml
│           ├── feedback.wxss
│           └── feedback.json
│
├── database/
│   ├── canteen_docs/
│   │   └── rules.txt         # 食堂公告知识库
│   └── chroma_db/            # 向量数据库（自动生成）
│
├── evaluation/
│   ├── accuracy_eval.py      # 分类准确率评估
│   └── hallucination_test.py # 抗幻觉率评估
│
├── requirements.txt
└── README.md
```

---

## 核心功能

### 1. 智能问答（RAG）

学生可直接提问，AI助手结合知识库生成回答：

- "今天二食堂还有低糖套餐吗？"
- "一食堂二楼档口为什么关门了？"

**技术实现：**
- 文档切分：RecursiveCharacterTextSplitter（按换行符切分，chunk_size=100）
- 向量化：BGE-small-zh-v1.5 模型
- 检索：ChromaDB 相似度搜索（k=2）
- 生成：Qwen3-1.7B，temperature=0.1 控制随机性
- 抗幻觉：严格Prompt限制，不知道就说不知道

### 2. 反馈提交与自动分类

学生提交投诉/建议，大模型自动分类：

| 分类 | 示例 |
|------|------|
| 食品卫生 | "餐具上全是油，根本没洗干净" |
| 菜品口味 | "红烧肉太咸了" |
| 菜价建议 | "素菜都卖5块钱了" |
| 服务态度 | "打菜阿姨态度差，冲我翻白眼" |
| 其他建议 | "建议加装排队隔离带" |

### 3. 时间感知

后端动态注入当前日期，使模型能理解"今天"的含义，准确回答时间相关问题。

---

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | /api/chat | RAG智能问答 |
| POST | /api/feedback | 反馈提交与自动分类 |

---

## 快速开始

### 后端启动

```bash
# 进入backend目录
cd backend

# 激活虚拟环境
venv\Scripts\activate

# 启动服务
python app.py
```

服务运行在 http://127.0.0.1:8080

### 小程序联调

1. 打开微信开发者工具
2. 导入 `miniapp/` 目录
3. 勾选"不校验合法域名"
4. 在模拟器中测试

---

## 评估指标

### 分类准确率

- 测试样本：8条
- 准确率：**100%**

### 抗幻觉拦截率

- 越界提问测试：5条
- 拦截率：**100%**

---

## 注意事项

- 确保 Ollama 已安装并下载 qwen3:1.7b 模型
- 首次运行会自动下载 BGE 嵌入模型
- 模型缓存路径已配置为无中文字符路径
