---
name: testcase-generator
description: >-
  Generates professional test points from a PRD/OpenAPI. Default flow: Step 0a
  RAG retrieval, universal coverage matrix, case IDs, review table, and open
  questions. Use when the user asks to generate test cases, test points, or a
  testcase markdown from requirements — before writing automation scripts.
---

# Test case generation (professional)

Generate **PASS/FAIL–decidable** test points from requirements. Deliver only in the format below and follow these rules completely.

## Quick start

```text
@testcase-generator/SKILL.md
@requirements.md
(optional) @openapi.yaml
Generate test cases → output booking_system/test_cases/<module>_testcases.md
```

**Default flow runs RAG before writing cases** (Step 0a). The agent should run (when the rag script exists in the skills pack):

```bash
cd skills-专业版V3.0
python3 testcase-skills/生成/scripts/rag_prefetch.py templates/requirements.md \
  --out output/rag_context_<module>.md
```

Fold the “knowledge-base retrieval summary” into generation context. If nothing hits, continue and mark `RAG: no hits` in document info.

> In this AI-playwright repo, if RAG scripts are unavailable, skip the script, write `RAG: no hits` (or `RAG: skipped — script not in repo`), and continue with PRD + matrix only.

---

## Core principles

### 1. A test point ≠ a feature description

See `references/test_point_validation.md`. Before writing, ask three questions: Does it verify behavior? Can it PASS/FAIL? Is the expected result explicit?

### 2. Moderate hierarchy

See `references/hierarchy_patterns.md` (2 / 3 / 4 levels).

### 3. Checkpoint format

See `references/checkpoint_format.md`. Do **not** use “Precondition / Steps / Expected” labels as the checkpoint style.

### 4. PRD vs universal matrix

| Source | Rule |
|--------|------|
| **Explicitly in the PRD** | Must cover |
| **Triggered by the universal matrix** | Must have a point **or** a `T-xx (to clarify)` placeholder |
| **Not in PRD and not triggered by matrix** | Do not invent features |

Do not guess business rules; if unclear, add an open question — see `references/delivery_standard.md`.

### 5. Coverage dimensions

Positive, negative, boundary, state/time, permission; also scan `references/universal_coverage_matrix.md`.

---

## Workflow

### Step 0a: RAG knowledge retrieval (required before analysis)

Before reading the PRD and writing points, retrieve team history from the `rag-engine` knowledge base when available. Details: `references/rag_knowledge.md`.

1. **Build query terms**: module name, PRD title, API names, business nouns.
2. **Run retrieval** (prefer script when available):
   ```bash
   python3 testcase-skills/生成/scripts/rag_prefetch.py <requirements.md> --top-k 5 \
     --out output/rag_context_<module>.md
   ```
   Or: `cd rag-engine/scripts && python3 rag_search.py "<query>" --top-k 5`
3. **Absorption rules**:
   - Retrieved `[case]` / `[bug]` / `[best_practice]` may add test points — **cite the source** in the checkpoint or traceability table (e.g. “RAG — auth design”).
   - Conflicts with PRD → do not adopt; put in the open-questions list.
   - **No hits** → do not block; document info: `RAG: no hits`; continue with PRD + matrix only.
4. **Output**: a “Knowledge-base retrieval summary” (see Step 5 template) for Step 4.

---

### Step 0b: Requirements pre-analysis (raw PRD required)

If a structured `func_list.md` already exists, skip to Step 1.

1. **Structure**: keep PRD heading levels → `references/structure_preservation.md`
2. **Core flows**: tree of 10–15 steps → `references/core_flows.md`
3. **Function points**: `- condition` + `Expected:` → `references/requirement_patterns.md`
4. **Threshold list**: extract all comparators / counts / times → for Step 4 boundaries and matrix dimension E
5. **Pre-analysis self-check**: all PRD sections covered; consistent terminology

If a **detailed design docx** exists: load `references/seckill_detailed_design_inputs.md`, extract §4 APIs and §3 flows; output UI cases in a separate chapter (IDs from 301+).  
If a **seckill/finance detailed design** exists: load `examples/tech_mini_seckill.md`; cover the Step 0 checklist line by line; do not expand only API + console templates and skip chapters.

If OpenAPI exists: record the endpoint list for Step 4 (`references/api_contract_supplement.md`).

If **UI/API automation cases** are requested: read `references/automation_generation_gate.md` first, then load `references/automation_*.md` as needed.

---

### Step 1: Analyze requirements

Decide: whether core flows exist, complexity (2/3/4 levels), module split, which matrix dimensions will fire.

---

### Step 2: Core-flow tests

If core flows exist, generate them first → `references/core_flow_testing.md`  
`### Flow N:` + tree aligned with `func_list`; IDs `F-01`…

---

### Step 3: Choose hierarchy

| Type | Structure |
|------|-----------|
| Simple | H2 → H3 |
| Standard | H2 → H3 → H4 |
| Complex | H2 → H3 → H4 → H5 |

---

### Step 4: Generate detailed test points

For each feature/scenario:

1. Write checkpoints from PRD function points (verification-sentence style)
2. **Boundaries**: PRD thresholds → trio (`references/boundary_value_testing.md`)
3. **Time/state**: → `references/time_and_state.md`
4. **Universal coverage matrix**:
   - Load `references/universal_coverage_matrix.md`
   - For each triggered dimension A–G: write a checkpoint or `T-xx to clarify`
   - If OpenAPI exists, add dimension H via `references/api_contract_supplement.md`
   - For security/performance packs, load `references/appendix_security.md` / `references/appendix_performance.md`
5. **IDs and priority**: assign `L-` / `D-` / `C-` / `V-` / `P-` and P0–P3 per `references/delivery_standard.md`
6. **Review-table name (Description)**: for Web / UI modules, the “Name” column must include `{product} > {page} > {feature}` (see `delivery_standard.md` §4.2.1). H4 titles may be short; the review table uses the full path.

---

### Step 5: Output (delivery standard)

Default path in this repo: `booking_system/test_cases/<module>_testcases.md`

```markdown
# [Module] test cases

## Document info
- Based on requirements:
- Generator version: rules 1.2.0 (skills V3 · testcase-generator)
- RAG retrieval: N hits / no hits (query terms: …)
- Scope:
- Structure notes:
- Open questions total: N

## Knowledge-base retrieval summary

(Step 0a output; if none: “RAG: no hits”)

## Requirements traceability

| Requirement section | Case ID | Notes |

## Core-flow tests

### Flow 1: …

## Detailed feature tests

## Case review table

| ID | Name | Priority | Type | Tags |

## Universal coverage matrix self-check

(Copy the matrix checklist from universal_coverage_matrix.md)

## Open questions

| # | Question | Related IDs |
```

---

### Step 6: Self-check and revise (must edit the draft)

#### Check 1: Test-point format

`references/test_point_validation.md` — remove “supports / needs to pass” phrasing.

#### Check 2: Boundaries

Every PRD threshold: -1 / boundary / +1; time windows in three states.

#### Check 3: PRD coverage

Every `func_list` function point has a matching case ID.

#### Check 4: Core-flow structure

Matches the `func_list` tree.

#### Check 5: Universal coverage matrix

Matrix A–I checklist filled; every triggered row has a point or `T-xx`.

#### Check 6: Delivery standard

- Review table complete
- No duplicate IDs
- P0 share reasonable (≤ 20%)
- Open questions summarized

#### Check 7: Page / menu path (Web / UI)

- Review-table “Name” contains ` > ` page path, or maps 1:1 to `##` / `###` headings
- Pure API modules may use `EventHub > API > …`

**Hard gate (run when validator exists):**

```bash
python3 testcase-skills/生成/scripts/step6_validator.py output/<module>_testcases.md
# exit: 0=pass | 1=P0 block | 2=P1 suggest | 3=P2 polish
# P0 must be fixed before review; P1 preferred before review
```

---

## Boundary quick reference

| Requirement | Must test |
|-------------|-----------|
| X > N | N+1, N, N-1 |
| min–max | min-1, min, min+1, max-1, max, max+1 |
| Limit of N times | N-1, N, N+1 |

---

## Reference docs (load when needed)

| File | When |
|------|------|
| `references/rag_knowledge.md` | Step 0a (required) |
| `references/universal_coverage_matrix.md` | Step 4, 6 (required) |
| `references/delivery_standard.md` | Step 5, 6 (required) |
| `references/test_point_validation.md` | Every checkpoint |
| `references/core_flow_testing.md` | Step 2 |
| `references/time_and_state.md` | Time / state / counts |
| `references/api_contract_supplement.md` | When OpenAPI exists |
| `references/appendix_security.md` | Security pack |
| `references/appendix_performance.md` | Performance pack |
| `references/automation_generation_gate.md` | UI/API automation entry |
| `references/checkpoint_format.md` | Step 4 |
| `references/boundary_value_testing.md` | Numeric boundaries |

> Full Chinese pack paths live under the external skills V3 tree. This English skill is the control file for this repo; load sibling `references/` when present.

---

## Quality checklist (before delivery)

- [ ] Step 0a RAG done (or “no hits” / “skipped” noted)
- [ ] Matrix self-check + review table + open questions present
- [ ] Every test point is PASS/FAIL decidable
- [ ] Requirements traceability complete
- [ ] Boundaries and triggered matrix rows covered
- [ ] No invented features outside the PRD
- [ ] Web/UI: review-table names include page path (` > `)

---

## Pipeline

| Stage | Skill |
|-------|--------|
| Plan | `testcase-skills/planning` |
| Analyze | `testcase-skills/analysis` (≈ Step 0b; RAG is Step 0a) |
| **Generate** | **This skill** → `*_testcases.md` (full · for review/archive) |
| **UI slim** | `testcase-skills/UI-slim` → `*_ui_cases.md` (automation input) |
| Review | `testcase-skills/review` |
| UI transform | `UI-skills/transform` → spec → pytest |

API automation: see `api-skills/` / `generate.sh` (OpenAPI → pytest).

## Deprecated

~~`testcase_generator.py`~~ — do not use; use this skill only.

---

## This repo (EventHub / AI-playwright)

1. **Test cases first** — write `booking_system/test_cases/<module>_testcases.md` with this skill.
2. Do **not** write Playwright/API scripts until the user approves the case doc.
3. User owns expected results / asserts; if unclear, add open questions (`T-xx`), do not invent.
4. Product path example: `EventHub > Login > Sign In`.
