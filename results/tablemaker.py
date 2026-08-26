import os
import re
import pandas as pd


# ============================================================
# CONFIGURAÇÃO
# ============================================================

BASE_DIR = "/home/luana/Documentos/eniac_final/results"

EXTRA = ["dn", "tb"]

MODELS = [
    "phi-4",
    "gpt-oss-20b",
    "mistral-small-3.2-24b-instruct-2506",
    "qwen3-32b",
    "gpt-oss-120b",
    "qwen3.5-35b-a3b",
    "google_gemma-4-26b-a4b"
]

TIPOS = ["PRO", "PRE"]

PROMPTS = [
    "S0",
    "S1",
    "S2",
    "S3",
    "S5",
    "C0",
    "C1",
    "C2",
    "C3",
    "C5"
]


# ============================================================
# QUESTÕES FS
# ============================================================

dn_pro_FS_MAP = [
    '(A->B)&(~A->B)|-B',
    'A|B|-(~A->B)&(~B->A)',
    '~(A&B)|-~A|~B',
    '~A->~B,(C&D)|B,~A->~D|-~C|A',
    '~(A->~B)|-A&B'
]

dn_pre_FS_MAP = [
    '|- (B->Ex C(x))->Ex (B->C(x))',
    'Ax ((B(x)->C(x))&(C(x)->B(x))) |- Ax ((~B(x)->~C(x))&(~C(x)->~B(x)))',
    'Ax Ey (B(x)|C(y)) |- Ey Ax (B(x)|C(y))',
    '|- Ax (B(x)|C)->(Ax B(x)|C)',
    'Ax (~B(x)|C(x)), Ex B(x) |- Ex C(x)'
]

tb_pro_FS_MAP = [
    '(A|B)&(A|C)|-A|(B&C)',
    '|-(~A->B)->((~A->~B)->A)',
    '~(~A|~B)|-A&B',
    '~A->~B|-B->A',
    '~A|~B|-~(A&B)'
]

tb_pre_FS_MAP = [
    'Ex B(x), Ax (B(x)->C(x)) |- Ex C(x)',
    'Ax (B(x)|B(x)) |- Ax B(x)',
    '|- Ex (B(x)|C(x))->(Ex B(x)|Ex C(x))',
    'Ax ~(B(x)&~C(x))',
    'Ax ~C(x) |- Ax ~B(x)',
    '|- Ex B(x)->~Ax ~B(x)'
]


FS_MAPS = {
    ("dn", "PRO"): dn_pro_FS_MAP,
    ("dn", "PRE"): dn_pre_FS_MAP,
    ("tb", "PRO"): tb_pro_FS_MAP,
    ("tb", "PRE"): tb_pre_FS_MAP,
}


# ============================================================
# PADRÕES DOS ARQUIVOS
# ============================================================

SIMPLE_FILE_PATTERNS = {
    "S0": "{extra}/{model}/{tipo}/zero_simples/results_zero_simples_{model}_{tipo}.csv",
    "S1": "{extra}/{model}/{tipo}/few1_simples/results_few1_simples_{model}_{tipo}.csv",
    "S2": "{extra}/{model}/{tipo}/few2_simples/results_few2_simples_{model}_{tipo}.csv",
    "S3": "{extra}/{model}/{tipo}/few3_simples/results_few3_simples_{model}_{tipo}.csv",
    "S5": "{extra}/{model}/{tipo}/few_simples/results_few_simples_{model}_{tipo}.csv",
}

COMPLEX_FILE_PATTERNS = {
    "C0": "{extra}/{model}/{tipo}/zero_completo/results_zero_completo_{model}_{tipo}.csv",
    "C1": "{extra}/{model}/{tipo}/few1_completo/results_few1_completo_{model}_{tipo}.csv",
    "C2": "{extra}/{model}/{tipo}/few2_completo/results_few2_completo_{model}_{tipo}.csv",
    "C3": "{extra}/{model}/{tipo}/few3_completo/results_few3_completo_{model}_{tipo}.csv",
    "C5": "{extra}/{model}/{tipo}/few_completo/results_few_completo_{model}_{tipo}.csv",
}

ALL_PATTERNS = {
    **SIMPLE_FILE_PATTERNS,
    **COMPLEX_FILE_PATTERNS
}


# ============================================================
# NORMALIZAÇÃO
# ============================================================

def normalize(s):

    if pd.isna(s):
        return ""

    s = str(s).strip()

    # seta
    s = s.replace("→", "->")

    # remove espaços/quebras
    s = re.sub(r"\s+", "", s)

    return s


# ============================================================
# CONSIDERA O RESULTADO COMO ACERTO
# ============================================================

def is_correct(verification, logic):

    if pd.isna(verification):
        return False

    verification = str(verification).strip()

    # --------------------------------------------------------
    # DEMONSTRAÇÃO DO TEOREMA ERRADO
    # também conta como ACERTO
    # --------------------------------------------------------

    if "Demonstração do teorema errado" in verification:
        return True

    # --------------------------------------------------------
    # Resultado normal de demonstração correta
    # --------------------------------------------------------

    if logic == "dn":

        if "A demonstração está" in verification:
            return True

    elif logic == "tb":

        if "The proof is valid" in verification:
            return True

    return False


# ============================================================
# CALCULA UMA TABELA
# ============================================================

def calcular_tabela(logic, tipo):

    print()
    print("=" * 100)
    print(f"TABELA: {logic.upper()} {tipo}")
    print("=" * 100)

    # --------------------------------------------------------
    # FS correspondente
    # --------------------------------------------------------

    fs_questions = {
        normalize(q)
        for q in FS_MAPS[(logic, tipo)]
    }

    tabela = []

    for model in MODELS:

        linha = {
            "modelo": model
        }

        for prompt in PROMPTS:

            pattern = ALL_PATTERNS[prompt]

            file_path = os.path.join(
                BASE_DIR,
                pattern.format(
                    extra=logic,
                    model=model,
                    tipo=tipo
                )
            )

            # ------------------------------------------------
            # Arquivo não existe
            # ------------------------------------------------

            if not os.path.exists(file_path):

                print(
                    f"⚠️ NÃO ENCONTRADO: "
                    f"{logic}/{tipo}/{model}/{prompt}"
                )

                linha[prompt] = None
                continue

            # ------------------------------------------------
            # Lê
            # ------------------------------------------------

            try:

                df = pd.read_csv(file_path)

            except Exception as e:

                print(
                    f"❌ ERRO: "
                    f"{file_path}"
                )

                print(e)

                linha[prompt] = None
                continue

            # ------------------------------------------------
            # Verifica colunas
            # ------------------------------------------------

            if "question" not in df.columns:

                print(
                    f"⚠️ Sem coluna question: "
                    f"{file_path}"
                )

                linha[prompt] = None
                continue

            if "verification" not in df.columns:

                print(
                    f"⚠️ Sem coluna verification: "
                    f"{file_path}"
                )

                linha[prompt] = None
                continue

            # ------------------------------------------------
            # Remove FS
            # ------------------------------------------------

            question_normalized = (
                df["question"]
                .map(normalize)
            )

            fs_mask = question_normalized.isin(
                fs_questions
            )

            df_analysis = df.loc[
                ~fs_mask
            ].copy()

            qtd_fs = int(fs_mask.sum())

            # ------------------------------------------------
            # Acertos
            # ------------------------------------------------

            correct_mask = df_analysis[
                "verification"
            ].apply(
                lambda x: is_correct(x, logic)
            )

            total_acertos = int(
                correct_mask.sum()
            )

            total_questoes = len(
                df_analysis
            )

            # ------------------------------------------------
            # Acurácia
            # ------------------------------------------------

            if total_questoes > 0:

                accuracy = (
                    total_acertos
                    / total_questoes
                    * 100
                )

            else:

                accuracy = None

            linha[prompt] = (
                f"{accuracy:.2f}%"
                if accuracy is not None
                else None
            )

            print(
                f"{model:45} "
                f"{prompt}: "
                f"{accuracy:.2f}% "
                f"({total_acertos}/{total_questoes}) "
                f"FS removidas={qtd_fs}"
            )

        tabela.append(linha)

    return pd.DataFrame(
        tabela,
        columns=["modelo"] + PROMPTS
    )


# ============================================================
# CALCULA AS 4 TABELAS
# ============================================================

tabelas = {}

for logic in EXTRA:

    for tipo in TIPOS:

        nome = f"{logic}_{tipo}"

        tabelas[nome] = calcular_tabela(
            logic,
            tipo
        )


# ============================================================
# MOSTRA AS TABELAS
# ============================================================

print("\n\n")
print("#" * 100)
print("RESULTADOS FINAIS")
print("#" * 100)

for nome, tabela in tabelas.items():

    print("\n")
    print("=" * 100)
    print(nome.upper())
    print("=" * 100)

    print(
        tabela.to_string(
            index=False,
            float_format=lambda x: f"{x:.2f}"
        )
    )


# ============================================================
# SALVA CSVs INDIVIDUAIS
# ============================================================

for nome, tabela in tabelas.items():

    output_csv = os.path.join(
        BASE_DIR,
        f"acuracia_{nome}_sem_FS.csv"
    )

    tabela.to_csv(
        output_csv,
        index=False,
        encoding="utf-8-sig"
    )

    print(
        f"✅ Salvo: {output_csv}"
    )


# ============================================================
# SALVA TUDO EM UM EXCEL
# ============================================================

output_excel = os.path.join(
    BASE_DIR,
    "acuracia_modelos_por_prompt_sem_FS.xlsx"
)

with pd.ExcelWriter(
    output_excel,
    engine="openpyxl"
) as writer:

    for nome, tabela in tabelas.items():

        tabela.to_excel(
            writer,
            sheet_name=nome.upper(),
            index=False
        )


print()
print("=" * 100)
print("FINALIZADO")
print("=" * 100)

print(
    f"Excel: {output_excel}"
)