"""
PROBLEMA DE TRANSBORDO CON CAPACIDADES - OPTIMIZACIÓN
Solución usando PuLP para resolver el problema con y sin restricciones de capacidad
"""

from pulp import *

def solve_transshipment_without_capacity():
    """
    Resuelve el problema de transbordo SIN restricciones de capacidad
    """
    print("="*80)
    print("PROBLEMA DE TRANSBORDO - SIN RESTRICCIONES DE CAPACIDAD")
    print("="*80)

    # Crear el problema de minimización
    prob = LpProblem("Transbordo_Sin_Capacidad", LpMinimize)

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

    # Función Objetivo (Minimizar costos)
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
    print(f"\nEstado de la solución: {LpStatus[prob.status]}")
    print(f"Costo Total Óptimo: Z = {value(prob.objective):.2f}")

    print("\n" + "-"*80)
    print("SOLUCIÓN ÓPTIMA - FLUJOS DE FUENTES A TRANSBORDOS:")
    print("-"*80)
    print(f"S1 → H1: {value(S1H1):.2f}")
    print(f"S1 → H2: {value(S1H2):.2f}")
    print(f"S1 → H3: {value(S1H3):.2f}")
    print(f"S2 → H1: {value(S2H1):.2f}")
    print(f"S2 → H2: {value(S2H2):.2f}")
    print(f"S2 → H3: {value(S2H3):.2f}")

    print("\n" + "-"*80)
    print("SOLUCIÓN ÓPTIMA - FLUJOS DE TRANSBORDOS A DESTINOS:")
    print("-"*80)
    print("Desde H1:")
    print(f"  H1 → D1: {value(H1D1):.2f}")
    print(f"  H1 → D2: {value(H1D2):.2f}")
    print(f"  H1 → D3: {value(H1D3):.2f}")
    print(f"  H1 → D4: {value(H1D4):.2f}")

    print("\nDesde H2:")
    print(f"  H2 → D1: {value(H2D1):.2f}")
    print(f"  H2 → D2: {value(H2D2):.2f}")
    print(f"  H2 → D3: {value(H2D3):.2f}")
    print(f"  H2 → D4: {value(H2D4):.2f}")
    print(f"  H2 → D5: {value(H2D5):.2f}")

    print("\nDesde H3:")
    print(f"  H3 → D2: {value(H3D2):.2f}")
    print(f"  H3 → D3: {value(H3D3):.2f}")
    print(f"  H3 → D4: {value(H3D4):.2f}")
    print(f"  H3 → D5: {value(H3D5):.2f}")

    # Verificación de balance en transbordos
    print("\n" + "-"*80)
    print("VERIFICACIÓN DE BALANCE EN TRANSBORDOS:")
    print("-"*80)
    h1_in = value(S1H1) + value(S2H1)
    h1_out = value(H1D1) + value(H1D2) + value(H1D3) + value(H1D4)
    print(f"H1: Entrada = {h1_in:.2f}, Salida = {h1_out:.2f}, Balance = {h1_in - h1_out:.2f}")

    h2_in = value(S1H2) + value(S2H2)
    h2_out = value(H2D1) + value(H2D2) + value(H2D3) + value(H2D4) + value(H2D5)
    print(f"H2: Entrada = {h2_in:.2f}, Salida = {h2_out:.2f}, Balance = {h2_in - h2_out:.2f}")

    h3_in = value(S1H3) + value(S2H3)
    h3_out = value(H3D2) + value(H3D3) + value(H3D4) + value(H3D5)
    print(f"H3: Entrada = {h3_in:.2f}, Salida = {h3_out:.2f}, Balance = {h3_in - h3_out:.2f}")

    return prob, value(prob.objective)


def solve_transshipment_with_capacity():
    """
    Resuelve el problema de transbordo CON restricciones de capacidad
    """
    print("\n\n" + "="*80)
    print("PROBLEMA DE TRANSBORDO - CON RESTRICCIONES DE CAPACIDAD")
    print("="*80)

    # Crear el problema de minimización
    prob = LpProblem("Transbordo_Con_Capacidad", LpMinimize)

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

    # Función Objetivo (Minimizar costos)
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

    # Restricciones de Capacidad
    print("\nAplicando restricciones de capacidad...")

    # Capacidades Fuentes → Transbordos
    prob += S1H1 <= 600, "Cap_S1H1"
    prob += S1H2 <= 400, "Cap_S1H2"
    prob += S1H3 <= 300, "Cap_S1H3"
    prob += S2H1 <= 500, "Cap_S2H1"
    prob += S2H2 <= 300, "Cap_S2H2"
    prob += S2H3 <= 400, "Cap_S2H3"

    # Capacidades Transbordos → Destinos
    prob += H1D1 <= 250, "Cap_H1D1"
    prob += H1D2 <= 300, "Cap_H1D2"
    prob += H1D3 <= 250, "Cap_H1D3"
    prob += H1D4 <= 300, "Cap_H1D4"

    prob += H2D1 <= 150, "Cap_H2D1"
    prob += H2D2 <= 200, "Cap_H2D2"
    prob += H2D3 <= 300, "Cap_H2D3"
    prob += H2D4 <= 350, "Cap_H2D4"
    prob += H2D5 <= 250, "Cap_H2D5"

    prob += H3D2 <= 150, "Cap_H3D2"
    prob += H3D3 <= 200, "Cap_H3D3"
    prob += H3D4 <= 250, "Cap_H3D4"
    prob += H3D5 <= 250, "Cap_H3D5"

    # Resolver el problema
    prob.solve(PULP_CBC_CMD(msg=0))

    # Mostrar resultados
    print(f"\nEstado de la solución: {LpStatus[prob.status]}")
    print(f"Costo Total Óptimo: Z = {value(prob.objective):.2f}")

    print("\n" + "-"*80)
    print("SOLUCIÓN ÓPTIMA - FLUJOS DE FUENTES A TRANSBORDOS:")
    print("-"*80)
    print(f"S1 → H1: {value(S1H1):.2f} (Capacidad: 600)")
    print(f"S1 → H2: {value(S1H2):.2f} (Capacidad: 400)")
    print(f"S1 → H3: {value(S1H3):.2f} (Capacidad: 300)")
    print(f"S2 → H1: {value(S2H1):.2f} (Capacidad: 500)")
    print(f"S2 → H2: {value(S2H2):.2f} (Capacidad: 300)")
    print(f"S2 → H3: {value(S2H3):.2f} (Capacidad: 400)")

    print("\n" + "-"*80)
    print("SOLUCIÓN ÓPTIMA - FLUJOS DE TRANSBORDOS A DESTINOS:")
    print("-"*80)
    print("Desde H1:")
    print(f"  H1 → D1: {value(H1D1):.2f} (Capacidad: 250)")
    print(f"  H1 → D2: {value(H1D2):.2f} (Capacidad: 300)")
    print(f"  H1 → D3: {value(H1D3):.2f} (Capacidad: 250)")
    print(f"  H1 → D4: {value(H1D4):.2f} (Capacidad: 300)")

    print("\nDesde H2:")
    print(f"  H2 → D1: {value(H2D1):.2f} (Capacidad: 150)")
    print(f"  H2 → D2: {value(H2D2):.2f} (Capacidad: 200)")
    print(f"  H2 → D3: {value(H2D3):.2f} (Capacidad: 300)")
    print(f"  H2 → D4: {value(H2D4):.2f} (Capacidad: 350)")
    print(f"  H2 → D5: {value(H2D5):.2f} (Capacidad: 250)")

    print("\nDesde H3:")
    print(f"  H3 → D2: {value(H3D2):.2f} (Capacidad: 150)")
    print(f"  H3 → D3: {value(H3D3):.2f} (Capacidad: 200)")
    print(f"  H3 → D4: {value(H3D4):.2f} (Capacidad: 250)")
    print(f"  H3 → D5: {value(H3D5):.2f} (Capacidad: 250)")

    # Verificación de balance en transbordos
    print("\n" + "-"*80)
    print("VERIFICACIÓN DE BALANCE EN TRANSBORDOS:")
    print("-"*80)
    h1_in = value(S1H1) + value(S2H1)
    h1_out = value(H1D1) + value(H1D2) + value(H1D3) + value(H1D4)
    print(f"H1: Entrada = {h1_in:.2f}, Salida = {h1_out:.2f}, Balance = {h1_in - h1_out:.2f}")

    h2_in = value(S1H2) + value(S2H2)
    h2_out = value(H2D1) + value(H2D2) + value(H2D3) + value(H2D4) + value(H2D5)
    print(f"H2: Entrada = {h2_in:.2f}, Salida = {h2_out:.2f}, Balance = {h2_in - h2_out:.2f}")

    h3_in = value(S1H3) + value(S2H3)
    h3_out = value(H3D2) + value(H3D3) + value(H3D4) + value(H3D5)
    print(f"H3: Entrada = {h3_in:.2f}, Salida = {h3_out:.2f}, Balance = {h3_in - h3_out:.2f}")

    # Identificar restricciones de capacidad activas
    print("\n" + "-"*80)
    print("RESTRICCIONES DE CAPACIDAD ACTIVAS (en el límite):")
    print("-"*80)

    capacities = {
        'S1H1': (value(S1H1), 600),
        'S1H2': (value(S1H2), 400),
        'S1H3': (value(S1H3), 300),
        'S2H1': (value(S2H1), 500),
        'S2H2': (value(S2H2), 300),
        'S2H3': (value(S2H3), 400),
        'H1D1': (value(H1D1), 250),
        'H1D2': (value(H1D2), 300),
        'H1D3': (value(H1D3), 250),
        'H1D4': (value(H1D4), 300),
        'H2D1': (value(H2D1), 150),
        'H2D2': (value(H2D2), 200),
        'H2D3': (value(H2D3), 300),
        'H2D4': (value(H2D4), 350),
        'H2D5': (value(H2D5), 250),
        'H3D2': (value(H3D2), 150),
        'H3D3': (value(H3D3), 200),
        'H3D4': (value(H3D4), 250),
        'H3D5': (value(H3D5), 250)
    }

    active_constraints = []
    for var_name, (var_value, capacity) in capacities.items():
        if abs(var_value - capacity) < 0.01:  # Tolerancia para considerar activa
            active_constraints.append((var_name, var_value, capacity))
            print(f"{var_name}: {var_value:.2f} / {capacity} (ACTIVA)")

    if not active_constraints:
        print("No hay restricciones de capacidad activas en la solución óptima.")

    return prob, value(prob.objective)


def compare_solutions(cost_without, cost_with):
    """
    Compara las soluciones con y sin restricciones de capacidad
    """
    print("\n\n" + "="*80)
    print("ANÁLISIS COMPARATIVO DE SOLUCIONES")
    print("="*80)

    print(f"\nCosto Óptimo SIN restricciones de capacidad: Z = {cost_without:.2f}")
    print(f"Costo Óptimo CON restricciones de capacidad: Z = {cost_with:.2f}")

    difference = cost_with - cost_without
    if difference > 0:
        percentage = (difference / cost_without) * 100
        print(f"\nIncremento en el costo: {difference:.2f} ({percentage:.2f}%)")
        print("\nCONCLUSIÓN:")
        print("Las restricciones de capacidad AUMENTAN el costo total de la solución.")
        print("Esto se debe a que las capacidades limitan el uso de rutas más económicas,")
        print("forzando el uso de rutas alternativas más costosas para satisfacer la demanda.")
    elif difference < 0:
        percentage = (abs(difference) / cost_without) * 100
        print(f"\nReducción en el costo: {abs(difference):.2f} ({percentage:.2f}%)")
        print("\nCONCLUSIÓN:")
        print("Las restricciones de capacidad REDUCEN el costo total.")
        print("(Esto es inusual y sugiere que las capacidades no están activas)")
    else:
        print("\nNo hay diferencia en el costo.")
        print("\nCONCLUSIÓN:")
        print("Las restricciones de capacidad NO afectan la solución óptima.")
        print("La solución sin capacidades ya respeta todos los límites de capacidad.")

    print("\n" + "="*80)


def main():
    """
    Función principal que ejecuta ambas versiones del problema
    """
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*15 + "PROBLEMA DE TRANSBORDO CON CAPACIDADES" + " "*24 + "║")
    print("║" + " "*25 + "OPTIMIZACIÓN CON PuLP" + " "*32 + "║")
    print("╚" + "="*78 + "╝")

    # Resolver sin capacidades
    prob1, cost_without = solve_transshipment_without_capacity()

    # Resolver con capacidades
    prob2, cost_with = solve_transshipment_with_capacity()

    # Comparar soluciones
    compare_solutions(cost_without, cost_with)

    print("\n" + "="*80)
    print("EJECUCIÓN COMPLETADA")
    print("="*80)


if __name__ == "__main__":
    main()
