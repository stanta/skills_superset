---
name: practice-materials-generator
description: This skill should be used when the task is to create teaching practice materials—concept checks, problems, mini-cases, quizzes, and answer keys—for any academic, technical, business, or professional domain.
---

# Practice Materials Generator

Create compact, teaching-ready practice materials for any subject area.

## Use this skill when

Apply this skill when the user needs exercises, problem sets, cases, worksheets, formative assessment items, or homework with solutions, but does not need a full lecture package.

Typical triggers:
- "Create exercises"
- "Make tasks for students"
- "Build a worksheet"
- "Prepare a quiz with answers"
- "Give cases and solutions"
- "Make practice materials for this topic"

## Do not use this skill when

Do not use this skill when the user needs:
- a full lecture package from scratch
- only slide writing from an outline
- a multi-week module plan
- critique and rewriting of existing lecture materials

Use a more specific teaching-planning skill in those cases.

## Core workflow

1. Identify the domain, topic, learner level, format, and difficulty.
2. Infer conservative defaults when inputs are missing:
   - audience: beginner/intermediate learners
   - format: classroom or homework
   - difficulty: easy to medium
3. Build a balanced activity set that usually includes:
   - 5 micro concept checks with short model answers
   - 3 main tasks or problems with full step-by-step solutions
   - 2 short scenario mini-cases with guiding questions and takeaways
   - 1 quick quiz with answer key
4. Adapt task type to the domain:
   - quantitative domains: calculations, proofs, data interpretation
   - technical domains: coding, debugging, system reasoning
   - humanities/social sciences: interpretation, argument mapping, source analysis
   - business/professional domains: decision cases, trade-offs, applied scenarios
5. Keep notation, instructions, and answer format consistent.
6. Add short teacher notes when useful.

## Output requirements

Produce materials that are:
- coherent as a single packet
- solvable with the assumed prior knowledge
- explicit in expected reasoning
- clear enough for classroom or independent use

Include full solutions unless the user explicitly asks for student-only materials.

## Quality bar

Avoid trick questions, unnecessary jargon, domain-lawyer edge cases, and unrealistic assumptions. Prefer small, teachable tasks over encyclopedic coverage.
