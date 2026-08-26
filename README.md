# Results

**Paper submitted to ENIAC 2026:**

*Formal Proof Generation in Deductive Logic Systems with Open LLMs: An Empirical Study on Natural Deduction and Analytic Tableau*

This directory contains the experimental results obtained from evaluating Large Language Models (LLMs) on formal proof generation tasks using **Natural Deduction** and **Analytic Tableau**. The experiments cover both **Propositional Logic (PL)** and **First-Order Logic (FOL)** under different prompting strategies.

## Directory Structure

```text
.
├── datasets/                  # Datasets used in the experiments + some solutions for the datasets in the .json files
│
├── prompts/                   # Prompt templates used for each reasoning method
│   ├── prompt_dn.py           # Prompts for Natural Deduction
│   └── prompt_tb.py           # Prompts for Analytic Tableau
│
└── results/                   # Experimental results
    ├── accuracy_tables/       # Tables with accuracy measurements
    │
    ├── dn/                    # Natural Deduction results
    │   └── <model_name>/
    │       ├── pro/           # Results using the propositional logic
    │       └── pre/           # Results using the FOL ('predicate') logic
    │
    └── tb/                    # Analytic Tableau results
        └── <model_name>/
            ├── pro/           # Results using the propositional logic
            └── pre/           # Results using the FOL ('predicate') logic
```

# Dataset

The complete datasets used are provided in `pro_dataset.txt` and `pre_dataset.txt`. For each proof system, **5 problems from each dataset are reserved as few-shot demonstrations** and are therefore not included in the accuracy evaluation. Consequently, each proof system is evaluated on:

| Logic                    | Original Dataset | Few-Shot Demonstrations | Evaluation Set |
| ------------------------ | ---------------: | ----------------------: | -------------: |
| Propositional Logic (PL) |              411 |                       5 |        **406** |
| First-Order Logic (FOL)  |              117 |                       5 |        **112** |
|                          |                  |                         |                |

The few-shot demonstrations are excluded from evaluation because they are explicitly provided to the models as examples during prompting.

## Natural Deduction

For the **Natural Deduction (DN)** experiments, the following problems are reserved as few-shot demonstrations and are therefore excluded from the natural deduction tables count for the accuracy calculation.

### Propositional Logic

```text
(A->B)&(~A->B)|-B 
A|B|-(~A->B)&(~B->A)
~(A&B)|-~A|~B 
~A->~B,(C&D)|B,~A->~D|-~C|A 
~(A->~B)|-A&B 
```

### First-Order Logic

```text
|- (B->Ex C(x))->Ex (B->C(x)) 
Ax ((B(x)->C(x))&(C(x)->B(x))) |- Ax ((~B(x)->~C(x))&(~C(x)->~B(x))) 
Ax Ey (B(x)|C(y)) |- Ey Ax (B(x)|C(y)) 
|- Ax (B(x)|C)->(Ax B(x)|C) 
Ax (~B(x)|C(x)), Ex B(x) |- Ex C(x) 
```

## Analytic Tableau

For the **Analytic Tableau (TB)** experiments, the following problems are reserved as few-shot demonstrations and are therefore excluded from the natural deduction tables count for the accuracy calculation.

### Propositional Logic

```text
(A|B)&(A|C)|-A|(B&C) 
|-(~A->B)->((~A->~B)->A) 
~(~A|~B)|-A&B 
~A->~B|-B->A
~A|~B|-~(A&B)
```

### First-Order Logic

```text
Ex B(x), Ax (B(x)->C(x)) |- Ex C(x) 
Ax (B(x)|B(x)) |- Ax B(x) 
|- Ex (B(x)|C(x))->(Ex B(x)|Ex C(x))
Ax ~(B(x)&~C(x)), Ax ~C(x) |- Ax ~B(x) 
|- Ex B(x)->~Ax ~B(x)
```
---
---

# Verifiers and Proof Assistants

The experiments reported in this article use two formal verification tools:
- **NADIA** — used for **Natural Deduction** proofs.
- **NADIA rules description:** [(https://github.com/daviromero/nadia/blob/main/ND-Rules.pdf)]
- **ANITA** — used for **Analytic Tableau** proofs.
- **ANITA rules description:** https://github.com/daviromero/anita/blob/main/AT-Rules.pdf
Both tools use syntax inspired by the **Fitch-style notation**, a widely adopted representation for formal proofs. They automatically verify whether a generated proof satisfies the rules of the corresponding deductive system and provide information about errors when a proof is not valid.

The notation accepted by both follows the compact syntax used throughout the datasets. The correspondence between standard logical notation and NADIA/ANITA notation is summarized below.

| Standard Symbol | NADIA/ANITA Notation | Meaning |
|-----------------|----------------|---------|
| $\neg$          | `~`            | Negation |
| $\land$         | `&`            | Conjunction |
| $\lor$          | `\|`           | Disjunction |
| $\rightarrow$   | `->`           | Implication |
| $\forall x$     | `Ax`           | Universal quantifier |
| $\exists x$     | `Ex`           | Existential quantifier |
| $\bot$          | `@`            | Contradiction / falsum |
| $\vdash$        | `\|-`          | Derivation / entailment |
| Premise         | `pre`          | Premise |
| Hypothesis      | `hip`          | Temporary hypothesis |

---
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
