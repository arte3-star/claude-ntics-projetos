# Sincronização Sites: GitHub vs SecondBrain (fonte da verdade)

Data: 2026-05-24
Fonte canônica: **`SecondBrain/projetos/`** (ativos) e **`SecondBrain/projetos-anteriores/`** (encerrados)
Repo Github obsoleto: `arte3-star/ntics-project-sites`
Planilha de URLs ntics.com.br (para referência cruzada): [Mapeamento Sites](https://docs.google.com/spreadsheets/d/1K0J9n19mJzj8WsNvb9WsyMxW6pSNilIPG9Fh0Stttfg/edit?gid=722408823)

> **Decisão (2026-05-24, Lucas):** Os perfis de projeto no SecondBrain são a fonte da verdade. Todas as 18 pastas no repo Github `arte3-star/ntics-project-sites` estão **OBSOLETAS** e devem ser sinalizadas como tal. Os slugs do Github não batem nem com ntics.com.br, nem com os slugs canônicos do SecondBrain.

---

## 1. Projetos ATIVOS — Github obsoleto → ir para `SecondBrain/projetos/`

| Github (obsoleto) | SecondBrain canônico | Cliente / Edição |
|-------------------|----------------------|------------------|
| `116_cultura_robotica` | [116-aster/](../SecondBrain/projetos/116-aster/) | Áster Máquinas |
| `117_teatro_robotica` | [117-whirlpool/](../SecondBrain/projetos/117-whirlpool/) | Whirlpool — 4ª Ed |
| `119_pec` | [119-sylvamo/](../SecondBrain/projetos/119-sylvamo/) | Sylvamo |
| `120_statkraft` | [120-negocio-cultural-statkraft-itapoa/](../SecondBrain/projetos/120-negocio-cultural-statkraft-itapoa/) | Statkraft + Porto Itapoá — Negócio Cultural 2ª Ed |
| `124_compagas` | [124-compagas/](../SecondBrain/projetos/124-compagas/) | Compagás |
| `125_gastronomia` | [125-gastronomia-gru/](../SecondBrain/projetos/125-gastronomia-gru/) | GRU Airport — Gastronomia 2ª Ed |
| `127_pie_guarulhos` | [127-pie-gru-sotreq/](../SecondBrain/projetos/127-pie-gru-sotreq/) | **UNIFICADO** com 127_pie_serra |
| `127_pie_serra` | [127-pie-gru-sotreq/](../SecondBrain/projetos/127-pie-gru-sotreq/) | **UNIFICADO** com 127_pie_guarulhos |

⚠️ O Github trata 127 como dois projetos separados (`_guarulhos` e `_serra`) mas o SecondBrain trata como **um projeto único** com duas cidades (GRU + SOTREQ). Forma correta = SecondBrain.

---

## 2. Projetos ENCERRADOS — Github obsoleto → ir para `SecondBrain/projetos-anteriores/`

| Github (obsoleto) | SecondBrain canônico (1+ perfis por código) |
|-------------------|---------------------------------------------|
| `81_cultura_robotica_ferroporte` | `81-cultura-robotica-ferroporte` |
| `82_robotica_cultural_nas_escolas` | `82-robotica-cultural-nas-escolas-mahle` **+** `82-robotica-cultural-nas-escolas-peroxidos` (2 edições) |
| `86_teatro_bons_habitos_ferroporte` | `86-teatro-dos-bons-habitos-culinaria-sustentavel-ferroporte` |
| `87_exposicao_culinaria_sustentavel_imetame` | `87-...-imetame` **+** `87-...-enercan` **+** `87-...-teleperformance` (3 edições) |
| `89_oficina_teatro_sustentavel_ferroport` | `89-oficina-de-teatro-sustentavel-cods-ferroport` **+** `89-...-cnh` (2 edições) |
| `91_teatro_dos_ods` | `91-teatro-nas-escolas-objetivos-de-desenvolvimento-sustentavel--ctg` |
| `98_conhecendo_os_ods` | `98-conhecendo-os-ods-aksell` **+** `98-conhecendo-os-ods-wilson-sons` (2 edições) |
| `104_pec_3aed_porto_itapoa` | `104-programa-de-empreendedorismo-e-cultura-porto-itapoa` |
| `106_teatro_oficina_robotica_2aed_cnh` | `106-teatro-e-oficina-robotica-2aed-cnh` **+** `106-teatro-e-oficina-robotica-2aed-peroxidos` (2 edições) |
| `110_caminhao_cultura_sustentabilidade_jaepel` | `110-caminhao-da-cultura-e-sustentabilidade-jaepel` |

⚠️ Onde o Github tem **uma única pasta por código**, o SecondBrain tem **vários perfis** (um por cliente/edição). A informação que sumiu no Github está separada corretamente no SecondBrain.

---

## 3. Por que o Github está obsoleto

1. **Slugs não-canônicos** — não batem com a URL pública em ntics.com.br (`116_cultura_robotica` vs `/cultura-robotica-aster/`).
2. **Granularidade errada** — o GitHub colapsa múltiplos patrocinadores num único folder (87 Imetame ignora Enercan e Teleperformance; 98 Wilson Sons mistura com Aksell).
3. **Desunificado onde deveria estar unificado** — 127 está dividido em `_guarulhos` / `_serra`, mas é um projeto único.
4. **README do repo desatualizado** — só lista 6 das 18 pastas.
5. **Conteúdo do site agora vive em `criar-landing-v2`** — o pipeline atual gera HTML direto a partir do briefing ClickUp + assets locais e publica em `ntics.com.br/{slug-canônico}/` via Code Snippets WordPress. O Github static-site foi substituído.

---

## 4. Ação recomendada

### Curto prazo (sinalizar obsolescência)
- [ ] Editar `README.md` do repo `arte3-star/ntics-project-sites` com aviso no topo: "⚠️ REPOSITÓRIO ARQUIVADO. Fonte da verdade: `SecondBrain/projetos/` (ativos) e `SecondBrain/projetos-anteriores/` (encerrados). Sites em produção: `ntics.com.br/{slug}/`."
- [ ] Arquivar o repo no Github (Settings → Archive this repository) — bloqueia commits acidentais.

### Médio prazo (limpeza)
- [ ] Se quiser preservar histórico do conteúdo HTML de cada pasta antes de arquivar, criar release Github "v1-final-snapshot" com tudo congelado.
- [ ] Atualizar qualquer skill ou workflow que ainda referencie `arte3-star/ntics-project-sites` para apontar para SecondBrain + pipeline `criar-landing-v2`.

### Validação cruzada
- [ ] Confirmar com Bruna/Jéssica que nenhum site no ar puxa diretamente do Github (deve estar tudo no WordPress NTICS via Code Snippets).
