# PDM学习项目 - AI辅助全栈开发

## 项目概述
这是一个通过AI辅助在3个月内构建的模块化PDM（产品数据管理）系统。项目旨在学习全栈开发（FastAPI + React + PostgreSQL）和AI集成（OCR、NLP、机器学习）。

## 项目目标
### 学习目标
1. 掌握全栈开发技能（前端 + 后端 + 数据库）
2. 学习AI工程化集成（OCR、NLP、向量搜索）
3. 实践项目管理和系统设计
4. 构建可展示的作品集项目

### 功能目标（MVP）
- ✅ 产品数据管理（CRUD）
- ✅ 文档管理（上传、版本、预览）
- ✅ BOM管理（树形结构、版本）
- ✅ 用户认证系统
- ✅ AI增强功能（文档解析、语义搜索）

## 项目状态
**开始日期**：2026年3月27日
**预期完成**：2026年6月27日（3个月）
**当前阶段**：第1周 - 环境搭建与基础框架

## 项目结构

```
pdm-project/
├── README.md                 # 项目总览
├── code/                     # 代码目录
│   ├── backend/             # FastAPI后端
│   └── frontend/            # React前端
├── docs/                    # 文档目录
│   ├── prd/                 # 产品需求文档
│   ├── design/              # 设计文档
│   ├── architecture/        # 架构文档
│   ├── adr/                 # 架构决策记录
│   ├── requirements/         # 需求文档
│   ├── test/                # 测试文档
│   ├── project/             # 项目管理
│   │   ├── plan/            # 计划文件
│   │   ├── tasks/           # 任务管理
│   │   └── progress/        # 进度跟踪
│   ├── references/          # 参考资料
│   ├── diagrams/            # 图表
│   ├── specifications/      # 规格说明
│   ├── vcs/                 # 版本控制
│   └── mbse/                # MBSE分析
└── start.sh                 # 启动脚本
```

## 快速开始

1. **环境准备**：
   ```bash
   # 安装 Docker 和 Node.js
   # 克隆项目仓库
   git clone <repository-url>
   cd pdm-project
   ```

2. **开发计划**：
   - 查看 `docs/project/plan/month-1-plan.md` 了解第一个月任务
   - 从 `docs/project/tasks/backlog.md` 选择任务开始
   - 在 `docs/project/progress/learning-notes.md` 记录学习过程

3. **学习资源**：
   - 技术栈说明：`docs/references/tech-stack.md`
   - AI提示词技巧：`docs/references/ai-prompts.md`

4. **文档索引**：
   - 项目路线图：`docs/project/plan/3-month-roadmap.md`
   - 里程碑定义：`docs/project/milestones.md`
   - 系统架构：`docs/architecture/system-architecture.md`
   - API设计：`docs/design/api-design.md`
   - 测试策略：`docs/test/test-strategy.md`

## 联系方式
- **学习方式**：AI辅助开发 + 自主学习
- **时间投入**：每天1-2小时，周末4-6小时
- **更新频率**：每周更新进度和计划

---
*本项目采用渐进式开发，优先实现核心功能，逐步添加AI能力。*