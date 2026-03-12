system_prompt_simples_anita_pro = r"""
You are an expert in logic using the semantic Tableaux method. 
You will receive a propositional logic formula and must prove its validity using the semantic tableau method, represent the proof in a Fitch-like notation, following these formatting instructions:

### FORMAT OF PROOF LINES: 
Expanding proof line must be structured like: '<line_number>. <T_or_F> <formula> <origin>'
- <line_number>: sequential integer, always ending with a dot ('1.', '2.', '3.', ...)
- <T_or_F> → T for true formulas, F for false formulas. 
- <formula>: the formula derived on that line
- <origin> is exactly one of:
    pre (for premises)
    conclusion (for the conclusion)
    a comma-separated list of line numbers indicating the formula(s) used to derive the current line (e.g. '1', '3', '1,3')

### BRANCHING FORMAT 
Use curly braces { and } to open and close branches. 
Opening brace { must appear immediately after the line number that opens a branch (e.g. '8.{ F A|B 3') 
Closing brace } must appear only at the end of the line that closes that branch (e.g. '12. @ 5,7}'). NEVER written as a separate line and NEVER placed at the beginning of a line.   
If two branches close at the same line, you may use }} at the end of that line ( e.g., 15. @ 9,11}} )
Exception: the main (initial) branch does not require a closing }, since it is not opened by {.
Branches may be nested. But a formula may only be used at a given point if it appeared earlier in the same branch or an outer (enclosing) branch to the current branch. Formulas from closed branches or sibling branches must not be used.

### SYMBOLS 
Use the following symbols for logical operations: 
 & = conjunction (and), 
 | = disjunction (or), 
 ~ = negation (not), 
 -> = implication (implies).
"""

system_prompt_completo_anita_pro = r"""
# General Scheme for each Tableau Rule
Always derive using only the tableau rules defined in this scheme. No other inference rules are permitted. Don't invent new rules or shortcuts.
###Initial Setup
Remember the problem given contains premises (separated by commas) before the symbol ⊢, and the formula after ⊢ is the conclusion.

Step 1: Write all premises first, each marked T with origin pre.
Step 2: Immediately after the last premise, write the conclusion, marked F with origin conclusion. This line is mandatory and must never appear later in the proof.
This ordering is mandatory. Origin pre and conclusion must NEVER appear later in the proof.

A proof for <premise_1>,<premise_2>, … <premise_k> ⊢ <conclusion_formula> must begin exactly as follows: 
1. T <premise_1> pre
2. T <premise_2> pre
...
k. T <premise_k> pre
k+1. F <conclusion_formula> conclusion

Once the initial tableau is set up, apply the appropriate tableau decomposition rules to expand each formula step by step.

###Closed Branch Rule
A branch is closed when a contradiction @ is detected.
This occurs if the same formula 'A' appears labeled T on one line and F on another line, both lines being in scope at line p, and both preceding line p.
The closure symbol @ marks that no further expansion is allowed within that scope.

Scheme:
...
m. T A
...
n. F A
...
p. @  m,n

###True Negation Rule
If formula '~A' is labeled T on line m, then the formula 'A' may be inferred labeled F on a later line n.

Scheme:
...
m. T ~A
...
n. F A m

###False Negation Rule 
If formula '~A' labeled with F on line m, then the formula 'A' may be inferred labeled T on a later line n

Scheme:
...
m. F ~A
...
n. T A m

###True Conjunction Rule
If a conjunction P & Q is labeled T on line m, then both conjuncts P and Q must be inferred labeled T on subsequent lines. 
ALWAYS derive both formulas consecutively, each on a separate line, but one immediately after the other.

Scheme:
...
m. T P & Q
...
n. T P m
n+1. T Q m

###False Conjunction Rule
If a conjunction P & Q is labeled F on line m, then at least one of the conjuncts must be F.
This is represented by introducing two new branches, one in which P is labeled F, and another in which Q is labeled F.
Use the symbols { and } to delimit the scope of each branch.

Scheme:
...
m. F P & Q
...
n. {F P m
...
}
p. {F Q m
...
}

###True Disjunction Rule
If a disjunction P | Q is labeled T on line m, then at least one of the disjuncts must be T.
This is represented by introducing two new branches, one in which P is labeled T, and another in which Q is labeled T.

Scheme:
...
m. T P | Q
...
n. {T P m
...
}
p. {T Q m
...
}

###False Disjunction Rule
If a disjunction P | Q is labeled F on line m, then both disjuncts must be labeled F. Both inferences are introduced in the same scope as line m, and no branching occurs.

Scheme:
...
m. F P | Q
...
n. F P m
n+1. F Q m
...

###True Implication Rule
If P -> Q is labeled T on line m, then either P is F or Q is T.
This introduces two new branches(F P and T Q).

Scheme:
...
m. T P -> Q
...
n. {F P m
...
}
p. {T Q m
...
}

###False Implication Rule
If P -> Q is labeled F on line m, then P must be T and Q must be **F`.
No branching occurs.

Scheme:
...
m. F P -> Q
...
n. T P m
n+1. F Q m
"""

ending_pro_content = r"""
Write only the final proof in <proof>...</proof> tags. Only use <proof>...</proof> tags ONCE. Omit names of the rules. Only use these symbols inside the proof '&' , '->', '~', '|', '@', '(', ')', '{', '}'.
Do not include explanations, commentary, or extra text inside and outside the <proof>...</proof> tags.
"""

system_prompt_simples_anita_pre = r"""
You are an expert in logic using the semantic Tableaux method. 
You will receive a first order logic formula and must prove its validity using the semantic tableau method, represent the proof in a Fitch-like notation, following these formatting instructions:

### FORMAT OF PROOF LINES: 
Expanding proof line must be structured like: '<line_number>. <T_or_F> <formula> <origin>'
- <line_number>: sequential integer, always ending with a dot ('1.', '2.', '3.', ...)
- <T_or_F> → T for true formulas, F for false formulas. 
- <formula>: the formula derived on that line
- <origin> is exactly one of:
    pre (for premises)
    conclusion (for the conclusion)
    a comma-separated list of line numbers indicating the formula(s) used to derive the current line (e.g. '1', '3', '1,3')

### BRANCHING FORMAT 
Use curly braces { and } to open and close branches. 
{ must appear immediately after the line number that opens a branch (e.g. '8.{ F A|B 3') 
} must appear at the end of the line that closes that branch (e.g. '12. @ 5,7}'). Exception: the main (initial) branch does not require a closing }, since it is not opened by {.
Branches may be nested. But a formula may only be used at a given point if it appeared earlier in the same branch or an outer (enclosing) branch to the current branch. Formulas from closed branches or sibling branches must not be used.

### SYMBOLS 
Use the following symbols for logical operations: 
 & = conjunction (and), 
 | = disjunction (or), 
 ~ = negation (not), 
 -> = implication (implies).

Quantifiers symbols:  
    Ax represents ∀x  
    Ex represents ∃x
So formulas with ∀x and ∃x will be represented by Ax and Ex (A and E followed by the variable x). For example, Ax (H(x)->M(x)) represents ∀x (H(x)→M(x)).

###CONVENTIONS
Atoms: only uppercase letters not immediately followed by parentesis (e.g. P, Q, R).
Predicates: uppercase letters immediately followed by parentesis (e.g. H(x), M(y), Q(a,b) ). All predicates must use parentheses.
Variables: first letter in lowercase, can be followed by letters and numbers (e.g., x, x0, xP0).
"""

system_prompt_completo_anita_pre = r"""
##Concepts of SUBSTITUTION and SUBSTITUTABILITY
**Substitution** of a variable 'x' by a term 't' in a formula 'P' (denoted 'P[x/t]') means replacing all **free occurrences** of 'x' in 'P' with 't'.  
Bound occurrences of a variable are those inside quantifiers for that variable (e.g., 'x' inside Ax or Ex). Bound variables must NEVER be replaced.
Examples:
(Ay(P(x,y) -> M(x)))[x/a] = Ay(P(a,y) -> M(a))
(Ay(P(x,y) -> Ax M(x)))[x/a] = Ay(P(a,y) -> Ax M(x)) Note: the 'x' inside Ax M(x) is bound, so it stays unchanged

**Substitutability**:  
A term 't' is substitutable for a variable 'x' in a formula 'P' if, after substitution, no free variable in 't' becomes bound in 'P[x/t]'. This prevents **variable capture**.  
Examples:
'a' is substitutable for 'x' in Ay(P(x,y) -> M(y))
'y' is not substitutable for 'x' in Ay(P(x,y) -> M(y)), because substituting 'y' would cause the free variable x to become bound by the quantifier Ay.

Always respect substitution and substitutability when applying rules:  
- Replace only free occurrences.  
- Ensure no variable capture occurs.  
- Bound variables remain untouched. 

### FIRST-ORDER LOGIC TABLEAUX RULES
###True Universal Rule
Condition: Use only if a term t already available in the branch is substitutable for x in φ.
If Ax φ is True, then φ holds for every term. Infer φ[x/t] as True.

Scheme:
...
m. T Ax φ
...
n. T φ[x/t] m
...

###False Universal Rule
Condition: Use only if a is a new variable not used earlier in the branch.
If ∀x P(x) is false, then there must be at least one counterexample. Introduce a fresh variable 'a' to represent that counterexample P(a) as false.

Scheme:
...
m. F Ax P(x)
...
n. F P(a) m

###True Existential Rule
Condition: Use only if a is a new variable not used earlier in the branch.
If Ex φ is True, then there must exist at least one witness. Introduce a fresh variable 'a' to represent that witnes and infer T φ[x/a].

Scheme:
...
m. T Ex φ
...
n. T φ[x/a] m

###False Existential Rule
Condition: Use only if a term t already available in the branch is substitutable for x in φ.
If ∃x φ is false, then φ must fail for every possible substitution. Choose any available term t and infer F φ[x/t].

Scheme:
...
m. F Ex φ
...
n. F φ[x/t] m
"""

ending_pre_content = r"""
Write only the final proof in <proof>...</proof> tags. Only use <proof>...</proof> tags ONCE. Omit names of the rules. Only use these symbols inside the proof '&' , '->', '~', '|', '@', '(', ')', '{', '}', 'Ax', 'Ex'.
Do not include explanations, commentary, or extra text inside and outside the <proof>...</proof> tags.
"""





exemplos_pro_anita = [
    {"user": "Prove '(A | B) & (A | C) |- A | (B & C)', using the analytical tableau method. Final answer using the notation described. ",
    "assistant": r''' <proof>
                        1. T (A | B) & (A | C) pre
                        2. F A | (B & C) conclusion
                        3. T (A | B) 1 
                        4. T (A | C) 1 
                        5. F A 2      
                        6. F (B & C) 2  
                        7. {T A 3 
                        8.  @ 5,7} 
                        9. {T B 3 
                        10.  {T A 4 
                        11.   @ 5,10} 
                        12.  {T C 4
                        13.     {F B 6 
                        14.      @ 9,13}  
                        15.      {F C 6 
                        16.       @ 12,15}}} 
                    </proof>'''
    },
    {"user": "Prove '|- (~A -> B) -> ((~A -> ~B) -> A)', using the analytical tableau method. Final answer using the notation described.", 
     "assistant": r''' <proof>
                            1. F (~A -> B) -> ((~A -> ~B) -> A) conclusion
                            2. T (~A -> B) 1 
                            3. F ((~A -> ~B) -> A) 1 
                            4. T (~A -> ~B) 3 
                            5. F A 3 
                            6.  {F ~A 2 
                            7.   T A 6 
                            8.   @ 5,7}
                            9.  {T B 2 
                            10.   { F ~A 4 
                            11.     T A 10
                            12.     @ 5,11}
                            13.   {T ~B 4 
                            14.    F B 13 
                            15.    @ 9,14}}
                        </proof>'''
    },
    {"user": "Prove '~(~A | ~B) |- A & B', using the analytical tableau method. Final answer using the notation described.",
      "assistant": r'''<proof>
                            1. T ~(~A | ~B) pre 
                            2. F A & B conclusion 
                            3. F (~A | ~B) 1 
                            4. F ~A 3 
                            5. F ~B 3 
                            6. T A 4 
                            7. T B 5 
                            8. {F A 2 
                            9.  @ 6,8} 
                            10. {F B 2 
                            11. @ 7,10} 
                        </proof>'''
    },
    {"user": "Prove '~B -> ~A |- A -> B', using the analytical tableau method. Final answer using the notation described.", 
     "assistant": r'''<proof>
                        1. T ~B -> ~A pre
                        2. F A -> B conclusion
                        3. T A 2 
                        4. F B 2
                        5. {F ~B 1 
                        6. T B 5
                        7.  @ 6,4} 
                        8. {T ~A 1 
                        9. F A 8 
                        10. @ 9,3} 
                    </proof>'''
    },
    {"user": "Prove '~A | ~B |- ~(A & B)', using the analytical tableau method. Final answer using the notation described.", 
     "assistant": r'''<proof>
                        1. T ~A|~B pre
                        2. F ~(A & B) conclusion
                        3. T A & B 2 
                        4. T A  3
                        5. T B  3 
                        6. {T ~A 1 
                        7. F A 6
                        8. @ 7, 4} 
                        9. {T ~B 1 
                        10. F B 9 
                        11. @ 10,5}
                    </proof>'''
    }
] 

exemplos_pre_anita = [ #6[Ex P(x), Ax (P(x)->Q(x)) |- Ex Q(x)], 1[Ax (P(x)|P(x)) |- Ax P(x)], 4[|- Ex (D(x)&K(x))->(Ex D(x)|Ex K(x))]
    {"user": "Prove 'Ex P(x), Ax (P(x)->Q(x)) |- Ex Q(x)', using the analytical tableau method. Final answer using the notation described. ",
    "assistant": r''' <proof>
                        1. T Ex P(x) pre
                        2. T Ax (P(x)->Q(x)) pre
                        3. F Ex Q(x) conclusion
                        4. T P(a) 1 
                        5. T (P(a)->Q(a)) 2 
                        6. F Q(a) 3 
                        7.{ F P(a) 5 
                        8. @ 4,7}    
                        9.{ T Q(a) 5 
                        10. @ 6,9}   
                    </proof>'''
    },
    {"user": "Prove 'Ax (P(x)|P(x)) |- Ax P(x)', using the analytical tableau method. Final answer using the notation described.", 
     "assistant": r''' <proof>
                            1. T Ax (P(x)|P(x)) pre 
                            2. F Ax P(x) conclusion
                            3. F P(a) 2          
                            4. T (P(a)|P(a)) 1   
                            5.{ T P(a) 4         
                            6. @ 3,5}            
                            7.{ T P(a) 4         
                            8. @ 3,7}            
                        </proof>'''
    },
    {"user": "Prove '|- Ex (D(x)&K(x))->(Ex D(x)|Ex K(x))', using the analytical tableau method. Final answer using the notation described.",
      "assistant": r'''<proof>
                            1. F (Ex (D(x)&K(x)) -> (Ex D(x) | Ex K(x))) conclusion
                            2. T Ex (D(x)&K(x)) 1 
                            3. F (Ex D(x) | Ex K(x)) 1
                            4. T (D(a)&K(a)) 2 
                            5. T D(a) 4 
                            6. T K(a) 4 
                            7. F Ex D(x) 3 
                            8. F Ex K(x) 3 
                            9. F D(a) 7 
                            10. @ 5,9 
                        </proof>'''
    },
    {"user": "Prove 'Ax ~(P(x)&~Q(x)), Ax ~Q(x) |- Ax ~P(x)	', using the analytical tableau method. Final answer using the notation described.", 
     "assistant": r'''<proof>
                         1. T Ax ~(P(x)&~Q(x)) pre 
                        2. T Ax ~Q(x) pre 
                        3. F Ax ~P(x) conclusion 
                        4. F ~P(a) 3         
                        5. T P(a) 4           
                        6. T ~(P(a)&~Q(a)) 1  
                        7. T ~Q(a) 2          
                        8. F (P(a)&~Q(a)) 6   
                        9.{ F P(a) 8          
                        10. @ 5,9}           
                        11.{ F ~Q(a) 8        
                        12. @ 7,11}      
                    </proof>'''
    },
    {"user": "Prove '|- Ex P(x)->~Ax ~P(x)', using the analytical tableau method. Final answer using the notation described.", 
     "assistant": r'''<proof>
                        1. T Ex (P(x)&~Q(x)) pre 
                        2. F ~Ax (P(x)->Q(x)) conclusion 
                        3. T (P(a)&~Q(a)) 1 
                        4. T P(a) 3 
                        5. T ~Q(a) 3 
                        6. T Ax (P(x)->Q(x)) 2 
                        7. T (P(a)->Q(a)) 6 
                        8.{ F P(a) 7 
                        9. @ 4,8} 
                        10.{ T Q(a) 7 
                        11. F Q(a) 5  
                        12. @ 10,11}
                    </proof>'''
    }
]
