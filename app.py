from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request, Form, Response
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import uvicorn
import json
import io
from datetime import datetime
from fpdf import FPDF

# Importar la lógica existente
from programacion_dinamica import ProgramacionDinamica
from optimizacion_nolineal import OptimizacionNoLineal
from integracion_ia import IntegracionIA
from linea_espera import LineaEspera

app = FastAPI(title="Calculadora Estratégica Pro")
templates = Jinja2Templates(directory="templates")

# Ejemplos (Casos de Estudio)
EJEMPLO_SERVIDORES = [
    {"nombre": "Autenticación", "peso": 3, "valor": 5},
    {"nombre": "Matchmaking", "peso": 4, "valor": 7},
    {"nombre": "Sincronización", "peso": 7, "valor": 11},
    {"nombre": "Caché", "peso": 5, "valor": 8}
]

EJEMPLOS_COLA = [
    {"nombre": "Revisión de Motores (M/M/1)", "descripcion": "Base de mantenimiento, 1 motor revisado a la vez", "modelo": "MM1", "lam": 1.0, "mu": 2.0, "s": 1, "K": 10, "unidad": "motor/día"},
    {"nombre": "Inspección PCB (M/D/1)", "descripcion": "Estación AOI con tiempo de inspección constante de 5 min", "modelo": "MD1", "lam": 10.0, "mu": 12.0, "s": 1, "K": 10, "unidad": "tarjeta/hora"},
    {"nombre": "Cola RabbitMQ (M/M/s)", "descripcion": "Sistema de pagos con 4 workers, 30 msg/min", "modelo": "MMs", "lam": 30.0, "mu": 11.0, "s": 4, "K": 10, "unidad": "mensaje/min"},
    {"nombre": "Caja con Límite de Espacio (M/M/1/K)", "descripcion": "Supermercado con capacidad máxima de 8 clientes", "modelo": "MM1K", "lam": 5.0, "mu": 6.0, "s": 1, "K": 8, "unidad": "cliente/hora"},
]

EJEMPLO_GRAFO = {
    'A': {'B': 4, 'C': 6, 'D': 3},
    'B': {'E': 7, 'F': 5},
    'C': {'E': 3, 'F': 8, 'G': 4},
    'D': {'F': 6, 'G': 9},
    'E': {'H': 5, 'I': 6},
    'F': {'H': 3, 'I': 5},
    'G': {'H': 8, 'I': 2},
    'H': {'J': 4},
    'I': {'J': 7}
}

# ── PDF color palette ──────────────────────────────────────────────────────
_NAVY  = (15,  45,  85)
_BLUE  = (41, 128, 185)
_LBLUE = (232, 243, 251)
_LGREY = (245, 247, 249)
_MGREY = (108, 117, 125)
_DARK  = (30,  40,  50)
_WHITE = (255, 255, 255)
_GREEN = (39,  174,  96)
_GOLD  = (180, 120,   0)

_UNICODE_FONT_PATHS = [
    "/Library/Fonts/Arial Unicode.ttf",              # macOS
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
    "/Windows/Fonts/arial.ttf",                      # Windows
]

class PDF(FPDF):
    doc_tipo = ""

    def __init__(self):
        super().__init__()
        self._ufont = "helvetica"
        for path in _UNICODE_FONT_PATHS:
            if os.path.exists(path):
                self.add_font("_uni", fname=path)
                self._ufont = "_uni"
                break

    # ── Page chrome ──────────────────────────────────────────────────────────

    def header(self):
        # Navy banner
        self.set_fill_color(*_NAVY)
        self.rect(0, 0, 210, 26, "F")
        # Blue accent stripe
        self.set_fill_color(*_BLUE)
        self.rect(0, 22, 210, 4, "F")
        # Title
        self.set_xy(12, 4)
        self.set_font("helvetica", "B", 15)
        self.set_text_color(*_WHITE)
        self.cell(118, 14, "Calculadora Estrategica Pro", border=0)
        # Document-type badge
        if self.doc_tipo:
            self.set_xy(132, 5)
            self.set_fill_color(*_BLUE)
            self.set_font("helvetica", "B", 7.5)
            self.cell(66, 16, self.doc_tipo.upper(), border=0, fill=True, align="C")
        # Meta strip
        self.set_fill_color(*_LGREY)
        self.rect(0, 26, 210, 8, "F")
        self.set_xy(12, 27.5)
        self.set_font("helvetica", "", 7)
        self.set_text_color(*_MGREY)
        fecha = datetime.now().strftime("%d/%m/%Y  %H:%M hrs")
        self.cell(95, 5, f"Generado: {fecha}")
        self.cell(91, 5, "Documento Confidencial  -  Solo uso interno", align="R")
        self.set_text_color(*_DARK)
        self.set_y(40)

    def footer(self):
        self.set_y(-13)
        self.set_fill_color(*_NAVY)
        self.rect(0, self.get_y(), 210, 18, "F")
        self.set_font("helvetica", "I", 7.5)
        self.set_text_color(160, 195, 225)
        self.cell(
            0, 10,
            f"Calculadora Estrategica Pro   |   Pagina {self.page_no()}"
            "   |   Generado automaticamente   |   Confidencial",
            align="C",
        )
        self.set_text_color(*_DARK)

    # ── Reusable building blocks ──────────────────────────────────────────────

    def _section(self, title):
        self.ln(5)
        y = self.get_y()
        self.set_fill_color(*_BLUE)
        self.rect(10, y, 4, 8, "F")
        self.set_fill_color(*_LBLUE)
        self.rect(14, y, 186, 8, "F")
        self.set_xy(19, y + 0.5)
        self.set_font("helvetica", "B", 9.5)
        self.set_text_color(*_NAVY)
        t = title.encode("latin-1", "replace").decode("latin-1")
        self.cell(180, 7, t)
        self.set_text_color(*_DARK)
        self.set_y(y + 11)

    def _kpi(self, x, y, w, label, value, color=None):
        c = color or _BLUE
        self.set_fill_color(*_LGREY)
        self.set_draw_color(*c)
        self.rect(x, y, w, 22, "FD")
        self.set_fill_color(*c)
        self.rect(x, y, w, 3, "F")
        self.set_xy(x + 2, y + 4)
        self.set_font("helvetica", "", 7)
        self.set_text_color(*_MGREY)
        lbl = str(label).encode("latin-1", "replace").decode("latin-1")
        self.cell(w - 4, 5, lbl, align="C")
        self.set_xy(x + 2, y + 10)
        r, g, b = c
        self.set_text_color(r, g, b)
        self.set_font("helvetica", "B", 12)
        val = str(value).encode("latin-1", "replace").decode("latin-1")
        self.cell(w - 4, 8, val, align="C")
        self.set_text_color(*_DARK)

    def _result_banner(self, label, value, subtitle="", color=None):
        c = color or _NAVY
        y = self.get_y()
        self.set_fill_color(*c)
        self.rect(10, y, 190, 24, "F")
        r, g, b = c
        self.set_fill_color(min(255, r + 25), min(255, g + 35), min(255, b + 55))
        self.rect(155, y, 45, 24, "F")
        # Label
        self.set_xy(16, y + 3)
        self.set_font("helvetica", "", 8)
        self.set_text_color(170, 205, 235)
        lbl = label.encode("latin-1", "replace").decode("latin-1")
        self.cell(130, 5, lbl)
        # Value
        self.set_xy(16, y + 9)
        self.set_font("helvetica", "B", 16)
        self.set_text_color(*_WHITE)
        val = str(value).encode("latin-1", "replace").decode("latin-1")
        self.cell(130, 10, val)
        # Subtitle
        if subtitle:
            self.set_xy(16, y + 19)
            self.set_font("helvetica", "", 7.5)
            self.set_text_color(170, 205, 235)
            sub = subtitle.encode("latin-1", "replace").decode("latin-1")
            self.cell(130, 4, sub)
        self.set_text_color(*_DARK)
        self.set_y(y + 27)

    def _table(self, headers, rows, widths=None):
        if not rows:
            return
        n = len(headers)
        if widths is None:
            widths = [190 // n] * n
        self.set_fill_color(*_NAVY)
        self.set_text_color(*_WHITE)
        self.set_draw_color(190, 200, 215)
        self.set_font("helvetica", "B", 8.5)
        for h, w in zip(headers, widths):
            hh = str(h).encode("latin-1", "replace").decode("latin-1")
            self.cell(w, 7, hh, border=1, fill=True, align="C")
        self.ln()
        self.set_font("helvetica", "", 8.5)
        for i, row in enumerate(rows):
            self.set_fill_color(*(_LGREY if i % 2 == 0 else _WHITE))
            self.set_text_color(*_DARK)
            for j, (val, w) in enumerate(zip(row, widths)):
                v = str(val).encode("latin-1", "replace").decode("latin-1")
                self.cell(w, 6, v, border=1, fill=True, align="L" if j == 0 else "C")
            self.ln()
        self.set_draw_color(0, 0, 0)
        self.ln(3)

    def _ai_block(self, text):
        self._section("Analisis del CTO (Inteligencia Artificial)")
        self.set_font("helvetica", "B", 28)
        self.set_text_color(195, 215, 235)
        self.set_xy(10, self.get_y() - 1)
        self.cell(10, 10, '"')
        self.set_xy(20, self.get_y())
        self.set_font(self._ufont, size=9)
        self.set_text_color(*_DARK)
        self.set_fill_color(*_LBLUE)
        self.multi_cell(180, 5.5, text, fill=True, align="J")
        self.ln(3)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

@app.get("/servidores", response_class=HTMLResponse)
async def get_servidores(request: Request):
    return templates.TemplateResponse(request, "servidores.html", {
        "ejemplo_servidores": json.dumps(EJEMPLO_SERVIDORES),
        "capacidad_default": 16
    })

@app.post("/servidores", response_class=HTMLResponse)
async def post_servidores(request: Request, capacidad: int = Form(...), servicios_json: str = Form(...)):
    servicios_raw = json.loads(servicios_json)
    # Convertir a formato esperado por la lógica: list of (nombre, peso, valor)
    microservicios = [(s['nombre'], int(s['peso']), int(s['valor'])) for s in servicios_raw]
    
    valor_optimo, seleccion = ProgramacionDinamica.optimizar_servidores(capacidad, microservicios)
    
    return templates.TemplateResponse(request, "servidores.html", {
        "resultado": {"valor": valor_optimo, "seleccion": seleccion},
        "ejemplo_servidores": servicios_json,
        "capacidad_default": capacidad,
        "raw_data": json.dumps({"capacidad": capacidad, "servicios": servicios_raw})
    })

@app.get("/ruta", response_class=HTMLResponse)
async def get_ruta(request: Request):
    return templates.TemplateResponse(request, "ruta.html", {
        "grafo_default": json.dumps(EJEMPLO_GRAFO, indent=2),
        "inicio_default": "A",
        "fin_default": "J"
    })

@app.post("/ruta", response_class=HTMLResponse)
async def post_ruta(request: Request, grafo_json: str = Form(...), inicio: str = Form(...), fin: str = Form(...)):
    grafo = json.loads(grafo_json)
    latencia, ruta = ProgramacionDinamica.ruta_minima_backward(grafo, inicio, fin)
    
    return templates.TemplateResponse(request, "ruta.html", {
        "resultado": {"latencia": latencia, "ruta": " -> ".join(ruta)},
        "grafo_default": grafo_json,
        "inicio_default": inicio,
        "fin_default": fin,
        "raw_data": json.dumps({"inicio": inicio, "fin": fin, "grafo": grafo})
    })

@app.get("/marketing", response_class=HTMLResponse)
async def get_marketing(request: Request):
    return templates.TemplateResponse(request, "marketing.html", {
        "presupuesto_default": 10,
        "a1_default": 4.0, "a2_default": 5.0,
        "b1_default": 0.2, "b2_default": 0.3,
    })

@app.post("/marketing", response_class=HTMLResponse)
async def post_marketing(
    request: Request,
    presupuesto: float = Form(...),
    a1: float = Form(4.0), a2: float = Form(5.0),
    b1: float = Form(0.2), b2: float = Form(0.3),
):
    roi, x1, x2 = OptimizacionNoLineal.maximizar_marketing(presupuesto, a1, a2, b1, b2)

    return templates.TemplateResponse(request, "marketing.html", {
        "resultado": {"roi": roi, "creadores": x1, "anuncios": x2},
        "a1_default": a1, "a2_default": a2,
        "b1_default": b1, "b2_default": b2,
        "presupuesto_default": presupuesto,
        "raw_data": json.dumps({"presupuesto": presupuesto})
    })

@app.get("/linea-espera", response_class=HTMLResponse)
async def get_linea_espera(request: Request):
    return templates.TemplateResponse(request, "linea_espera.html", {
        "ejemplos": EJEMPLOS_COLA,
        "resultado": None,
        "error": None,
        "modelo_sel": "MM1",
        "lam_val": "",
        "mu_val": "",
        "s_val": 2,
        "K_val": 10,
        "unidad_val": ""
    })

@app.post("/linea-espera", response_class=HTMLResponse)
async def post_linea_espera(
    request: Request,
    modelo: str = Form(...),
    lam: float = Form(...),
    mu: float = Form(...),
    s: int = Form(1),
    K: int = Form(10),
    unidad: str = Form("unidad")
):
    resultado = None
    error = None
    try:
        if modelo == "MM1":
            resultado = LineaEspera.modelo_mm1(lam, mu)
        elif modelo == "MMs":
            resultado = LineaEspera.modelo_mms(lam, mu, s)
        elif modelo == "MD1":
            resultado = LineaEspera.modelo_md1(lam, mu)
        elif modelo == "MM1K":
            resultado = LineaEspera.modelo_mm1k(lam, mu, K)
        else:
            error = f"Modelo desconocido: {modelo}"
    except ValueError as e:
        error = str(e)
    except Exception as e:
        error = f"Error inesperado: {str(e)}"

    return templates.TemplateResponse(request, "linea_espera.html", {
        "ejemplos": EJEMPLOS_COLA,
        "resultado": resultado,
        "error": error,
        "modelo_sel": modelo,
        "lam_val": lam,
        "mu_val": mu,
        "s_val": s,
        "K_val": K,
        "unidad_val": unidad
    })

def _html_ia(texto: str) -> str:
    safe = texto.replace("'", "&#39;").replace('"', "&quot;")
    return f"<div class='alert alert-info' id='ia-text-content'>{texto}</div><input type='hidden' id='ia-analisis-input' value='{safe}'>"

@app.post("/analizar-ia-servidores", response_class=HTMLResponse)
async def analizar_ia_servidores(request: Request, data: str = Form(...)):
    return HTMLResponse(_html_ia(IntegracionIA().analizar_servidores(json.loads(data))))

@app.post("/analizar-ia-ruta", response_class=HTMLResponse)
async def analizar_ia_ruta(request: Request, data: str = Form(...)):
    return HTMLResponse(_html_ia(IntegracionIA().analizar_ruta(json.loads(data))))

@app.post("/analizar-ia-marketing", response_class=HTMLResponse)
async def analizar_ia_marketing(request: Request, data: str = Form(...)):
    return HTMLResponse(_html_ia(IntegracionIA().analizar_marketing(json.loads(data))))

@app.post("/analizar-ia-cola", response_class=HTMLResponse)
async def analizar_ia_cola(request: Request, data: str = Form(...)):
    d  = json.loads(data)
    ia = IntegracionIA()
    mid = d.get("modelo_id", "")
    if mid == "MM1":
        texto = ia.analizar_mm1(d)
    elif mid == "MMs":
        texto = ia.analizar_mms(d)
    elif mid == "MD1":
        texto = ia.analizar_md1(d)
    elif mid == "MM1K":
        texto = ia.analizar_mm1k(d)
    else:
        texto = "⚠️ Modelo no reconocido."
    return HTMLResponse(_html_ia(texto))

@app.post("/descargar-pdf")
async def descargar_pdf(
    tipo: str = Form(...),
    datos: str = Form(...),
    resultado: str = Form(...),
    ia_analisis: str = Form(...)
):
    def _pick(lines, *keywords):
        for line in lines:
            for kw in keywords:
                if kw.lower() in line.lower() and "=" in line:
                    return line.split("=", 1)[1].strip()
        return ""

    pdf = PDF()
    pdf.doc_tipo = tipo
    pdf.add_page()

    try:
        raw = json.loads(datos)
    except Exception:
        raw = {}

    res_lines = resultado.split("\n")

    # ── Optimización de Servidores ──────────────────────────────────────────
    if "Servidor" in tipo:
        cap   = raw.get("capacidad", "N/A")
        servs = raw.get("servicios", [])

        pdf._section("Configuracion del Sistema")
        y = pdf.get_y()
        pdf._kpi(10,  y, 92, "Capacidad Maxima del Servidor", cap,       _NAVY)
        pdf._kpi(104, y, 96, "Microservicios Disponibles",    len(servs), _BLUE)
        pdf.set_y(y + 26)

        if servs:
            pdf._section("Microservicios Evaluados")
            rows = [(s.get("nombre",""), s.get("peso",""), s.get("valor",""))
                    for s in servs]
            pdf._table(
                ["Microservicio", "Peso (unidades)", "Valor (puntos)"],
                rows, [100, 45, 45]
            )

        valor = _pick(res_lines, "valor total", "valor")
        sel   = _pick(res_lines, "seleccion", "selección")

        pdf._section("Resultado Optimo - Algoritmo Knapsack")
        pdf._result_banner(
            "Valor Total Acumulado",
            valor,
            f"Seleccion optima: {sel}",
            _NAVY,
        )

        if sel:
            selected = {s.strip() for s in sel.split(",")}
            detail   = [s for s in servs if s.get("nombre","") in selected]
            if detail:
                pdf.ln(2)
                pdf.set_font("helvetica", "B", 8)
                pdf.set_text_color(*_MGREY)
                pdf.cell(0, 5, "Detalle de microservicios seleccionados:", ln=1)
                pdf.ln(2)
                r2 = [
                    (s["nombre"], s["peso"], s["valor"],
                     f"{s['valor']/s['peso']:.2f}" if s.get("peso") else "N/A")
                    for s in detail
                ]
                pdf._table(
                    ["Microservicio", "Peso", "Valor", "Eficiencia (v/p)"],
                    r2, [95, 32, 32, 31]
                )

    # ── Ruta Mínima ─────────────────────────────────────────────────────────
    elif "Ruta" in tipo:
        inicio = raw.get("inicio", "")
        fin    = raw.get("fin", "")
        grafo  = raw.get("grafo", {})

        pdf._section("Topologia de la Red")
        y = pdf.get_y()
        pdf._kpi(10,  y, 56, "Nodo Origen",    inicio,     _GREEN)
        pdf._kpi(68,  y, 56, "Nodo Destino",   fin,        _BLUE)
        pdf._kpi(126, y, 62, "Total de Nodos", len(grafo), _NAVY)
        pdf.set_y(y + 26)

        rows = [
            (origen, dest, f"{peso} ms")
            for origen, conns in grafo.items()
            for dest, peso in conns.items()
        ]
        if rows:
            pdf._section("Conexiones del Grafo")
            pdf._table(["Nodo Origen", "Nodo Destino", "Latencia"], rows, [65, 65, 60])

        latencia = _pick(res_lines, "latencia")
        ruta_str = _pick(res_lines, "ruta recomendada", "ruta")

        pdf._section("Resultado Optimo - Programacion Dinamica Backward")
        pdf._result_banner(
            "Latencia Minima Total",
            latencia,
            f"Ruta: {ruta_str}",
            _GREEN,
        )

    # ── Optimización de Marketing ────────────────────────────────────────────
    elif "Marketing" in tipo:
        presupuesto = raw.get("presupuesto", "N/A")
        a1 = raw.get("a1", ""); a2 = raw.get("a2", "")
        b1 = raw.get("b1", ""); b2 = raw.get("b2", "")

        roi       = _pick(res_lines, "roi")
        creadores = _pick(res_lines, "creadores", "x1")
        anuncios  = _pick(res_lines, "anuncios",  "x2")

        pdf._section("Parametros de la Campana")
        y = pdf.get_y()
        pdf._kpi(10,  y, 56, "Presupuesto Total",   f"${presupuesto}M", _GOLD)
        pdf._kpi(68,  y, 56, "Inv. Creadores (x1)", f"${creadores}M",   _BLUE)
        pdf._kpi(126, y, 62, "Inv. Anuncios (x2)",  f"${anuncios}M",    _NAVY)
        pdf.set_y(y + 26)

        if a1 and a2 and b1 and b2:
            pdf.ln(2)
            pdf.set_fill_color(*_LGREY)
            pdf.set_draw_color(*_BLUE)
            pdf.rect(10, pdf.get_y(), 190, 11, "FD")
            pdf.set_xy(14, pdf.get_y() + 2)
            pdf.set_font("helvetica", "", 8.5)
            pdf.set_text_color(*_NAVY)
            fn = (f"ROI(x1, x2) = {a1}*x1 + {a2}*x2 - {b1}*x1^2 - {b2}*x2^2"
                  f"   [x1 + x2 <= {presupuesto}]")
            pdf.cell(185, 7, fn)
            pdf.set_text_color(*_DARK)
            pdf.ln(14)

        pdf._section("Resultado Optimo - Optimizacion No Lineal")
        pdf._result_banner(
            "ROI Maximo Estimado",
            roi,
            f"Distribucion optima: ${creadores}M Creadores  +  ${anuncios}M Anuncios",
            _GOLD,
        )

    # ── Línea de Espera ──────────────────────────────────────────────────────
    elif "Espera" in tipo or "Cola" in tipo:
        modelo  = raw.get("modelo", "")
        unidad  = raw.get("unidad", "")
        lam_v   = raw.get("lam", "")
        mu_v    = raw.get("mu", "")
        s_v     = raw.get("s", "")
        K_v     = raw.get("K", "")

        MODEL_FULL = {
            "MM1":  "M/M/1 - 1 servidor, llegadas Poisson, servicio exponencial, cola infinita",
            "MMs":  "M/M/s - Multiples servidores, llegadas Poisson, servicio exponencial",
            "MD1":  "M/D/1 - 1 servidor, llegadas Poisson, tiempo de servicio constante",
            "MM1K": "M/M/1/K - 1 servidor, capacidad maxima K, clientes rechazados al llenar",
        }

        pdf._section("Configuracion del Sistema de Colas")
        y = pdf.get_y()
        pdf.set_fill_color(*_LBLUE)
        pdf.set_draw_color(*_BLUE)
        pdf.rect(10, y, 190, 14, "FD")
        pdf.set_fill_color(*_BLUE)
        pdf.rect(10, y, 4, 14, "F")
        pdf.set_xy(18, y + 2)
        pdf.set_font("helvetica", "B", 9)
        pdf.set_text_color(*_NAVY)
        desc = MODEL_FULL.get(modelo, modelo).encode("latin-1", "replace").decode("latin-1")
        pdf.cell(180, 5, f"Modelo: {desc}")
        pdf.set_xy(18, y + 8)
        parts = [f"lambda = {lam_v}", f"mu = {mu_v}"]
        if s_v: parts.append(f"s = {s_v} servidores")
        if K_v: parts.append(f"K = {K_v}")
        if unidad: parts.append(f"Unidad: {unidad}")
        pdf.set_font("helvetica", "", 8)
        pdf.set_text_color(*_MGREY)
        pdf.cell(180, 5, "   |   ".join(parts))
        pdf.set_text_color(*_DARK)
        pdf.set_y(y + 18)

        # Parse metrics
        metrics = {}
        for line in res_lines:
            if "=" in line:
                k, _, v = line.partition("=")
                metrics[k.strip()] = v.strip()

        if metrics:
            # Two rows of 3 KPI boxes
            KPI_ORDER  = ["rho", "P0", "L", "Lq", "W", "Wq"]
            KPI_COLORS = [_NAVY, _BLUE, _GREEN, _BLUE, _NAVY, _BLUE]
            kpi_vals = [(k, metrics[k]) for k in KPI_ORDER if k in metrics]

            y2 = pdf.get_y() + 2
            for i, (k, v) in enumerate(kpi_vals[:3]):
                pdf._kpi(10 + i * 64, y2, 62, k, v, KPI_COLORS[i])
            y3 = y2 + 26
            for i, (k, v) in enumerate(kpi_vals[3:6]):
                pdf._kpi(10 + i * 64, y3, 62, k, v, KPI_COLORS[3 + i])
            pdf.set_y(y3 + 26)

            # Full metrics table
            LABELS = {
                "rho":     "Factor de utilizacion (rho)",
                "P0":      "Probabilidad sistema vacio (P0)",
                "L":       "Clientes en el sistema (L)",
                "Lq":      "Clientes en la cola (Lq)",
                "Ls":      "Clientes en servicio (Ls)",
                "W":       f"Tiempo en el sistema (W) [{unidad}]",
                "Wq":      f"Tiempo en la cola (Wq) [{unidad}]",
                "Ws":      f"Tiempo en servicio (Ws) [{unidad}]",
                "Pw":      "Probabilidad de esperar - Erlang C (Pw)",
                "a":       "Intensidad de trafico (a = lambda/mu)",
                "PK":      "Probabilidad de rechazo (PK)",
                "lam_eff": "Tasa efectiva de llegada (lam_eff)",
                "Lq_mm1":  "Lq equivalente M/M/1 (referencia)",
            }
            pdf._section("Metricas Completas del Sistema")
            rows = [(LABELS.get(k, k), v) for k, v in metrics.items()]
            pdf._table(["Parametro", "Valor"], rows, [140, 50])

    # ── Fallback ────────────────────────────────────────────────────────────
    else:
        pdf._section("Datos de Entrada")
        clean_d = datos.encode("latin-1", "replace").decode("latin-1")
        pdf.set_font("helvetica", "", 9)
        pdf.multi_cell(0, 5.5, clean_d)
        pdf._section("Resultado")
        clean_r = resultado.encode("latin-1", "replace").decode("latin-1")
        pdf.multi_cell(0, 5.5, clean_r)

    # ── AI Analysis (all types) ──────────────────────────────────────────────
    if ia_analisis and ia_analisis.strip():
        pdf._ai_block(ia_analisis)

    pdf_bytes = pdf.output()
    return Response(
        content=bytes(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=Reporte_{tipo.replace(' ', '_')}.pdf"},
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
