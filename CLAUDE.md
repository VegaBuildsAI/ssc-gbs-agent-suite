# CLAUDE.md — SSC/GBS Agent Suite: Roadmap, Debug & Connector Integration
## Proyecto: SSC/GBS Deployment Pipeline — Costa Rica
## Estado: v1.0 (Junio 2026) | Próxima versión: v2.0

---

## CONTEXTO DEL PROYECTO

Este repositorio contiene el **SSC/GBS Agent Suite**, un conjunto de 11 skills de Claude
diseñados para facilitar el despliegue completo de un Centro de Servicios Compartidos o
Global Business Services en Costa Rica. La base metodológica es el toolkit SSC/GBS basado en prácticas Big 4
(SSC01–39, FNT03–38), actualizado con prácticas Big 4 (Deloitte, PwC, KPMG) para 2025–2026.

### Estructura del proyecto
```
SSC Module/
├── SSC-Agents/
│   ├── CLAUDE.md                  ← Este archivo
│   ├── README.md                  ← Guía de uso general (bilingüe)
│   ├── 00_ORCHESTRATOR.md         ← Contexto maestro del pipeline
│   ├── 01_diagnostic_agent.md     ← Módulo 1 (system prompts fuente)
│   ├── ...                        ← Módulos 2–10
│   ├── es/                        ← 14 skills en español (.skill) + README.md
│   │   ├── ssc-orchestrator.skill
│   │   └── ...                    ← Skills 2–14 (incl. hr-gbs, esg-hub, ma-support)
│   ├── en/                        ← 14 skills en inglés (-en.skill) + README_EN.md
│   │   ├── ssc-orchestrator-en.skill
│   │   └── ...
│   ├── templates/                 ← SSC_Business_Case + SSC_KPI_Dashboard (.xlsx)
│   └── scripts/                   ← update_cr_data.py, build_excel_templates.py
└── [Documentos de referencia]     ← Fuente primaria
```

---

## PARTE 1: ROADMAP — PENDIENTES V2.0

### TAREA 1: Agente HR GBS (nómina, beneficios, HRBP)
**Prioridad:** Alta | **Estimado:** 4–6 horas de trabajo

**Alcance del agente:**
- Nómina GBS: payroll processing multi-país, requerimientos CCSS CR, IMSS MX, etc.
- Gestión de beneficios: administración planes médicos, fondos de pensión
- HR Self-Service: portal empleados, onboarding digital, offboarding
- HRBP Support: data de empleados, reportes HR, analytics de workforce
- Talent Acquisition support: ATS integration, background checks

**Archivos a crear:**
```
ssc-skills/ssc-hr-gbs/
├── SKILL.md  (frontmatter + instrucciones del agente)
└── references/
    ├── hr_processes.md     (nómina, beneficios, ATS, HRBP workflows)
    ├── cr_labor_law.md     (CCSS, código de trabajo, teletrabajo Ley 9738)
    └── hr_tech_stack.md    (Workday, SAP SuccessFactors, Oracle HCM)
```

**Connectors a integrar:**
- `mcp__90c11731` (Gmail): recibir solicitudes HR, enviar notificaciones de nómina
- `mcp__c2253a72` (Google Calendar): gestión de calendarios de onboarding/offboarding
- `mcp__d7ab2e83` (Google Drive): almacenar expedientes digitales de empleados
- `operations:capacity-plan` skill: planificación de headcount GBS
- `finance:journal-entry` skill: asientos de nómina y beneficios
- `legal:compliance-check` skill: verificación marco laboral CR y multi-país

**Instrucciones para Claude Code:**
1. Leer `07_org_talent_agent.md` para contexto de estructura organizacional
2. Leer `references/regulatory_cr.md` en `ssc-location-cr` para marco laboral
3. Crear nuevo directorio `ssc-hr-gbs` con estructura arriba
4. Hacer zip como `ssc-hr-gbs.skill`
5. Añadir entrada al `README.md` en la tabla de módulos

---

### TAREA 2: Agente ESG Reporting Hub (CSRD compliance)
**Prioridad:** Alta — regulación CSRD en vigor desde 2025 | **Estimado:** 4–6 horas

**Alcance del agente:**
- CSRD (Corporate Sustainability Reporting Directive): requerimientos EU, aplicabilidad
- Doble materialidad: evaluación de impactos financieros y de sostenibilidad
- Taxonomía EU: alineación con actividades sostenibles
- Datos ESG desde GBS: emisiones Scope 1/2/3, datos sociales (empleados, proveedores)
- GBS como hub de recolección de datos ESG multi-entidad
- Herramientas: SAP Sustainability Footprint Management, Watershed, Salesforce Net Zero

**Archivos a crear:**
```
ssc-skills/ssc-esg-hub/
├── SKILL.md
└── references/
    ├── csrd_framework.md   (requerimientos, ESRS standards, timeline obligaciones)
    ├── esg_data_model.md   (qué datos recolectar, dónde, cómo)
    └── esg_tech_stack.md   (herramientas, integraciones ERP, reporting)
```

**Connectors a integrar:**
- `data:analyze` skill: análisis de datos ESG recolectados
- `data:create-viz` skill: dashboards de métricas ESG
- `data:statistical-analysis` skill: baseline, targets, progreso
- `finance:financial-statements` skill: integración ESG en reportes financieros
- `legal:compliance-check` skill: verificación cumplimiento CSRD, GRI, TCFD
- `brightdata-plugin:competitive-intel`: monitorear reporting ESG de competidores
- `nimble:nimble-web-expert`: extraer datos públicos de sostenibilidad

**Instrucciones para Claude Code:**
1. Buscar en la web prácticas CSRD más recientes (ESRS standards vigentes)
2. Verificar aplicabilidad para empresas con operaciones en Costa Rica
3. Crear el skill con foco en: qué datos recolectar, cómo estructurarlos, cómo reportarlos
4. Incluir templates de disclosure listos para usar

---

### TAREA 3: Agente M&A Support desde GBS
**Prioridad:** Media | **Estimado:** 3–5 horas

**Alcance del agente:**
- Due diligence financiero: soporte desde GBS para data rooms
- Integración post-adquisición: incorporar nuevas entidades al GBS
- Carve-out support: separar entidades que salen del grupo
- Sistemas: ERP migration/integration, data harmonization
- Procesos: harmonización de chart of accounts, vendor masters, customer masters
- Reporting: consolidación de entidades adquiridas

**Archivos a crear:**
```
ssc-skills/ssc-ma-support/
├── SKILL.md
└── references/
    ├── ma_playbook.md      (fases de integración, roles GBS, timeline tipo)
    ├── dd_checklist.md     (due diligence financiero desde GBS)
    └── integration_waves.md (cómo incorporar una entidad al GBS existente)
```

**Connectors a integrar:**
- `legal:review-contract` skill: revisión de acuerdos de compraventa (SPA)
- `legal:legal-risk-assessment` skill: riesgos legales de la transacción
- `finance:financial-statements` skill: análisis de estados financieros target
- `finance:reconciliation` skill: reconciliación de balances post-integración
- `data:explore-data` skill: análisis de datos financieros de la empresa adquirida
- `nimble:company-deep-dive` skill: research de la empresa target
- `mcp__d7ab2e83` (Google Drive): acceso a data room y documentos de M&A

---

### TAREA 4: Integración tiempo real CINDE y PROCOMER
**Prioridad:** Media | **Estimado:** 2–3 horas

**Objetivo:** Añadir al skill `ssc-location-cr` un módulo de scraping/fetching de datos
en tiempo real desde CINDE (cinde.org) y PROCOMER (procomer.com) para mantener
actualizados los datos de talento, zonas francas, incentivos y empresas operando en CR.

**Implementación:**
```python
# Fuentes de datos a extraer:
CINDE_URLS = [
    "https://cinde.org/en/why-invest-in-costa-rica",
    "https://cinde.org/en/sectors/business-services",
    "https://cinde.org/en/living-in-costa-rica/human-talent"
]
PROCOMER_URLS = [
    "https://www.procomer.com/zona-franca/",
    "https://www.procomer.com/estadisticas/"
]
```

**Connectors a integrar:**
- `brightdata-plugin:scrape` skill: scraping de CINDE/PROCOMER con bypass anti-bot
- `brightdata-plugin:search` skill: búsqueda de noticias recientes Costa Rica GBS
- `nimble:nimble-web-expert` skill: extracción estructurada de datos de talento
- `data:analyze` skill: análisis de datos extraídos
- `mcp__scheduled-tasks`: programar actualización semanal automática de datos CR

**Script a crear:** `scripts/update_cr_data.py`
- Extraer datos actualizados de salarios, empresas, incentivos
- Actualizar `references/talent_cr.md` y `references/costs_cr.md` en ssc-location-cr
- Generar reporte de cambios con diff vs. versión anterior

**Instrucciones para Claude Code:**
1. Verificar disponibilidad de Bright Data o Nimble CLI en el sistema
2. Crear script de scraping con manejo de errores
3. Configurar scheduled task semanal para actualización automática
4. Crear changelog automático de actualizaciones de datos

---

### TAREA 5: Templates descargables Excel (Business Case + KPI Dashboard)
**Prioridad:** Alta — usuarios necesitan herramientas concretas | **Estimado:** 3–4 horas

**Archivos Excel a crear:**

**5A. Business Case Template (`SSC_Business_Case_Template.xlsx`)**
- Sheet 1: Assumptions & Inputs (células editables en amarillo)
- Sheet 2: Labor Arbitrage Model (5 años, por función)
- Sheet 3: Automation Benefits (por proceso, por año)
- Sheet 4: One-Time Costs (CAPEX breakdown)
- Sheet 5: Operating Costs (OPEX por categoría)
- Sheet 6: P&L Summary (consolidado, 3 escenarios)
- Sheet 7: Financial Metrics (NPV, IRR, Payback, ROI)
- Sheet 8: Sensitivity Analysis (tabla de sensibilidad)
- Sheet 9: Executive Dashboard (gráficos para presentación)

**5B. KPI Dashboard Template (`SSC_KPI_Dashboard_Template.xlsx`)**
- Sheet 1: Monthly Input (ingresar métricas del mes)
- Sheet 2: P2P KPIs (facturas, pagos, touchless rate)
- Sheet 3: O2C KPIs (DSO, cash application, collections)
- Sheet 4: R2R KPIs (close days, recons, journals)
- Sheet 5: Service KPIs (CSAT, NPS, SLA compliance)
- Sheet 6: People KPIs (rotación, engagement, headcount)
- Sheet 7: Executive Dashboard (gráficos de tendencia + RAG status)
- Sheet 8: Benchmark Comparison (actual vs. best practice)

**Instrucciones para Claude Code:**
1. Leer `04_business_case_agent.md` y `references/financial_model.md`
2. Usar el `xlsx` skill para crear ambos archivos
3. Incluir fórmulas Excel para cálculos automáticos
4. Usar formato profesional con colores: verde=logrado, amarillo=en riesgo, rojo=no logrado
5. Guardar en `SSC Module/SSC-Agents/templates/`

---

### TAREA 6: Versión en inglés de todos los agentes
**Prioridad:** Media | **Estimado:** 6–8 horas

**Estructura a crear:**
```
SSC-Agents/
├── en/                          ← Versión en inglés
│   ├── ssc-orchestrator-en.skill
│   ├── ssc-diagnostic-en.skill
│   ├── ...
│   └── README_EN.md
└── es/                          ← Mover versión en español aquí
    ├── ssc-orchestrator.skill
    ├── ...
    └── README.md
```

**Consideraciones de traducción:**
- No es traducción literal: adaptar terminología al inglés de negocio GBS
- Mantener todos los datos de mercado de Costa Rica (no traducir los números)
- Actualizar los benchmarks al contexto global (no solo LATAM)
- Agregar contexto de US GAAP para audiencias norteamericanas
- Mantener referencias a Big 4 pero con énfasis en global practices

**Instrucciones para Claude Code:**
1. Traducir skill por skill, empezando por `ssc-orchestrator`
2. Validar terminología GBS con estándares APQC y Hackett Group
3. Crear README_EN.md adaptado
4. Hacer zip de cada skill con sufijo `-en`

---

## PARTE 2: INTEGRACIÓN CON CONNECTORS, PLUGINS Y MCP SERVERS

### Mapa completo de integración SSC ↔ Ecosystem

A continuación el playbook de cómo cada connector disponible en Claude Desktop
potencia los módulos del SSC Agent Suite.

---

### 🔵 GMAIL (mcp__90c11731__*)
**Uso en proyecto SSC:**

| Módulo SSC | Caso de uso Gmail |
|------------|-------------------|
| M09 Service Mgmt | Enviar reportes mensuales de KPIs a stakeholders automáticamente |
| M07 Org & Talent | Comunicaciones de change management, anuncios al equipo |
| M05 Procesos | Integrar e-invoicing: recibir facturas de proveedores por email |
| M08 Migración | Enviar updates de progreso de waves al PMO global |
| M09 VoC | Enviar encuestas de satisfacción a clientes internos |

**Comandos tipo:**
```
"Redacta y envía el KPI report mensual de P2P a los stakeholders del GBS"
"Programa un email semanal de status de migración a los sponsors ejecutivos"
"Busca en mi inbox facturas de proveedores sin procesar esta semana"
```

---

### 📅 GOOGLE CALENDAR (mcp__c2253a72__*)
**Uso en proyecto SSC:**

| Módulo SSC | Caso de uso Calendar |
|------------|---------------------|
| M09 Gobernanza | Crear y gestionar todas las reuniones del governance framework |
| M08 KT | Programar sesiones de KT con SMEs y trainees |
| M10 Kaizen | Calendario de eventos Kaizen mensuales/trimestrales |
| M09 Reviews | Recordatorios automáticos para reviews de SLA |

**Comandos tipo:**
```
"Crea el calendario completo de gobernanza del GBS para Q3 2026"
"Programa las sesiones de KT para Wave 2 con los SMEs de AP"
"Crea recordatorio mensual para la encuesta VoC de clientes internos"
```

---

### 📁 GOOGLE DRIVE (mcp__d7ab2e83__*)
**Uso en proyecto SSC:**

| Módulo SSC | Caso de uso Drive |
|------------|------------------|
| Todos | Repositorio central de documentación SSC (SOPs, process maps) |
| M04 Business Case | Almacenar y versionar el modelo financiero |
| M08 KT | Compartir templates de SOP y work instructions con SMEs |
| M09 SLAs | Centralizar contratos de SLA firmados |
| M01 Diagnóstico | Almacenar resultados del FRA para referencia futura |

**Comandos tipo:**
```
"Sube el SOP de AP actualizado al repositorio del GBS en Drive"
"Busca en Drive la última versión del Business Case del GBS"
"Crea estructura de carpetas para el GBS Costa Rica en Drive"
```

---

### 🎨 CANVA (mcp__80f8b464__*)
**Uso en proyecto SSC:**

| Módulo SSC | Caso de uso Canva |
|------------|------------------|
| M07 Org Design | Crear org chart visual profesional del GBS |
| M07 Inducción | Materiales de onboarding (welcome pack, cultura GBS) |
| M09 Service Mgmt | Infografías de SLAs y KPIs para clientes internos |
| M02 Estrategia | Poster de Vision & Values del GBS |
| M07 Change Mgmt | Materiales de comunicación para change management |

**Comandos tipo:**
```
"Crea el org chart del GBS Costa Rica usando la plantilla corporativa"
"Diseña el welcome pack de inducción para nuevos empleados del GBS"
"Crea infografía de los KPIs principales del mes para el reporte ejecutivo"
```

---

### 🖊️ FIGMA (mcp__e73feef8__*)
**Uso en proyecto SSC:**

| Módulo SSC | Caso de uso Figma |
|------------|------------------|
| M05 Procesos | Diagramas de flujo de procesos P2P/O2C/R2R to-be |
| M06 Tecnología | Arquitectura de referencia del stack tecnológico GBS |
| M09 Service Mgmt | Framework de Service Management en diagrama visual |
| M02 Operating Model | Diagrama del modelo operativo GBS (5 dimensiones) |

**Comandos tipo:**
```
"Crea el diagrama de flujo del proceso AP to-be con automation overlay en Figma"
"Diseña la arquitectura tecnológica del GBS en un diagrama de capas en Figma"
```

---

### 🎙️ MINUTES & MEETING MEMORY (mcp__Minutes___Meeting_Memory_for_AI__*)
**Uso en proyecto SSC — MUY VALIOSO:**

| Módulo SSC | Caso de uso Minutes |
|------------|---------------------|
| M09 Gobernanza | Grabar y transcribir todas las reuniones de gobernanza |
| M08 KT | Documentar sesiones de KT para referencia futura |
| M10 Kaizen | Capturar acuerdos y action items de eventos Kaizen |
| M01 Diagnóstico | Transcribir entrevistas con process owners |
| Todos | Track de compromisos entre reuniones de governance |

**Comandos tipo:**
```
"Graba la reunión del Comité de Operaciones del GBS y extrae los action items"
"Busca en el historial de reuniones qué se decidió sobre la migración de AR"
"Genera las minutas del Board trimestral con compromisos y responsables"
```

---

### 🔷 SAP FIORI (mcp__SAP_Fiori_MCP_Server__*)
**Uso en proyecto SSC — CRÍTICO para entornos SAP:**

| Módulo SSC | Caso de uso SAP Fiori |
|------------|-----------------------|
| M05 Procesos | Documentar transacciones SAP específicas en los SOPs |
| M06 Tecnología | Explorar apps de SAP S/4HANA disponibles para GBS |
| M08 KT | Referencia de transacciones SAP para materiales de training |
| M05 Automatización | Identificar APIs SAP para integración con RPA |

**Comandos tipo:**
```
"Lista las apps de SAP Fiori disponibles para el proceso de AP en S/4HANA"
"Documenta los pasos de la transacción FB60 de SAP para el SOP de AP"
"Busca en la documentación SAP cómo configurar automatic payment runs"
```

---

### 📊 DATA PLUGIN (data:analyze, data:sql-queries, etc.)
**Uso en proyecto SSC:**

| Módulo SSC | Caso de uso Data |
|------------|-----------------|
| M01 Diagnóstico | Analizar datos de ERP para benchmarking (volúmenes, costos) |
| M04 Business Case | Modelado financiero y análisis de escenarios |
| M09 KPIs | Analizar tendencias de desempeño del GBS |
| M10 Sustain | Estadísticas de proceso para identificar áreas de mejora |
| M03 Location | Análisis de datos de mercado laboral CR |

**Comandos tipo:**
```
"Analiza estos datos de transacciones de AP y calcula el costo promedio por factura"
"Construye un dashboard de KPIs del GBS con los datos del mes"
"Escribe una query SQL para extraer el invoice aging report desde el ERP"
```

---

### ⚖️ LEGAL PLUGIN (legal:compliance-check, legal:review-contract, etc.)
**Uso en proyecto SSC:**

| Módulo SSC | Caso de uso Legal |
|------------|------------------|
| M03 Location | Verificación de cumplimiento Zona Franca CR (Ley 7210) |
| M09 SLAs | Revisión de contratos SLA intercompany (transfer pricing) |
| M07 Talent | Compliance laboral CR (Código de Trabajo, CCSS) |
| M03 Datos | Compliance Ley 8968 (protección de datos CR) |
| M05 Procesos | Revisión de contratos de proveedores para AP |

**Comandos tipo:**
```
"Revisa este contrato de SLA intercompany para verificar compliance con precios de transferencia"
"Verifica si nuestra operación en Costa Rica cumple con todos los requisitos de Zona Franca"
"Analiza los riesgos legales laborales de la transición de personal al GBS"
```

---

### 📈 FINANCE PLUGIN (finance:financial-statements, finance:variance-analysis, etc.)
**Uso en proyecto SSC:**

| Módulo SSC | Caso de uso Finance |
|------------|---------------------|
| M04 Business Case | Modelado de estados financieros proyectados del GBS |
| M09 Chargeback | Análisis de varianzas en los cargos intercompany |
| M10 Sustain | Preparación de reportes financieros del GBS para Board |
| M05 R2R | Referencia para diseño de procesos contables |

**Comandos tipo:**
```
"Genera el P&L del GBS para los primeros 3 años proyectados"
"Analiza la varianza entre el costo real y el presupuestado del GBS este trimestre"
"Prepara el estado financiero del GBS para la revisión del Board"
```

---

### 🏗️ OPERATIONS PLUGIN (operations:process-doc, operations:runbook, etc.)
**Uso en proyecto SSC:**

| Módulo SSC | Caso de uso Operations |
|------------|------------------------|
| M08 KT | Crear runbooks operacionales para procesos migrados |
| M09 BCP | Documentar plan de continuidad del negocio (BCP) |
| M10 CI | Documentar procesos mejorados post-Kaizen |
| M09 Risk | Risk assessment de operaciones del GBS |
| M09 Status | Status reports mensuales para governance |

**Comandos tipo:**
```
"Crea el runbook operacional del proceso de payment run para el equipo de AP"
"Documenta el BCP del GBS con todos los riesgos identificados y sus mitigaciones"
"Genera el status report semanal del GBS para el Comité de Operaciones"
```

---

### 🚀 PRODUCT MANAGEMENT PLUGIN
**Uso en proyecto SSC:**

| Módulo SSC | Caso de uso PM |
|------------|----------------|
| M08 Migración | Sprint planning para cada wave de migración |
| M02 Estrategia | Roadmap del GBS (Now/Next/Later) |
| M09 Service Mgmt | Stakeholder updates para sponsors ejecutivos |
| M10 OKRs | OKR tracking y revisión trimestral |

**Comandos tipo:**
```
"Crea el sprint plan para Wave 2 de migración (AR + Cash Application)"
"Genera el stakeholder update mensual del GBS para el CFO"
"Crea el roadmap del GBS para los próximos 3 años en formato visual"
```

---

### 📣 MARKETING PLUGIN
**Uso en proyecto SSC:**

| Módulo SSC | Caso de uso Marketing |
|------------|----------------------|
| M07 EVP | Crear la propuesta de valor al empleado (EVP) del GBS |
| M07 Change Mgmt | Contenido para campaña interna de change management |
| M03 Location | Materiales de presentación a CINDE para atracción de inversión |

**Comandos tipo:**
```
"Crea la campaña de change management para el lanzamiento del GBS en CR"
"Redacta el EVP del GBS Costa Rica para reclutamiento en LinkedIn"
```

---

### 🔍 NIMBLE / BRIGHT DATA (research + scraping)
**Uso en proyecto SSC — CLAVE para datos actualizados:**

| Módulo SSC | Caso de uso Nimble/BrightData |
|------------|-------------------------------|
| M03 Location | Datos actualizados de salarios GBS en CR (LinkedIn Jobs, Indeed CR) |
| M03 Location | Noticias CINDE/PROCOMER sobre incentivos, nuevas empresas |
| M01 Diagnóstico | Benchmarks actualizados de costos por transacción (Hackett, Gartner) |
| M02 Estrategia | Competitive intel sobre Big 4 metodologías GBS más recientes |
| M10 Benchmarking | Datos de desempeño GBS de empresas comparables |

**Comandos tipo:**
```
"Busca los salarios actuales de AP Analyst bilingüe en Costa Rica en LinkedIn Jobs"
"Extrae de CINDE.org las últimas estadísticas de inversión en servicios 2025"
"Investiga qué empresas abrieron GBS en Costa Rica en el último año"
"Busca benchmarks actualizados de costo por factura AP en reports de Hackett Group"
```

---

### ⏰ SCHEDULED TASKS (mcp__scheduled-tasks__*)
**Automatizaciones periódicas recomendadas para el GBS:**

```yaml
Tarea 1 — KPI Report Semanal:
  Frecuencia: Lunes 8:00 AM
  Acción: Generar reporte semanal de KPIs del GBS y enviarlo por Gmail
  Skills: data:analyze + Gmail

Tarea 2 — VoC Survey Trimestral:
  Frecuencia: Primer día de cada trimestre
  Acción: Enviar encuesta VoC a lista de clientes internos por Gmail
  Skills: Gmail (envío) + data:analyze (resultados)

Tarea 3 — Actualización Datos CR:
  Frecuencia: Domingo 6:00 AM (semanal)
  Acción: Scraping CINDE/PROCOMER y actualización de references
  Skills: Bright Data scrape + Write tool

Tarea 4 — Health Check Reminder:
  Frecuencia: Primero de cada mes
  Acción: Recordatorio para ejecutar el GBS Health Check (Módulo 10)
  Skills: Gmail + ssc-sustain-ci skill

Tarea 5 — Governance Meeting Agenda:
  Frecuencia: Jueves antes de cada reunión mensual
  Acción: Preparar agenda del Comité de Operaciones con KPIs del mes
  Skills: data:analyze + Google Calendar + Gmail
```

---

### 📄 PDF TOOLS (mcp__PDF_Tools__*)
**Uso en proyecto SSC:**
- Extraer texto de documentos de referencia (PPT/PPTX/DOC de la fuente)
- Crear SOPs en PDF con firma electrónica para sign-off de KT
- Merge de reportes para paquete ejecutivo mensual
- Llenar formularios de registro PROCOMER (Zona Franca)
- Firmar SLAs intercompany digitalmente

---

## PARTE 3: DEBUG & TESTING CHECKLIST

### 3.1 Verificación de Skills Instalados

> **Nota V2.0:** desde la reorganización bilingüe, los skills en español viven en `es/` y los
> de inglés en `en/` (con sufijo `-en`). Los scripts de esta sección usan el prefijo `es/`.
> El nombre de la carpeta *dentro* del zip no lleva prefijo (sigue siendo `${skill}/SKILL.md`).

```bash
# Verificar que todos los .skill files (español) están correctamente formados:
for skill in ssc-orchestrator ssc-diagnostic ssc-strategy ssc-location-cr \
             ssc-business-case ssc-process-automation ssc-technology \
             ssc-org-talent ssc-migration-kt ssc-service-mgmt ssc-sustain-ci \
             ssc-hr-gbs ssc-esg-hub ssc-ma-support; do
    echo "Testing: es/${skill}.skill"
    unzip -t "es/${skill}.skill" && echo "✓ OK" || echo "✗ CORRUPT"
    unzip -p "es/${skill}.skill" "${skill}/SKILL.md" | head -5
    echo "---"
done

# Verificar las versiones en inglés:
for skill in ssc-orchestrator ssc-diagnostic ssc-strategy ssc-location-cr \
             ssc-business-case ssc-process-automation ssc-technology \
             ssc-org-talent ssc-migration-kt ssc-service-mgmt ssc-sustain-ci \
             ssc-hr-gbs ssc-esg-hub ssc-ma-support; do
    echo "Testing: en/${skill}-en.skill"
    unzip -t "en/${skill}-en.skill" && echo "✓ OK" || echo "✗ CORRUPT"
    unzip -p "en/${skill}-en.skill" "${skill}-en/SKILL.md" | head -5
    echo "---"
done
```

### 3.2 Verificación de SKILL.md Frontmatter

Cada SKILL.md debe tener:
```yaml
---
name: [slug-kebab-case]          # Requerido, debe coincidir con nombre del directorio
description: >                    # Requerido, descripción para triggering
  [descripción larga que incluya
   todas las frases de trigger]
---
```

### 3.3 Test Cases por Skill (prompts de prueba)

**ssc-orchestrator:**
- "Quiero implementar un SSC en Costa Rica, ¿por dónde empiezo?"
- "¿En qué fase del pipeline SSC estamos si ya tenemos el diagnóstico?"

**ssc-diagnostic:**
- "Necesito evaluar si nuestra área de Finance es candidata para un SSC"
- "¿Cuál es el benchmark de costo por factura de AP para empresas de mi industria?"

**ssc-location-cr:**
- "Compara Costa Rica vs. Colombia para establecer nuestro GBS"
- "¿Qué zonas francas en Costa Rica son mejores para un GBS de 200 personas?"

**ssc-business-case:**
- "Tenemos 50 FTEs en Finance en Colombia con costo promedio $45,000/año. ¿Cuánto ahorraríamos con un SSC en CR?"
- "Calcula el ROI de automatizar el proceso de AP con RPA"

**ssc-process-automation:**
- "Diseña el proceso to-be de AP con touchless invoicing"
- "¿Qué procesos de Finance son candidatos para RPA en nuestro GBS?"

**ssc-technology:**
- "¿Qué ERP recomiendas para nuestro GBS en Costa Rica si actualmente usamos SAP ECC?"
- "Compara UiPath vs. Power Automate para automatizar el GBS"

**ssc-org-talent:**
- "Diseña el org chart para un GBS de Finance de 150 personas en Costa Rica"
- "¿Cuánto debería ganar un AP Analyst bilingüe en Costa Rica?"

**ssc-migration-kt:**
- "Crea un plan de migración por waves para mover AP, AR y R2R a nuestro GBS en CR"
- "¿Cómo estructura el knowledge transfer cuando los SMEs de origen no pueden viajar?"

**ssc-service-mgmt:**
- "Necesito crear SLAs para el GBS con 5 BUs como clientes internos"
- "Diseña el KPI dashboard mensual para el Comité de Operaciones del GBS"

**ssc-sustain-ci:**
- "Haz un health check de nuestro GBS que lleva 6 meses operando"
- "¿Cómo implementamos un programa de Kaizen en nuestro centro de servicios?"

### 3.4 Checklist de Calidad de Contenido

Para cada skill verificar:
- [ ] Frontmatter YAML válido (name, description completos)
- [ ] Description incluye frases de trigger variadas
- [ ] SKILL.md < 500 líneas (progressive disclosure funciona)
- [ ] Referencias a archivos en `references/` son correctas y existen
- [ ] Los datos de mercado CR tienen fecha/fuente indicada
- [ ] Los benchmarks tienen atribución (Big 4, APQC, Hackett, etc.)
- [ ] Las preguntas de entrada están presentes (input collection)
- [ ] Los entregables están listados (output definition)
- [ ] No hay contradicciones entre skills relacionados

### 3.5 Debug de Integración con Connectors

Para cada integración crítica, testear:

```
TEST 1 — Gmail + ssc-service-mgmt:
Prompt: "Genera y envía el reporte de KPIs de P2P de esta semana a mi equipo"
Esperado: Gmail crea draft con datos de KPIs formateados

TEST 2 — Google Calendar + ssc-migration-kt:
Prompt: "Programa las sesiones de KT de Wave 1 para las próximas 8 semanas"
Esperado: Eventos creados en calendario con agenda y participantes

TEST 3 — Nimble + ssc-location-cr:
Prompt: "Busca los salarios actuales de AP Analyst bilingüe en Costa Rica"
Esperado: Datos extraídos de fuentes actuales (LinkedIn, Indeed CR, CINDE)

TEST 4 — Data:analyze + ssc-sustain-ci:
Prompt: "Analiza estos KPIs del GBS y genera el Health Check del trimestre"
Esperado: Análisis estructurado con semáforos y recomendaciones

TEST 5 — Legal + ssc-location-cr:
Prompt: "Verifica el compliance de nuestro contrato de Zona Franca con PROCOMER"
Esperado: Revisión contra Ley 7210 con hallazgos y gaps
```

---

## PARTE 4: COMANDOS PARA CLAUDE CODE

### Construir un nuevo skill desde cero:
```
1. Lee los archivos de referencia del módulo relacionado en SSC-Agents/
2. Crea directorio: /tmp/ssc-skills/[nombre-skill]/references/
3. Escribe SKILL.md siguiendo el formato de skills existentes
4. Crea archivos de references/ con contenido detallado
5. Ejecuta: cd /tmp/ssc-skills && zip -r /tmp/[nombre].skill [nombre]/
6. Copia el .skill a SSC Module/SSC-Agents/es/  (versión inglés → en/ con sufijo -en)
7. Actualiza es/README.md (y en/README_EN.md) con la nueva entrada
```
> En Windows sin `zip`/`unzip`, usar el empaquetador PowerShell con entradas de barra normal
> (forward slash) — ver `scripts/` para el patrón `System.IO.Compression.ZipArchive`.

### Actualizar un skill existente:
```
1. Extrae: unzip es/[skill].skill -d /tmp/[skill-name]-edit/
2. Edita los archivos necesarios
3. Re-empaqueta: cd /tmp && zip -r [skill-name].skill [skill-name]-edit/[skill-name]/
4. Reemplaza en SSC Module/SSC-Agents/es/  (o en/ para la versión -en)
```

### Crear los Excel templates (Tarea 5):
```
Usa el skill `xlsx` con estas instrucciones:
"Crea SSC_Business_Case_Template.xlsx con 9 hojas según especificación en CLAUDE.md Tarea 5"
"Crea SSC_KPI_Dashboard_Template.xlsx con 8 hojas según especificación en CLAUDE.md Tarea 5"
Guarda en: SSC Module/SSC-Agents/templates/
```

### Configurar las Scheduled Tasks (desde Cowork):
```
Para cada tarea en la sección 3.2, usar el skill `schedule` con:
- Descripción de la tarea
- Frecuencia (cron expression)
- Prompt de la acción a ejecutar
```

---

## PARTE 5: NOTAS DE MANTENIMIENTO

### Actualización periódica recomendada (trimestral):
1. Actualizar benchmarks en `references/benchmarks.md` con datos más recientes
2. Verificar salarios CR en `references/talent_cr.md` vs. market surveys
3. Actualizar zona franca benefits si hay cambios en Ley 7210
4. Revisar Big 4 publications para nuevas prácticas
5. Incorporar nuevas herramientas de automatización emergentes

### Control de versiones:
- Cada skill tiene versión implícita en la fecha del SKILL.md
- Para cambios mayores: crear nueva versión del skill con sufijo `-v2`
- Mantener backward compatibility en los triggers (description)

### Contacto y ownership:
- Proyecto iniciado: Junio 2026
- Plataforma: Claude Cowork (Anthropic)
- Base metodológica: SSC/GBS toolkit basado en prácticas Big 4, actualizado Big 4 2025–2026
