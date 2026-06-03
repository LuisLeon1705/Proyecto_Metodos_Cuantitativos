import subprocess
import shutil

CLAUDE_BIN = shutil.which("claude") or "/opt/homebrew/bin/claude"

def _claude(prompt: str) -> str:
    try:
        r = subprocess.run(
            [CLAUDE_BIN, "--print"],
            input=prompt, capture_output=True, text=True, timeout=30
        )
        return r.stdout.strip() if r.returncode == 0 and r.stdout.strip() \
               else f"⚠️ {r.stderr.strip()[:120]}"
    except subprocess.TimeoutExpired:
        return "⚠️ La IA tardó demasiado. Intenta de nuevo."
    except FileNotFoundError:
        return "⚠️ Claude CLI no encontrado."
    except Exception as e:
        return f"⚠️ Error: {e}"


class IntegracionIA:

    # ── 1. Optimización de Servidores (Problema de la Mochila) ──────────────
    def analizar_servidores(self, datos: dict) -> str:
        return _claude(f"""Eres un arquitecto de software experto en optimización de infraestructura.
Analiza este resultado del algoritmo de la mochila (knapsack) en español, en exactamente 4 oraciones directas sin listas:

- Capacidad máxima del servidor: {datos.get('capacidad')} unidades
- Valor óptimo alcanzado: {datos.get('valor')}
- Microservicios seleccionados: {datos.get('seleccion')}
- Microservicios disponibles: {datos.get('servicios')}

Evalúa: eficiencia de la selección, si se aprovecha bien la capacidad, riesgo de los servicios excluidos y recomendación de escalabilidad.""")

    # ── 2. Ruta Mínima (Programación Dinámica Backward) ─────────────────────
    def analizar_ruta(self, datos: dict) -> str:
        return _claude(f"""Eres un experto en redes y optimización de latencia.
Analiza este resultado de ruta mínima (programación dinámica backward) en español, en exactamente 4 oraciones directas sin listas:

- Nodo origen: {datos.get('inicio')}
- Nodo destino: {datos.get('fin')}
- Ruta óptima encontrada: {datos.get('ruta')}
- Latencia total: {datos.get('latencia')} ms

Evalúa: si la latencia es aceptable para producción, cuellos de botella en la ruta, redundancia ante fallos y recomendación de mejora de red.""")

    # ── 3. Maximización de ROI (Optimización No Lineal) ─────────────────────
    def analizar_marketing(self, datos: dict) -> str:
        return _claude(f"""Eres un director de marketing digital experto en optimización de presupuestos.
Analiza este resultado de optimización no lineal de ROI en español, en exactamente 4 oraciones directas sin listas:

- Presupuesto total asignado: ${datos.get('presupuesto')}M
- Función ROI: {datos.get('a1')}·x1 + {datos.get('a2')}·x2 − {datos.get('b1')}·x1² − {datos.get('b2')}·x2²
- Inversión óptima en Creadores de Contenido (x1): {datos.get('creadores')}M
- Inversión óptima en Anuncios Programáticos (x2): {datos.get('anuncios')}M
- ROI máximo estimado: {datos.get('roi')}

Evalúa: balance entre canales, rendimientos decrecientes, si el presupuesto es suficiente y recomendación de ajuste.""")

    # ── 4. Línea de Espera M/M/1 ────────────────────────────────────────────
    def analizar_mm1(self, datos: dict) -> str:
        return _claude(f"""Eres un experto en Investigación de Operaciones especializado en teoría de colas.
Analiza este sistema M/M/1 (1 servidor, llegadas Poisson, servicio exponencial, cola infinita) en español, en exactamente 4 oraciones directas sin listas:

- Tasa de llegada λ = {datos.get('lam')} | Tasa de servicio μ = {datos.get('mu')} | Unidad: {datos.get('unidad')}
- Factor de utilización ρ = {datos.get('rho')} | Prob. sistema vacío P₀ = {datos.get('P0')}
- Clientes en sistema L = {datos.get('L')} | Clientes en cola Lq = {datos.get('Lq')}
- Tiempo en sistema W = {datos.get('W')} {datos.get('unidad')} | Tiempo en cola Wq = {datos.get('Wq')} {datos.get('unidad')}

Evalúa: nivel de utilización (crítico si ρ>0.9), calidad del servicio, si se justifica agregar un servidor y recomendación concreta.""")

    # ── 5. Línea de Espera M/M/s ────────────────────────────────────────────
    def analizar_mms(self, datos: dict) -> str:
        return _claude(f"""Eres un experto en Investigación de Operaciones especializado en teoría de colas multiservidor.
Analiza este sistema M/M/s ({datos.get('s')} servidores paralelos, llegadas Poisson, servicio exponencial) en español, en exactamente 4 oraciones directas sin listas:

- λ = {datos.get('lam')} | μ = {datos.get('mu')} por servidor | s = {datos.get('s')} servidores | Unidad: {datos.get('unidad')}
- Utilización por servidor ρ = {datos.get('rho')} | Intensidad de tráfico a = {datos.get('a')}
- Prob. esperar (Erlang C) Pw = {datos.get('Pw')} | Prob. sistema vacío P₀ = {datos.get('P0')}
- L = {datos.get('L')} | Lq = {datos.get('Lq')} | W = {datos.get('W')} {datos.get('unidad')} | Wq = {datos.get('Wq')} {datos.get('unidad')}

Evalúa: si el número de servidores es adecuado, impacto de la Erlang C en la experiencia del cliente, costo-beneficio de agregar/quitar un servidor y recomendación concreta.""")

    # ── 6. Línea de Espera M/D/1 ────────────────────────────────────────────
    def analizar_md1(self, datos: dict) -> str:
        return _claude(f"""Eres un experto en Investigación de Operaciones especializado en sistemas con servicio determinístico.
Analiza este sistema M/D/1 (1 servidor, llegadas Poisson, tiempo de servicio CONSTANTE) en español, en exactamente 4 oraciones directas sin listas:

- λ = {datos.get('lam')} | μ = {datos.get('mu')} (servicio fijo = {datos.get('Ws')} {datos.get('unidad')}) | Unidad: {datos.get('unidad')}
- Factor de utilización ρ = {datos.get('rho')} | Prob. sistema vacío P₀ = {datos.get('P0')}
- Lq (M/D/1) = {datos.get('Lq')} vs Lq (M/M/1 equivalente) = {datos.get('Lq_mm1')} — el servicio constante reduce la cola a la mitad
- W = {datos.get('W')} {datos.get('unidad')} | Wq = {datos.get('Wq')} {datos.get('unidad')}

Evalúa: ventaja del servicio determinístico frente al exponencial, nivel de utilización, impacto de estandarizar los tiempos de servicio y recomendación concreta.""")

    # ── 7. Línea de Espera M/M/1/K ──────────────────────────────────────────
    def analizar_mm1k(self, datos: dict) -> str:
        return _claude(f"""Eres un experto en Investigación de Operaciones especializado en sistemas de colas con capacidad finita.
Analiza este sistema M/M/1/K (1 servidor, capacidad máxima K={datos.get('K')} clientes) en español, en exactamente 4 oraciones directas sin listas:

- λ = {datos.get('lam')} | μ = {datos.get('mu')} | Capacidad K = {datos.get('K')} | Unidad: {datos.get('unidad')}
- Factor de utilización ρ = {datos.get('rho')} | Prob. sistema vacío P₀ = {datos.get('P0')}
- Prob. rechazo PK = {datos.get('PK')} | Tasa efectiva de llegada λ_eff = {datos.get('lam_eff')}
- L = {datos.get('L')} | Lq = {datos.get('Lq')} | W = {datos.get('W')} {datos.get('unidad')} | Wq = {datos.get('Wq')} {datos.get('unidad')}

Evalúa: impacto económico de la tasa de rechazo PK, si la capacidad K es adecuada para la demanda, consecuencias de clientes perdidos y recomendación para ajustar K o μ.""")
