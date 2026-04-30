def calcular_hunt():
    print("--- Calculadora de Lucro Tibia 2026 ---")
    
    # 1. Entrada de Dados da Hunt
    tempo_minutos = float(input("Duração da hunt (em minutos): "))
    loot_total = float(input("Loot total (em GPS): "))
    
    # 2. Custos de Imbuements (Ex: 3 slots Tier 3 custam aprox. 2kk por 20h)
    # Vamos calcular o custo por minuto (2kk / 1200 minutos)
    custo_imbuements_total = float(input("Custo total dos seus imbuements para 20h (em GPS): "))
    custo_imbue_por_minuto = custo_imbuements_total / 1200
    gasto_imbue_hunt = custo_imbue_por_minuto * tempo_minutos

    # 3. Gastos com Consumíveis (Potes, Runas, Food)
    gastos_potes = float(input("Total gasto em potions/runas nesta hunt (em GPS): "))
    
    # 4. Cálculos Finais
    custo_total = gastos_potes + gasto_imbue_hunt
    lucro_real = loot_total - custo_total
    lucro_por_hora = (lucro_real / tempo_minutos) * 60

    # Saída de Resultados
    print("\n" + "="*30)
    print(f"RESUMO DA HUNT")
    print(f"Tempo: {tempo_minutos} min")
    print(f"Gasto com Imbuements: {gasto_imbue_hunt:.2f} gps")
    print(f"Gasto Total (Potes + Imbue): {custo_total:.2f} gps")
    print(f"LUCRO REAL: {lucro_real:.2f} gps")
    print(f"LUCRO POR HORA: {lucro_por_hora:.2f} gps")
    print("="*30)

if __name__ == "__main__":
    calcular_hunt()
