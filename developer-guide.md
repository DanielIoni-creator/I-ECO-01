# 👨‍💻 开发者指南 - MyZubster

## 1. 系统要求

- Node.js 20+
- npm 10+
- Git

## 2. 安装步骤

```bash
git clone https://github.com/DanielIoni-creator/I-ECO-01.git
cd I-ECO-01
npm install

# 启动网关 (端口 3001)
cd gateway
npm start

# 启动门户 (端口 3002)
cd ../portal 
npm start
. 项目结构
text

I-ECO-01/
├── gateway/        # API网关 (端口 3001)
├── portal/         # Web门户 (端口 3002)
├── discord-bot/    # Discord机器人
├── mvp/            # 文档和Legal
└── china-version/  # 中国版本

4. 贡献指南

    Fork仓库

    创建功能分支

    提交代码

    创建Pull Request

5. 赏金系统

查看可用赏金：
bash

gh issue list --state open --label "bounty"

👽 Pytho说: "每一行代码都是对未来的贡献!"
text


**Salva con Ctrl+O, Invio, poi Ctrl+X**

---

```bash
# 2. Crea Guida Utente
nano user-guide.md

COPIA E INCOLLA QUESTO CONTENUTO:
markdown

# 🌿 用户指南 - MyZubster

## 1. 注册和登录

1. 访问 http://localhost:3002
2. 点击"注册"创建账号
3. 使用邮箱和密码登录

## 2. 浏览植物

- 查看已注册的植物
- 按时代筛选（1500, 1800, 2124）
- 搜索特定物种

## 3. 探索矿物

- 查看矿物目录
- 按时代筛选
- 了解矿物的特性和用途

## 4. 时间旅行

- 选择目的地和时代
- 开始时间旅行
- 发现新的植物和矿物

## 5. 支付

- 查看钱包余额
- 创建支付请求
- 使用MYZ或XMR支付

---

*👽 Pytho说: "探索绿色未来的旅程从今天开始!"*

Salva con Ctrl+O, Invio, poi Ctrl+X
bash

# 3. Crea Guida WeChat
cd /opt/I-ECO-01/china-version
nano wechat-guide.md

COPIA E INCOLLA QUESTO CONTENUTO:
markdown

# 📱 微信指南 - MyZubster

## 1. 创建微信公众号

1. 访问 https://mp.weixin.qq.com/
2. 注册为"订阅号"
3. 名称: MyZubster (米祖斯特)

## 2. 内容策略

### 每周发布计划

**周一: 技术分享**
- 介绍MyZubster功能
- 技术文章翻译

**周三: 植物/矿物知识**
- 分享发现的植物和矿物
- 历史文化故事

**周五: 社区更新**
- 项目进展
- 新功能发布

## 3. 互动方式

- 回复关键词获取信息
- 投票决定下一个功能
- 用户反馈收集

---

*👽 Pytho说: "微信是连接中国社区的桥梁!"*

Salva con Ctrl+O, Invio, poi Ctrl+X
bash

# 4. Crea Guida Gitee
nano gitee-guide.md

COPIA E INCOLLA QUESTO CONTENUTO:
markdown

# 📦 Gitee 指南 - MyZubster

## 1. 注册Gitee账号

访问 https://gitee.com 注册账号

## 2. 导入仓库

```bash
# 在Gitee上点击"从GitHub导入"
# 输入: https://github.com/DanielIoni-creator/I-ECO-01.git
# 名称: myzubster

3. 保持同步
bash

# 添加远程仓库
git remote add gitee https://gitee.com/你的用户名/myzubster.git

# 推送更新
git push gitee main

4. 中国用户使用

中国用户可以通过Gitee克隆:
bash

git clone https://gitee.com/你的用户名/myzubster.git

👽 Pytho说: "Gitee让中国开发者更便捷!"


