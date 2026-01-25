# Planning Patterns Skill

## Overview

The Planning Patterns skill teaches orchestrators how to systematically plan projects through four sequential phases: architecture design, risk identification, roadmap creation, and implementation planning. Every step is specific and concrete.

## Skill Structure

```
planning-patterns/
├── SKILL.md                          # Main skill document (start here)
├── README.md                         # This file
├── references/                       # Detailed reference documents
│   ├── step-by-step-procedures.md   # Process overview and connection
│   ├── architecture-design.md        # Detailed architecture design
│   ├── risk-identification.md        # Detailed risk identification
│   ├── roadmap-creation.md           # Detailed roadmap creation
│   ├── implementation-planning.md    # Detailed implementation planning
│   └── planning-checklist.md         # Comprehensive planning checklist
└── scripts/                          # Automation and template generation
    ├── README.md                     # Script documentation
    ├── generate_planning_checklist.py
    ├── generate_risk_register.py
    ├── generate_roadmap_template.py
    ├── generate_task_tracker.py
    └── generate_status_report.py
```

## Quick Start

1. **New to planning?**
   - Start with `SKILL.md`
   - Read `references/step-by-step-procedures.md` first
   - Choose your scenario (new project, expanding system, etc.)

2. **Want to plan a specific project right now?**
   - Read the reference document for the phase you are currently in
   - Use the templates provided in that reference
   - Use the scripts to generate working documents

3. **Need to understand a specific planning activity?**
   - Go to the relevant reference document
   - Follow the step-by-step instructions
   - Use the templates and examples

## Key Concepts

### The Four Planning Phases

| Phase | Focus | Duration | Output |
|-------|-------|----------|--------|
| **Architecture Design** | System structure: components, interfaces, data flows | 1-2 weeks | Architecture document |
| **Risk Identification** | Obstacles: discovery, assessment, mitigation | 1 week | Risk register |
| **Roadmap Creation** | Timeline: phases, milestones, resources | 1 week | Roadmap with phases |
| **Implementation Planning** | Tasks: breakdown, ownership, tracking | 1 week | Task list with assignments |

### Core Principles

1. **Specificity**: Every component, risk, and task must be concrete and measurable
2. **Sequentiality**: Phases must be executed in order - do not skip
3. **Completeness**: All four phases are required, even under time pressure
4. **Documentation**: Record decisions, assumptions, and rationale
5. **Stakeholder Alignment**: Validate outputs at end of each phase

## File Descriptions

### SKILL.md (Main Entry Point)
- Purpose of the skill
- When to use this skill
- Quick navigation table
- The four phases explained
- Application scenarios
- Key concepts
- Learning paths
- Troubleshooting guide
- Summary

**Read this first** if you are new to the skill.

### References

#### step-by-step-procedures.md
Explains the process overview, showing how the four phases connect and why each is important.
- The four phases and their purposes
- Planning workflow diagram
- Key principles
- Common mistakes to avoid

**Duration**: 10 minutes | **Purpose**: Understand the process

#### architecture-design.md
Teaches how to design the structural blueprint of your system.
- What is architecture design
- Five-step process (identify components, define responsibilities, map flows, identify dependencies, define interfaces)
- Architecture patterns
- Templates and checklists
- Examples with concrete details

**Duration**: 30 minutes | **Purpose**: Design system architecture

#### risk-identification.md
Teaches how to discover and plan for obstacles.
- What is risk identification
- Four-step process (discover risks, assess impact/probability, plan mitigations, create register)
- Risk categories and types
- Mitigation strategies
- Monitoring and tracking
- Templates and checklists

**Duration**: 25 minutes | **Purpose**: Identify and plan for risks

#### roadmap-creation.md
Teaches how to create a time-bound execution plan.
- What is a roadmap
- Five-step process (define phases, sequence by dependencies, define milestones, allocate resources, create master roadmap)
- Phase sequencing and critical path
- Milestone and deliverable definition
- Resource allocation
- Communication formats

**Duration**: 35 minutes | **Purpose**: Create execution timeline

#### implementation-planning.md
Teaches how to break the roadmap into actionable, trackable tasks.
- What is implementation planning
- Four-step process (break into tasks, create dependency network, assign owners, create tracking)
- Task definition and estimation
- Dependency analysis
- Responsibility matrix (RACI)
- Daily and weekly tracking
- Change management

**Duration**: 20 minutes | **Purpose**: Plan implementation tasks

#### planning-checklist.md
Comprehensive checklist for all four planning phases.
- Pre-planning checklist
- Architecture design checklist
- Risk identification checklist
- Roadmap creation checklist
- Implementation planning checklist
- Post-planning verification checklist

**Duration**: 10 minutes to reference | **Purpose**: Ensure nothing is missed

### Scripts

All scripts are in the `scripts/` folder. See `scripts/README.md` for detailed documentation.

**Available scripts**:
- `generate_planning_checklist.py` - Create customized checklist for your project
- `generate_risk_register.py` - Create empty risk register template
- `generate_roadmap_template.py` - Create roadmap timeline template
- `generate_task_tracker.py` - Create task tracking spreadsheet
- `generate_status_report.py` - Create weekly status report template

## How to Use This Skill

### Scenario: Starting a New Project

1. **Week 1-2: Architecture Design**
   - Read: `references/architecture-design.md`
   - Activity: Design your system components and interfaces
   - Deliverable: Architecture document

2. **Week 1-2: Risk Identification (parallel)**
   - Read: `references/risk-identification.md`
   - Activity: Identify all risks and plan mitigations
   - Deliverable: Risk register

3. **Week 3: Roadmap Creation**
   - Read: `references/roadmap-creation.md`
   - Activity: Create timeline with phases and milestones
   - Deliverable: Roadmap document

4. **Week 4: Implementation Planning**
   - Read: `references/implementation-planning.md`
   - Activity: Break phases into tasks and assign owners
   - Deliverable: Task list with assignments

5. **Week 5: Stakeholder Review**
   - Present all four planning documents
   - Get approval to proceed

### Scenario: Planning Under Time Pressure

Still do all four phases, but compress the timeline:
1. Architecture Design: 2-3 days (rough, not perfect)
2. Risk Identification: 1-2 days (focus on critical risks only)
3. Roadmap Creation: 1-2 days (rough timeline, critical path only)
4. Implementation Planning: 2-3 days (detail next 4 weeks only)

**Important**: Do not skip phases - compress them instead.

## Templates Included

Every reference document includes templates for:
- Architecture design document
- Risk register
- Risk mitigation strategy
- Roadmap (multiple formats)
- Task definition
- Status reports
- Responsibility matrix
- Checklists

Copy these templates and customize for your project.

## Scripts Usage

Generate templates quickly with provided scripts:

```bash
# Generate planning checklist for your project
python scripts/generate_planning_checklist.py \
  --project "MyProject" \
  --phases 4 \
  --output checklist.md

# Generate risk register template
python scripts/generate_risk_register.py \
  --template excel \
  --risks 20 \
  --output risks.xlsx

# Generate roadmap template
python scripts/generate_roadmap_template.py \
  --weeks 12 \
  --phases 5 \
  --output roadmap.md
```

See `scripts/README.md` for detailed usage.

## Key Takeaways

1. **Planning is essential** - Projects without proper planning fail at higher rates

2. **Four phases are required** - All four (architecture, risks, roadmap, implementation) are needed for complete planning

3. **Every step must be specific** - Vague planning leads to vague execution. Be concrete and measurable.

4. **Plans change** - Revisit and update your plan every 2-4 weeks. This is normal and expected.

5. **Stakeholder alignment is critical** - Have stakeholders review and approve each phase output before moving to next phase

6. **Documentation is your record** - Your planning documents become the project bible. Keep them updated.

## Troubleshooting

### Problem: Architecture is too complex

**Solution**: You are including too much detail. Each component should have a single responsibility. Break complex components into smaller ones.

### Problem: Cannot identify all risks

**Solution**: Use systematic methods: review architecture for failure modes, review dependencies for cascade effects, ask stakeholders directly about their concerns.

### Problem: Timeline keeps slipping

**Solution**: You did not include sufficient buffer. Include 20-30% buffer time in estimates and schedules. If you scheduled 100% utilization, timelines always slip.

### Problem: Team does not understand the plan

**Solution**: Create multiple communication formats. Not everyone wants to read a 50-page document. Create executive summary, timeline, checklist, FAQ.

## Learning Resources

- Start with `SKILL.md` for complete overview
- Read references in order: procedures → architecture → risks → roadmap → implementation
- Review planning checklist after each phase
- Use scripts to generate working templates
- Apply patterns to real project
- Have experienced person review your outputs

## Next Steps

1. Read `SKILL.md`
2. Choose your scenario (new project, expansion, replan)
3. Read the relevant reference documents
4. Use templates and scripts to create planning documents
5. Have stakeholders review and approve
6. Execute the plan
7. Update plan every 2-4 weeks

---

**Last Updated**: 2025-12-29
**Skill Version**: 1.0
**For questions about planning patterns**: See troubleshooting section in `SKILL.md`
