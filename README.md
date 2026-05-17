# 🍱 Campus Canteen Feedback Mini Program AI Assistant

## 项目简介

本项目基于“大模型 + RAG（Retrieval-Augmented Generation）”技术，开发一个面向校园食堂反馈场景的微信小程序 AI 助手，用于复现“AI小安”的核心逻辑。

系统以微信小程序作为交互入口，学生可直接通过微信提交食堂相关问题、建议与投诉，AI助手结合知识库进行智能回复，实现“校园公共服务智能化”。

支持场景包括：

- 菜品口味反馈
- 食品卫生投诉
- 菜价建议
- 营业时间查询
- 排队情况反馈
- 特殊饮食需求咨询
- 食堂公告查询
- 历史记录查询

项目重点研究：

- 大模型在校园公共服务中的应用
- RAG知识检索准确性
- 幻觉（Hallucination）控制机制
- AI小安模式在高校场景中的可复制性

---

# 🧠 项目目标

1. 开发一个基于微信小程序的食堂反馈 AI 助手
2. 实现“大模型 + RAG”的智能问答流程
3. 实践 Prompt Engineering 技术
4. 构建校园食堂知识库
5. 分析大模型在校园治理中的实际效果

---

# 🛠 技术栈

| 模块 | 技术 |
|---|---|
| 前端 | 微信小程序（WXML + WXSS + JavaScript） |
| 后端 | Python + Flask/FastAPI |
| 大模型框架 | LangChain |
| 大语言模型 | Qwen-7B（本地部署） |
| 向量数据库 | ChromaDB |
| 数据处理 | Sentence Transformers / BGE Embedding |
| 数据通信 | REST API |

---

# 📱 小程序功能

## （1）智能问答

学生可直接提问：

> “今天二食堂还有低糖套餐吗？”

AI助手结合知识库生成回答。

---

## （2）食堂反馈提交

支持：

- 卫生问题反馈
- 菜品建议
- 服务态度投诉
- 排队情况反馈

并自动分类记录。

---

## （3）公告查询

例如：

- 食堂营业时间
- 临时停业通知
- 新菜品公告

---

## （4）历史记录

保存用户历史提问与反馈内容。

---

# 📦 项目结构

```bash
an_AI/
│
├── miniapp/                  # 微信小程序前端
│   ├── pages/
│       ├── index/
│       ├── feedback/
│   ├── components/
│   ├── utils/
│   └── app.js
│
├── backend/                  # Python后端
│   ├── api/
│   ├── rag/
│   ├── prompt/
│   ├── model/
│   └── app.py
│
├── database/
│   ├── canteen_docs/
│   └── chroma_db/
│
├── evaluation/
│   ├── hallucination_test.py
│   └── accuracy_eval.py
│
├── requirements.txt
└── README.md