#!/usr/bin/env python3
"""
build_excel_templates.py — Tarea 5 del roadmap CLAUDE.md
========================================================
Genera dos plantillas Excel profesionales con fórmulas vivas y formato RAG:

  templates/SSC_Business_Case_Template.xlsx   (9 hojas)
  templates/SSC_KPI_Dashboard_Template.xlsx   (8 hojas)

Base metodológica: 04_business_case_agent.md + 09_service_mgmt_agent.md.
Celdas de input editables resaltadas en amarillo. Cálculos automáticos por fórmula.
RAG: verde = logrado / amarillo = en riesgo / rojo = no logrado.

Requiere: openpyxl. Uso:  python scripts/build_excel_templates.py
"""

from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "templates"
OUT_DIR.mkdir(exist_ok=True)

# --------------------------------------------------------------------------- #
# Paleta y estilos
# --------------------------------------------------------------------------- #
NAVY = "1F3864"
BLUE = "2E5496"
LIGHTBLUE = "D9E1F2"
YELLOW = "FFF2CC"        # input editable
GREEN = "C6EFCE"
GREEN_T = "006100"
AMBER = "FFEB9C"
AMBER_T = "9C6500"
RED = "FFC7CE"
RED_T = "9C0006"
GREY = "F2F2F2"
WHITE = "FFFFFF"

F_TITLE = Font(name="Calibri", size=16, bold=True, color=WHITE)
F_SUB = Font(name="Calibri", size=10, italic=True, color=WHITE)
F_HDR = Font(name="Calibri", size=11, bold=True, color=WHITE)
F_SECTION = Font(name="Calibri", size=12, bold=True, color=NAVY)
F_BOLD = Font(name="Calibri", size=10, bold=True)
F_NORM = Font(name="Calibri", size=10)
F_NOTE = Font(name="Calibri", size=9, italic=True, color="808080")

FILL_TITLE = PatternFill("solid", fgColor=NAVY)
FILL_HDR = PatternFill("solid", fgColor=BLUE)
FILL_SECTION = PatternFill("solid", fgColor=LIGHTBLUE)
FILL_INPUT = PatternFill("solid", fgColor=YELLOW)
FILL_GREY = PatternFill("solid", fgColor=GREY)
FILL_LIGHT = PatternFill("solid", fgColor=LIGHTBLUE)

THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
CTR = Alignment(horizontal="center", vertical="center")
LEFT = Alignment(horizontal="left", vertical="center", wrap_text=True)
RIGHT = Alignment(horizontal="right", vertical="center")

USD = '#,##0;(#,##0)'
USD0 = '$#,##0;($#,##0)'
PCT = '0.0%'
PCT0 = '0%'
NUM1 = '#,##0.0'
NUM = '#,##0'


def style_cell(ws, ref, value=None, font=None, fill=None, align=None,
               fmt=None, border=True):
    c = ws[ref]
    if value is not None:
        c.value = value
    if font:
        c.font = font
    if fill:
        c.fill = fill
    if align:
        c.alignment = align
    if fmt:
        c.number_format = fmt
    if border:
        c.border = BORDER
    return c


def title_block(ws, title, subtitle, last_col="H"):
    ws.merge_cells(f"A1:{last_col}1")
    style_cell(ws, "A1", title, F_TITLE, FILL_TITLE, CTR, border=False)
    ws.merge_cells(f"A2:{last_col}2")
    style_cell(ws, "A2", subtitle, F_SUB, FILL_TITLE, CTR, border=False)
    ws.row_dimensions[1].height = 26
    ws.row_dimensions[2].height = 16


def section(ws, row, text, last_col="H"):
    ws.merge_cells(f"A{row}:{last_col}{row}")
    style_cell(ws, f"A{row}", text, F_SECTION, FILL_SECTION, LEFT)


def rag_rules(ws, rng):
    """Aplica RAG simple: verde>=0 si mayor mejor — usado para flujos."""
    ws.conditional_formatting.add(
        rng, CellIsRule(operator="greaterThanOrEqual", formula=["0"],
                        fill=PatternFill("solid", fgColor=GREEN), font=Font(color=GREEN_T)))
    ws.conditional_formatting.add(
        rng, CellIsRule(operator="lessThan", formula=["0"],
                        fill=PatternFill("solid", fgColor=RED), font=Font(color=RED_T)))


YEARS = ["Year 0", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]


# =========================================================================== #
# BUSINESS CASE WORKBOOK
# =========================================================================== #
def build_business_case():
    wb = Workbook()

    # ---- Sheet 1: Assumptions & Inputs ----
    ws = wb.active
    ws.title = "1. Assumptions"
    title_block(ws, "SSC / GBS — Business Case Model",
                "Plantilla 5 años · Celdas amarillas = editables · Cálculo automático", "F")
    ws.column_dimensions["A"].width = 44
    ws.column_dimensions["B"].width = 16
    for c in "CDEF":
        ws.column_dimensions[c].width = 14

    r = 4
    section(ws, r, "Parámetros generales", "F"); r += 1
    gen = [
        ("Moneda del modelo", "USD"),
        ("Tasa de descuento / WACC", 0.10, PCT),
        ("Salario promedio FTE origen (fully-loaded, USD/año)", 55000, USD0),
        ("Costo promedio FTE Costa Rica (fully-loaded, USD/año)", 26000, USD0),
        ("Factor de cargas sociales CR (sobre salario base)", 0.265, PCT),
        ("Inflación salarial CR anual", 0.05, PCT),
        ("FTEs retenidos en origen (retained org)", 6, NUM),
        ("Management fee intercompany (% del costo SSC)", 0.06, PCT),
    ]
    ws[f"A{r-1}"]
    start_gen = r
    for label, *rest in gen:
        val = rest[0]
        fmt = rest[1] if len(rest) > 1 else None
        style_cell(ws, f"A{r}", label, F_NORM, None, LEFT)
        style_cell(ws, f"B{r}", val, F_BOLD, FILL_INPUT, RIGHT, fmt)
        r += 1
    # named refs (by cell) — capture rows
    WACC = f"'1. Assumptions'!$B${start_gen+1}"
    COST_ORIGIN = f"'1. Assumptions'!$B${start_gen+2}"
    COST_CR = f"'1. Assumptions'!$B${start_gen+3}"
    INFL = f"'1. Assumptions'!$B${start_gen+5}"
    RETAINED = f"'1. Assumptions'!$B${start_gen+6}"
    MGMT_FEE = f"'1. Assumptions'!$B${start_gen+7}"

    r += 1
    section(ws, r, "Ramp-up: % del ahorro steady-state realizado por año", "F"); r += 1
    style_cell(ws, f"A{r}", "Factor de realización", F_BOLD, FILL_GREY, LEFT)
    ramp_vals = [0.0, 0.40, 0.80, 1.00, 1.00, 1.00]
    ramp_row = r
    for i, v in enumerate(ramp_vals):
        col = get_column_letter(2 + i) if i < 4 else get_column_letter(2 + i)
    # place ramp across B..G is 6 cols but we only have B..F width; extend G
    ws.column_dimensions["G"].width = 14
    style_cell(ws, f"A{r}", "Factor de realización del ahorro", F_NORM, None, LEFT)
    for i, v in enumerate(ramp_vals):
        col = get_column_letter(2 + i)  # B..G
        style_cell(ws, f"{col}{r}", YEARS[i], F_NOTE, FILL_GREY, CTR)
    r += 1
    style_cell(ws, f"A{r}", "Valor (editable)", F_NORM, None, LEFT)
    for i, v in enumerate(ramp_vals):
        col = get_column_letter(2 + i)
        style_cell(ws, f"{col}{r}", v, F_BOLD, FILL_INPUT, CTR, PCT0)
    ramp_value_row = r
    RAMP = {i: f"'1. Assumptions'!${get_column_letter(2+i)}${ramp_value_row}" for i in range(6)}

    r += 2
    section(ws, r, "Escenarios — multiplicadores", "F"); r += 1
    style_cell(ws, f"A{r}", "Variable", F_HDR, FILL_HDR, LEFT)
    style_cell(ws, f"B{r}", "Conservador", F_HDR, FILL_HDR, CTR)
    style_cell(ws, f"C{r}", "Base", F_HDR, FILL_HDR, CTR)
    style_cell(ws, f"D{r}", "Optimista", F_HDR, FILL_HDR, CTR)
    r += 1
    scen = [
        ("Multiplicador de ahorro (consolidación + automatización)", 0.75, 1.00, 1.25),
        ("Multiplicador de CAPEX", 1.15, 1.00, 0.95),
    ]
    scen_rows = {}
    for label, a, b, c in scen:
        style_cell(ws, f"A{r}", label, F_NORM, None, LEFT)
        style_cell(ws, f"B{r}", a, F_BOLD, FILL_INPUT, CTR, '0.00')
        style_cell(ws, f"C{r}", b, F_BOLD, FILL_INPUT, CTR, '0.00')
        style_cell(ws, f"D{r}", c, F_BOLD, FILL_INPUT, CTR, '0.00')
        scen_rows[label.split(" (")[0]] = r
        r += 1
    SAVE_MULT_BASE = f"'1. Assumptions'!$C${scen_rows['Multiplicador de ahorro']}"

    r += 1
    style_cell(ws, f"A{r}", "Nota: edita solo celdas amarillas. Las demás hojas leen estos parámetros.",
               F_NOTE, None, LEFT, border=False)

    # store refs on wb for reuse
    refs = dict(WACC=WACC, COST_ORIGIN=COST_ORIGIN, COST_CR=COST_CR, INFL=INFL,
                RETAINED=RETAINED, MGMT_FEE=MGMT_FEE, RAMP=RAMP,
                SAVE_MULT_BASE=SAVE_MULT_BASE)

    # ---- Sheet 2: Labor Arbitrage ----
    ws2 = wb.create_sheet("2. Labor Arbitrage")
    title_block(ws2, "Labor Arbitrage Model", "Ahorro por consolidación de FTEs, por función (steady-state)", "G")
    ws2.column_dimensions["A"].width = 26
    for c in "BCDEFG":
        ws2.column_dimensions[c].width = 15
    headers = ["Función", "FTEs origen", "Ratio consolidación", "FTEs en CR",
               "Costo origen (USD)", "Costo CR (USD)", "Ahorro anual (USD)"]
    hr = 4
    for i, h in enumerate(headers):
        style_cell(ws2, f"{get_column_letter(1+i)}{hr}", h, F_HDR, FILL_HDR, CTR)
    funcs = [
        ("AP / Procure-to-Pay", 10, 2.3),
        ("AR / Order-to-Cash", 8, 2.4),
        ("R2R / General Ledger", 12, 2.2),
        ("Payroll / Nómina", 6, 2.0),
        ("T&E", 4, 2.0),
    ]
    first = hr + 1
    rr = first
    for name, ftes, ratio in funcs:
        style_cell(ws2, f"A{rr}", name, F_NORM, None, LEFT)
        style_cell(ws2, f"B{rr}", ftes, F_BOLD, FILL_INPUT, CTR, NUM)
        style_cell(ws2, f"C{rr}", ratio, F_BOLD, FILL_INPUT, CTR, '0.0"x"')
        style_cell(ws2, f"D{rr}", f"=B{rr}/C{rr}", F_NORM, None, CTR, NUM1)
        style_cell(ws2, f"E{rr}", f"=B{rr}*{refs['COST_ORIGIN']}", F_NORM, None, RIGHT, USD0)
        style_cell(ws2, f"F{rr}", f"=D{rr}*{refs['COST_CR']}", F_NORM, None, RIGHT, USD0)
        style_cell(ws2, f"G{rr}", f"=E{rr}-F{rr}", F_BOLD, None, RIGHT, USD0)
        rr += 1
    last = rr - 1
    style_cell(ws2, f"A{rr}", "TOTAL", F_BOLD, FILL_LIGHT, LEFT)
    for col in "BDEFG":
        style_cell(ws2, f"{col}{rr}", f"=SUM({col}{first}:{col}{last})", F_BOLD, FILL_LIGHT,
                   RIGHT if col in "EFG" else CTR, USD0 if col in "EFG" else NUM1)
    style_cell(ws2, f"C{rr}", "", F_BOLD, FILL_LIGHT, CTR)
    labor_total_row = rr
    refs["LABOR_SAVING"] = f"'2. Labor Arbitrage'!$G${labor_total_row}"
    style_cell(ws2, f"A{rr+2}", "Retained org (costo que permanece en origen):", F_NORM, None, LEFT, border=False)
    style_cell(ws2, f"E{rr+2}", f"={refs['RETAINED']}*{refs['COST_ORIGIN']}", F_BOLD, None, RIGHT, USD0)
    refs["RETAINED_COST"] = f"'2. Labor Arbitrage'!$E${rr+2}"

    # ---- Sheet 3: Automation Benefits ----
    ws3 = wb.create_sheet("3. Automation")
    title_block(ws3, "Automation Benefits", "Ahorro adicional por RPA + AI, por proceso y por año", "H")
    ws3.column_dimensions["A"].width = 26
    ws3.column_dimensions["B"].width = 16
    for c in "CDEFGH":
        ws3.column_dimensions[c].width = 13
    hr = 4
    hdr3 = ["Proceso", "Base FTE-cost CR (USD)", "Autom. % objetivo"] + YEARS[1:]
    for i, h in enumerate(hdr3):
        style_cell(ws3, f"{get_column_letter(1+i)}{hr}", h, F_HDR, FILL_HDR, CTR)
    procs = [
        ("AP — Invoice Processing", 120000, 0.85),
        ("AP — Payment Run", 60000, 0.95),
        ("AR — Cash Application", 90000, 0.90),
        ("R2R — Journals estándar", 80000, 0.75),
        ("R2R — Reconciliaciones", 70000, 0.88),
        ("T&E — Procesamiento", 50000, 0.80),
        ("Reporting estándar", 60000, 0.90),
    ]
    first3 = hr + 1
    rr = first3
    for name, base, autom in procs:
        style_cell(ws3, f"A{rr}", name, F_NORM, None, LEFT)
        style_cell(ws3, f"B{rr}", base, F_BOLD, FILL_INPUT, RIGHT, USD0)
        style_cell(ws3, f"C{rr}", autom, F_BOLD, FILL_INPUT, CTR, PCT0)
        # ramp uses Assumptions ramp factors for Y1..Y5 (idx 1..5)
        for i in range(1, 6):
            col = get_column_letter(3 + i)  # D..H
            style_cell(ws3, f"{col}{rr}", f"=$B{rr}*$C{rr}*{refs['RAMP'][i]}",
                       F_NORM, None, RIGHT, USD0)
        rr += 1
    last3 = rr - 1
    style_cell(ws3, f"A{rr}", "TOTAL automatización", F_BOLD, FILL_LIGHT, LEFT)
    style_cell(ws3, f"B{rr}", "", F_BOLD, FILL_LIGHT)
    style_cell(ws3, f"C{rr}", "", F_BOLD, FILL_LIGHT)
    for i in range(1, 6):
        col = get_column_letter(3 + i)
        style_cell(ws3, f"{col}{rr}", f"=SUM({col}{first3}:{col}{last3})", F_BOLD, FILL_LIGHT, RIGHT, USD0)
    autom_total_row = rr
    refs["AUTOM_ROW"] = autom_total_row

    # ---- Sheet 4: One-Time Costs (CAPEX) ----
    ws4 = wb.create_sheet("4. One-Time Costs")
    title_block(ws4, "One-Time Costs (CAPEX)", "Inversión de implementación — desglose y fasaje", "E")
    ws4.column_dimensions["A"].width = 40
    for c in "BCD":
        ws4.column_dimensions[c].width = 16
    hr = 4
    for i, h in enumerate(["Categoría CAPEX", "Year 0", "Year 1", "Total"]):
        style_cell(ws4, f"{get_column_letter(1+i)}{hr}", h, F_HDR, FILL_HDR, CTR)
    capex = [
        ("Consultoría (Strategy + Design + Deliver)", 600000, 300000),
        ("Tecnología (infra + licencias año 1)", 350000, 150000),
        ("Instalaciones (setup inicial)", 300000, 100000),
        ("Recursos Humanos (reclutamiento + training)", 250000, 100000),
        ("Transición (paralelismo, KT, viajes)", 200000, 200000),
    ]
    first4 = hr + 1
    rr = first4
    for name, y0, y1 in capex:
        style_cell(ws4, f"A{rr}", name, F_NORM, None, LEFT)
        style_cell(ws4, f"B{rr}", y0, F_BOLD, FILL_INPUT, RIGHT, USD0)
        style_cell(ws4, f"C{rr}", y1, F_BOLD, FILL_INPUT, RIGHT, USD0)
        style_cell(ws4, f"D{rr}", f"=B{rr}+C{rr}", F_NORM, None, RIGHT, USD0)
        rr += 1
    last4 = rr - 1
    style_cell(ws4, f"A{rr}", "TOTAL CAPEX", F_BOLD, FILL_LIGHT, LEFT)
    for col in "BCD":
        style_cell(ws4, f"{col}{rr}", f"=SUM({col}{first4}:{col}{last4})", F_BOLD, FILL_LIGHT, RIGHT, USD0)
    capex_row = rr
    refs["CAPEX_Y0"] = f"'4. One-Time Costs'!$B${capex_row}"
    refs["CAPEX_Y1"] = f"'4. One-Time Costs'!$C${capex_row}"

    # ---- Sheet 5: Operating Costs (OPEX) ----
    ws5 = wb.create_sheet("5. Operating Costs")
    title_block(ws5, "Operating Costs (OPEX Run-Rate)", "Costo anual de operar el GBS — Year 1..5", "G")
    ws5.column_dimensions["A"].width = 30
    for c in "BCDEFG":
        ws5.column_dimensions[c].width = 14
    hr = 4
    style_cell(ws5, f"A{hr}", "Categoría OPEX", F_HDR, FILL_HDR, LEFT)
    for i in range(1, 6):
        style_cell(ws5, f"{get_column_letter(1+i)}{hr}", YEARS[i], F_HDR, FILL_HDR, CTR)
    first5 = hr + 1
    # Personal CR = (Labor CR cost + automation reduces? keep gross CR personnel) grows with inflation
    # Row: Personal CR
    rr = first5
    style_cell(ws5, f"A{rr}", "Personal CR (post-consolidación)", F_NORM, None, LEFT)
    for i in range(1, 6):
        col = get_column_letter(1 + i)
        # CR personnel cost base = total CR cost from labor sheet (sum of F), grown by inflation
        crbase = f"SUM('2. Labor Arbitrage'!$F${first}:$F${last})"
        style_cell(ws5, f"{col}{rr}", f"={crbase}*(1+{refs['INFL']})^{i-1}", F_NORM, None, RIGHT, USD0)
    personal_row = rr
    rr += 1
    # Defaults dimensionados para el centro CR del ejemplo (~17 FTEs tras
    # consolidar las funciones de la hoja 2). Escalar con el headcount real.
    opex_static = [
        ("Instalaciones CR (renta + servicios)", 180000),
        ("Tecnología (ERP + automatización + IT)", 200000),
        ("Overhead (auditoría, legal, compliance)", 70000),
    ]
    for name, base in opex_static:
        style_cell(ws5, f"A{rr}", name, F_NORM, None, LEFT)
        for i in range(1, 6):
            col = get_column_letter(1 + i)
            if i == 1:
                style_cell(ws5, f"{col}{rr}", base, F_BOLD, FILL_INPUT, RIGHT, USD0)
            else:
                prev = get_column_letter(1 + i - 1)
                style_cell(ws5, f"{col}{rr}", f"={prev}{rr}*(1+{refs['INFL']})", F_NORM, None, RIGHT, USD0)
        rr += 1
    # Management fee = % of subtotal above
    style_cell(ws5, f"A{rr}", "Management fee intercompany", F_NORM, None, LEFT)
    for i in range(1, 6):
        col = get_column_letter(1 + i)
        style_cell(ws5, f"{col}{rr}", f"=SUM({col}{first5}:{col}{rr-1})*{refs['MGMT_FEE']}", F_NORM, None, RIGHT, USD0)
    fee_row = rr
    rr += 1
    style_cell(ws5, f"A{rr}", "TOTAL OPEX", F_BOLD, FILL_LIGHT, LEFT)
    for i in range(1, 6):
        col = get_column_letter(1 + i)
        style_cell(ws5, f"{col}{rr}", f"=SUM({col}{first5}:{col}{fee_row})", F_BOLD, FILL_LIGHT, RIGHT, USD0)
    opex_total_row = rr
    refs["OPEX_ROW"] = opex_total_row
    style_cell(ws5, f"A{rr+2}",
               "Nota: defaults dimensionados para el centro CR del ejemplo (hoja 2). "
               "Escala instalaciones/tecnología con el headcount real del GBS.",
               F_NOTE, None, LEFT, border=False)
    ws5.merge_cells(f"A{rr+2}:G{rr+2}")

    # ---- Sheet 6: P&L Summary (3 scenarios) ----
    ws6 = wb.create_sheet("6. P&L Summary")
    title_block(ws6, "P&L Summary — Cashflow del proyecto", "Escenario base · ver multiplicadores en Assumptions", "G")
    ws6.column_dimensions["A"].width = 34
    for c in "BCDEFG":
        ws6.column_dimensions[c].width = 14
    hr = 4
    style_cell(ws6, f"A{hr}", "Concepto", F_HDR, FILL_HDR, LEFT)
    for i in range(0, 6):
        style_cell(ws6, f"{get_column_letter(2+i)}{hr}", YEARS[i], F_HDR, FILL_HDR, CTR)
    rr = hr + 1
    # Gross savings = (labor saving + automation by year) * save_mult, realized by ramp; Year0 = 0
    style_cell(ws6, f"A{rr}", "Ahorro bruto (labor + automatización)", F_NORM, None, LEFT)
    gross_row = rr
    for i in range(0, 6):
        col = get_column_letter(2 + i)
        if i == 0:
            style_cell(ws6, f"{col}{rr}", 0, F_NORM, None, RIGHT, USD0)
        else:
            acol = get_column_letter(3 + i)  # automation sheet D..H for Y1..Y5
            f = (f"=({refs['LABOR_SAVING']}*{refs['RAMP'][i]}"
                 f"+'3. Automation'!${acol}${refs['AUTOM_ROW']})*{refs['SAVE_MULT_BASE']}")
            style_cell(ws6, f"{col}{rr}", f, F_NORM, None, RIGHT, USD0)
    rr += 1
    # less OPEX incremental? OPEX is cost of running; savings already net of CR personnel via labor sheet.
    # We model net benefit = gross savings - retained extra - management fee proxy already in savings.
    # Keep it transparent: subtract management fee and facilities/tech delta as "GBS run costs not in labor".
    style_cell(ws6, f"A{rr}", "(-) Costos GBS no laborales (instal.+tech+fee)", F_NORM, None, LEFT)
    runcost_row = rr
    for i in range(0, 6):
        col = get_column_letter(2 + i)
        if i == 0:
            style_cell(ws6, f"{col}{rr}", 0, F_NORM, None, RIGHT, USD0)
        else:
            ocol = get_column_letter(1 + i)  # opex sheet B..F for Y1..Y5
            # non-labor opex = total opex - personal row
            f = (f"=-('5. Operating Costs'!${ocol}${refs['OPEX_ROW']}"
                 f"-'5. Operating Costs'!${ocol}${personal_row})")
            style_cell(ws6, f"{col}{rr}", f, F_NORM, None, RIGHT, USD0)
    rr += 1
    style_cell(ws6, f"A{rr}", "(-) CAPEX (one-time)", F_NORM, None, LEFT)
    capex_pl_row = rr
    for i in range(0, 6):
        col = get_column_letter(2 + i)
        if i == 0:
            style_cell(ws6, f"{col}{rr}", f"=-{refs['CAPEX_Y0']}*'1. Assumptions'!$C${scen_rows['Multiplicador de CAPEX']}",
                       F_NORM, None, RIGHT, USD0)
        elif i == 1:
            style_cell(ws6, f"{col}{rr}", f"=-{refs['CAPEX_Y1']}*'1. Assumptions'!$C${scen_rows['Multiplicador de CAPEX']}",
                       F_NORM, None, RIGHT, USD0)
        else:
            style_cell(ws6, f"{col}{rr}", 0, F_NORM, None, RIGHT, USD0)
    rr += 1
    style_cell(ws6, f"A{rr}", "FLUJO NETO ANUAL", F_BOLD, FILL_LIGHT, LEFT)
    net_row = rr
    for i in range(0, 6):
        col = get_column_letter(2 + i)
        style_cell(ws6, f"{col}{rr}", f"=SUM({col}{gross_row}:{col}{capex_pl_row})",
                   F_BOLD, FILL_LIGHT, RIGHT, USD0)
    rr += 1
    style_cell(ws6, f"A{rr}", "FLUJO ACUMULADO", F_BOLD, None, LEFT)
    cum_row = rr
    style_cell(ws6, f"B{rr}", f"=B{net_row}", F_BOLD, None, RIGHT, USD0)
    for i in range(1, 6):
        col = get_column_letter(2 + i)
        prev = get_column_letter(1 + i)
        style_cell(ws6, f"{col}{rr}", f"={prev}{rr}+{col}{net_row}", F_BOLD, None, RIGHT, USD0)
    rag_rules(ws6, f"B{net_row}:G{cum_row}")
    refs["NET_ROW"] = net_row
    refs["CUM_ROW"] = cum_row

    # ---- Sheet 7: Financial Metrics ----
    ws7 = wb.create_sheet("7. Financial Metrics")
    title_block(ws7, "Financial Metrics", "NPV · IRR · Payback · ROI (escenario base)", "D")
    ws7.column_dimensions["A"].width = 34
    ws7.column_dimensions["B"].width = 20
    nr = f"'6. P&L Summary'!$B${refs['NET_ROW']}:$G${refs['NET_ROW']}"
    flows_y1_5 = f"'6. P&L Summary'!$C${refs['NET_ROW']}:$G${refs['NET_ROW']}"
    y0 = f"'6. P&L Summary'!$B${refs['NET_ROW']}"
    metrics = [
        ("NPV (a WACC)", f"={y0}+NPV({refs['WACC']},{flows_y1_5})", USD0),
        ("IRR", f"=IFERROR(IRR({nr}),\"n/a\")", PCT),
        ("Ahorro neto acumulado 5 años", f"='6. P&L Summary'!$G${refs['CUM_ROW']}", USD0),
        ("Inversión total (CAPEX)", f"={refs['CAPEX_Y0']}+{refs['CAPEX_Y1']}", USD0),
        ("ROI 5 años", f"='6. P&L Summary'!$G${refs['CUM_ROW']}/({refs['CAPEX_Y0']}+{refs['CAPEX_Y1']})", PCT0),
        ("Payback (años, aprox.)",
         f"=IFERROR(MATCH(TRUE,INDEX('6. P&L Summary'!$B${refs['CUM_ROW']}:$G${refs['CUM_ROW']}>=0,0),0)-1,\"> 5\")",
         '0.0'),
    ]
    rr = 4
    for label, formula, fmt in metrics:
        style_cell(ws7, f"A{rr}", label, F_BOLD, FILL_LIGHT, LEFT)
        style_cell(ws7, f"B{rr}", formula, F_BOLD, None, CTR, fmt)
        rr += 1
    style_cell(ws7, f"A{rr+1}", "Nota: Payback usa el primer año con flujo acumulado ≥ 0.",
               F_NOTE, None, LEFT, border=False)

    # ---- Sheet 8: Sensitivity ----
    ws8 = wb.create_sheet("8. Sensitivity")
    title_block(ws8, "Sensitivity Analysis", "Impacto de variables clave sobre el NPV (referencia direccional)", "D")
    ws8.column_dimensions["A"].width = 34
    for c in "BCD":
        ws8.column_dimensions[c].width = 18
    hr = 4
    for i, h in enumerate(["Variable", "Cambio", "Dirección impacto NPV"]):
        style_cell(ws8, f"{get_column_letter(1+i)}{hr}", h, F_HDR, FILL_HDR, CTR)
    sens = [
        ("Ratio de consolidación FTE", "+0.5x", "▲ Alto positivo"),
        ("Salarios CR", "+10%", "▼ Negativo"),
        ("Automatización", "+10 pts", "▲ Positivo"),
        ("CAPEX implementación", "+20%", "▼ Negativo"),
        ("Tipo de cambio USD/CRC", "±5%", "↕ Bajo"),
        ("Velocidad de ramp-up", "-3 meses", "▲ Positivo"),
    ]
    rr = hr + 1
    for v, ch, imp in sens:
        style_cell(ws8, f"A{rr}", v, F_NORM, None, LEFT)
        style_cell(ws8, f"B{rr}", ch, F_BOLD, FILL_INPUT, CTR)
        style_cell(ws8, f"C{rr}", imp, F_NORM, None, CTR)
        rr += 1
    style_cell(ws8, f"A{rr+1}",
               "Para sensibilidad cuantitativa: variar el multiplicador de ahorro/CAPEX en la hoja Assumptions y observar NPV en la hoja 7.",
               F_NOTE, None, LEFT, border=False)
    ws8.merge_cells(f"A{rr+1}:D{rr+1}")

    # ---- Sheet 9: Executive Dashboard ----
    ws9 = wb.create_sheet("9. Exec Dashboard")
    title_block(ws9, "Executive Dashboard", "Resumen para presentación a Junta Directiva", "H")
    ws9.column_dimensions["A"].width = 28
    for c in "BCDEFGH":
        ws9.column_dimensions[c].width = 13
    # KPI cards
    cards = [
        ("NPV", f"='7. Financial Metrics'!$B$4", USD0),
        ("IRR", f"='7. Financial Metrics'!$B$5", PCT),
        ("Payback (años)", f"='7. Financial Metrics'!$B$9", '0.0'),
        ("ROI 5 años", f"='7. Financial Metrics'!$B$8", PCT0),
    ]
    cr = 4
    col_i = 1
    for label, f, fmt in cards:
        c1 = get_column_letter(col_i)
        c2 = get_column_letter(col_i + 1)
        ws9.merge_cells(f"{c1}{cr}:{c2}{cr}")
        style_cell(ws9, f"{c1}{cr}", label, F_HDR, FILL_HDR, CTR)
        ws9.merge_cells(f"{c1}{cr+1}:{c2}{cr+1}")
        style_cell(ws9, f"{c1}{cr+1}", f, Font(size=14, bold=True, color=NAVY), FILL_LIGHT, CTR, fmt)
        col_i += 2
    # data block for chart: cumulative cashflow
    dr = cr + 4
    style_cell(ws9, f"A{dr}", "Flujo acumulado", F_BOLD, FILL_GREY, LEFT)
    for i in range(0, 6):
        style_cell(ws9, f"{get_column_letter(2+i)}{dr}", YEARS[i], F_NOTE, FILL_GREY, CTR)
    style_cell(ws9, f"A{dr+1}", "USD", F_NORM, None, LEFT)
    for i in range(0, 6):
        col = get_column_letter(2 + i)
        style_cell(ws9, f"{col}{dr+1}", f"='6. P&L Summary'!{col}{refs['CUM_ROW']}", F_NORM, None, RIGHT, USD0)
    # line chart
    chart = LineChart()
    chart.title = "Flujo de caja acumulado (5 años)"
    chart.height = 8
    chart.width = 18
    data = Reference(ws9, min_col=2, max_col=7, min_row=dr + 1, max_row=dr + 1)
    cats = Reference(ws9, min_col=2, max_col=7, min_row=dr, max_row=dr)
    chart.add_data(data, titles_from_data=False)
    chart.set_categories(cats)
    chart.legend = None
    ws9.add_chart(chart, f"A{dr+3}")

    # net flow bar chart data
    nr2 = dr + 14
    style_cell(ws9, f"A{nr2}", "Flujo neto anual", F_BOLD, FILL_GREY, LEFT)
    for i in range(0, 6):
        style_cell(ws9, f"{get_column_letter(2+i)}{nr2}", YEARS[i], F_NOTE, FILL_GREY, CTR)
    style_cell(ws9, f"A{nr2+1}", "USD", F_NORM, None, LEFT)
    for i in range(0, 6):
        col = get_column_letter(2 + i)
        style_cell(ws9, f"{col}{nr2+1}", f"='6. P&L Summary'!{col}{refs['NET_ROW']}", F_NORM, None, RIGHT, USD0)
    bar = BarChart()
    bar.title = "Flujo neto por año"
    bar.height = 8
    bar.width = 18
    bdata = Reference(ws9, min_col=2, max_col=7, min_row=nr2 + 1, max_row=nr2 + 1)
    bcats = Reference(ws9, min_col=2, max_col=7, min_row=nr2, max_row=nr2)
    bar.add_data(bdata, titles_from_data=False)
    bar.set_categories(bcats)
    bar.legend = None
    ws9.add_chart(bar, f"A{nr2+3}")

    # freeze headers on data sheets
    for s in wb.worksheets:
        s.sheet_view.showGridLines = False

    out = OUT_DIR / "SSC_Business_Case_Template.xlsx"
    wb.save(out)
    return out


# =========================================================================== #
# KPI DASHBOARD WORKBOOK
# =========================================================================== #
def kpi_header(ws, cols_widths):
    for col, w in cols_widths.items():
        ws.column_dimensions[col].width = w


def kpi_table(ws, start_row, headers, rows, rag_col=None, target_col=None,
              direction="higher"):
    """Generic KPI table. rows = list of tuples matching headers."""
    hr = start_row
    for i, h in enumerate(headers):
        style_cell(ws, f"{get_column_letter(1+i)}{hr}", h, F_HDR, FILL_HDR, CTR)
    rr = hr + 1
    for row in rows:
        for i, val in enumerate(row):
            col = get_column_letter(1 + i)
            is_input = (i >= 1 and not (isinstance(val, str) and val.startswith("=")))
            fill = FILL_INPUT if is_input else None
            align = LEFT if i == 0 else CTR
            font = F_NORM if i == 0 else F_BOLD
            style_cell(ws, f"{col}{rr}", val, font, fill, align)
        rr += 1
    return hr, rr - 1


def build_kpi_dashboard():
    wb = Workbook()

    # ---- Sheet 1: Monthly Input ----
    ws = wb.active
    ws.title = "1. Monthly Input"
    title_block(ws, "SSC / GBS — KPI Dashboard",
                "Ingresa las métricas del mes (celdas amarillas). Las hojas de KPIs leen de aquí.", "E")
    kpi_header(ws, {"A": 40, "B": 16, "C": 16, "D": 16, "E": 16})
    style_cell(ws, "A4", "Métrica", F_HDR, FILL_HDR, LEFT)
    for i, m in enumerate(["Mes actual", "Mes anterior", "Meta", "Best practice"]):
        style_cell(ws, f"{get_column_letter(2+i)}4", m, F_HDR, FILL_HDR, CTR)
    inputs = [
        # (label, current, prev, target, benchmark)
        ("P2P — Facturas procesadas (#)", 12000, 11800, 13000, 15000),
        ("P2P — Touchless invoice rate (%)", 0.62, 0.58, 0.75, 0.85),
        ("P2P — Costo por factura (USD)", 4.5, 4.8, 3.5, 2.5),
        ("P2P — % pagos a tiempo", 0.96, 0.95, 0.98, 0.99),
        ("O2C — DSO (días)", 52, 55, 45, 40),
        ("O2C — Cash application automática (%)", 0.80, 0.76, 0.90, 0.95),
        ("O2C — Collections effectiveness (%)", 0.88, 0.86, 0.92, 0.95),
        ("R2R — Días de cierre mensual", 6, 7, 5, 4),
        ("R2R — Reconciliaciones a tiempo (%)", 0.90, 0.88, 0.95, 0.98),
        ("R2R — Journals automatizados (%)", 0.55, 0.50, 0.70, 0.80),
        ("Servicio — CSAT (1-5)", 4.1, 4.0, 4.3, 4.6),
        ("Servicio — NPS", 35, 32, 45, 60),
        ("Servicio — SLA compliance (%)", 0.94, 0.93, 0.97, 0.99),
        ("People — Rotación anualizada (%)", 0.18, 0.20, 0.15, 0.10),
        ("People — Engagement (%)", 0.74, 0.72, 0.80, 0.85),
        ("People — Headcount (FTE)", 180, 178, 185, 200),
    ]
    first = 5
    rr = first
    label_to_row = {}
    for label, cur, prev, tgt, bm in inputs:
        style_cell(ws, f"A{rr}", label, F_NORM, None, LEFT)
        style_cell(ws, f"B{rr}", cur, F_BOLD, FILL_INPUT, CTR)
        style_cell(ws, f"C{rr}", prev, F_BOLD, FILL_INPUT, CTR)
        style_cell(ws, f"D{rr}", tgt, F_BOLD, FILL_INPUT, CTR)
        style_cell(ws, f"E{rr}", bm, F_BOLD, FILL_INPUT, CTR)
        label_to_row[label] = rr
        rr += 1
    MI = "'1. Monthly Input'"

    def link(area_rows, names):
        return [(n, f"={MI}!$B${label_to_row[n]}", f"={MI}!$C${label_to_row[n]}",
                 f"={MI}!$D${label_to_row[n]}", f"={MI}!$E${label_to_row[n]}") for n in names]

    # helper to build a KPI sheet that references Monthly Input + RAG vs target
    def kpi_sheet(name, title, sub, metric_names, higher_better):
        wsx = wb.create_sheet(name)
        title_block(wsx, title, sub, "F")
        kpi_header(wsx, {"A": 40, "B": 14, "C": 14, "D": 14, "E": 14, "F": 16})
        style_cell(wsx, "A4", "KPI", F_HDR, FILL_HDR, LEFT)
        for i, h in enumerate(["Actual", "Anterior", "Meta", "Best pract.", "Status"]):
            style_cell(wsx, f"{get_column_letter(2+i)}4", h, F_HDR, FILL_HDR, CTR)
        rr = 5
        for nm in metric_names:
            src = label_to_row[nm]
            style_cell(wsx, f"A{rr}", nm, F_NORM, None, LEFT)
            style_cell(wsx, f"B{rr}", f"={MI}!$B${src}", F_BOLD, None, CTR)
            style_cell(wsx, f"C{rr}", f"={MI}!$C${src}", F_NORM, None, CTR)
            style_cell(wsx, f"D{rr}", f"={MI}!$D${src}", F_NORM, None, CTR)
            style_cell(wsx, f"E{rr}", f"={MI}!$E${src}", F_NORM, None, CTR)
            hb = nm in higher_better
            if hb:
                f = (f'=IF(B{rr}>=D{rr},"🟢 Logrado",'
                     f'IF(B{rr}>=D{rr}*0.9,"🟡 En riesgo","🔴 No logrado"))')
            else:
                f = (f'=IF(B{rr}<=D{rr},"🟢 Logrado",'
                     f'IF(B{rr}<=D{rr}*1.1,"🟡 En riesgo","🔴 No logrado"))')
            style_cell(wsx, f"F{rr}", f, F_BOLD, None, CTR)
            rr += 1
        # RAG conditional formatting on status text (FormulaRule + SEARCH)
        rng = f"F5:F{rr-1}"
        wsx.conditional_formatting.add(rng, FormulaRule(
            formula=[f'ISNUMBER(SEARCH("Logrado",F5))'],
            fill=PatternFill("solid", fgColor=GREEN), font=Font(color=GREEN_T)))
        wsx.conditional_formatting.add(rng, FormulaRule(
            formula=[f'ISNUMBER(SEARCH("riesgo",F5))'],
            fill=PatternFill("solid", fgColor=AMBER), font=Font(color=AMBER_T)))
        wsx.conditional_formatting.add(rng, FormulaRule(
            formula=[f'ISNUMBER(SEARCH("No logrado",F5))'],
            fill=PatternFill("solid", fgColor=RED), font=Font(color=RED_T)))
        wsx.sheet_view.showGridLines = False
        return wsx

    p2p = ["P2P — Facturas procesadas (#)", "P2P — Touchless invoice rate (%)",
           "P2P — Costo por factura (USD)", "P2P — % pagos a tiempo"]
    o2c = ["O2C — DSO (días)", "O2C — Cash application automática (%)",
           "O2C — Collections effectiveness (%)"]
    r2r = ["R2R — Días de cierre mensual", "R2R — Reconciliaciones a tiempo (%)",
           "R2R — Journals automatizados (%)"]
    svc = ["Servicio — CSAT (1-5)", "Servicio — NPS", "Servicio — SLA compliance (%)"]
    ppl = ["People — Rotación anualizada (%)", "People — Engagement (%)", "People — Headcount (FTE)"]

    higher_better = {
        "P2P — Facturas procesadas (#)", "P2P — Touchless invoice rate (%)", "P2P — % pagos a tiempo",
        "O2C — Cash application automática (%)", "O2C — Collections effectiveness (%)",
        "R2R — Reconciliaciones a tiempo (%)", "R2R — Journals automatizados (%)",
        "Servicio — CSAT (1-5)", "Servicio — NPS", "Servicio — SLA compliance (%)",
        "People — Engagement (%)", "People — Headcount (FTE)",
    }
    # lower better: cost/invoice, DSO, close days, rotation

    kpi_sheet("2. P2P KPIs", "P2P KPIs", "Procure-to-Pay / Accounts Payable", p2p, higher_better)
    kpi_sheet("3. O2C KPIs", "O2C KPIs", "Order-to-Cash / Accounts Receivable", o2c, higher_better)
    kpi_sheet("4. R2R KPIs", "R2R KPIs", "Record-to-Report / General Ledger", r2r, higher_better)
    kpi_sheet("5. Service KPIs", "Service KPIs", "Satisfacción y cumplimiento de servicio", svc, higher_better)
    kpi_sheet("6. People KPIs", "People KPIs", "Talento y organización del GBS", ppl, higher_better)

    # ---- Sheet 7: Executive Dashboard ----
    ws7 = wb.create_sheet("7. Exec Dashboard")
    title_block(ws7, "Executive Dashboard", "RAG status + tendencia para el Comité de Operaciones", "G")
    kpi_header(ws7, {"A": 36, "B": 14, "C": 14, "D": 14, "E": 14, "F": 14, "G": 14})
    # Summary RAG block: pull headline KPIs
    headline = [
        ("Touchless invoice rate (%)", "P2P — Touchless invoice rate (%)", True),
        ("DSO (días)", "O2C — DSO (días)", False),
        ("Días de cierre", "R2R — Días de cierre mensual", False),
        ("SLA compliance (%)", "Servicio — SLA compliance (%)", True),
        ("CSAT", "Servicio — CSAT (1-5)", True),
        ("Rotación (%)", "People — Rotación anualizada (%)", False),
    ]
    style_cell(ws7, "A4", "KPI clave", F_HDR, FILL_HDR, LEFT)
    for i, h in enumerate(["Actual", "Meta", "Status"]):
        style_cell(ws7, f"{get_column_letter(2+i)}4", h, F_HDR, FILL_HDR, CTR)
    rr = 5
    for disp, nm, hb in headline:
        src = label_to_row[nm]
        style_cell(ws7, f"A{rr}", disp, F_NORM, None, LEFT)
        style_cell(ws7, f"B{rr}", f"={MI}!$B${src}", F_BOLD, None, CTR)
        style_cell(ws7, f"C{rr}", f"={MI}!$D${src}", F_NORM, None, CTR)
        if hb:
            f = (f'=IF(B{rr}>=C{rr},"🟢",IF(B{rr}>=C{rr}*0.9,"🟡","🔴"))')
        else:
            f = (f'=IF(B{rr}<=C{rr},"🟢",IF(B{rr}<=C{rr}*1.1,"🟡","🔴"))')
        style_cell(ws7, f"D{rr}", f, F_BOLD, None, CTR)
        rr += 1

    # Trend data (illustrative 6-month series, editable)
    tr = rr + 2
    style_cell(ws7, f"A{tr}", "Tendencia (editable) — Touchless rate %", F_BOLD, FILL_GREY, LEFT)
    months = ["M-5", "M-4", "M-3", "M-2", "M-1", "Actual"]
    for i, m in enumerate(months):
        style_cell(ws7, f"{get_column_letter(2+i)}{tr}", m, F_NOTE, FILL_GREY, CTR)
    style_cell(ws7, f"A{tr+1}", "Touchless %", F_NORM, None, LEFT)
    series = [0.52, 0.55, 0.57, 0.58, 0.60, None]
    for i, v in enumerate(series):
        col = get_column_letter(2 + i)
        if v is None:
            style_cell(ws7, f"{col}{tr+1}", f"={MI}!$B${label_to_row['P2P — Touchless invoice rate (%)']}",
                       F_BOLD, None, CTR, PCT0)
        else:
            style_cell(ws7, f"{col}{tr+1}", v, F_BOLD, FILL_INPUT, CTR, PCT0)
    chart = LineChart()
    chart.title = "Touchless invoice rate — tendencia"
    chart.height = 7.5
    chart.width = 16
    data = Reference(ws7, min_col=2, max_col=7, min_row=tr + 1, max_row=tr + 1)
    cats = Reference(ws7, min_col=2, max_col=7, min_row=tr, max_row=tr)
    chart.add_data(data, titles_from_data=False)
    chart.set_categories(cats)
    chart.legend = None
    ws7.add_chart(chart, f"A{tr+3}")
    ws7.sheet_view.showGridLines = False

    # ---- Sheet 8: Benchmark Comparison ----
    ws8 = wb.create_sheet("8. Benchmark")
    title_block(ws8, "Benchmark Comparison", "Actual vs. best practice (Hackett / APQC referencial)", "E")
    kpi_header(ws8, {"A": 40, "B": 14, "C": 16, "D": 14, "E": 18})
    style_cell(ws8, "A4", "KPI", F_HDR, FILL_HDR, LEFT)
    for i, h in enumerate(["Actual", "Best practice", "Gap", "% del benchmark"]):
        style_cell(ws8, f"{get_column_letter(2+i)}4", h, F_HDR, FILL_HDR, CTR)
    rr = 5
    for label in [r[0] for r in inputs]:
        src = label_to_row[label]
        style_cell(ws8, f"A{rr}", label, F_NORM, None, LEFT)
        style_cell(ws8, f"B{rr}", f"={MI}!$B${src}", F_BOLD, None, CTR)
        style_cell(ws8, f"C{rr}", f"={MI}!$E${src}", F_NORM, None, CTR)
        style_cell(ws8, f"D{rr}", f"=B{rr}-C{rr}", F_NORM, None, CTR)
        style_cell(ws8, f"E{rr}", f"=IFERROR(B{rr}/C{rr},\"n/a\")", F_BOLD, None, CTR, PCT0)
        rr += 1
    ws8.sheet_view.showGridLines = False

    for s in wb.worksheets:
        s.sheet_view.showGridLines = False

    out = OUT_DIR / "SSC_KPI_Dashboard_Template.xlsx"
    wb.save(out)
    return out


if __name__ == "__main__":
    bc = build_business_case()
    print("Creado:", bc)
    kpi = build_kpi_dashboard()
    print("Creado:", kpi)
