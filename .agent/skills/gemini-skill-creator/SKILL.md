---
name: gemini-skill-creator
description: Creates structured skills for the Antigravity agent environment. Use when the user requests to create a new skill, build a skill system, or mentions skill development for agent capabilities.
---

# Gemini Skill Creator

## When to use this skill

- User asks to create a new skill for the Antigravity agent
- User mentions building agent capabilities or extending agent functionality
- User requests skill templates or skill structure guidance
- User wants to standardize skill creation across projects

## Core Structural Requirements

Every skill you generate must follow this folder hierarchy:

```
<skill-name>/
├── SKILL.md          (Required: Main logic and instructions)
├── scripts/          (Optional: Helper scripts)
├── examples/         (Optional: Reference implementations)
└── resources/        (Optional: Templates or assets)
```

## YAML Frontmatter Standards

The `SKILL.md` must start with YAML frontmatter following these strict rules:

- **name**: Gerund form (e.g., `testing-code`, `managing-databases`). Max 64 chars. Lowercase, numbers, and hyphens only. No "claude" or "anthropic" in the name.
- **description**: Written in **third person**. Must include specific triggers/keywords. Max 1024 chars.
  - Example: "Extracts text from PDFs. Use when the user mentions document processing or PDF files."

## Writing Principles (The "Claude Way")

When writing the body of `SKILL.md`, adhere to these best practices:

### Conciseness
- Assume the agent is smart
- Do not explain basic concepts (what a PDF is, what a Git repo is)
- Focus only on the unique logic of the skill

### Progressive Disclosure
- Keep `SKILL.md` under 500 lines
- If more detail is needed, link to secondary files (e.g., `[See ADVANCED.md](ADVANCED.md)`)
- Only one level deep for references

### Path Standards
- Always use `/` for paths, never `\`

### Degrees of Freedom
Choose the right format based on task flexibility:

- **Bullet Points**: High-freedom tasks (heuristics, decision-making)
- **Code Blocks**: Medium-freedom (templates, structured examples)
- **Specific Bash Commands**: Low-freedom (fragile operations, exact sequences)

## Workflow & Feedback Loops

For complex tasks, include:

1. **Checklists**: A markdown checklist the agent can copy and update to track state
2. **Validation Loops**: A "Plan-Validate-Execute" pattern
   - Example: Run a script to check a config file BEFORE applying changes
3. **Error Handling**: Instructions for scripts should be "black boxes"
   - Tell the agent to run `--help` if they are unsure

## Skill Creation Workflow

When creating a new skill, follow these steps:

### 1. Understand Requirements
- [ ] Clarify the skill's purpose
- [ ] Identify trigger keywords/scenarios
- [ ] Determine required tools/scripts
- [ ] Define expected inputs and outputs

### 2. Design Structure
- [ ] Choose appropriate folder structure
- [ ] Determine if scripts/examples/resources are needed
- [ ] Plan the workflow steps

### 3. Write SKILL.md
- [ ] Create YAML frontmatter with proper name and description
- [ ] Add "When to use this skill" section
- [ ] Document the workflow with checklist
- [ ] Write clear, concise instructions
- [ ] Link to supporting files if needed

### 4. Create Supporting Files
- [ ] Add scripts to `scripts/` if needed
- [ ] Provide examples in `examples/` if helpful
- [ ] Include templates/assets in `resources/` if applicable

### 5. Validate
- [ ] Check YAML frontmatter follows standards
- [ ] Verify skill name is in gerund form
- [ ] Ensure description is third-person with triggers
- [ ] Confirm SKILL.md is under 500 lines
- [ ] Test that paths use forward slashes

## Output Template

When creating a skill, use this structure:

```markdown
---
name: [gerund-name]
description: [3rd-person description with triggers]
---

# [Skill Title]

## When to use this skill
- [Trigger 1]
- [Trigger 2]

## Workflow
- [ ] [Step 1]
- [ ] [Step 2]
- [ ] [Step 3]

## Instructions
[Specific logic, code snippets, or rules]

## Resources
- [Link to scripts/ or resources/]
```

## Example Skill Names

Good examples:
- `testing-code`
- `managing-databases`
- `deploying-applications`
- `processing-pdfs`
- `analyzing-logs`

Bad examples:
- `test` (not gerund)
- `DatabaseManager` (not lowercase)
- `claude-helper` (contains "claude")
- `do_deployment` (uses underscore)

## Location Guidelines

### Project-Specific Skills
Store in: `.agent/skills/<skill-name>/`

### Global Skills
Store in: `~/.agent/skills/<skill-name>/`

Global skills are available across all projects and should be used for:
- Universal development workflows
- Cross-project utilities
- Standardized processes
- Reusable templates

## Best Practices

1. **Start Simple**: Begin with minimal structure, add complexity only when needed
2. **Be Specific**: Include exact commands for critical operations
3. **Provide Context**: Add "When to use" sections with clear triggers
4. **Enable Self-Service**: Include `--help` references for scripts
5. **Maintain Consistency**: Follow naming and structure conventions
6. **Think Reusability**: Design skills to work across different projects
7. **Document Assumptions**: State prerequisites clearly
8. **Test Instructions**: Ensure steps are reproducible

## Common Patterns

### For Testing Skills
- Include setup/teardown steps
- Provide example test cases
- Document assertion patterns

### For Deployment Skills
- Add validation checkpoints
- Include rollback procedures
- Document environment requirements

### For Processing Skills
- Define input/output formats
- Include error handling
- Provide sample data

## Error Handling

When scripts fail:
1. Check script exists and is executable
2. Run with `--help` to understand usage
3. Verify prerequisites are met
4. Check environment variables
5. Review error messages for specific issues

## References

- Original skill creation guide: `/home/bamboosam/teddy/skillcreateinfo.md`
- Skills directory: `.agent/skills/` (project) or `~/.agent/skills/` (global)
