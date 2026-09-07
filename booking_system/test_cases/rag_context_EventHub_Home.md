## 知识库检索摘要（RAG · 生成前必做）

- **检索词**：EventHub — Home (observed UI scope) 测试用例 业务规则 验收标准 边界
- **命中条数**：5
- **使用规则**：以下片段仅作补充；与 PRD 冲突时以 PRD 为准，并在待澄清清单记录。

【RAG 检索结果】
1. [bug] bug sample seckill redis - 实际结果: bug sample seckill redis 实际结果 
- HTTP 500，响应为通用 Internal Server Error。
- 服务端日志含 Redis connection refused。

2. [bug] bug sample seckill redis - 分流建议: bug sample seckill redis 分流建议 
- [ ] 环境（先启动 Redis：`redis-server` 或 Docker）
- [x] 产品待确认（失败时的错误码与文案）
- [ ] 脚本自愈

3. [case] output seckill auth testcases - 核心流程测试: output seckill auth testcases 核心流程测试 
### 流程1：新用户注册并登录查 Profile

```
- 访客调用 POST /api/auth/register（合法 username/password/email）
  - 预期：HTTP 201，返回用户标识或成功语义
- 使用新账号 POST /api/auth/login
  - 预期：HTTP 200，响应含 JWT（access_token 或 token 字段）
- 携带 Bearer Token GET /api/auth/profile
  - 预期：HTTP 200，username 与注册一致，role 为 customer
```

4. [skill_doc] 规划/SKILL.md: testcase-skills 规划/SKILL.md ---
name: testcase-planner
description: Defines overall test scope, strategy, risk-driven cuts, and schedule before detailed cases. Use when requirements are coarse or multi-team coordination is needed.
---

# 测试规划 — 范围、策略与节奏

需求还粗、**分析**还没往下拆的时候，先用这篇把**测哪些、大概多久、先动哪块**说清楚，方便排期和拉人。产出给评审会和资源协调用，不是替代具体
5. [general] spec seckill api smoke.filled - 用例说明: spec seckill api smoke.filled 用例说明 
| ID | 接口 | 说明 |
|----|------|------|
| TC-SECKILL-PROD-LIST-001 | GET /api/products | 匿名拉在售商品列表 |
| TC-SECKILL-PROD-CREATE-001 | POST /api/products | 管理员创建商品（需 JWT） |

首次无 admin 时可：`curl -X POST http://your-server:5000/api/test/init -H "Content-Type: application/json" -d "{\"admin_password\":\"admin
