simple_pro_content = r"""
You are an expert in logic using the Natural Deduction method.
You will receive one propositional logic problem. You must prove its validity using the natural deduction method, represent the proof in a Fitch-like notation, following these formatting instructions:

### FORMAT OF PROOF LINES
Each proof line must be structured like: '<line_number>. <formula> <origin>'
- <line_number>: sequential integer, always ending with a dot ('1.', '2.', '3.', ...)
- <formula>: the formula derived on that line
- <origin> is exactly one of:
    'pre' (for premises)
    'hip' (for hypothesis)
    '<rule_name> <line_refs>'

### Rules names and their reference formats:
&e (1 line) → e.g., &e 3
&i (2 lines) → e.g., &i 1,3
->e (2 lines) → e.g., ->e 2,5
->i (1 range) → e.g., ->i 8-12
~e (2 lines) → e.g., ~e 4,7
~i (1 range) → e.g., ~i 9-11
|e (1 line + 2 ranges) → e.g., |e 4, 5-9, 10-14
|i (1 line) → e.g., |i 6
@e (1 line) → e.g., @e 7
raa (1 range) → e.g., raa 12-15
copie (1 line) → e.g., copy 2
Note: <line_refs> must be a comma-separated list of line numbers or ranges (used to denote subproofs)

### SUBPROOFS/HYPOTHESES FORMAT
Use curly braces { and } to open and close subproofs. 
Open a subproof with `{` immediately after the line number (e.g. '8.{ A|B |i 3') 
Close a subproof with `}`  at the end of the line (e.g. '12. @ 5,7}'). NEVER written as a separate line and NEVER placed at the beginning of a line.   
If two subproofs close at the same line, you may use }} at the end of that line ( e.g., 15. @ 9,11}} )
Nested subproofs are allowed. Formulas may only be used inside their own subproof or an enclosing one. Never use formulas from closed or sibling subproofs.

### SYMBOLS
Use the following symbols for logical operations: 
 & = conjunction (and), 
 | = disjunction (or), 
 ~ = negation (not), 
 -> = implication (implies).
 """

complet_pro_content = r"""
# General Scheme for each Natural Deduction Rule
Only use the natural deduction rules defined below. Don't invent new rules or shortcuts.

###Initial Setup
Remember the problem given contains premises (separated by commas) before the symbol |-, and the formula after |- is the conclusion.

Step 1: Write all premises first with origin 'pre'.

A proof for <premise_1>,<premise_2>, … <premise_k> ⊢ <conclusion_formula> must begin like: 
1. <premise_1> pre 
2. <premise_2> pre 
... 
n. <premise_k> pre
...

Then expand line by line using only the rules below until the <conclusion_formula> is derived.
----------------------------------------------------------------------------------------
### Conjunction Introduction (&i)
If 'D' and 'B' are true, infer D & B.

Scheme:
m. D
n. B
...
p. D & B   &i  m,n

### Conjunction Elimination (&e)
From D & B, infer D or B (or both).

Scheme 1:
m. D & B 
...
n. D   &e m

Scheme 2:
m. D & B 
...
p. B   &e m

### Implication Introduction (->i)
If the hypothesizing D leads to B, infer D -> B.

Scheme:
m.{D hip 
...
n. B   }
n+1. D -> B ->i  m-n

### Implication Elimination (->e)
From D -> B and D, infer B.

Scheme:
m. D -> B 
...
n. D 
...
p. B   ->e  m,n

### Disjunction Introduction (|i)
From D or B, infer D | B.

Scheme 1:
m. D 
...
p. D | B   |i  m

Scheme 2:
m. B 
...
p. D | B   |i  m

### Disjunction Elimination (|e)
From D | B, prove C by showing that in both of these cases C is true.

Scheme:
m.  D | B 
m+1. { D hip
n. C  }
n+1. { B hip
p. C  }
...
p+1. C   |e  m, (m+1)-n, (n+1)-p

### Negation Introduction (~i)
If assuming B leads to contradiction (@), infer ~B.

Scheme:
m.{B hip 
... 
n. @ }
n+1. ~B   ~i  m-n

### Negation Elimination (~e)
From D and ~D, infer contradiction.

Scheme:
m.  D 
n.  ~D 
...
p. @   ~e  m,n

### Contradiction Elimination (@e)
**ONLY** inside a subproof: from @ infer any formula B.

Scheme:
m.  @ 
...
n.  B   @e m

### Reductio ad Absurdum (raa)
If assuming ~D leads to contradiction, infer D.

Scheme:
m.{~D hip
...
n. @ }
n+1. D   raa  m-n

### Copy Rule (copie)
Duplicate a formula at a later line if needed.

Scheme:
m. D
...
n. D   copie m
"""

ending_pro_content = r""" 
Write only the final proof in <proof>...</proof> tags. Only use <proof>...</proof> tags ONCE. Only use these symbols inside the proof '&' , '->', '~', '|', '@', '(', ')', '{', '}'.
Do not include explanations, commentary, or extra text inside and outside the <proof>...</proof> tags.
 """

simple_pre_content = r"""
You are an expert in logic using the Natural Deduction method.
You will receive one first order logic problem. Your task is to prove its validity using Natural Deduction and represent the proof in a Fitch-like notation, following these formatting instructions.

### FORMAT OF PROOF LINES
Each proof line must be structured like: '<line_number>. <formula> <origin>'
- <line_number>: sequential integer, always ending with a dot ('1.', '2.', '3.', ...)
- <formula>: the formula derived on that line
- <origin>: either 'pre' (premise), 'hip' (hypothesis) or '<rule_name> <line_refs>'
  - <rule_name> and <line_refs>: 
    - &e (1 line)  
    - &i (2 lines)  
    - ->e (2 lines)  
    - ->i (1 range)  
    - ~e (2 lines)  
    - ~i (1 range)  
    - |e (1 line + 2 ranges)  
    - |i (1 line)  
    - @e (1 line)  
    - raa (1 range)  
    - copy (1 line)  
    - Ae (1 line)
    - Ai (1 range)
    - Ee (1 line + 1 range)
    - Ei (1 line)
  - <line_refs>: Must be comma-separated line numbers or ranges. Ranges denote subproofs (e.g., `->i 8-12`, `|e 4, 5-9, 10-14`)

### SUBPROOFS / HYPOTHESES
Use subproofs for hypotheses. Use curly braces '{' and '}' to open and close subproofs. 
Place `{` immediately after the line number (e.g. '8.{ A|B hip') and `}` at the end of the final line of the subproof (e.g. '10. B @e 4}').
Nested subproofs are allowed. But a formula may only be used at a specific point if it appeared earlier in the same subproof or an outer subproof to the current subproof.

### SYMBOLS & CONVENTIONS
Use the following symbols for logical operations: 
- & = conjunction (and) 
- | = disjunction (or) 
- ~ = negation (not) 
- -> = implication (implies)

Quantifiers symbols:  
    Ax represents ∀x  
    Ex represents ∃x
So formulas with ∀x and ∃x will be represented by Ax and Ex (A and E followed by the variable x). For example, Ax (H(x)->M(x)) represents ∀x (H(x)→M(x)).

###CONVENTIONS
Atoms: only uppercase letters not immediately followed by parentesis (e.g. P, Q, R).
Predicates: uppercase letters immediately followed by parentesis (e.g. H(x), M(y), Q(a,b) ). All predicates must use parentheses.
Variables: first letter in lowercase, can be followed by letters and numbers (e.g., x, x0, xP0).

### TO CREATE NEW VARIABLE:
For Universal Introduction rule(Ai): open a subproof with a fresh variable not occurring in any open hypothesis.
Create new variable like this:  '<line_number>. { <new_variable> '

For Existential Elimination rule(Ee): open a subproof with a fresh witness constant/variable. 
Create new variable like this: '<line_number>. {<new_variable> φ[<old_variable>/<new_variable>] hip
 """

complet_pre_content = r"""
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

### FIRST-ORDER LOGIC NATURAL DEDUCTION RULES
###Rule of Universal Elimination (Ae)
From Ax φ, infer φ[x/t]
Condition: 't' is replaceable for the variable 'x' in φ.

Scheme:
m. AxP
...
n. φ[x/t] Ae m

###Rule of Existential Introduction (Ei)
From φ[x/t], infer Ex φ
Condition: 't' is replaceable for the variable 'x' in φ.

Scheme:
m. φ[x/t]
...
p. Ex φ Ei m

###Rule of Universal Introduction (Ai)
Begin with a new variable 'a' and prove M(a) to infer Ax M(x).  

Scheme:
m. { a
...
n.   M(a) }
n+1. Ax M(x) Ai m-n

###Rule of Existential Elimination (Ee)
Assume φ[a] with a fresh variable a inside a subproof. From that assumption, derive either a contradiction or a desired conclusion. Then discharge the assumption to infer the result outside the subproof.

Scheme 1:
m. Ex φ
n. {a φ[x/a] hip
...
p.  @ }
p+1. @ Ee m, n-p 

Scheme 2:
m. Ex φ
n. {a φ[x/a] hip
...
p.  P }
p+1. P Ee m, n-p 
"""

ending_pre_content = r""" Write only the final proof in <proof>...</proof> tags. Only use <proof>...</proof> tags ONCE. Only use these symbols inside the proof '&' , '->', '~', '|', '@', '(', ')', '{', '}', 'Ax', 'Ex'.
Do not include explanations, commentary, or extra text inside and outside the <proof>...</proof> tags.
"""



exemplos_pro_nadia = [
    {"user": "Prove '(A->B)&(~A->B) |- B', using the natural deduction method. Final answer using the notation described. ",
    "assistant": r''' <proof>
                        1. (A -> B) & (~A -> B) pre
                        2. A -> B &e 1
                        3. ~A -> B &e 1
                        4. { ~(A | ~A) hip
                        5. { A hip
                        6. A | ~A |i 5
                        7. @ ~e 6,4}
                        8. ~A ~i 5-7
                        9. A | ~A |i 8
                        10. @ ~e 9,4}
                        11. A | ~A raa 4-10
                        12. { A hip
                        13. B ->e 12,2}
                        14. { ~A hip
                        15. B ->e 14,3}
                        16. B |e 11, 12-13, 14-15
                        </proof>'''
    },
    {"user": "Prove 'A|B |- (~A->B)&(~B->A)', using the natural deduction method. Final answer using the notation described.", 
     "assistant": r''' <proof>
                        1. A | B pre
                        2. {~A hip
                        3. {A hip
                        4. @ ~e 2,3
                        5. B @e 4}
                        6. {B hip
                        7. B copie 6}
                        8. B |e 1,3-5,6-7}
                        9. ~A -> B ->i 2-8
                        10. {~B hip
                        11. {A hip
                        12. A copie 11}
                        13. {B hip
                        14. @ ~e 10,13
                        15. A @e 14}
                        16. A |e 1,11-12,13-15}
                        17. ~B -> A ->i 10-16
                        18. (~A -> B) & (~B -> A) &i 9,17
                        </proof>'''
    },
    {"user": "Prove '~(A&B) |- ~A|~B', using the natural deduction method. Final answer using the notation described.",
      "assistant": r'''<proof>
                        1. ~(A & B) pre 
                        2. { ~(~A | ~B) hip 
                        3. { ~A hip 
                        4. ~A | ~B |i 3 
                        5. @ ~e 4, 2 } 
                        6. A raa 3-5 
                        7. { ~B hip 
                        8. ~A | ~B |i 7 
                        9. @ ~e 8, 2 } 
                        10. B raa 7-9 
                        11. A & B &i 6, 10 
                        12. @ ~e 11, 1 } 
                        13. ~A | ~B raa 2-12 
                        </proof>'''
    },
    {"user": "Prove '~S->~R, (P&Q)|R, ~S->~Q |- ~P|S', using the natural deduction method. Final answer using the notation described.", 
     "assistant": r'''<proof>
                        1. (~S->~R)				pre
                        2. ((P&Q)|R)				pre
                        3. (~S->~Q)				pre
                        4. { (P&Q)				hip
                        5.   Q					&e 4
                        6.   { ~S				hip
                        7.     ~Q				->e 6,3
                        8.     @				~e 5,7}
                        9.   S					raa 6-8}
                        10. { R					hip
                        11.   { ~S				hip
                        12.      ~R				->e 1,11
                        13.      @				~e 10,12}
                        14.   S					raa 11-13}
                        15. S					|e 2,4-9,10-14
                        16. (~P|S)				|i 15
                        </proof>'''
    },
    {"user": "Prove '~(A->~B) |- A&B', using the natural deduction method. Final answer using the notation described.", 
     "assistant": r'''<proof>
                        1. ~ (A -> ~ B) pre 
                        2. { ~ A hip 
                        3. { A hip 
                        4. @ ~e 2,3 
                        5. ~B @e 4 } 
                        6. A->~B ->i 3-5 
                        7. @ ~e 6,1 } 
                        8. A raa 2-7 
                        9. { ~ B hip 
                        10. { A hip 
                        11. ~ B copie 9 } 
                        12. (A -> ~ B) ->i 10-11 
                        13. @ ~e 12, 1 } 
                        14. B raa 9-13 
                        15. A & B &i 8, 14 
                        </proof>'''
    },
] 

exemplos_pre_nadia = [
    {"user": "Prove '|- (P->Ex Q(x))->Ex (P->Q(x))', using the natural deduction method. Final answer using the notation described. ",
    "assistant": r''' <proof>
                        1. { 	(P -> Ex Q(x))					hip
                        2.	{	~(~P | Ex Q(x))					hip
                        3.		{	P								      hip
                        4.      Ex Q(x)               ->e 3, 1
                        5.			~P | Ex Q(x)					|i 4
                        6.			@								~e 5,2 }		
                        7.		~P									~i 3-6
                        8.		~P | Ex Q(x)						|i 7
                        9.		@									~e 8,2 }
                        10.	~P | Ex Q(x)        raa 2-9
                        11.	{	~P									hip
                        12.		{	P								hip
                        13.			@								~e 11,12
                        14.     Q(a)            @e 13 }
                        15.		P -> Q(a)							->i 12-14
                        16.		Ex  (P -> Q(x))					Ei 15 }
                        17.	{	Ex Q(x)							hip
                        18.		{ a		Q(a)						hip
                        19.			{	P							hip
                        20.				Q(a)						copie 18 }
                        21.			P -> Q(a)						->i 19-20
                        22.			Ex (P -> Q(x))				Ei 21 }
                        23.		Ex (P -> Q(x))					Ee 17, 18-22 }
                        24.	Ex (P -> Q(x))						|e 10, 11-16, 17-23}
                        25. (P -> Ex Q(x)) -> Ex (P -> Q(x))	->i 1-24
                    </proof>'''
    },
    {"user": "Prove 'Ax ((P(x)->Q(x))&(Q(x)->P(x))) |- Ax ((~P(x)->~Q(x))&(~Q(x)->~P(x)))', using the natural deduction method. Final answer using the notation described.", 
     "assistant": r''' <proof>
                            1. Ax((P(x) -> Q(x)) & (Q(x) -> P(x))) pre
                            2. { a
                            3.   (P(a) -> Q(a)) & (Q(a) -> P(a)) Ae 1
                            4.   P(a) -> Q(a) &e 3
                            5.   Q(a) -> P(a) &e 3
                            6.   { ~Q(a) hip
                            7.     { P(a) hip
                            8.       Q(a) ->e 7,4
                            9.       @ ~e 6,8 }
                            10.   ~P(a) ~i 7-9 }
                            11. ~Q(a) -> ~P(a) ->i 6-10
                            12. { ~P(a) hip
                            13.   { Q(a) hip
                            14.     P(a) ->e 13,5
                            15.     @ ~e 12,14 }
                            16.   ~Q(a) ~i 13-15 }
                            17. ~P(a) -> ~Q(a) ->i 12-16
                            18. (~P(a) -> ~Q(a)) & (~Q(a) -> ~P(a)) &i 17,11 }
                            19. Ax((~P(x) -> ~Q(x)) & (~Q(x) -> ~P(x))) Ai 2-18 
                        </proof>'''
    },
    {"user": "Prove 'Ax Ey (P(x)|Q(y)) |- Ey Ax (P(x)|Q(y))', using the natural deduction method. Final answer using the notation described.",
      "assistant": r'''<proof>
                            1. AxEy(P(x)|Q(y))					pre
                            2. { 	~EyAx(P(x)|Q(y))				hip
                            3.	{ a
                            4.		{	Ax(P(x)|Q(a))			hip
                            5.			EyAx(P(x)|Q(y))			Ei 4
                            6.			@				~e 2,5 }
                            7.		~Ax(P(x)|Q(a))				~i 4-6 }
                            8.	Ay~Ax(P(x)|Q(y))				Ai 3-7
                            9.	{ a
                            10.		~Ax(P(x)|Q(a))				Ae 8
                            11.		{	~Ex~(P(x)|Q(a))			hip
                            12.			{ b
                            13.				{ 	~(P(b)|Q(a))	hip
                            14.					Ex~(P(x)|Q(a))	Ei 13
                            15.					@		~e 11,14 }
                            16.				P(b)|Q(a)		raa 13-15 }
                            17.			Ax(P(x)|Q(a))			Ai 12-16
                            18.			@				~e 10,17 }
                            19.		Ex~(P(x)|Q(a))				raa 11-18 }	
                            20.	AyEx~(P(x)|Q(y))				Ai 9-19
                            21.    	Ex ~(P(x)|Q(b))					Ae 20
                            22.	{ a	~(P(a)|Q(b))				hip
                            23.		Ey(P(a)|Q(y))				Ae 1		
                            24.		{ c	P(a)|Q(c)			hip
                            25.			{	P(a)			hip
                            26.				P(a)|Q(b)		|i 25
                            27.				@			~e 22,26 }
                            28.			{	Q(c)			hip
                            29.				Ex ~(P(x)|Q(c))		Ae 20
                            30.				{ d	~(P(d)|Q(c))	hip
                            31.					P(d)|Q(c)	|i 28
                            32.					@		~e 30,31 }
                            33.				@			Ee 29, 30-32 }
                            34.			@				|e 24, 25-27, 28-33 }
                            35.		@					Ee 23, 24-34  }	
                            36.	@						Ee 21, 22-35 }
                            37. EyAx(P(x)|Q(y))					raa 2-36
                        </proof>'''
    },
    {"user": "Prove '|- Ax (P(x)|Q)->(Ax P(x)|Q)', using the natural deduction method. Final answer using the notation described.", 
     "assistant": r'''<proof>
                        1. { Ax(P(x) | Q) hip 
                        2. { ~(Ax P(x) | Q) hip 
                        3. { a 
                        4. P(a) | Q Ae 1 
                        5. { P(a) hip } 
                        6. { Q hip 
                        7. Ax P(x) | Q |i 6 
                        8. @ ~e 7,2 
                        9. P(a) @e 8 } 
                        10. P(a) |e 4, 5-5, 6-9 } 
                        11. Ax P(x) Ai 3-10 
                        12. Ax P(x) | Q |i 11 
                        13. @ ~e 2,12 } 
                        14. Ax P(x) | Q raa 2-13 } 
                        15. Ax(P(x) | Q) -> (Ax P(x) | Q) ->i 1-14
                    </proof>'''
    },
    {"user": "Prove 'Ax (~H(x)|M(x)), Ex H(x) |- Ex M(x)', using the natural deduction method. Final answer using the notation described.", 
     "assistant": r'''<proof>
                        1. Ax (~H(x)|M(x)) pre 
                        2. Ex H(x) pre 
                        3. { a H(a) hip 
                        4. ~H(a)|M(a) Ae 1 
                        5. { ~H(a) hip 
                        6. @ ~e 3,5 
                        7. Ex M(x) @e 6 } 
                        8. { M(a) hip 
                        9. Ex M(x) Ei 8 } 
                        10. Ex M(x) |e 4, 5-7, 8-9 } 
                        11.Ex M(x) Ee 2, 3-10
                    </proof>'''
    },
] 
