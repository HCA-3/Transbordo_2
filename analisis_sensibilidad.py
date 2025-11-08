"""
ANÁLISIS DE SENSIBILIDAD - PROBLEMA DE TRANSBORDO
Análisis exhaustivo de sensibilidad con precios sombra, rangos de optimalidad y simulación de escenarios
"""

from pulp import *
import copy

def solve_with_costs(costs_dict):
    """
    Resuelve el problema de transbordo con costos personalizados

    Args:
        costs_dict: Diccionario con los costos de transporte

    Returns:
        prob: Problema resuelto
        variables: Diccionario de variables
        objective_value: Valor de la función objetivo
    """
    prob = LpProblem("Transbordo_Sensibilidad", LpMinimize)

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

    # Función Objetivo con costos personalizados
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


def analyze_sensitivity():
    """
    Realiza un análisis completo de sensibilidad del problema de transbordo
    """
    print("="*80)
    print("ANÁLISIS DE SENSIBILIDAD - PROBLEMA DE TRANSBORDO")
    print("="*80)

    # Costos originales
    original_costs = {
        'S1H1': 4, 'S1H2': 6, 'S1H3': 5,
        'S2H1': 3, 'S2H2': 4, 'S2H3': 6,
        'H1D1': 8, 'H1D2': 6, 'H1D3': 7, 'H1D4': 9,
        'H2D1': 7, 'H2D2': 5, 'H2D3': 6, 'H2D4': 4, 'H2D5': 5,
        'H3D2': 8, 'H3D3': 5, 'H3D4': 7, 'H3D5': 6
    }

    # Resolver problema original
    print("\n📊 RESOLVIENDO PROBLEMA ORIGINAL...")
    prob_original, vars_original, cost_original = solve_with_costs(original_costs)

    print(f"\n{'='*80}")
    print("SOLUCIÓN ÓPTIMA ORIGINAL")
    print(f"{'='*80}")
    print(f"\n💰 Costo Total: {cost_original:,.2f}")

    print("\n📦 Variables Básicas (con flujo > 0):")
    print("-" * 80)
    basic_vars = []
    non_basic_vars = []

    for var_name, var_obj in vars_original.items():
        var_value = value(var_obj)
        cost = original_costs[var_name]
        if var_value > 0.01:
            basic_vars.append((var_name, var_value, cost))
            print(f"  {var_name}: {var_value:>10.2f} unidades (costo unitario: {cost})")
        else:
            non_basic_vars.append((var_name, var_value, cost))

    print("\n📭 Variables No Básicas (flujo = 0):")
    print("-" * 80)
    for var_name, var_value, cost in non_basic_vars:
        print(f"  {var_name}: {var_value:>10.2f} unidades (costo unitario: {cost})")

    # Análisis de Precios Sombra (Dual Prices)
    print(f"\n{'='*80}")
    print("ANÁLISIS DE PRECIOS SOMBRA (DUAL PRICES)")
    print(f"{'='*80}")
    print("\nLos precios sombra indican el cambio en el costo total por unidad")
    print("adicional de capacidad o demanda.\n")

    print("Restricción                | Precio Sombra | Interpretación")
    print("-" * 80)

    for name, constraint in prob_original.constraints.items():
        if constraint.pi is not None:
            shadow_price = constraint.pi
            interpretation = ""
            if abs(shadow_price) < 0.01:
                interpretation = "No activa (holgura disponible)"
            elif shadow_price > 0:
                interpretation = f"Aumentar capacidad reduce costo en {abs(shadow_price):.2f}/unidad"
            else:
                interpretation = f"Aumentar demanda aumenta costo en {abs(shadow_price):.2f}/unidad"

            print(f"{name:26} | {shadow_price:13.2f} | {interpretation}")

    # Análisis de Sensibilidad a Cambios en Costos
    print(f"\n{'='*80}")
    print("ANÁLISIS DE ROBUSTEZ - SENSIBILIDAD A CAMBIOS EN COSTOS")
    print(f"{'='*80}")
    print("\nEvaluando impacto de ±10% en cada costo de transporte...\n")

    print("Ruta   | Costo Base | -10% Costo | +10% Costo | Cambio -10% | Cambio +10% | Sensibilidad")
    print("-" * 100)

    sensitivity_results = []

    for var_name in original_costs.keys():
        base_cost = original_costs[var_name]

        # Probar con -10%
        costs_minus = copy.deepcopy(original_costs)
        costs_minus[var_name] = base_cost * 0.9
        _, _, cost_minus = solve_with_costs(costs_minus)
        change_minus = cost_minus - cost_original

        # Probar con +10%
        costs_plus = copy.deepcopy(original_costs)
        costs_plus[var_name] = base_cost * 1.1
        _, _, cost_plus = solve_with_costs(costs_plus)
        change_plus = cost_plus - cost_original

        # Determinar sensibilidad
        max_change = max(abs(change_minus), abs(change_plus))
        if max_change < 1:
            sensitivity = "BAJA"
        elif max_change < 100:
            sensitivity = "MEDIA"
        else:
            sensitivity = "ALTA"

        sensitivity_results.append((var_name, base_cost, max_change, sensitivity))

        print(f"{var_name:6} | {base_cost:10.2f} | {cost_minus:10.2f} | {cost_plus:10.2f} | "
              f"{change_minus:11.2f} | {change_plus:11.2f} | {sensitivity}")

    # Identificar rutas críticas
    print(f"\n{'='*80}")
    print("RUTAS CRÍTICAS (Alta Sensibilidad)")
    print(f"{'='*80}")

    critical_routes = [r for r in sensitivity_results if r[3] == "ALTA"]
    if critical_routes:
        print("\n⚠️  Las siguientes rutas son críticas y requieren monitoreo especial:\n")
        for var_name, base_cost, max_change, _ in critical_routes:
            print(f"  • {var_name}: Costo base = {base_cost}, Impacto máximo = ±{max_change:.2f}")
    else:
        print("\n✅ No hay rutas con alta sensibilidad. El sistema es robusto.")

    # Simulación de Escenarios
    print(f"\n{'='*80}")
    print("SIMULACIÓN DE ESCENARIOS")
    print(f"{'='*80}")

    scenarios = {
        'Optimista': 0.9,  # Reducción del 10% en todos los costos
        'Pesimista': 1.1,  # Aumento del 10% en todos los costos
        'Inflación': 1.15  # Aumento del 15% en todos los costos
    }

    print("\nEscenario       | Factor | Costo Total | Cambio vs Base | Cambio %")
    print("-" * 80)
    print(f"{'Base':15} | {1.0:6.2f} | {cost_original:11.2f} | {0:14.2f} | {0:8.2f}%")

    for scenario_name, factor in scenarios.items():
        scenario_costs = {k: v * factor for k, v in original_costs.items()}
        _, _, scenario_cost = solve_with_costs(scenario_costs)
        change = scenario_cost - cost_original
        change_pct = (change / cost_original) * 100

        print(f"{scenario_name:15} | {factor:6.2f} | {scenario_cost:11.2f} | "
              f"{change:14.2f} | {change_pct:8.2f}%")

    # Análisis de Rangos de Optimalidad
    print(f"\n{'='*80}")
    print("ANÁLISIS DE RANGOS DE OPTIMALIDAD")
    print(f"{'='*80}")
    print("\nProbando rangos donde la solución óptima se mantiene...\n")

    print("Variable | Valor Óptimo | Rango Inferior | Rango Superior | Amplitud")
    print("-" * 80)

    for var_name, var_obj in vars_original.items():
        var_value = value(var_obj)
        base_cost = original_costs[var_name]

        # Buscar rango donde la solución no cambia
        lower_bound = base_cost
        upper_bound = base_cost

        # Buscar límite inferior
        for test_cost in [base_cost * 0.5, base_cost * 0.7, base_cost * 0.9]:
            test_costs = copy.deepcopy(original_costs)
            test_costs[var_name] = test_cost
            _, test_vars, _ = solve_with_costs(test_costs)
            if abs(value(test_vars[var_name]) - var_value) < 0.01:
                lower_bound = test_cost
                break

        # Buscar límite superior
        for test_cost in [base_cost * 1.5, base_cost * 1.3, base_cost * 1.1]:
            test_costs = copy.deepcopy(original_costs)
            test_costs[var_name] = test_cost
            _, test_vars, _ = solve_with_costs(test_costs)
            if abs(value(test_vars[var_name]) - var_value) < 0.01:
                upper_bound = test_cost
                break

        range_width = upper_bound - lower_bound
        print(f"{var_name:8} | {var_value:12.2f} | {lower_bound:14.2f} | {upper_bound:14.2f} | {range_width:8.2f}")

    # Recomendaciones Gerenciales
    print(f"\n{'='*80}")
    print("RECOMENDACIONES GERENCIALES")
    print(f"{'='*80}\n")

    print("📌 RECOMENDACIONES CRÍTICAS:\n")

    print("1. MONITOREO DE RUTAS CRÍTICAS:")
    if critical_routes:
        print("   ⚠️  Establecer contratos de largo plazo para las siguientes rutas:")
        for var_name, base_cost, max_change, _ in critical_routes:
            print(f"      • {var_name} (impacto potencial: ±{max_change:.2f})")
    else:
        print("   ✅ El sistema actual es robusto ante variaciones de costos.")

    print("\n2. GESTIÓN DE CAPACIDAD:")
    print("   • Revisar precios sombra para identificar cuellos de botella")
    print("   • Considerar expansión de capacidad donde el precio sombra es alto")

    print("\n3. DIVERSIFICACIÓN:")
    print("   • Mantener rutas alternativas activas para reducir riesgo")
    print("   • Evitar dependencia excesiva de una sola ruta de transporte")

    print("\n4. PLANIFICACIÓN DE ESCENARIOS:")
    print(f"   • En escenario optimista: Ahorro potencial de {(cost_original * 0.1):,.2f}")
    print(f"   • En escenario pesimista: Costo adicional de {(cost_original * 0.1):,.2f}")
    print("   • Mantener presupuesto de contingencia del 15% para inflación")

    print("\n5. OPTIMIZACIÓN CONTINUA:")
    print("   • Revisar costos de transporte trimestralmente")
    print("   • Renegociar contratos para rutas con alta sensibilidad")
    print("   • Implementar sistema de monitoreo en tiempo real")

    print(f"\n{'='*80}")

    return prob_original, vars_original, sensitivity_results


def main():
    """Función principal"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*18 + "ANÁLISIS DE SENSIBILIDAD" + " "*35 + "║")
    print("║" + " "*20 + "PROBLEMA DE TRANSBORDO" + " "*35 + "║")
    print("╚" + "="*78 + "╝")
    print()

    prob, variables, sensitivity = analyze_sensitivity()

    print("\n✅ ANÁLISIS COMPLETADO")
    print("="*80)

    return prob, variables, sensitivity


if __name__ == "__main__":
    main()
