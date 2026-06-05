# 🏢 SSC/GBS Deployment Agent Suite — Costa Rica
## Basado en metodología Big 4 | Actualizado con Big 4 Best Practices 2025–2026

---

## ¿QUÉ ES ESTO?

Este es un conjunto de **13 agentes especializados + 1 orquestador** (disponibles en español en `es/` y en inglés en `en/`) diseñados para facilitar el despliegue completo de un **Centro de Servicios Compartidos (SSC) o Global Business Services (GBS)** en Costa Rica.

Cada archivo `.md` es un **system prompt de agente** que puedes cargar en Claude (o cualquier LLM) para obtener asistencia experta en ese módulo específico del pipeline de implementación.

---

## ARQUITECTURA — TOOLKIT UNIFICADO

Un solo toolkit: el **orquestador** coordina los 14 skills, agrupados por área de
capacidad (no es un pipeline secuencial por fases).

![SSC/GBS Agent Suite — Toolkit unificado](docs/architecture.png)

> Versión vectorial: [docs/architecture.svg](docs/architecture.svg) · Editable en FigJam: [abrir](https://www.figma.com/board/uYtRtE7TXOp7dM3OgCaovU)

---

## CÓMO USAR ESTOS AGENTES

### Opción 1: Con Claude en Cowork (Recomendado)
1. Abre una nueva sesión de chat en Claude
2. Copia el contenido del archivo del módulo que necesitas
3. Úsalo como contexto de tu conversación
4. El agente se comportará como ese especialista

### Opción 2: Copiar como System Prompt
1. En cualquier interfaz de LLM con system prompt
2. Pega el contenido del archivo `.md` como system prompt
3. Comienza tu conversación

### Opción 3: Referencia directa
- Abre el archivo del módulo que corresponde a tu etapa actual
- Úsalo como guía de trabajo y checklist

---

## GUÍA DE USO POR NECESIDAD

| ¿Qué necesitas? | Activa este agente |
|---------------------|-------------------|
| Evaluando si hacer un SSC/GBS | `01_diagnostic_agent.md` |
| Decidiendo el modelo (SSC vs GBS vs BPO) | `02_strategy_agent.md` |
| Analizando Costa Rica como locación | `03_location_agent.md` |
| Construyendo el caso financiero | `04_business_case_agent.md` |
| Rediseñando procesos y automatizando | `05_process_automation_agent.md` |
| Definiendo stack tecnológico y ERP | `06_technology_agent.md` |
| Diseñando la organización y talento | `07_org_talent_agent.md` |
| Migrando procesos y haciendo KT | `08_migration_kt_agent.md` |
| Definiendo SLAs y gobernanza | `09_service_mgmt_agent.md` |
| Mejorando operaciones post go-live | `10_sustain_ci_agent.md` |
| No sé por dónde empezar | `00_ORCHESTRATOR.md` |

---

## FUENTES Y METODOLOGÍA BASE

### Metodología prácticas Big 4 (documentos originales analizados):
- Finance SSC Stage Overview (2011)
- SSC Getting Started Guide
- SSC01–39: Toolkit completo (Operating Model, Org Design, Business Case, 
  Location Selection, Process Mapping, Service Management, Migration, 
  Knowledge Transfer, Health Check, Voice of Customer)
- Finance Transformation Toolkit FNT03–FNT38
- Record-to-Report Technology Overlay
- Finance Rapid Assessment (FRA) methodology

### Actualizaciones Big 4 integradas (2024–2026):
| Firma | Contribución principal |
|-------|----------------------|
| **Prácticas Big 4** | Base metodológica y toolkits completos (SSC/GBS) |
| **Deloitte** | GBS evolution, Intelligent Automation, Process Mining (Celonis) |
| **PwC** | Cloud ERP first, Touchless AP/AR, ESG Reporting Hub, Agile Finance |
| **KPMG** | Connected Finance, Zero-touch processing, OKR framework, BCP |

### Fuentes de datos de mercado:
- CINDE (Agencia de Promoción de Inversiones CR) — datos de talento y zonas francas
- PROCOMER — régimen de zona franca actualizado
- APQC Benchmarking Suite — benchmarks de costos por transacción
- Gartner Finance Function Research 2025
- Hackett Group GBS Benchmarking 2024–2025

---

## ALCANCE FUNCIONAL CUBIERTO

Los agentes cubren los siguientes procesos Finance GBS:
- ✅ P2P (Accounts Payable / Procure-to-Pay)
- ✅ O2C (Accounts Receivable / Order-to-Cash)
- ✅ R2R (Record-to-Report / General Ledger)
- ✅ Cash Management / Treasury Support
- ✅ Fixed Assets
- ✅ Tax Compliance
- ✅ Payroll Processing
- ✅ T&E (Travel & Expenses)
- ✅ Master Data Management
- ✅ Management Reporting & Analytics
- ✅ FP&A Support (fases avanzadas)
- ⬜ HR Services (referenciado, guía básica)
- ⬜ IT Helpdesk (referenciado, guía básica)
- ⬜ Procurement (referenciado, guía básica)

---

## STACK TECNOLÓGICO CUBIERTO

Los agentes brindan orientación sobre:
- ERP: SAP S/4HANA, Oracle Fusion, Microsoft D365 F&O
- RPA: UiPath, Automation Anywhere, Power Automate
- IDP: ABBYY Vantage, Microsoft AI Builder, AWS Textract
- Close Management: BlackLine, Trintech, FloQast, OneStream
- FP&A: Workday Adaptive, Anaplan, OneStream
- Process Mining: Celonis, UiPath Process Mining, SAP Signavio
- BI/Analytics: Power BI, Tableau, SAP Analytics Cloud
- Service Management: ServiceNow, Freshservice
- Collaboration: Microsoft 365 + Teams

---

## CONTEXTO COSTA RICA 2025

Todos los agentes incluyen datos específicos y actualizados sobre:
- 📍 Zonas Francas (Ley 7210): beneficios fiscales y requisitos
- 💰 Salarios de mercado GBS por nivel y función
- 👥 Disponibilidad de talento bilingüe y pipeline universitario
- ⚖️ Marco legal laboral (Código de Trabajo, CCSS, teletrabajo)
- 🏢 Parques empresariales recomendados (America FZ, Ultrapark, Coyol, etc.)
- 🌐 Infraestructura digital y conectividad
- 🔒 Protección de datos (Ley 8968)
- 🏦 Transfer pricing y facturación electrónica (Hacienda CR)

---

## ROADMAP V2.0 — ESTADO

- [x] Agente específico para **HR GBS** (nómina, beneficios, HRBP) → `ssc-hr-gbs`
- [x] Agente para **ESG Reporting Hub** (CSRD compliance) → `ssc-esg-hub`
- [x] Agente para **M&A Support** desde GBS → `ssc-ma-support`
- [x] Integración con datos en tiempo real de CINDE y PROCOMER → `scripts/update_cr_data.py`
- [x] Templates descargables de Excel (Business Case, KPI Dashboard) → `templates/`
- [x] Versión en inglés de todos los agentes → `en/` (14 skills `-en`)

---

## NUEVA ESTRUCTURA (V2.0)

```
SSC-Agents/
├── es/                     ← 14 skills en español (.skill) + README.md
├── en/                     ← 14 skills en inglés (-en.skill) + README_EN.md
├── templates/
│   ├── SSC_Business_Case_Template.xlsx   (9 hojas, fórmulas NPV/IRR/Payback)
│   └── SSC_KPI_Dashboard_Template.xlsx   (8 hojas, RAG dashboard)
├── scripts/
│   ├── update_cr_data.py                 (refresco CINDE/PROCOMER + changelog)
│   └── build_excel_templates.py          (regenera los templates)
├── source-documents/       ← Toolkit Big 4 original (SSC01–39, FNT, R2R) vía Git LFS *
├── 00–10_*.md              ← system prompts fuente (referencia)
├── LICENSE                 ← Propietario / All Rights Reserved (VegaBuildsAI)
├── .gitattributes          ← normaliza EOL + Git LFS para source-documents/
└── CLAUDE.md
```

> \* `source-documents/` contiene materiales de referencia de las Big 4 (propiedad de sus dueños,
> incluidos solo como referencia interna — ver `LICENSE`). Se versionan con **Git LFS**;
> tras clonar, ejecutar `git lfs pull` para descargar los binarios.

### Módulos nuevos (extensiones GBS)
| Módulo | Skill | Cubre |
|--------|-------|-------|
| M11 HR GBS | `ssc-hr-gbs` | Nómina multi-país (CCSS/IMSS), beneficios, HR self-service, ATS, HRBP |
| M12 ESG Hub | `ssc-esg-hub` | CSRD/ESRS (post-Omnibus 2026), doble materialidad, Scope 1/2/3, EU Taxonomy |
| M13 M&A Support | `ssc-ma-support` | Due diligence, integración post-adquisición (PMI), carve-outs, TSA |

### Herramientas
- **Templates Excel** (`templates/`): Business Case (9 hojas) y KPI Dashboard (8 hojas) con fórmulas
  vivas, celdas de input en amarillo y semáforos RAG. Regenerables con `build_excel_templates.py`.
- **Datos CR en tiempo real** (`scripts/update_cr_data.py`): extrae datos de CINDE/PROCOMER, refresca
  las secciones `AUTO` de `talent_cr.md`/`costs_cr.md` y genera `cr_data_changelog.md`. Recomendado
  como scheduled task semanal (Domingo 6:00 AM) — confirmar antes de programar.

---

*Creado: Junio 2026 | Versión 2.0 | Actualizar anualmente con nuevos benchmarks Big 4*
