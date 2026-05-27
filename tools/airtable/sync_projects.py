"""
Lê os dados do SecondBrain e faz upsert em todas as tabelas do Airtable.
Pode ser rodado múltiplas vezes (idempotente via upsert).

Uso:
  cd tools/airtable
  python sync_projects.py
"""
import sys
import yaml
from pathlib import Path
from datetime import date

sys.path.insert(0, str(Path(__file__).parent))
from _common import upsert_records, BASE_ID

CONFIG_PATH = Path(__file__).parent / "config.yaml"
SECONDBRAIN = Path(__file__).parent.parent.parent / "SecondBrain" / "projetos"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def load_config() -> dict:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError("config.yaml não encontrado. Rode setup_base.py primeiro.")
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))


def load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def str_or(value, default="A confirmar") -> str:
    if value is None or str(value).strip().startswith("_"):
        return default
    return str(value)


# ---------------------------------------------------------------------------
# Dados dos projetos
# ---------------------------------------------------------------------------

PROJETOS = [
    {
        "slug": "128-cnh-festival-agricultura",
        "codigo": "128",
        "nome": "Festival Agricultura Sustentável",
        "patrocinador": "CNH / New Holland Agriculture",
        "sub_marca": "New Holland",
        "lei": "Rouanet",
        "pronac": "259965",
        "empresa_proponente": "Sustentabilidade e Cultura Produções Artísticas Ltda",
        "cnpj": "19.541.589/0001-63",
        "executor": "Lucas Rotta",
        "responsavel_tecnico": "Ana Carolina",
        "drive": "https://drive.google.com/drive/folders/1ay0JHTF3rP2WCBZojrbWoKe2vom3mRyc",
        "clickup": "https://app.clickup.com/9011929793/v/l/li/901113794977",
        "orcamento_original": 1_500_000,
        "orcamento_aprovado": 600_000,
    },
    {
        "slug": "129-cnh-agrofuturo-escolas",
        "codigo": "129",
        "nome": "Agrofuturo Cultural nas Escolas",
        "patrocinador": "CNH / Case IH Agriculture",
        "sub_marca": "Case IH",
        "lei": "Rouanet",
        "pronac": "A confirmar",
        "empresa_proponente": "A confirmar",
        "cnpj": "A confirmar",
        "executor": "Lucas Rotta",
        "responsavel_tecnico": "Abilio Martins",
        "drive": "https://drive.google.com/drive/folders/1xV3NRhagpS20g3qZ0rcc4TqIEfbnH9Q0",
        "clickup": "https://app.clickup.com/9011929793/v/l/li/901113794979",
        "orcamento_original": None,
        "orcamento_aprovado": None,
    },
    {
        "slug": "132-estacao-samarco",
        "codigo": "132",
        "nome": "Estação Samarco, Territórios do Futuro",
        "patrocinador": "Samarco Mineração",
        "sub_marca": "Samarco",
        "lei": "Corporativo direto",
        "pronac": "N/A",
        "empresa_proponente": "NTICS",
        "cnpj": "A confirmar",
        "executor": "Lucas Rotta",
        "responsavel_tecnico": "Bruna Seibel / Abilio Martins",
        "drive": "A confirmar",
        "clickup": "A confirmar",
        "orcamento_original": None,
        "orcamento_aprovado": None,
    },
]


# ---------------------------------------------------------------------------
# Sync Projetos
# ---------------------------------------------------------------------------

FASES = {"128": "pre-kickoff", "129": "kickoff-pendente", "132": "execucao"}

def sync_projetos(table_name: str):
    print("\n[Projetos]")
    records = []
    for p in PROJETOS:
        rec = {
            "Código": p["codigo"],
            "Nome": p["nome"],
            "Patrocinador": p["patrocinador"],
            "Sub-marca": p["sub_marca"],
            "Lei": p["lei"],
            "PRONAC": p["pronac"],
            "Empresa Proponente": p["empresa_proponente"],
            "CNPJ Proponente": p["cnpj"],
            "Fase": FASES.get(p["codigo"], "A confirmar"),
            "Executor Direto": p["executor"],
            "Responsável Técnico": p["responsavel_tecnico"],
            "Pasta Drive": p["drive"],
            "ClickUp Lista": p["clickup"],
            "Atualizado em": str(date.today()),
        }
        if p["orcamento_original"]:
            rec["Orçamento Original (R$)"] = p["orcamento_original"]
        if p["orcamento_aprovado"]:
            rec["Orçamento Aprovado (R$)"] = p["orcamento_aprovado"]
        records.append(rec)
        print(f"  {p['codigo']}: {p['nome']}")
    r = upsert_records(table_name, records, ["Código"])
    print(f"  criados: {len(r['createdRecords'])} | atualizados: {len(r['updatedRecords'])}")


# ---------------------------------------------------------------------------
# Sync TAP
# ---------------------------------------------------------------------------

TAP_DATA = {
    "128": {
        "status": "rascunho",
        "objetivo": (
            "Promover consciência ambiental, alimentar e agrícola entre crianças da rede pública "
            "(preferencialmente escolas rurais) por meio de 7 oficinas práticas mensais sobre "
            "agricultura sustentável, com encerramento em DOMO imersivo itinerante em praça pública."
        ),
        "escopo": (
            "4 cidades: Curitiba/PR (principal, DOMO + oficinas), Guarapuava/PR, Toledo/PR, Dom Pedrito/RS.\n"
            "Etapa 1: 7 oficinas escolares/cidade (ensino fundamental e médio, rede pública rural).\n"
            "Etapa 2: Plataforma Digital 'New Holland Online' (professor, estudante, gestor).\n"
            "Etapa 3: DOMO imersivo itinerante em praça pública em Curitiba (evento final)."
        ),
        "cidades": "Dom Pedrito/RS → Toledo/PR → Guarapuava/PR → Curitiba/PR (itinerância sequencial, decisão 18/05)",
        "publico": "Estudantes do ensino fundamental e médio. Escolas públicas, preferencialmente rurais.",
        "entregas": (
            "1. 7 temas trabalhados por escola (oficinas + materiais)\n"
            "2. Kit pedagógico físico por escola\n"
            "3. Plataforma digital 'New Holland Online'\n"
            "4. Relatórios mensais + relatório ESG final\n"
            "5. DOMO imersivo com 2 ambientes temáticos\n"
            "6. Celebração final (exposição + feira + certificação)"
        ),
        "resultados": (
            "Aproximação entre população urbana e rural com foco em tecnologia e sustentabilidade.\n"
            "Engajamento de empresas, universidades e lideranças para pensar o futuro do agro brasileiro.\n"
            "Estímulo à educação agro em jovens da rede pública.\n"
            "1.000 alunos únicos beneficiados. 7.000 atendimentos totais."
        ),
        "lei": "Rouanet | PRONAC 259965",
    },
    "129": {
        "status": "pendente formal",
        "objetivo": (
            "Integrar arte, cultura e tecnologia ao ensino público com foco em inovação no agronegócio, "
            "por meio de 8 oficinas presenciais, plataforma digital 'Agrofuturo Digital', peça de teatro "
            "interativa, Feira de Tecnologia, Arte e Cultura, e Seminário AgroInova Summit."
        ),
        "escopo": (
            "Frente 1: Agrofuturo nas Escolas — 8 oficinas + plataforma digital + teatro + feira.\n"
            "Frente 2: Seminário AgroInova Summit — 'O Futuro do Campo em Debate'.\n"
            "Frente 3: Apoio à comunicação e mídia local alinhado à marca Case IH."
        ),
        "cidades": "A definir (modelo 'cidades-cabeça' similar ao projeto 128 — 3 a 4 cidades)",
        "publico": "Alunos da rede pública, professores, colaboradores CNH (Seminário), pais e comunidade (Feira).",
        "entregas": (
            "1. 8 oficinas presenciais + Oficina Final 'Desafio AgroFuturo' (escape room)\n"
            "2. Peça de Teatro Interativa\n"
            "3. Plataforma digital 'Agrofuturo Digital'\n"
            "4. Feira de Tecnologia, Arte e Cultura (startups, agro, universidades, ONGs)\n"
            "5. Seminário AgroInova Summit\n"
            "6. Kit pedagógico por escola"
        ),
        "resultados": (
            "Jovens da rede pública com visão de inovação e tecnologia no agro.\n"
            "Case IH posicionada como referência em inovação social.\n"
            "Conexão entre escolas, empresas do agro e comunidade local."
        ),
        "lei": "Rouanet | PRONAC a confirmar",
    },
    "132": {
        "status": "rascunho",
        "objetivo": (
            "Oferecer capacitação profissionalizante gratuita em empreendedorismo, culinária e beleza "
            "para comunidades prioritárias de Minas Gerais e Espírito Santo impactadas pelo programa "
            "Samarco, com certificação rastreável e acesso à plataforma digital de apoio."
        ),
        "escopo": (
            "12 comunidades prioritárias: 7 MG (Camargos, Antônio Pereira, Bento Rodrigues, "
            "Paracatu de Baixo, Santa Rita Durão, Brumal, Catas Altas) + "
            "5 ES (Meaípe, Mãe-Bá, Parati, Ubu, Recanto do Sol).\n"
            "3 trilhas: Inicial Empreendedorismo (4h), Culinária (50h), Beleza (50h).\n"
            "Certificação via e-certificado.com. Plataforma de apoio em Lovable."
        ),
        "cidades": "MG: Camargos, Antônio Pereira, Bento Rodrigues†, Paracatu de Baixo†, Santa Rita Durão†, Brumal, Catas Altas | ES: Meaípe, Mãe-Bá, Parati, Ubu, Recanto do Sol (†comunidades diretamente atingidas — cuidado editorial máximo)",
        "publico": "Moradores das 12 comunidades prioritárias Samarco MG e ES. Foco em mulheres empreendedoras.",
        "entregas": (
            "1. Trilha Inicial Empreendedorismo (4h presenciais — 12 comunidades)\n"
            "2. Trilha de Culinária (24h presenciais + 22h digitais)\n"
            "3. Trilha de Beleza (24h presenciais + 22h digitais)\n"
            "4. Plataforma digital Lovable com conteúdo das trilhas\n"
            "5. Certificação via e-certificado.com (LinkedIn)\n"
            "6. 19 entregas de design (KV, rollups, camisetas, certificados etc.)\n"
            "7. Grade de redes sociais (vídeos pré/durante/pós + carrosseis)"
        ),
        "resultados": (
            "Participantes capacitados com certificação reconhecida.\n"
            "Geração de renda e empreendedorismo nas comunidades.\n"
            "12 comunidades atendidas em MG e ES.\n"
            "Samarco posicionada como correalizadora do desenvolvimento territorial."
        ),
        "lei": "Patrocínio corporativo direto (sem PRONAC/MINC)",
    },
}


def sync_tap(table_name: str):
    print("\n[TAP]")
    records = []
    for p in PROJETOS:
        d = TAP_DATA[p["codigo"]]
        records.append({
            "Projeto": p["nome"],
            "Código": p["codigo"],
            "Status TAP": d["status"],
            "Objetivo Geral": d["objetivo"],
            "Escopo": d["escopo"],
            "Cidades": d["cidades"],
            "Público-alvo": d["publico"],
            "Entregas Principais": d["entregas"],
            "Resultados Esperados": d["resultados"],
            "Legislação / Programa": d["lei"],
        })
        print(f"  {p['codigo']}: TAP — {d['status']}")
    r = upsert_records(table_name, records, ["Código"])
    print(f"  criados: {len(r['createdRecords'])} | atualizados: {len(r['updatedRecords'])}")


# ---------------------------------------------------------------------------
# Sync Metodologias
# ---------------------------------------------------------------------------

METODOLOGIAS = [
    # 128 — 7 temas
    {"ID": "128-T1", "Código Projeto": "128", "Projeto": "Festival Agricultura Sustentável",
     "Nome": "A Terra e a Semente", "Tipo": "oficina-cultural-minc",
     "Conceitos / Tópicos": "Solo, germinação, compostagem",
     "Atividade / Metodologia": "Instalação coletiva com materiais recicláveis + plantio de sementes",
     "ODS": "ODS 2", "Linguagem MinC": "Artes Plásticas"},
    {"ID": "128-T2", "Código Projeto": "128", "Projeto": "Festival Agricultura Sustentável",
     "Nome": "Ciclo da Água e Irrigação Sustentável", "Tipo": "oficina-tematica",
     "Conceitos / Tópicos": "Uso racional da água, captação de chuva",
     "Atividade / Metodologia": "Construção de maquete de irrigação por gotejamento",
     "ODS": "ODS 6", "Linguagem MinC": ""},
    {"ID": "128-T3", "Código Projeto": "128", "Projeto": "Festival Agricultura Sustentável",
     "Nome": "Alimentos do Campo e da Cidade", "Tipo": "oficina-cultural-minc",
     "Conceitos / Tópicos": "Origem dos alimentos, cadeia produtiva",
     "Atividade / Metodologia": "Ensaio fotográfico do percurso do alimento (do campo à mesa)",
     "ODS": "ODS 2, ODS 12", "Linguagem MinC": "Fotografia"},
    {"ID": "128-T4", "Código Projeto": "128", "Projeto": "Festival Agricultura Sustentável",
     "Nome": "A Nova Agricultura e Sabores Locais", "Tipo": "oficina-tematica",
     "Conceitos / Tópicos": "Cultura do campo, indicações geográficas, saberes indígenas e quilombolas",
     "Atividade / Metodologia": "Roda de histórias + desenho das plantas e produtos da região",
     "ODS": "ODS 4, ODS 12", "Linguagem MinC": ""},
    {"ID": "128-T5", "Código Projeto": "128", "Projeto": "Festival Agricultura Sustentável",
     "Nome": "Clima e o Campo", "Tipo": "oficina-tematica",
     "Conceitos / Tópicos": "Efeitos do clima na produção agrícola, conectividade, plantio direto",
     "Atividade / Metodologia": "Jogo de simulação de clima (seca, geada, calor) e suas soluções",
     "ODS": "ODS 13", "Linguagem MinC": ""},
    {"ID": "128-T6", "Código Projeto": "128", "Projeto": "Festival Agricultura Sustentável",
     "Nome": "Ciclo do Metano como Combustível Alternativo", "Tipo": "oficina-tematica",
     "Conceitos / Tópicos": "Aproveitamento de resíduos, geração de energia, tecnologias no campo",
     "Atividade / Metodologia": "Dinâmica sobre aproveitamento de resíduos e geração de energia",
     "ODS": "ODS 7, ODS 13", "Linguagem MinC": ""},
    {"ID": "128-T7", "Código Projeto": "128", "Projeto": "Festival Agricultura Sustentável",
     "Nome": "Cidadania e Sustentabilidade", "Tipo": "oficina-cultural-minc",
     "Conceitos / Tópicos": "Papel da criança como guardiã da terra",
     "Atividade / Metodologia": "Grande Contação de Histórias (toda a escola) + carta ao futuro + mural do compromisso + entrega Guardião da Terra",
     "ODS": "ODS 12", "Linguagem MinC": "Contação de Histórias"},

    # 129 — 8 temas + eventos
    {"ID": "129-T1", "Código Projeto": "129", "Projeto": "Agrofuturo Cultural nas Escolas",
     "Nome": "Do Campo à Mesa", "Tipo": "oficina-tematica",
     "Conceitos / Tópicos": "Cadeia produtiva do alimento, agro sustentável",
     "Atividade / Metodologia": "Mapeamento da cadeia do alimento + debate sobre origem e impacto ambiental",
     "ODS": "ODS 2, ODS 12", "Linguagem MinC": ""},
    {"ID": "129-T2", "Código Projeto": "129", "Projeto": "Agrofuturo Cultural nas Escolas",
     "Nome": "Tecnologia no Campo", "Tipo": "oficina-tematica",
     "Conceitos / Tópicos": "Drones, sensores, agricultura de precisão, IoT rural",
     "Atividade / Metodologia": "Demonstração de tecnologias Case IH + simulação de uso",
     "ODS": "ODS 9", "Linguagem MinC": ""},
    {"ID": "129-T3", "Código Projeto": "129", "Projeto": "Agrofuturo Cultural nas Escolas",
     "Nome": "Água: Fonte de Vida e Produção", "Tipo": "oficina-tematica",
     "Conceitos / Tópicos": "Gestão hídrica, irrigação eficiente, conservação",
     "Atividade / Metodologia": "Experimento prático de captação e reuso de água",
     "ODS": "ODS 6", "Linguagem MinC": ""},
    {"ID": "129-T4", "Código Projeto": "129", "Projeto": "Agrofuturo Cultural nas Escolas",
     "Nome": "Energia no Agro", "Tipo": "oficina-tematica",
     "Conceitos / Tópicos": "Biocombustíveis, energia renovável no campo",
     "Atividade / Metodologia": "Demonstração de biocombustíveis + debate sobre matriz energética",
     "ODS": "ODS 7, ODS 13", "Linguagem MinC": ""},
    {"ID": "129-T5", "Código Projeto": "129", "Projeto": "Agrofuturo Cultural nas Escolas",
     "Nome": "Agro e Clima", "Tipo": "oficina-tematica",
     "Conceitos / Tópicos": "Mudanças climáticas, impacto na produção, adaptação",
     "Atividade / Metodologia": "Jogo de simulação de cenários climáticos + soluções de adaptação",
     "ODS": "ODS 13", "Linguagem MinC": ""},
    {"ID": "129-T6", "Código Projeto": "129", "Projeto": "Agrofuturo Cultural nas Escolas",
     "Nome": "Cidadania e Sustentabilidade no Campo", "Tipo": "oficina-tematica",
     "Conceitos / Tópicos": "Papel do jovem no agro, ESG rural, liderança comunitária",
     "Atividade / Metodologia": "Dinâmica de liderança + carta compromisso com o futuro do campo",
     "ODS": "ODS 12, ODS 17", "Linguagem MinC": ""},
    {"ID": "129-T7", "Código Projeto": "129", "Projeto": "Agrofuturo Cultural nas Escolas",
     "Nome": "Oficina de Robótica e RA/VR", "Tipo": "oficina-tematica",
     "Conceitos / Tópicos": "Robótica educacional, realidade aumentada/virtual no agro",
     "Atividade / Metodologia": "Montagem e programação básica de robôs + experiência RA/VR",
     "ODS": "ODS 4, ODS 9", "Linguagem MinC": ""},
    {"ID": "129-T8", "Código Projeto": "129", "Projeto": "Agrofuturo Cultural nas Escolas",
     "Nome": "Desafio AgroFuturo (Escape Room Rural)", "Tipo": "oficina-tematica",
     "Conceitos / Tópicos": "Integração de todos os temas anteriores, trabalho em equipe",
     "Atividade / Metodologia": "Escape room temático: missões agro que integram tecnologia, sustentabilidade e cidadania",
     "ODS": "ODS 4, ODS 9, ODS 13", "Linguagem MinC": ""},
    {"ID": "129-TEATRO", "Código Projeto": "129", "Projeto": "Agrofuturo Cultural nas Escolas",
     "Nome": "Peça de Teatro Interativa", "Tipo": "peça-teatro",
     "Conceitos / Tópicos": "Inovação no campo, jovens protagonistas do agro",
     "Atividade / Metodologia": "Espetáculo teatral interativo com participação da plateia escolar",
     "ODS": "ODS 4", "Linguagem MinC": "Teatro"},
    {"ID": "129-FEIRA", "Código Projeto": "129", "Projeto": "Agrofuturo Cultural nas Escolas",
     "Nome": "Feira de Tecnologia, Arte e Cultura", "Tipo": "feira",
     "Conceitos / Tópicos": "Startups do agro, universidades, ONGs, arte regional, gastronomia local",
     "Atividade / Metodologia": "Evento aberto à comunidade com estandes, bandas regionais e gastronomia local. Parceiros aprovados pela CNH.",
     "ODS": "ODS 9, ODS 11, ODS 17", "Linguagem MinC": ""},
    {"ID": "129-SEMINARIO", "Código Projeto": "129", "Projeto": "Agrofuturo Cultural nas Escolas",
     "Nome": "Seminário AgroInova Summit", "Tipo": "seminario",
     "Conceitos / Tópicos": "O Futuro do Campo em Debate — colaboradores, pais, cidade",
     "Atividade / Metodologia": "Palco com palestrantes do agro, tecnologia e sustentabilidade. Público: colaboradores CNH + comunidade.",
     "ODS": "ODS 9, ODS 17", "Linguagem MinC": ""},

    # 132 — 3 trilhas
    {"ID": "132-TRILHA-INICIAL", "Código Projeto": "132", "Projeto": "Estação Samarco, Territórios do Futuro",
     "Nome": "Trilha Inicial — Empreendedorismo", "Tipo": "trilha-formativa",
     "Carga Horária": "4h presenciais (3h em Camargos)",
     "Conceitos / Tópicos": "Mentalidade empreendedora, gestão financeira básica, precificação, atendimento ao cliente, turismo/hospitalidade, marketing digital, IA para divulgar",
     "Atividade / Metodologia": "6 tópicos em 1 encontro presencial. Aplicada em todas as 12 comunidades.",
     "ODS": "ODS 8, ODS 11", "Linguagem MinC": ""},
    {"ID": "132-TRILHA-CULINARIA", "Código Projeto": "132", "Projeto": "Estação Samarco, Territórios do Futuro",
     "Nome": "Trilha de Culinária", "Tipo": "trilha-formativa",
     "Carga Horária": "24h presenciais (4 encontros de 5h + 1 encontro de 4h) + 22h digitais = 46h",
     "Conceitos / Tópicos": "5 módulos de culinária profissionalizante. Técnicas de preparo, manipulação de alimentos, gastronomia regional, empreendedorismo culinário.",
     "Atividade / Metodologia": "Aulas práticas presenciais com culinarista + conteúdo digital na plataforma Lovable. Certificação via e-certificado.com.",
     "ODS": "ODS 4, ODS 8", "Linguagem MinC": ""},
    {"ID": "132-TRILHA-BELEZA", "Código Projeto": "132", "Projeto": "Estação Samarco, Territórios do Futuro",
     "Nome": "Trilha de Beleza", "Tipo": "trilha-formativa",
     "Carga Horária": "24h presenciais (4 encontros de 5h + 1 encontro de 4h) + 22h digitais = 46h",
     "Conceitos / Tópicos": "Corte de cabelo, coloração, manicure/pedicure, maquiagem, empreendedorismo em beleza. Nova trilha em 2026.",
     "Atividade / Metodologia": "Aulas práticas presenciais com educadora de beleza + conteúdo digital na plataforma Lovable. Certificação via e-certificado.com.",
     "ODS": "ODS 4, ODS 8", "Linguagem MinC": ""},
]


def sync_metodologias(table_name: str):
    print("\n[Metodologias]")
    for m in METODOLOGIAS:
        print(f"  {m['ID']}: {m['Nome']}")
    r = upsert_records(table_name, METODOLOGIAS, ["ID"])
    print(f"  criados: {len(r['createdRecords'])} | atualizados: {len(r['updatedRecords'])}")


# ---------------------------------------------------------------------------
# Sync KPIs
# ---------------------------------------------------------------------------

KPIS = [
    # 128
    {"Código Projeto": "128", "Projeto": "Festival Agricultura Sustentável",
     "Indicador": "Alunos únicos beneficiados", "Meta": "1.000", "Realizado": "0",
     "Unidade": "alunos", "Status": "a confirmar"},
    {"Código Projeto": "128", "Projeto": "Festival Agricultura Sustentável",
     "Indicador": "Alunos únicos por cidade", "Meta": "250", "Realizado": "0",
     "Unidade": "alunos/cidade", "Status": "a confirmar"},
    {"Código Projeto": "128", "Projeto": "Festival Agricultura Sustentável",
     "Indicador": "Atendimentos totais (alunos x oficinas)", "Meta": "7.000", "Realizado": "0",
     "Unidade": "atendimentos", "Status": "a confirmar"},
    {"Código Projeto": "128", "Projeto": "Festival Agricultura Sustentável",
     "Indicador": "Oficinas executadas", "Meta": "28", "Realizado": "0",
     "Unidade": "oficinas", "Status": "a confirmar",
     "Observações": "7 temas x 4 cidades"},
    {"Código Projeto": "128", "Projeto": "Festival Agricultura Sustentável",
     "Indicador": "Cidades atendidas", "Meta": "4", "Realizado": "0",
     "Unidade": "cidades", "Status": "a confirmar"},
    {"Código Projeto": "128", "Projeto": "Festival Agricultura Sustentável",
     "Indicador": "Público festival DOMO Curitiba (mínimo)", "Meta": "500", "Realizado": "0",
     "Unidade": "pessoas", "Status": "a confirmar"},
    {"Código Projeto": "128", "Projeto": "Festival Agricultura Sustentável",
     "Indicador": "Público festival DOMO Curitiba (máximo)", "Meta": "1.000", "Realizado": "0",
     "Unidade": "pessoas", "Status": "a confirmar"},
    {"Código Projeto": "128", "Projeto": "Festival Agricultura Sustentável",
     "Indicador": "Orçamento aprovado", "Meta": "R$ 600.000", "Realizado": "A confirmar",
     "Unidade": "R$", "Status": "a confirmar",
     "Observações": "Original era R$1,5M — reduzido 60% para adequar verba aprovada"},

    # 129
    {"Código Projeto": "129", "Projeto": "Agrofuturo Cultural nas Escolas",
     "Indicador": "Alunos únicos beneficiados", "Meta": "A confirmar", "Realizado": "0",
     "Unidade": "alunos", "Status": "a confirmar"},
    {"Código Projeto": "129", "Projeto": "Agrofuturo Cultural nas Escolas",
     "Indicador": "Oficinas executadas", "Meta": "A confirmar", "Realizado": "0",
     "Unidade": "oficinas", "Status": "a confirmar",
     "Observações": "8 temas + teatro + feira + seminário por cidade"},
    {"Código Projeto": "129", "Projeto": "Agrofuturo Cultural nas Escolas",
     "Indicador": "Cidades atendidas", "Meta": "A definir", "Realizado": "0",
     "Unidade": "cidades", "Status": "a confirmar",
     "Observações": "Modelo cidades-cabeça similar ao 128 — 3 a 4 cidades"},
    {"Código Projeto": "129", "Projeto": "Agrofuturo Cultural nas Escolas",
     "Indicador": "Orçamento contratado", "Meta": "A confirmar", "Realizado": "A confirmar",
     "Unidade": "R$", "Status": "a confirmar"},

    # 132
    {"Código Projeto": "132", "Projeto": "Estação Samarco, Territórios do Futuro",
     "Indicador": "Comunidades atendidas", "Meta": "12", "Realizado": "0",
     "Unidade": "comunidades", "Status": "a confirmar",
     "Observações": "7 MG + 5 ES"},
    {"Código Projeto": "132", "Projeto": "Estação Samarco, Territórios do Futuro",
     "Indicador": "Comunidades MG", "Meta": "7", "Realizado": "0",
     "Unidade": "comunidades", "Status": "a confirmar"},
    {"Código Projeto": "132", "Projeto": "Estação Samarco, Territórios do Futuro",
     "Indicador": "Comunidades ES", "Meta": "5", "Realizado": "0",
     "Unidade": "comunidades", "Status": "a confirmar"},
    {"Código Projeto": "132", "Projeto": "Estação Samarco, Territórios do Futuro",
     "Indicador": "Horas de formação por trilha (Culinária/Beleza)", "Meta": "46h", "Realizado": "0",
     "Unidade": "horas", "Status": "a confirmar",
     "Observações": "24h presenciais + 22h digitais"},
    {"Código Projeto": "132", "Projeto": "Estação Samarco, Territórios do Futuro",
     "Indicador": "Horas de formação Trilha Inicial", "Meta": "4h", "Realizado": "0",
     "Unidade": "horas", "Status": "a confirmar"},
    {"Código Projeto": "132", "Projeto": "Estação Samarco, Territórios do Futuro",
     "Indicador": "Participantes por trilha", "Meta": "A confirmar", "Realizado": "0",
     "Unidade": "participantes", "Status": "a confirmar",
     "Observações": "Turmas de 40 ou 2x20 — pendente definição com Samarco"},
    {"Código Projeto": "132", "Projeto": "Estação Samarco, Territórios do Futuro",
     "Indicador": "Orçamento contratado", "Meta": "A confirmar", "Realizado": "A confirmar",
     "Unidade": "R$", "Status": "a confirmar",
     "Observações": "Dentro do PIIS Samarco R$8M/ano. Solicitar a Cíntia/Abilio."},
]


def sync_kpis(table_name: str):
    print("\n[KPIs e Metas]")
    for k in KPIS:
        print(f"  {k['Código Projeto']}: {k['Indicador']}")
    r = upsert_records(table_name, KPIS, ["Código Projeto", "Indicador"])
    print(f"  criados: {len(r['createdRecords'])} | atualizados: {len(r['updatedRecords'])}")


# ---------------------------------------------------------------------------
# Sync Execução (deliverables)
# ---------------------------------------------------------------------------

def _build_exec_records() -> list[dict]:
    records = []

    # 128 — Bloco A
    for item in [
        ("A1", "KV New Holland Festival Agricultura + biblioteca de ícones (7 oficinas)", "A - Pré-projeto digital", "kv", "P1"),
        ("A2", "Carrossel informativo pré (8 cards)", "A - Pré-projeto digital", "carrossel", "P1"),
        ("A3", "Convite post cidade (template editável, 4 cidades)", "A - Pré-projeto digital", "template", "P2"),
        ("A4", "Imagem convite WhatsApp escolas (template, 4 cidades)", "A - Pré-projeto digital", "template", "P2"),
        ("A5", "Card inscrição QR para professores (plataforma New Holland Online)", "A - Pré-projeto digital", "template", "P2"),
        ("A6", "Mockup LP plataforma New Holland Online", "A - Pré-projeto digital", "mockup", "P2"),
    ]:
        records.append({"ID Entregável": f"128-{item[0]}", "Código Projeto": "128",
                         "Projeto": "Festival Agricultura Sustentável", "Nome": item[1],
                         "Bloco": item[2], "Tipo": item[3], "Status": "pendente", "Prioridade": item[4]})

    # 128 — Bloco B
    for item in [
        ("B1", "Kit pedagógico físico por escola (apostilas + jogos + materiais)", "B - Material pedagógico", "impresso"),
        ("B2", "Manual do facilitador (7 oficinas detalhadas)", "B - Material pedagógico", "documento"),
        ("B3", "Plano de aula para professor (alinhado BNCC)", "B - Material pedagógico", "documento"),
    ]:
        records.append({"ID Entregável": f"128-{item[0]}", "Código Projeto": "128",
                         "Projeto": "Festival Agricultura Sustentável", "Nome": item[1],
                         "Bloco": item[2], "Tipo": item[3], "Status": "pendente", "Prioridade": "P2"})

    # 128 — Bloco C
    for item in [
        ("C1", "Layout interno DOMO (2 ambientações)", "C - Estrutura de campo", "cenografia"),
        ("C2", "Sinalização externa DOMO (placa, banner, pantojet)", "C - Estrutura de campo", "impresso-grande"),
        ("C3", "Camisetas equipe + uniforme facilitador", "C - Estrutura de campo", "textil"),
    ]:
        records.append({"ID Entregável": f"128-{item[0]}", "Código Projeto": "128",
                         "Projeto": "Festival Agricultura Sustentável", "Nome": item[1],
                         "Bloco": item[2], "Tipo": item[3], "Status": "pendente", "Prioridade": "P2"})

    # 128 — Bloco D
    for item in [
        ("D1", "Certificado 'Guardião da Terra' para alunos", "D - Certificados", "template"),
        ("D2", "Certificado formação 20h BNCC para professores", "D - Certificados", "template"),
    ]:
        records.append({"ID Entregável": f"128-{item[0]}", "Código Projeto": "128",
                         "Projeto": "Festival Agricultura Sustentável", "Nome": item[1],
                         "Bloco": item[2], "Tipo": item[3], "Status": "pendente", "Prioridade": "P3"})

    # 128 — Conteúdo
    for item in [
        ("VIDEO-PRE", "Vídeo apresentação pré (1 por cidade, 4 total)", "reels"),
        ("CARROSSEL-DURANTE", "Carrossel editorial durante (1 por cidade, 4 total)", "carrossel"),
        ("VIDEO-DURANTE", "Vídeo cobertura durante oficinas + DOMO (1 por cidade)", "reels"),
        ("VIDEO-CASE", "Vídeo case final (2-3 min)", "video-horizontal"),
        ("CARROSSEL-POS", "Carrossel encerramento (números + fotos)", "carrossel"),
        ("RELATORIO-ESG", "Relatório ESG completo + indicadores ODS", "documento"),
    ]:
        records.append({"ID Entregável": f"128-{item[0]}", "Código Projeto": "128",
                         "Projeto": "Festival Agricultura Sustentável", "Nome": item[1],
                         "Bloco": "Conteúdo / Redes", "Tipo": item[2], "Status": "pendente", "Prioridade": "P2"})

    # 132 — Bloco A
    for item in [
        ("A1", "KV Estação Samarco Empreendedorismo + biblioteca de ícones", "A - Pré-projeto digital", "kv", "P1"),
        ("A2", "Carrossel informativo pré (8 cards)", "A - Pré-projeto digital", "carrossel", "P1"),
        ("A3", "Convite post cidade (template editável, por cidade)", "A - Pré-projeto digital", "template", "P2"),
        ("A4", "Convite WhatsApp (template, por cidade)", "A - Pré-projeto digital", "template", "P2"),
        ("A5", "Card inscrição QR (plataforma Lovable)", "A - Pré-projeto digital", "template", "P2"),
        ("A6", "Mockup LP plataforma Lovable", "A - Pré-projeto digital", "mockup", "P2"),
    ]:
        records.append({"ID Entregável": f"132-{item[0]}", "Código Projeto": "132",
                         "Projeto": "Estação Samarco, Territórios do Futuro", "Nome": item[1],
                         "Bloco": item[2], "Tipo": item[3], "Status": "pendente", "Prioridade": item[4]})

    # 132 — Bloco B
    for item in [
        ("B1", "Pantojet inflável", "estrutura"),
        ("B2", "Rollup Empreendedorismo e Turismo", "impresso-grande"),
        ("B3", "Rollup Culinária", "impresso-grande"),
        ("B4", "Rollup Beleza", "impresso-grande"),
        ("B5", "Rollup Institucional NTICS + Samarco", "impresso-grande"),
        ("B6", "Rollup Plataforma Digital", "impresso-grande"),
        ("B7", "Wind Banner", "impresso-grande"),
        ("B8", "Avental culinária participante", "textil"),
        ("B9", "Saia bancada", "impresso"),
        ("B10", "Moldura espelho beleza", "impressao"),
        ("B11", "Dolma culinária", "textil"),
    ]:
        records.append({"ID Entregável": f"132-{item[0]}", "Código Projeto": "132",
                         "Projeto": "Estação Samarco, Territórios do Futuro", "Nome": item[1],
                         "Bloco": "C - Estrutura de campo", "Tipo": item[2], "Status": "pendente", "Prioridade": "P2"})

    # 132 — Bloco C (certificados)
    for item in [
        ("C1", "Certificado profissionalizante (Culinária + Beleza)"),
        ("C2", "Certificado Trilha Inicial Empreendedorismo"),
    ]:
        records.append({"ID Entregável": f"132-{item[0]}", "Código Projeto": "132",
                         "Projeto": "Estação Samarco, Territórios do Futuro", "Nome": item[1],
                         "Bloco": "D - Certificados", "Tipo": "template", "Status": "pendente", "Prioridade": "P2"})

    # 132 — Conteúdo
    for item in [
        ("VIDEO-PRE-MG", "Vídeo pré-projeto MG", "reels"),
        ("VIDEO-PRE-ES", "Vídeo pré-projeto ES", "reels"),
        ("CARROSSEL-INFO", "Carrossel informativo pré", "carrossel"),
        ("VIDEO-COBERTURA", "Vídeo cobertura durante (1 por cidade, 12 total)", "reels"),
        ("VIDEO-CASE", "Vídeo case final (2-3 min)", "video-horizontal"),
        ("CARROSSEL-ENCERRAMENTO", "Carrossel encerramento", "carrossel"),
    ]:
        records.append({"ID Entregável": f"132-{item[0]}", "Código Projeto": "132",
                         "Projeto": "Estação Samarco, Territórios do Futuro", "Nome": item[1],
                         "Bloco": "Conteúdo / Redes", "Tipo": item[2], "Status": "pendente", "Prioridade": "P2"})

    return records


def sync_execucao(table_name: str):
    print("\n[Execução]")
    records = _build_exec_records()
    print(f"  {len(records)} entregas a sincronizar...")
    r = upsert_records(table_name, records, ["ID Entregável"])
    print(f"  criados: {len(r['createdRecords'])} | atualizados: {len(r['updatedRecords'])}")


# ---------------------------------------------------------------------------
# Sync Aprovação de Peças
# ---------------------------------------------------------------------------

APROVACOES = [
    {"Peça": "Fluxo geral — Projeto 128", "Projeto": "Festival Agricultura Sustentável", "Código Projeto": "128",
     "Tipo": "Fluxo de aprovação", "Status": "produção",
     "Aprovador Interno": "Lucas Rotta",
     "Aprovador Cliente": "CNH/New Holland (interlocutor a confirmar — provavelmente Raquel)",
     "Canal de Aprovação": "E-mail / WhatsApp",
     "Prazo Resposta": "A definir após kick-off",
     "Observações": "Etapa 1: aprovação interna (Lucas). Etapa 2: CNH/New Holland. Etapa 3: MINC (Mayara Ferreira) para entregáveis Rouanet."},
    {"Peça": "Fluxo geral — Projeto 129", "Projeto": "Agrofuturo Cultural nas Escolas", "Código Projeto": "129",
     "Tipo": "Fluxo de aprovação", "Status": "produção",
     "Aprovador Interno": "Lucas Rotta",
     "Aprovador Cliente": "CNH/Case IH (interlocutor a confirmar)",
     "Canal de Aprovação": "E-mail / WhatsApp",
     "Prazo Resposta": "A definir após kick-off",
     "Observações": "Etapa 1: aprovação interna (Lucas). Etapa 2: CNH/Case IH. Etapa 3: MINC (Mayara) para entregáveis Rouanet."},
    {"Peça": "Fluxo geral — Projeto 132", "Projeto": "Estação Samarco, Territórios do Futuro", "Código Projeto": "132",
     "Tipo": "Fluxo de aprovação", "Status": "produção",
     "Aprovador Interno": "Bruna Seibel + Lucas Rotta",
     "Aprovador Cliente": "Amanda (corporativo) + Rayane (ES)",
     "Canal de Aprovação": "SharePoint / Teams Samarco — NUNCA WhatsApp Web",
     "Prazo Resposta": "48h ideal / 24h mínimo",
     "Observações": "Aprovação dupla obrigatória: Amanda (MG+ES) + Rayane (ES). Cíntia quando houver questão contratual."},
]


def sync_aprovacoes(table_name: str):
    print("\n[Aprovação de Peças]")
    for a in APROVACOES:
        print(f"  {a['Código Projeto']}: {a['Peça']}")
    r = upsert_records(table_name, APROVACOES, ["Código Projeto", "Peça"])
    print(f"  criados: {len(r['createdRecords'])} | atualizados: {len(r['updatedRecords'])}")


# ---------------------------------------------------------------------------
# Sync Financeiro
# ---------------------------------------------------------------------------

def _build_financeiro() -> list[dict]:
    records = []

    # 128 — 10 frentes
    frentes_128 = [
        ("F1", "Produção visual (NTICS skills)", "Produção interna", "baixo"),
        ("F2", "Plataforma digital New Holland Online", "Lovable ou equivalente", "a cotar"),
        ("F3", "Produtor/articulador local (4 cidades)", "Local por cidade", "a cotar"),
        ("F4", "DOMO imersivo (Curitiba)", "Fornecedor cenografia + audiovisual", "a cotar"),
        ("F5", "Kit pedagógico físico por escola", "Gráfica/fornecedor", "a cotar"),
        ("F6", "Material gráfico (rollups, placas, banners DOMO)", "Gráfica", "a cotar"),
        ("F7", "Vídeo (pré + durante + case)", "Produtora local", "a cotar"),
        ("F8", "Logística (4 cidades, deslocamento, alimentação equipe)", "Diverso", "a cotar"),
        ("F9", "Estamparia têxtil (camisetas equipe + uniforme facilitador)", "Fornecedor têxtil", "a cotar"),
        ("F10", "Educadores/oficineiros locais (4 cidades)", "Profissionais locais", "a cotar"),
    ]
    for id_, cat, forn, custo in frentes_128:
        records.append({
            "ID Frente": f"128-{id_}", "Código Projeto": "128",
            "Projeto": "Festival Agricultura Sustentável",
            "Categoria": cat, "Fornecedor": forn, "Custo Estimado (R$)": custo,
            "Status": "a cotar",
            "Observações": "Orçamento total aprovado: R$600.000 (original R$1,5M — redução 60%)",
        })

    # 129 — 16 frentes
    frentes_129 = [
        ("F1", "Produção visual (skills ntics-brain)", "Produção interna", "baixo"),
        ("F2", "Plataforma digital Agrofuturo Digital", "Lovable ou equivalente", "a cotar"),
        ("F3", "Produtor/articulador local", "Local por cidade", "a cotar"),
        ("F4", "Cenografia Feira de Tecnologia, Arte e Cultura", "Fornecedor", "a cotar"),
        ("F5", "Companhia de teatro (Peça Interativa)", "Companhia de teatro", "a cotar"),
        ("F6", "RA/VR — apresentações interativas + simulações", "Tech/fornecedor", "a cotar"),
        ("F7", "Oficina de robótica (parceria ou contratação)", "Parceiro/fornecedor", "a cotar"),
        ("F8", "Bandas + artistas regionais (Feira)", "Artistas locais", "a cotar"),
        ("F9", "Gastronomia local (Feira)", "Fornecedores locais", "a cotar"),
        ("F10", "Seminário AgroInova Summit (palco, locação, palestrantes)", "Fornecedor evento", "a cotar"),
        ("F11", "Kit pedagógico físico por escola", "Gráfica/fornecedor", "a cotar"),
        ("F12", "Material gráfico (rollups, banners Feira)", "Gráfica", "a cotar"),
        ("F13", "Vídeo (pré + durante + case)", "Produtora local", "a cotar"),
        ("F14", "Logística (deslocamento, alimentação equipe)", "Diverso", "a cotar"),
        ("F15", "Estamparia têxtil (uniforme equipe)", "Fornecedor têxtil", "a cotar"),
        ("F16", "Educadores/oficineiros locais", "Profissionais locais", "a cotar"),
    ]
    for id_, cat, forn, custo in frentes_129:
        records.append({
            "ID Frente": f"129-{id_}", "Código Projeto": "129",
            "Projeto": "Agrofuturo Cultural nas Escolas",
            "Categoria": cat, "Fornecedor": forn, "Custo Estimado (R$)": custo,
            "Status": "a cotar",
            "Observações": "Orçamento total não confirmado. PRONAC a confirmar.",
        })

    # 132 — 7 categorias
    frentes_132 = [
        ("CAT1", "Educadores", "Culinarista MG+ES, educadoras beleza MG+ES, palestrante trilha inicial", "Profissionais locais"),
        ("CAT2", "Produção local", "4 produtores (2 MG + 2 ES), fotógrafos MG+ES, editor vídeo", "Profissionais locais"),
        ("CAT3", "Plataforma digital", "Dev Lovable + e-certificado.com", "Tech"),
        ("CAT4", "Kits participante", "Avental, touca, tábua, faca (culinária) + kits beleza", "Fornecedor"),
        ("CAT5", "Estrutura de campo", "Pantojet inflável, rollups (6), wind banner, saia bancada, placas fotos, camisetas equipe", "Gráfica/têxtil"),
        ("CAT6", "Comunicação", "Produção de peças NTICS (KV, carrosseis, vídeos, certificados)", "NTICS"),
        ("CAT7", "Impressos locais", "Convites, folhetos por cidade (gráfica/copiadora local)", "Gráfica local"),
    ]
    for id_, cat, desc, forn in frentes_132:
        records.append({
            "ID Frente": f"132-{id_}", "Código Projeto": "132",
            "Projeto": "Estação Samarco, Territórios do Futuro",
            "Categoria": cat, "Descrição": desc, "Fornecedor": forn,
            "Custo Estimado (R$)": "a cotar",
            "Status": "a cotar",
            "Observações": "Orçamento total não compartilhado. Solicitar breakdown a Cíntia/Abilio. Referência: PIIS Samarco R$8M/ano.",
        })

    return records


def sync_financeiro(table_name: str):
    print("\n[Financeiro]")
    records = _build_financeiro()
    print(f"  {len(records)} frentes de custo a sincronizar...")
    r = upsert_records(table_name, records, ["ID Frente"])
    print(f"  criados: {len(r['createdRecords'])} | atualizados: {len(r['updatedRecords'])}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    config = load_config()
    tables = config["tables"]

    print(f"Base ID: {config['base_id']}")
    print(f"Tabelas carregadas: {list(tables.keys())}\n")

    sync_projetos(tables["Projetos"])
    sync_tap(tables["TAP"])
    sync_metodologias(tables["Metodologias"])
    sync_kpis(tables["KPIs e Metas"])
    sync_execucao(tables["Execução"])
    sync_aprovacoes(tables["Aprovação de Peças"])
    sync_financeiro(tables["Financeiro"])

    print("\nSync concluído. Abra o Airtable para verificar.")


if __name__ == "__main__":
    main()
