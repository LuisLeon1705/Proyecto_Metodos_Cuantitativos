import math


class LineaEspera:

    @staticmethod
    def modelo_mm1(lam: float, mu: float) -> dict:
        """M/M/1: un servidor, llegadas Poisson, servicio exponencial."""
        if lam <= 0 or mu <= 0:
            raise ValueError("Las tasas λ y μ deben ser positivas.")
        rho = lam / mu
        if rho >= 1:
            raise ValueError(
                f"Sistema inestable: ρ = {rho:.4f} ≥ 1. "
                "La tasa de llegada λ debe ser menor que la tasa de servicio μ."
            )

        P0 = 1 - rho
        L  = lam / (mu - lam)
        Lq = (lam ** 2) / (mu * (mu - lam))
        Ls = rho
        W  = 1 / (mu - lam)
        Wq = lam / (mu * (mu - lam))
        Ws = 1 / mu

        Pn = [round((1 - rho) * (rho ** n), 6) for n in range(11)]

        pasos = [
            {
                "formula": "ρ = λ / μ",
                "calculo":  f"ρ = {lam} / {mu}",
                "resultado": f"ρ = {round(rho, 6)}"
            },
            {
                "formula": "P₀ = 1 − ρ",
                "calculo":  f"P₀ = 1 − {round(rho, 6)}",
                "resultado": f"P₀ = {round(P0, 6)}"
            },
            {
                "formula": "L = λ / (μ − λ)",
                "calculo":  f"L = {lam} / ({mu} − {lam})",
                "resultado": f"L = {round(L, 6)}"
            },
            {
                "formula": "Lq = λ² / [μ(μ − λ)]",
                "calculo":  f"Lq = {lam}² / [{mu} × ({mu} − {lam})]",
                "resultado": f"Lq = {round(Lq, 6)}"
            },
            {
                "formula": "Ls = ρ",
                "calculo":  f"Ls = {round(rho, 6)}",
                "resultado": f"Ls = {round(Ls, 6)}"
            },
            {
                "formula": "W = 1 / (μ − λ)",
                "calculo":  f"W = 1 / ({mu} − {lam})",
                "resultado": f"W = {round(W, 6)}"
            },
            {
                "formula": "Wq = λ / [μ(μ − λ)]",
                "calculo":  f"Wq = {lam} / [{mu} × ({mu} − {lam})]",
                "resultado": f"Wq = {round(Wq, 6)}"
            },
            {
                "formula": "Ws = 1 / μ",
                "calculo":  f"Ws = 1 / {mu}",
                "resultado": f"Ws = {round(Ws, 6)}"
            },
            {
                "formula": "Pn = (1 − ρ) · ρⁿ",
                "calculo":  f"P₀ = (1 − {round(rho, 6)}) · {round(rho, 6)}⁰",
                "resultado": f"P₀ = {Pn[0]}"
            },
            {
                "formula": "Verificación Ley de Little: L = λ · W",
                "calculo":  f"L = {lam} × {round(W, 6)}",
                "resultado": f"L = {round(lam * W, 6)} ≈ {round(L, 6)}"
            },
            {
                "formula": "Verificación Ley de Little: Lq = λ · Wq",
                "calculo":  f"Lq = {lam} × {round(Wq, 6)}",
                "resultado": f"Lq = {round(lam * Wq, 6)} ≈ {round(Lq, 6)}"
            },
        ]

        return {
            "modelo":     "M/M/1",
            "modelo_id":  "MM1",
            "estable":    True,
            "rho":  round(rho, 6),
            "P0":   round(P0, 6),
            "L":    round(L, 6),
            "Lq":   round(Lq, 6),
            "Ls":   round(Ls, 6),
            "W":    round(W, 6),
            "Wq":   round(Wq, 6),
            "Ws":   round(Ws, 6),
            "Pn":   Pn,
            "pasos": pasos,
        }

    @staticmethod
    def modelo_mms(lam: float, mu: float, s: int) -> dict:
        """M/M/s: s servidores paralelos, llegadas Poisson, servicio exponencial."""
        if lam <= 0 or mu <= 0:
            raise ValueError("Las tasas λ y μ deben ser positivas.")
        if s < 1:
            raise ValueError("El número de servidores s debe ser al menos 1.")

        a   = lam / mu          # intensidad de tráfico
        rho = lam / (s * mu)   # utilización por servidor

        if rho >= 1:
            raise ValueError(
                f"Sistema inestable: ρ = λ/(s·μ) = {rho:.4f} ≥ 1. "
                f"Se necesitan al menos {math.ceil(lam / mu) + 1} servidores o mayor μ."
            )

        # P0
        sum_terms = sum((a ** n) / math.factorial(n) for n in range(s))
        last_term  = (a ** s) / (math.factorial(s) * (1 - rho))
        P0 = 1.0 / (sum_terms + last_term)

        # Erlang C (Pw = probabilidad de esperar)
        Pw = ((a ** s) / (math.factorial(s) * (1 - rho))) * P0

        Lq = Pw * rho / (1 - rho)
        Ls = a                  # = lam / mu
        L  = Lq + Ls
        Wq = Lq / lam
        Ws = 1 / mu
        W  = Wq + Ws

        # Pn para n = 0..s+5
        Pn = []
        for n in range(s + 6):
            if n < s:
                pn = ((a ** n) / math.factorial(n)) * P0
            else:
                pn = ((a ** n) / (math.factorial(s) * (s ** (n - s)))) * P0
            Pn.append(round(pn, 6))

        pasos = [
            {
                "formula": "a = λ / μ  (intensidad de tráfico)",
                "calculo":  f"a = {lam} / {mu}",
                "resultado": f"a = {round(a, 6)}"
            },
            {
                "formula": "ρ = λ / (s · μ)  (utilización por servidor)",
                "calculo":  f"ρ = {lam} / ({s} × {mu})",
                "resultado": f"ρ = {round(rho, 6)}"
            },
            {
                "formula": "P₀ = 1 / [Σₙ₌₀^(s-1) aⁿ/n! + aˢ/(s!(1-ρ))]",
                "calculo":  (
                    f"Σ = {round(sum_terms, 6)} + {round(last_term, 6)} = "
                    f"{round(sum_terms + last_term, 6)}"
                ),
                "resultado": f"P₀ = {round(P0, 6)}"
            },
            {
                "formula": "Pw (Erlang C) = [aˢ/(s!(1-ρ))] · P₀",
                "calculo":  f"Pw = {round((a**s)/(math.factorial(s)*(1-rho)), 6)} × {round(P0, 6)}",
                "resultado": f"Pw = {round(Pw, 6)}"
            },
            {
                "formula": "Lq = Pw · ρ / (1 − ρ)",
                "calculo":  f"Lq = {round(Pw, 6)} × {round(rho, 6)} / (1 − {round(rho, 6)})",
                "resultado": f"Lq = {round(Lq, 6)}"
            },
            {
                "formula": "Ls = a = λ / μ",
                "calculo":  f"Ls = {round(a, 6)}",
                "resultado": f"Ls = {round(Ls, 6)}"
            },
            {
                "formula": "L = Lq + Ls",
                "calculo":  f"L = {round(Lq, 6)} + {round(Ls, 6)}",
                "resultado": f"L = {round(L, 6)}"
            },
            {
                "formula": "Wq = Lq / λ",
                "calculo":  f"Wq = {round(Lq, 6)} / {lam}",
                "resultado": f"Wq = {round(Wq, 6)}"
            },
            {
                "formula": "Ws = 1 / μ",
                "calculo":  f"Ws = 1 / {mu}",
                "resultado": f"Ws = {round(Ws, 6)}"
            },
            {
                "formula": "W = Wq + Ws",
                "calculo":  f"W = {round(Wq, 6)} + {round(Ws, 6)}",
                "resultado": f"W = {round(W, 6)}"
            },
            {
                "formula": "Verificación Ley de Little: L = λ · W",
                "calculo":  f"L = {lam} × {round(W, 6)}",
                "resultado": f"L = {round(lam * W, 6)} ≈ {round(L, 6)}"
            },
            {
                "formula": "Verificación Ley de Little: Lq = λ · Wq",
                "calculo":  f"Lq = {lam} × {round(Wq, 6)}",
                "resultado": f"Lq = {round(lam * Wq, 6)} ≈ {round(Lq, 6)}"
            },
        ]

        return {
            "modelo":    "M/M/s",
            "modelo_id": "MMs",
            "estable":   True,
            "s":    s,
            "a":    round(a, 6),
            "rho":  round(rho, 6),
            "Pw":   round(Pw, 6),
            "P0":   round(P0, 6),
            "L":    round(L, 6),
            "Lq":   round(Lq, 6),
            "Ls":   round(Ls, 6),
            "W":    round(W, 6),
            "Wq":   round(Wq, 6),
            "Ws":   round(Ws, 6),
            "Pn":   Pn,
            "pasos": pasos,
        }

    @staticmethod
    def modelo_md1(lam: float, mu: float) -> dict:
        """M/D/1: servicio determinístico (Pollaczek-Khintchine)."""
        if lam <= 0 or mu <= 0:
            raise ValueError("Las tasas λ y μ deben ser positivas.")
        rho = lam / mu
        if rho >= 1:
            raise ValueError(
                f"Sistema inestable: ρ = {rho:.4f} ≥ 1. "
                "La tasa de llegada λ debe ser menor que la tasa de servicio μ."
            )

        E_S  = 1 / mu          # Tiempo de servicio esperado
        sigma2 = 0.0           # Varianza = 0 (determinístico)
        E_S2 = E_S ** 2        # E[S²] = (E[S])² cuando σ² = 0

        # Fórmula PK generalizada: Lq = λ²·E[S²] / (2(1-ρ))
        # Con σ²=0: Lq = λ²·(1/μ)² / (2(1-ρ)) = ρ²/(2(1-ρ))
        Lq = (lam ** 2 * E_S2) / (2 * (1 - rho))
        Ls = rho
        L  = Lq + Ls
        Wq = Lq / lam
        Ws = E_S
        W  = Wq + Ws

        P0 = 1 - rho           # Prob. de sistema vacío (M/G/1)

        Lq_mm1 = rho ** 2 / (1 - rho)   # M/M/1 para comparación

        pasos = [
            {
                "formula": "ρ = λ / μ",
                "calculo":  f"ρ = {lam} / {mu}",
                "resultado": f"ρ = {round(rho, 6)}"
            },
            {
                "formula": "E[S] = 1 / μ  (tiempo de servicio)",
                "calculo":  f"E[S] = 1 / {mu}",
                "resultado": f"E[S] = {round(E_S, 6)}"
            },
            {
                "formula": "σ² = 0  (servicio determinístico)",
                "calculo":  "σ² = 0",
                "resultado": "σ² = 0"
            },
            {
                "formula": "E[S²] = σ² + (E[S])² = (E[S])²  (cuando σ²=0)",
                "calculo":  f"E[S²] = 0 + ({round(E_S, 6)})² = {round(E_S**2, 6)}",
                "resultado": f"E[S²] = {round(E_S2, 6)}"
            },
            {
                "formula": "Lq = λ² · E[S²] / [2(1 − ρ)]  (Pollaczek-Khintchine)",
                "calculo":  (
                    f"Lq = {lam}² × {round(E_S2, 6)} / [2 × (1 − {round(rho, 6)})]"
                ),
                "resultado": f"Lq = {round(Lq, 6)}"
            },
            {
                "formula": "Lq (M/D/1 simplificado) = ρ² / [2(1 − ρ)]",
                "calculo":  f"Lq = {round(rho, 6)}² / [2 × (1 − {round(rho, 6)})]",
                "resultado": f"Lq = {round(Lq, 6)}"
            },
            {
                "formula": "Lq (M/M/1 comparación) = ρ² / (1 − ρ)",
                "calculo":  f"Lq_MM1 = {round(rho, 6)}² / (1 − {round(rho, 6)})",
                "resultado": f"Lq_MM1 = {round(Lq_mm1, 6)}  [el doble que M/D/1]"
            },
            {
                "formula": "Ls = ρ",
                "calculo":  f"Ls = {round(rho, 6)}",
                "resultado": f"Ls = {round(Ls, 6)}"
            },
            {
                "formula": "L = Lq + Ls",
                "calculo":  f"L = {round(Lq, 6)} + {round(Ls, 6)}",
                "resultado": f"L = {round(L, 6)}"
            },
            {
                "formula": "Wq = Lq / λ",
                "calculo":  f"Wq = {round(Lq, 6)} / {lam}",
                "resultado": f"Wq = {round(Wq, 6)}"
            },
            {
                "formula": "Ws = E[S] = 1 / μ",
                "calculo":  f"Ws = 1 / {mu}",
                "resultado": f"Ws = {round(Ws, 6)}"
            },
            {
                "formula": "W = Wq + Ws",
                "calculo":  f"W = {round(Wq, 6)} + {round(Ws, 6)}",
                "resultado": f"W = {round(W, 6)}"
            },
            {
                "formula": "P₀ = 1 − ρ  (prob. servidor ocioso, M/G/1)",
                "calculo":  f"P₀ = 1 − {round(rho, 6)}",
                "resultado": f"P₀ = {round(P0, 6)}"
            },
            {
                "formula": "Verificación Ley de Little: L = λ · W",
                "calculo":  f"L = {lam} × {round(W, 6)}",
                "resultado": f"L = {round(lam * W, 6)} ≈ {round(L, 6)}"
            },
            {
                "formula": "Verificación Ley de Little: Lq = λ · Wq",
                "calculo":  f"Lq = {lam} × {round(Wq, 6)}",
                "resultado": f"Lq = {round(lam * Wq, 6)} ≈ {round(Lq, 6)}"
            },
        ]

        return {
            "modelo":    "M/D/1",
            "modelo_id": "MD1",
            "estable":   True,
            "rho":     round(rho, 6),
            "P0":      round(P0, 6),
            "L":       round(L, 6),
            "Lq":      round(Lq, 6),
            "Ls":      round(Ls, 6),
            "W":       round(W, 6),
            "Wq":      round(Wq, 6),
            "Ws":      round(Ws, 6),
            "Pn":      None,
            "Lq_mm1":  round(Lq_mm1, 6),
            "pasos":   pasos,
        }

    @staticmethod
    def modelo_mm1k(lam: float, mu: float, K: int) -> dict:
        """M/M/1/K: capacidad finita K (máximo de clientes en el sistema)."""
        if lam <= 0 or mu <= 0:
            raise ValueError("Las tasas λ y μ deben ser positivas.")
        if K < 1:
            raise ValueError("La capacidad máxima K debe ser al menos 1.")

        rho = lam / mu

        # P0 y Pn
        if abs(rho - 1.0) < 1e-12:
            P0 = 1.0 / (K + 1)
            Pn = [round(P0, 6) for _ in range(K + 1)]
        else:
            P0 = (1 - rho) / (1 - rho ** (K + 1))
            Pn = [round(P0 * (rho ** n), 6) for n in range(K + 1)]

        PK = Pn[K]                         # Probabilidad de rechazo
        lam_eff = lam * (1 - PK)           # Tasa efectiva de llegada

        # L
        if abs(rho - 1.0) < 1e-12:
            L = K / 2.0
        else:
            L = (rho / (1 - rho)) - ((K + 1) * rho ** (K + 1)) / (1 - rho ** (K + 1))

        Ls = 1 - P0                        # Tiempo promedio en servicio = 1 - prob(servidor libre)
        Lq = max(0.0, L - Ls)

        # W, Wq pueden ser None si lam_eff = 0 (sistema bloqueado por completo)
        if lam_eff > 1e-12:
            W  = L / lam_eff
            Wq = Lq / lam_eff
        else:
            W  = None
            Wq = None

        Ws = 1 / mu

        pasos = [
            {
                "formula": "ρ = λ / μ",
                "calculo":  f"ρ = {lam} / {mu}",
                "resultado": f"ρ = {round(rho, 6)}"
            },
        ]

        if abs(rho - 1.0) < 1e-12:
            pasos.append({
                "formula": "P₀ = 1 / (K + 1)  [cuando ρ = 1]",
                "calculo":  f"P₀ = 1 / ({K} + 1)",
                "resultado": f"P₀ = {round(P0, 6)}"
            })
        else:
            pasos.append({
                "formula": "P₀ = (1 − ρ) / (1 − ρ^(K+1))",
                "calculo":  f"P₀ = (1 − {round(rho, 6)}) / (1 − {round(rho, 6)}^({K}+1))",
                "resultado": f"P₀ = {round(P0, 6)}"
            })

        pasos += [
            {
                "formula": "Pn = P₀ · ρⁿ  para n = 0, 1, …, K",
                "calculo":  f"PK = P₀ · ρ^K = {round(P0, 6)} × {round(rho, 6)}^{K}",
                "resultado": f"PK = P({K}) = {round(PK, 6)}"
            },
            {
                "formula": "λ_eff = λ · (1 − PK)  (tasa efectiva)",
                "calculo":  f"λ_eff = {lam} × (1 − {round(PK, 6)})",
                "resultado": f"λ_eff = {round(lam_eff, 6)}"
            },
        ]

        if abs(rho - 1.0) < 1e-12:
            pasos.append({
                "formula": "L = K / 2  [cuando ρ = 1]",
                "calculo":  f"L = {K} / 2",
                "resultado": f"L = {round(L, 6)}"
            })
        else:
            pasos.append({
                "formula": "L = ρ/(1−ρ) − (K+1)·ρ^(K+1)/(1−ρ^(K+1))",
                "calculo":  (
                    f"L = {round(rho, 6)}/(1−{round(rho, 6)}) − "
                    f"({K}+1)·{round(rho, 6)}^({K}+1)/(1−{round(rho, 6)}^({K}+1))"
                ),
                "resultado": f"L = {round(L, 6)}"
            })

        pasos += [
            {
                "formula": "Ls = 1 − P₀",
                "calculo":  f"Ls = 1 − {round(P0, 6)}",
                "resultado": f"Ls = {round(Ls, 6)}"
            },
            {
                "formula": "Lq = L − Ls  (≥ 0)",
                "calculo":  f"Lq = {round(L, 6)} − {round(Ls, 6)}",
                "resultado": f"Lq = {round(Lq, 6)}"
            },
            {
                "formula": "Ws = 1 / μ",
                "calculo":  f"Ws = 1 / {mu}",
                "resultado": f"Ws = {round(Ws, 6)}"
            },
        ]

        if W is not None:
            pasos += [
                {
                    "formula": "W = L / λ_eff  (Ley de Little)",
                    "calculo":  f"W = {round(L, 6)} / {round(lam_eff, 6)}",
                    "resultado": f"W = {round(W, 6)}"
                },
                {
                    "formula": "Wq = Lq / λ_eff  (Ley de Little)",
                    "calculo":  f"Wq = {round(Lq, 6)} / {round(lam_eff, 6)}",
                    "resultado": f"Wq = {round(Wq, 6)}"
                },
                {
                    "formula": "Verificación: L = λ_eff · W",
                    "calculo":  f"L = {round(lam_eff, 6)} × {round(W, 6)}",
                    "resultado": f"L = {round(lam_eff * W, 6)} ≈ {round(L, 6)}"
                },
            ]
        else:
            pasos.append({
                "formula": "W, Wq = N/A (λ_eff ≈ 0, sistema completamente bloqueado)",
                "calculo":  "λ_eff = 0",
                "resultado": "N/A"
            })

        return {
            "modelo":    "M/M/1/K",
            "modelo_id": "MM1K",
            "estable":   True,
            "K":       K,
            "rho":     round(rho, 6),
            "P0":      round(P0, 6),
            "PK":      round(PK, 6),
            "lam_eff": round(lam_eff, 6),
            "L":       round(L, 6),
            "Lq":      round(Lq, 6),
            "Ls":      round(Ls, 6),
            "W":       round(W, 6) if W is not None else None,
            "Wq":      round(Wq, 6) if Wq is not None else None,
            "Ws":      round(Ws, 6),
            "Pn":      Pn,
            "pasos":   pasos,
        }
