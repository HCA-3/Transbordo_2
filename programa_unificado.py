"""
PROGRAMA UNIFICADO - PROBLEMA DE TRANSBORDO
Solución completa con optimización y análisis de sensibilidad integrado
"""

from pulp import *
import copy

class TransshipmentProblem:
    """
    Clase para resolver y analizar problemas de transbordo
    """

    def __init__(self):
        """Inicializa el problema con los parámetros por defecto"""
        self.original_costs = {
            'S1H1': 4, 'S1H2': 6, 'S1H3': 5,
            'S2H1': 3, 'S2H2': 4, 'S2H3': 6,
            'H1D1': 8, 'H1D2': 6, 'H1D3': 7, 'H1D4': 9,
            'H2D1': 7, 'H2D2': 5, 'H2D3': 6, 'H2D4': 4, 'H2D5': 5,
            'H3D2': 8, 'H3D3': 5, 'H3D4': 7, 'H3D5': 6
        }
        self.prob = None
        self.variables = None
        self.objective_value = None

    def solve_with_costs(self, costs_dict):
        """
        Resuelve el problema de transbordo con costos personalizados

        Args:
            costs_dict: Diccionario con los costos de transporte

        Returns:
            prob: Problema resuelto
            variables: Diccionario de variables
            objective_value: Valor de la función objetivo
        """
        prob = LpProblem("Transbordo", LpMinimize)

        # Variables de decisión
        S1H1 = LpVariable("S1H1", lowBound=0)
        S1H2 = LpVariable("S1H2", lowBound=0)
        S1H3 = LpVariable("S1H3", lowBound=0)
        S2H1 = LpVariable("S2H1", lowBound=0)
        S2H2 = LpVariable("S2H2", lowBound=0)
        S2H3 = LpVariable("S2H3", lowBound=0)

        H1D1 = LpVariable("H1D1", lowBound=0)
        H1D2 = LpVariable("H1D2", lowBound=0)
        H1D3 = LpVariable("H1D3", lowBound=0)
        H1D4 = LpVariable("H1D4", lowBound=0)

        H2D1 = LpVariable("H2D1", lowBound=0)
        H2D2 = LpVariable("H2D2", lowBound=0)
        H2D3 = LpVariable("H2D3", lowBound=0)
        H2D4 = LpVariable("H2D4", lowBound=0)
        H2D5 = LpVariable("H2D5", lowBound=0)

        H3D2 = LpVariable("H3D2", lowBound=0)
        H3D3 = LpVariable("H3D3", lowBound=0)
        H3D4 = LpVariable("H3D4", lowBound=0)
        H3D5 = LpVariable("H3D5", lowBound=0)

        variables = {
            'S1H1': S1H1, 'S1H2': S1H2, 'S1H3': S1H3,
            'S2H1': S2H1, 'S2H2': S2H2, 'S2H3': S2H3,
            'H1D1': H1D1, 'H1D2': H1D2, 'H1D3': H1D3, 'H1D4': H1D4,
            'H2D1': H2D1, 'H2D2': H2D2, 'H2D3': H2D3, 'H2D4': H2D4, 'H2D5': H2D5,
            'H3D2': H3D2, 'H3D3': H3D3, 'H3D4': H3D4, 'H3D5': H3D5
        }

        # Función Objetivo
        prob += (costs_dict['S1H1']*S1H1 + costs_dict['S1H2']*S1H2 + costs_dict['S1H3']*S1H3 +
                 costs_dict['S2H1']*S2H1 + costs_dict['S2H2']*S2H2 + costs_dict['S2H3']*S2H3 +
                 costs_dict['H1D1']*H1D1 + costs_dict['H1D2']*H1D2 + costs_dict['H1D3']*H1D3 + costs_dict['H1D4']*H1D4 +
                 costs_dict['H2D1']*H2D1 + costs_dict['H2D2']*H2D2 + costs_dict['H2D3']*H2D3 + costs_dict['H2D4']*H2D4 + costs_dict['H2D5']*H2D5 +
                 costs_dict['H3D2']*H3D2 + costs_dict['H3D3']*H3D3 + costs_dict['H3D4']*H3D4 + costs_dict['H3D5']*H3D5), "Costo_Total"

        # Restricciones
        prob += S1H1 + S1H2 + S1H3 == 900, "Oferta_S1"
        prob += S2H1 + S2H2 + S2H3 == 700, "Oferta_S2"
        prob += S1H1 + S2H1 == H1D1 + H1D2 + H1D3 + H1D4, "Balance_H1"
        prob += S1H2 + S2H2 == H2D1 + H2D2 + H2D3 + H2D4 + H2D5, "Balance_H2"
        prob += S1H3 + S2H3 == H3D2 + H3D3 + H3D4 + H3D5, "Balance_H3"
        prob += H1D1 + H2D1 == 300, "Demanda_D1"
        prob += H1D2 + H2D2 + H3D2 == 250, "Demanda_D2"
        prob += H1D3 + H2D3 + H3D3 == 350, "Demanda_D3"
        prob += H1D4 + H2D4 + H3D4 == 400, "Demanda_D4"
        prob += H2D5 + H3D5 == 300, "Demanda_D5"

        prob.solve(PULP_CBC_CMD(msg=0))

        return prob, variables, value(prob.objective)

    def solve_original(self):
        """Resuelve el problema con los costos originales"""
        self.prob, self.variables, self.objective_value = self.solve_with_costs(self.original_costs)
        return self.prob, self.variables, self.objective_value

    def display_solution(self):
        """Muestra la solución óptima del problema"""
        if self.prob is None:
            print("⚠️  Primero debe resolver el problema usando solve_original()")
            return

        print("="*80)
        print("SOLUCIÓN ÓPTIMA DEL PROBLEMA DE TRANSBORDO")
        print("="*80)

        print(f"\n{'='*80}")
        print(f"ESTADO: {LpStatus[self.prob.status]}")
        print(f"{'='*80}")
        print(f"\nCOSTO TOTAL MINIMO: Z = {self.objective_value:,.2f}")

        print(f"\n{'='*80}")
        print("VALORES DE LAS VARIABLES")
        print(f"{'='*80}")

        print("\nFLUJOS DE FUENTES A TRANSBORDOS:")
        print("-" * 80)
        for var_name in ['S1H1', 'S1H2', 'S1H3', 'S2H1', 'S2H2', 'S2H3']:
            var_value = value(self.variables[var_name])
            print(f"  {var_name}: {var_value:>10.2f} unidades")

        print("\nFLUJOS DE TRANSBORDOS A DESTINOS:")
        print("-" * 80)
        print("Desde H1:")
        for var_name in ['H1D1', 'H1D2', 'H1D3', 'H1D4']:
            var_value = value(self.variables[var_name])
            print(f"  {var_name}: {var_value:>10.2f} unidades")

        print("\nDesde H2:")
        for var_name in ['H2D1', 'H2D2', 'H2D3', 'H2D4', 'H2D5']:
            var_value = value(self.variables[var_name])
            print(f"  {var_name}: {var_value:>10.2f} unidades")

        print("\nDesde H3:")
        for var_name in ['H3D2', 'H3D3', 'H3D4', 'H3D5']:
            var_value = value(self.variables[var_name])
            print(f"  {var_name}: {var_value:>10.2f} unidades")

        self._verify_constraints()
        self._visualize_flow()
        self._compare_known_solution()

    def _verify_constraints(self):
        """Verifica que todas las restricciones se cumplan"""
        print(f"\n{'='*80}")
        print("VERIFICACIÓN DE RESTRICCIONES")
        print(f"{'='*80}")

        print("\nOFERTA DE FUENTES:")
        print("-" * 80)
        s1_total = value(self.variables['S1H1']) + value(self.variables['S1H2']) + value(self.variables['S1H3'])
        s2_total = value(self.variables['S2H1']) + value(self.variables['S2H2']) + value(self.variables['S2H3'])
        print(f"  S1: {s1_total:.2f} / 900 {'OK' if abs(s1_total - 900) < 0.01 else 'ERROR'}")
        print(f"  S2: {s2_total:.2f} / 700 {'OK' if abs(s2_total - 700) < 0.01 else 'ERROR'}")

        print("\nBALANCE EN TRANSBORDOS:")
        print("-" * 80)
        h1_in = value(self.variables['S1H1']) + value(self.variables['S2H1'])
        h1_out = value(self.variables['H1D1']) + value(self.variables['H1D2']) + value(self.variables['H1D3']) + value(self.variables['H1D4'])
        h2_in = value(self.variables['S1H2']) + value(self.variables['S2H2'])
        h2_out = value(self.variables['H2D1']) + value(self.variables['H2D2']) + value(self.variables['H2D3']) + value(self.variables['H2D4']) + value(self.variables['H2D5'])
        h3_in = value(self.variables['S1H3']) + value(self.variables['S2H3'])
        h3_out = value(self.variables['H3D2']) + value(self.variables['H3D3']) + value(self.variables['H3D4']) + value(self.variables['H3D5'])
        print(f"  H1: Entrada={h1_in:.2f}, Salida={h1_out:.2f}, Balance={h1_in-h1_out:.2f} {'OK' if abs(h1_in-h1_out) < 0.01 else 'ERROR'}")
        print(f"  H2: Entrada={h2_in:.2f}, Salida={h2_out:.2f}, Balance={h2_in-h2_out:.2f} {'OK' if abs(h2_in-h2_out) < 0.01 else 'ERROR'}")
        print(f"  H3: Entrada={h3_in:.2f}, Salida={h3_out:.2f}, Balance={h3_in-h3_out:.2f} {'OK' if abs(h3_in-h3_out) < 0.01 else 'ERROR'}")

        print("\nDEMANDA EN DESTINOS:")
        print("-" * 80)
        d1_supply = value(self.variables['H1D1']) + value(self.variables['H2D1'])
        d2_supply = value(self.variables['H1D2']) + value(self.variables['H2D2']) + value(self.variables['H3D2'])
        d3_supply = value(self.variables['H1D3']) + value(self.variables['H2D3']) + value(self.variables['H3D3'])
        d4_supply = value(self.variables['H1D4']) + value(self.variables['H2D4']) + value(self.variables['H3D4'])
        d5_supply = value(self.variables['H2D5']) + value(self.variables['H3D5'])

        print(f"  D1: Recibe={d1_supply:.2f}, Necesita=300 {'OK' if abs(d1_supply-300) < 0.01 else 'ERROR'}")
        print(f"  D2: Recibe={d2_supply:.2f}, Necesita=250 {'OK' if abs(d2_supply-250) < 0.01 else 'ERROR'}")
        print(f"  D3: Recibe={d3_supply:.2f}, Necesita=350 {'OK' if abs(d3_supply-350) < 0.01 else 'ERROR'}")
        print(f"  D4: Recibe={d4_supply:.2f}, Necesita=400 {'OK' if abs(d4_supply-400) < 0.01 else 'ERROR'}")
        print(f"  D5: Recibe={d5_supply:.2f}, Necesita=300 {'OK' if abs(d5_supply-300) < 0.01 else 'ERROR'}")

    def _visualize_flow(self):
        """Visualiza el flujo de materiales"""
        print(f"\n{'='*80}")
        print("VISUALIZACIÓN DEL FLUJO DE MATERIALES")
        print(f"{'='*80}\n")

        print("S1 (900)")
        if value(self.variables['S1H1']) > 0:
            print(f"  -> H1: {value(self.variables['S1H1']):.0f} unidades")
        if value(self.variables['S1H2']) > 0:
            print(f"  -> H2: {value(self.variables['S1H2']):.0f} unidades")
        if value(self.variables['S1H3']) > 0:
            print(f"  -> H3: {value(self.variables['S1H3']):.0f} unidades")

        print("\nS2 (700)")
        if value(self.variables['S2H1']) > 0:
            print(f"  -> H1: {value(self.variables['S2H1']):.0f} unidades")
        if value(self.variables['S2H2']) > 0:
            print(f"  -> H2: {value(self.variables['S2H2']):.0f} unidades")
        if value(self.variables['S2H3']) > 0:
            print(f"  -> H3: {value(self.variables['S2H3']):.0f} unidades")

        h1_in = value(self.variables['S1H1']) + value(self.variables['S2H1'])
        h2_in = value(self.variables['S1H2']) + value(self.variables['S2H2'])
        h3_in = value(self.variables['S1H3']) + value(self.variables['S2H3'])

        print(f"\nH1 (Total: {h1_in:.0f})")
        if value(self.variables['H1D1']) > 0:
            print(f"  -> D1: {value(self.variables['H1D1']):.0f} unidades")
        if value(self.variables['H1D2']) > 0:
            print(f"  -> D2: {value(self.variables['H1D2']):.0f} unidades")
        if value(self.variables['H1D3']) > 0:
            print(f"  -> D3: {value(self.variables['H1D3']):.0f} unidades")
        if value(self.variables['H1D4']) > 0:
            print(f"  -> D4: {value(self.variables['H1D4']):.0f} unidades")

        print(f"\nH2 (Total: {h2_in:.0f})")
        if value(self.variables['H2D1']) > 0:
            print(f"  -> D1: {value(self.variables['H2D1']):.0f} unidades")
        if value(self.variables['H2D2']) > 0:
            print(f"  -> D2: {value(self.variables['H2D2']):.0f} unidades")
        if value(self.variables['H2D3']) > 0:
            print(f"  -> D3: {value(self.variables['H2D3']):.0f} unidades")
        if value(self.variables['H2D4']) > 0:
            print(f"  -> D4: {value(self.variables['H2D4']):.0f} unidades")
        if value(self.variables['H2D5']) > 0:
            print(f"  -> D5: {value(self.variables['H2D5']):.0f} unidades")

        print(f"\nH3 (Total: {h3_in:.0f})")
        if value(self.variables['H3D2']) > 0:
            print(f"  -> D2: {value(self.variables['H3D2']):.0f} unidades")
        if value(self.variables['H3D3']) > 0:
            print(f"  -> D3: {value(self.variables['H3D3']):.0f} unidades")
        if value(self.variables['H3D4']) > 0:
            print(f"  -> D4: {value(self.variables['H3D4']):.0f} unidades")
        if value(self.variables['H3D5']) > 0:
            print(f"  -> D5: {value(self.variables['H3D5']):.0f} unidades")

    def _compare_known_solution(self):
        """Compara con la solución conocida"""
        print(f"\n{'='*80}")
        print("COMPARACIÓN CON SOLUCIÓN CONOCIDA")
        print(f"{'='*80}")

        known_solution = {
            'S1H1': 550, 'S1H2': 0, 'S1H3': 350,
            'S2H1': 0, 'S2H2': 700, 'S2H3': 0,
            'H1D1': 300, 'H1D2': 250, 'H1D3': 0, 'H1D4': 0,
            'H2D1': 0, 'H2D2': 0, 'H2D3': 0, 'H2D4': 400, 'H2D5': 300,
            'H3D2': 0, 'H3D3': 350, 'H3D4': 0, 'H3D5': 0
        }

        all_match = True
        print("\nVariable | Calculado | Conocido | Estado")
        print("-" * 80)
        for var_name, known_value in known_solution.items():
            calc_value = value(self.variables[var_name])
            match = abs(calc_value - known_value) < 0.01
            all_match = all_match and match
            status = "✓" if match else "✗"
            print(f"{var_name:8} | {calc_value:9.2f} | {known_value:8.2f} | {status}")

        known_cost = 15500
        cost_match = abs(self.objective_value - known_cost) < 0.01
        all_match = all_match and cost_match

        print("-" * 80)
        print(f"{'Costo':8} | {self.objective_value:9.2f} | {known_cost:8.2f} | {'✓' if cost_match else '✗'}")

        if all_match:
            print(f"\nVERIFICACION EXITOSA: La solucion coincide perfectamente!")
        else:
            print(f"\nADVERTENCIA: Hay diferencias con la solucion conocida.")

    def analyze_sensitivity(self):
        """Realiza análisis completo de sensibilidad"""
        if self.prob is None:
            print("ADVERTENCIA: Primero debe resolver el problema usando solve_original()")
            return

        print("\n" + "="*80)
        print("ANALISIS DE SENSIBILIDAD")
        print("="*80)

        # Clasificar variables
        print("\nCLASIFICACION DE VARIABLES:")
        print("-" * 80)
        basic_vars = []
        non_basic_vars = []

        for var_name, var_obj in self.variables.items():
            var_value = value(var_obj)
            cost = self.original_costs[var_name]
            if var_value > 0.01:
                basic_vars.append((var_name, var_value, cost))
            else:
                non_basic_vars.append((var_name, var_value, cost))

        print("\nVariables Básicas (con flujo > 0):")
        for var_name, var_value, cost in basic_vars:
            print(f"  {var_name}: {var_value:>10.2f} unidades (costo: {cost})")

        print("\nVariables No Básicas (flujo = 0):")
        for var_name, var_value, cost in non_basic_vars:
            print(f"  {var_name}: {var_value:>10.2f} unidades (costo: {cost})")

        # Precios Sombra
        self._analyze_shadow_prices()

        # Sensibilidad a cambios en costos
        self._analyze_cost_sensitivity()

        # Simulación de escenarios
        self._simulate_scenarios()

        # Recomendaciones
        self._generate_recommendations()

    def _analyze_shadow_prices(self):
        """Analiza los precios sombra de las restricciones"""
        print(f"\n{'='*80}")
        print("PRECIOS SOMBRA (DUAL PRICES)")
        print(f"{'='*80}\n")

        print("Restricción                | Precio Sombra | Interpretación")
        print("-" * 80)

        for name, constraint in self.prob.constraints.items():
            if constraint.pi is not None:
                shadow_price = constraint.pi
                interpretation = ""
                if abs(shadow_price) < 0.01:
                    interpretation = "No activa (holgura disponible)"
                elif shadow_price > 0:
                    interpretation = f"Aumentar capacidad reduce costo"
                else:
                    interpretation = f"Aumentar demanda aumenta costo"

                print(f"{name:26} | {shadow_price:13.2f} | {interpretation}")

    def _analyze_cost_sensitivity(self):
        """Analiza sensibilidad a cambios en costos"""
        print(f"\n{'='*80}")
        print("SENSIBILIDAD A CAMBIOS EN COSTOS (±10%)")
        print(f"{'='*80}\n")

        print("Ruta   | Costo Base | Cambio -10% | Cambio +10% | Sensibilidad")
        print("-" * 80)

        self.sensitivity_results = []

        for var_name in self.original_costs.keys():
            base_cost = self.original_costs[var_name]

            # Probar con -10%
            costs_minus = copy.deepcopy(self.original_costs)
            costs_minus[var_name] = base_cost * 0.9
            _, _, cost_minus = self.solve_with_costs(costs_minus)
            change_minus = cost_minus - self.objective_value

            # Probar con +10%
            costs_plus = copy.deepcopy(self.original_costs)
            costs_plus[var_name] = base_cost * 1.1
            _, _, cost_plus = self.solve_with_costs(costs_plus)
            change_plus = cost_plus - self.objective_value

            # Determinar sensibilidad
            max_change = max(abs(change_minus), abs(change_plus))
            if max_change < 1:
                sensitivity = "BAJA"
            elif max_change < 100:
                sensitivity = "MEDIA"
            else:
                sensitivity = "ALTA"

            self.sensitivity_results.append((var_name, base_cost, max_change, sensitivity))

            print(f"{var_name:6} | {base_cost:10.2f} | {change_minus:11.2f} | {change_plus:11.2f} | {sensitivity}")

        # Identificar rutas críticas
        critical_routes = [r for r in self.sensitivity_results if r[3] == "ALTA"]
        if critical_routes:
            print(f"\nRUTAS CRITICAS (Alta Sensibilidad):")
            for var_name, base_cost, max_change, _ in critical_routes:
                print(f"   - {var_name}: Impacto maximo = +/-{max_change:.2f}")

    def _simulate_scenarios(self):
        """Simula diferentes escenarios de costos"""
        print(f"\n{'='*80}")
        print("SIMULACIÓN DE ESCENARIOS")
        print(f"{'='*80}\n")

        scenarios = {
            'Optimista (-10%)': 0.9,
            'Pesimista (+10%)': 1.1,
            'Inflación (+15%)': 1.15
        }

        print("Escenario              | Factor | Costo Total | Cambio      | Cambio %")
        print("-" * 80)
        print(f"{'Base':22} | {1.0:6.2f} | {self.objective_value:11.2f} | {0:11.2f} | {0:8.2f}%")

        for scenario_name, factor in scenarios.items():
            scenario_costs = {k: v * factor for k, v in self.original_costs.items()}
            _, _, scenario_cost = self.solve_with_costs(scenario_costs)
            change = scenario_cost - self.objective_value
            change_pct = (change / self.objective_value) * 100

            print(f"{scenario_name:22} | {factor:6.2f} | {scenario_cost:11.2f} | "
                  f"{change:11.2f} | {change_pct:8.2f}%")

    def _generate_recommendations(self):
        """Genera recomendaciones gerenciales"""
        print(f"\n{'='*80}")
        print("RECOMENDACIONES GERENCIALES")
        print(f"{'='*80}\n")

        print("ACCIONES RECOMENDADAS:\n")

        print("1. MONITOREO DE COSTOS:")
        critical_routes = [r for r in self.sensitivity_results if r[3] == "ALTA"]
        if critical_routes:
            print("   - Establecer contratos de largo plazo para rutas criticas:")
            for var_name, _, max_change, _ in critical_routes:
                print(f"      - {var_name} (impacto: +/-{max_change:.2f})")
        else:
            print("   - Sistema robusto - mantener monitoreo regular")

        print("\n2. GESTION DE CAPACIDAD:")
        print("   - Revisar precios sombra para identificar cuellos de botella")
        print("   - Considerar expansion donde el precio sombra es significativo")

        print("\n3. PLANIFICACION FINANCIERA:")
        print(f"   - Presupuesto base: {self.objective_value:,.2f}")
        print(f"   - Contingencia recomendada: {self.objective_value * 0.15:,.2f} (15%)")

        print("\n4. OPTIMIZACION CONTINUA:")
        print("   - Revisar costos trimestralmente")
        print("   - Renegociar contratos para rutas de alta sensibilidad")
        print("   - Mantener rutas alternativas activas")


def main():
    """Función principal del programa unificado"""
    print("\n")
    print("="*80)
    print(" "*20 + "PROGRAMA UNIFICADO")
    print(" "*15 + "TRANSBORDO + ANÁLISIS DE SENSIBILIDAD")
    print("="*80)
    print()

    # Crear instancia del problema
    problem = TransshipmentProblem()

    # Resolver problema original
    print("="*80)
    print("PASO 1: RESOLVIENDO PROBLEMA DE TRANSBORDO")
    print("="*80)
    problem.solve_original()
    problem.display_solution()

    # Análisis de sensibilidad
    print("\n" + "="*80)
    print("PASO 2: ANÁLISIS DE SENSIBILIDAD")
    print("="*80)
    problem.analyze_sensitivity()

    print("\n" + "="*80)
    print("ANALISIS COMPLETO FINALIZADO")
    print("="*80)

    return problem


if __name__ == "__main__":
    main()
