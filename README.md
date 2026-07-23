# Results

**Paper submitted to ENIAC 2026:**

*Formal Proof Generation in Deductive Logic Systems with Open LLMs: An Empirical Study on Natural Deduction and Analytic Tableau*

This directory contains the experimental results obtained from evaluating Large Language Models (LLMs) on formal proof generation tasks using **Natural Deduction** and **Analytic Tableau**. The experiments cover both **Propositional Logic (PL)** and **First-Order Logic (FOL)** under different prompting strategies.

## Directory Structure

```text
.
├── DNprompt.py          # Prompt templates for Natural Deduction experiments
├── TBprompt.py          # Prompt templates for Analytic Tableau experiments
├── README.md
├── natural_deduction/   # Experimental results for Natural Deduction
└── tableau/             # Experimental results for Analytic Tableau
```

### Folder Description
- **dn/**
  - Contains all experimental outputs related to the Natural Deduction proof system.
  - Includes results for both Propositional Logic and First-Order Logic.
  - Experiments evaluate zero-shot and few-shot prompting using simple and complex prompts.

- **tableau/**
  - Contains all experimental outputs related to the Analytic Tableau proof system.
  - Includes both Propositional Logic and First-Order Logic experiments.
  - Results were obtained using the same prompting configurations as the Natural Deduction experiments.

## Prompt Files
### `DNprompt.py`
Defines all prompt templates used in the **Natural Deduction** experiments, 
### `TBprompt.py`
Defines the prompt templates used in the **Analytic Tableau** experiments following the same experimental protocol.

## Prompt Configurations
Two prompt families were evaluated:

### Simple Prompts
Contain only formatting instructions describing the expected proof output.

### Complex Prompts
Extend the simple prompts by including:

- Formal explanation of inference rules
- Rule application schemes
- Additional guidance for proof construction

Each prompt family was evaluated using:

| Configuration | Description |
|--------------|-------------|
| S0 / C0 | Zero-shot |
| S1 / C1 | One demonstration (partial rule coverage) |
| S2 / C2 | Complete rule coverage (each inference rule appears once) |
| S3 / C3 | Three demonstrations |
| S5 / C5 | Five demonstrations |

---
# Summary of Results
## Natural Deduction

The Natural Deduction experiments show that:

- Few-shot prompting consistently improves performance over zero-shot.
- Complex prompts generally outperform simple prompts by providing explicit explanations of inference rules.
- Performance decreases substantially when moving from Propositional Logic to First-Order Logic due to the increased reasoning complexity introduced by quantifiers and variable bindings.

### Best Propositional Result
| Model | Accuracy |
|--------|---------:|
| Qwen3-32B | **62.4%** |

### Best First-Order Result
| Model | Accuracy |
|--------|---------:|
| GPT-120B | **32.14%** |

Overall, model size alone does not determine performance. Several medium-sized models outperform larger ones depending on the prompting strategy.

---

## Tableau
The Tableau experiments achieved considerably stronger performance than Natural Deduction.

Main observations include:

- Complex prompts consistently improve accuracy.
- Few-shot prompting remains highly beneficial.
- Unlike Natural Deduction, First-Order Logic performance does not degrade and, for several models, even improves.
- GPT-OSS models exhibit particularly strong performance in Tableau reasoning.

### Best Propositional Result
| Model | Accuracy |
|--------|---------:|
| GPT-OSS-120B | **59.51%** |

### Best First-Order Result
| Model | Accuracy |
|--------|---------:|
| GPT-OSS-120B | **84.96%** |

The largest observed improvement from simple to complex prompting reached **+45.14 percentage points**.

---

# Main Findings
- Few-shot prompting consistently improves formal proof generation.
- Complex prompts outperform simple prompts in nearly every configuration.
- Natural Deduction remains considerably more challenging than Tableau.
- First-Order Logic significantly reduces accuracy in Natural Deduction.
- Model architecture and training appear more important than parameter count alone.
- Current open-weight LLMs still struggle with producing formally correct proofs under strict logical constraints.
