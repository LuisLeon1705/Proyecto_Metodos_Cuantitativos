class OptimizacionNoLineal:
    @staticmethod
    def maximizar_marketing(presupuesto_max=10, a1=4.0, a2=5.0, b1=0.2, b2=0.3):
        max_roi = -float('inf')
        opt_x1, opt_x2 = 0, 0
        paso = 0.1

        pasos_totales = int(presupuesto_max / paso) + 1
        for i in range(pasos_totales):
            x1 = i * paso
            for j in range(int((presupuesto_max - x1) / paso) + 1):
                x2 = j * paso
                roi = a1*x1 + a2*x2 - b1*(x1**2) - b2*(x2**2)
                if roi > max_roi:
                    max_roi = roi
                    opt_x1, opt_x2 = x1, x2

        return round(max_roi, 2), round(opt_x1, 2), round(opt_x2, 2)