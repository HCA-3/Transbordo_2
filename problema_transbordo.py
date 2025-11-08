"""
PROBLEMA DE TRANSBORDO - OPTIMIZACIÓN CON PuLP
Solución completa del problema de transbordo con verificación automática
"""

from pulp import *

def solve_transshipment_problem():
    """
    Resuelve el problema de transbordo usando PuLP

    Red de Transbordo:
    - 2 Fuentes: S1 (900 unidades), S2 (700 unidades)
    - 3 Centros de Transbordo: H1, H2, H3
    - 5 Destinos: D1 (300), D2 (250), D3 (350), D4 (400), D5 (300)
    """

    print("="*80)
    print("PROBLEMA DE TRANSBORDO - OPTIMIZACIÓN CON PuLP")
    print("="*80)

    # Crear el problema de minimización
    prob = LpProblem("Problema_Transbordo", LpMinimize)

    # Variables de decisión (todas >= 0)
    # Fuentes a Transbordos
    S1H1 = LpVariable("S1H1", lowBound=0)
    S1H2 = LpVariable("S1H2", lowBound=0)
    S1H3 = LpVariable("S1H3", lowBound=0)
    S2H1 = LpVariable("S2H1", lowBound=0)
    S2H2 = LpVariable("S2H2", lowBound=0)
    S2H3 = LpVariable("S2H3", lowBound=0)

    # Transbordos a Destinos
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

    # Función Objetivo (Minimizar costos de transporte)
    prob += (4*S1H1 + 6*S1H2 + 5*S1H3 + 3*S2H1 + 4*S2H2 + 6*S2H3 +
             8*H1D1 + 6*H1D2 + 7*H1D3 + 9*H1D4 +
             7*H2D1 + 5*H2D2 + 6*H2D3 + 4*H2D4 + 5*H2D5 +
             8*H3D2 + 5*H3D3 + 7*H3D4 + 6*H3D5), "Costo_Total"

    # Restricciones de Oferta
    prob += S1H1 + S1H2 + S1H3 == 900, "Oferta_S1"
    prob += S2H1 + S2H2 + S2H3 == 700, "Oferta_S2"

    # Restricciones de Balance en Transbordos
    prob += S1H1 + S2H1 == H1D1 + H1D2 + H1D3 + H1D4, "Balance_H1"
    prob += S1H2 + S2H2 == H2D1 + H2D2 + H2D3 + H2D4 + H2D5, "Balance_H2"
    prob += S1H3 + S2H3 == H3D2 + H3D3 + H3D4 + H3D5, "Balance_H3"

    # Restricciones de Demanda
    prob += H1D1 + H2D1 == 300, "Demanda_D1"
    prob += H1D2 + H2D2 + H3D2 == 250, "Demanda_D2"
    prob += H1D3 + H2D3 + H3D3 == 350, "Demanda_D3"
    prob += H1D4 + H2D4 + H3D4 == 400, "Demanda_D4"
    prob += H2D5 + H3D5 == 300, "Demanda_D5"

    # Resolver el problema
    prob.solve(PULP_CBC_CMD(msg=0))

    # Mostrar resultados
    print(f"\n{'='*80}")
    print(f"ESTADO DE LA SOLUCIÓN: {LpStatus[prob.status]}")
    print(f"{'='*80}")
    print(f"\n💰 COSTO TOTAL MÍNIMO: Z = {value(prob.objective):,.2f}")

    print(f"\n{'='*80}")
    print("SOLUCIÓN ÓPTIMA - VALORES DE LAS VARIABLES")
    print(f"{'='*80}")

    # Diccionario con todas las variables
    variables = {
        'S1H1': S1H1, 'S1H2': S1H2, 'S1H3': S1H3,
        'S2H1': S2H1, 'S2H2': S2H2, 'S2H3': S2H3,
        'H1D1': H1D1, 'H1D2': H1D2, 'H1D3': H1D3, 'H1D4': H1D4,
        'H2D1': H2D1, 'H2D2': H2D2, 'H2D3': H2D3, 'H2D4': H2D4, 'H2D5': H2D5,
        'H3D2': H3D2, 'H3D3': H3D3, 'H3D4': H3D4, 'H3D5': H3D5
    }

    print("\n📦 FLUJOS DE FUENTES A TRANSBORDOS:")
    print("-" * 80)
    for var_name in ['S1H1', 'S1H2', 'S1H3', 'S2H1', 'S2H2', 'S2H3']:
        var_value = value(variables[var_name])
        print(f"  {var_name}: {var_value:>10.2f} unidades")

    print("\n🚚 FLUJOS DE TRANSBORDOS A DESTINOS:")
    print("-" * 80)
    print("Desde H1:")
    for var_name in ['H1D1', 'H1D2', 'H1D3', 'H1D4']:
        var_value = value(variables[var_name])
        print(f"  {var_name}: {var_value:>10.2f} unidades")

    print("\nDesde H2:")
    for var_name in ['H2D1', 'H2D2', 'H2D3', 'H2D4', 'H2D5']:
        var_value = value(variables[var_name])
        print(f"  {var_name}: {var_value:>10.2f} unidades")

    print("\nDesde H3:")
    for var_name in ['H3D2', 'H3D3', 'H3D4', 'H3D5']:
        var_value = value(variables[var_name])
        print(f"  {var_name}: {var_value:>10.2f} unidades")

    # Verificación de restricciones
    print(f"\n{'='*80}")
    print("VERIFICACIÓN DE RESTRICCIONES")
    print(f"{'='*80}")

    print("\n✅ OFERTA DE FUENTES:")
    print("-" * 80)
    s1_total = value(S1H1) + value(S1H2) + value(S1H3)
    s2_total = value(S2H1) + value(S2H2) + value(S2H3)
    print(f"  S1: {s1_total:.2f} / 900 {'✓' if abs(s1_total - 900) < 0.01 else '✗'}")
    print(f"  S2: {s2_total:.2f} / 700 {'✓' if abs(s2_total - 700) < 0.01 else '✗'}")

    print("\n✅ BALANCE EN TRANSBORDOS:")
    print("-" * 80)
    h1_in = value(S1H1) + value(S2H1)
    h1_out = value(H1D1) + value(H1D2) + value(H1D3) + value(H1D4)
    h2_in = value(S1H2) + value(S2H2)
    h2_out = value(H2D1) + value(H2D2) + value(H2D3) + value(H2D4) + value(H2D5)
    h3_in = value(S1H3) + value(S2H3)
    h3_out = value(H3D2) + value(H3D3) + value(H3D4) + value(H3D5)
    print(f"  H1: Entrada={h1_in:.2f}, Salida={h1_out:.2f}, Balance={h1_in-h1_out:.2f} {'✓' if abs(h1_in-h1_out) < 0.01 else '✗'}")
    print(f"  H2: Entrada={h2_in:.2f}, Salida={h2_out:.2f}, Balance={h2_in-h2_out:.2f} {'✓' if abs(h2_in-h2_out) < 0.01 else '✗'}")
    print(f"  H3: Entrada={h3_in:.2f}, Salida={h3_out:.2f}, Balance={h3_in-h3_out:.2f} {'✓' if abs(h3_in-h3_out) < 0.01 else '✗'}")

    print("\n✅ DEMANDA EN DESTINOS:")
    print("-" * 80)
    d1_supply = value(H1D1) + value(H2D1)
    d2_supply = value(H1D2) + value(H2D2) + value(H3D2)
    d3_supply = value(H1D3) + value(H2D3) + value(H3D3)
    d4_supply = value(H1D4) + value(H2D4) + value(H3D4)
    d5_supply = value(H2D5) + value(H3D5)

    print(f"  D1: Recibe={d1_supply:.2f}, Necesita=300 {'✓' if abs(d1_supply-300) < 0.01 else '✗'}")
    print(f"  D2: Recibe={d2_supply:.2f}, Necesita=250 {'✓' if abs(d2_supply-250) < 0.01 else '✗'}")
    print(f"  D3: Recibe={d3_supply:.2f}, Necesita=350 {'✓' if abs(d3_supply-350) < 0.01 else '✗'}")
    print(f"  D4: Recibe={d4_supply:.2f}, Necesita=400 {'✓' if abs(d4_supply-400) < 0.01 else '✗'}")
    print(f"  D5: Recibe={d5_supply:.2f}, Necesita=300 {'✓' if abs(d5_supply-300) < 0.01 else '✗'}")

    # Visualización del flujo
    print(f"\n{'='*80}")
    print("VISUALIZACIÓN DEL FLUJO DE MATERIALES")
    print(f"{'='*80}\n")

    print("S1 (900)")
    if value(S1H1) > 0:
        print(f"  ├─→ H1: {value(S1H1):.0f} unidades")
    if value(S1H2) > 0:
        print(f"  ├─→ H2: {value(S1H2):.0f} unidades")
    if value(S1H3) > 0:
        print(f"  └─→ H3: {value(S1H3):.0f} unidades")

    print("\nS2 (700)")
    if value(S2H1) > 0:
        print(f"  ├─→ H1: {value(S2H1):.0f} unidades")
    if value(S2H2) > 0:
        print(f"  ├─→ H2: {value(S2H2):.0f} unidades")
    if value(S2H3) > 0:
        print(f"  └─→ H3: {value(S2H3):.0f} unidades")

    print(f"\nH1 (Total: {h1_in:.0f})")
    if value(H1D1) > 0:
        print(f"  ├─→ D1: {value(H1D1):.0f} unidades")
    if value(H1D2) > 0:
        print(f"  ├─→ D2: {value(H1D2):.0f} unidades")
    if value(H1D3) > 0:
        print(f"  ├─→ D3: {value(H1D3):.0f} unidades")
    if value(H1D4) > 0:
        print(f"  └─→ D4: {value(H1D4):.0f} unidades")

    print(f"\nH2 (Total: {h2_in:.0f})")
    if value(H2D1) > 0:
        print(f"  ├─→ D1: {value(H2D1):.0f} unidades")
    if value(H2D2) > 0:
        print(f"  ├─→ D2: {value(H2D2):.0f} unidades")
    if value(H2D3) > 0:
        print(f"  ├─→ D3: {value(H2D3):.0f} unidades")
    if value(H2D4) > 0:
        print(f"  ├─→ D4: {value(H2D4):.0f} unidades")
    if value(H2D5) > 0:
        print(f"  └─→ D5: {value(H2D5):.0f} unidades")

    print(f"\nH3 (Total: {h3_in:.0f})")
    if value(H3D2) > 0:
        print(f"  ├─→ D2: {value(H3D2):.0f} unidades")
    if value(H3D3) > 0:
        print(f"  ├─→ D3: {value(H3D3):.0f} unidades")
    if value(H3D4) > 0:
        print(f"  ├─→ D4: {value(H3D4):.0f} unidades")
    if value(H3D5) > 0:
        print(f"  └─→ D5: {value(H3D5):.0f} unidades")

    # Comparación con solución conocida
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
        calc_value = value(variables[var_name])
        match = abs(calc_value - known_value) < 0.01
        all_match = all_match and match
        status = "✓" if match else "✗"
        print(f"{var_name:8} | {calc_value:9.2f} | {known_value:8.2f} | {status}")

    known_cost = 15500
    cost_match = abs(value(prob.objective) - known_cost) < 0.01
    all_match = all_match and cost_match

    print("-" * 80)
    print(f"{'Costo':8} | {value(prob.objective):9.2f} | {known_cost:8.2f} | {'✓' if cost_match else '✗'}")

    if all_match:
        print(f"\n{'✅ VERIFICACIÓN EXITOSA: La solución coincide perfectamente con la solución conocida!'}")
    else:
        print(f"\n{'⚠️ ADVERTENCIA: Hay diferencias con la solución conocida.'}")

    print(f"\n{'='*80}")

    return prob, variables


def main():
    """Función principal"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "PROBLEMA DE TRANSBORDO" + " "*37 + "║")
    print("║" + " "*25 + "OPTIMIZACIÓN CON PuLP" + " "*32 + "║")
    print("╚" + "="*78 + "╝")
    print()

    prob, variables = solve_transshipment_problem()

    print("\n✅ EJECUCIÓN COMPLETADA")
    print("="*80)

    return prob, variables


if __name__ == "__main__":
    main()
