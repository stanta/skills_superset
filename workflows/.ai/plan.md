# Plan: Update `fullproject.md` for Kilo Code Workflows

## Goal
Create a structured, step-by-step plan to revise `fullproject.md` so it is compatible with Kilo Code workflows per the official guidance.

## Scope
- **In scope:** Planning the work only.
- **Out of scope:** Editing any documentation or code beyond this plan file.

## References
- Kilo Code workflows documentation: https://kilo.ai/docs/customize/workflows

## Assumptions
- `fullproject.md` is the primary workflow documentation that must align with Kilo Code expectations.
- The plan must identify gaps, specify edits to structure/commands/paths, validate links, and ensure workflow invocation guidance is accurate.

## Subtasks (Small, Clearly Scoped)

### 1) Analyze Workflow Requirements
- Review Kilo Code workflow requirements and conventions from the official documentation.
- Extract required structure, mandatory sections, expected command formats, and path conventions.
- Note any required metadata, naming, or file placement rules.

### 2) Identify Gaps in `fullproject.md`
- Read `fullproject.md` and map current sections to required workflow elements.
- Record missing or non-compliant sections, outdated instructions, and ambiguous guidance.
- Capture discrepancies in command examples, file paths, or invocation steps.

### 3) Plan Structural Updates
- Define a revised outline that matches Kilo Code workflow expectations.
- Specify which sections need to be added, removed, or reordered.
- Plan headings and cross-references to keep navigation coherent.

### 4) Plan Command and Path Corrections
- Enumerate all commands/invocations described in `fullproject.md`.
- Identify updates needed to align command syntax, flags, and path examples with Kilo Code workflows.
- Ensure command examples use correct relative paths and workspace references.

### 5) Plan Link and Invocation Validation
- List all external and internal links in `fullproject.md` for verification.
- Define how each workflow is invoked (commands, files, triggers) and ensure the plan covers any missing steps.
- Include checks for broken links or outdated references.

### 6) Plan Final Review Criteria
- Define a checklist for compliance against Kilo Code workflow requirements.
- Include readability and consistency checks (terminology, formatting, examples).
- Specify a final pass to ensure all edits are aligned with the documented workflow standards.

## Deliverables
- A detailed edit plan with mapped gaps and specific update actions.
- A final compliance checklist tailored to Kilo Code workflow requirements.

---

## 2026-02-11 — Repeatable Markdown link-audit approach (paths + `#anchors`)

### Scope
Audit Markdown links in this repository’s workflow docs (primarily under `workflows/` and `workflows/.ai/`).

This approach validates:

1. **Target paths** (relative links resolve to an existing file/directory)
2. **Fragments / anchors** (`#...`) (fragment matches a heading in the target document)

### Step 0 — Choose the entrypoint and traversal set

1. Pick a starting doc (e.g., `workflows/fullproject.md`).
2. Extract *all* Markdown links from it.
3. Follow links to other docs and **audit transitively** for the required subset (e.g., FAQ + Quick Start docs + referenced commands/agents).

### Step 1 — Extract links (repeatable)

For each audited Markdown file:

1. Collect all inline links of the form:
   - `[text](path)`
   - `[text](path#fragment)`
2. Ignore (or handle separately) non-file targets:
   - `http://`, `https://`, `mailto:`, etc.
3. Record each link with:
   - **Source file**
   - **Source line number** (for precise fixes)
   - **Raw target** (path + optional fragment)

### Step 2 — Validate target path

Given a link target `target` from `source.md`:

1. Split into:
   - `path` (everything before `#`)
   - `fragment` (everything after `#`, if any)
2. Resolve `path`:
   - If `path` is empty (e.g., `(#section)`), the target is the **same file**.
   - Otherwise, resolve **relative to the source file directory**.
3. Verify the resolved path exists in the repo.
   - If the link points to a directory (ends with `/`), confirm the directory exists.
   - If it points to a file, confirm the file exists (case-sensitive on Linux).

### Step 3 — Validate `#fragment` against headings

If a link includes `#fragment`:

1. Load the target Markdown file (or the source file if `path` is empty).
2. Collect headings:
   - ATX headings: `#`, `##`, …
   - (Optionally) Setext headings if present.
3. Compute the expected heading IDs using the same slug rules as common renderers (GitHub-style is a practical default):
   - Lowercase
   - Trim whitespace
   - Replace spaces with `-`
   - Remove punctuation characters
   - Collapse repeated `-`
   - For duplicate headings, append `-1`, `-2`, … (if needed)
4. Confirm the link’s `fragment` matches one of the computed IDs.

### Step 4 — Minimal-fix policy (documentation-safe)

When a link is broken:

1. Prefer fixing the **link target** (path/fragment) over changing headings/text.
2. Preserve existing Russian text and formatting.
3. Apply the smallest edit that makes the link resolve:
   - Fix wrong relative path (e.g., `../Readme.md` → `../../fullproject.md`)
   - Fix filename casing (`Readme.md` vs `README.md`)
   - Fix fragment to the correct slug (casing / punctuation differences)
4. After editing, re-validate the corrected link.

### Step 5 — Report format (what to capture)

For each broken link, record:

- Source: file + line
- Broken link as written
- Why it’s broken (missing file, wrong fragment, wrong path base)
- Exact fix applied

### Recommended automation (optional)

If you later want to automate this check, implement a small script that:

- Parses links with a Markdown parser (preferred) or a conservative regex fallback
- Resolves filesystem paths
- Extracts headings and computes slugs
- Outputs a CI-friendly report (broken link list with file:line)
