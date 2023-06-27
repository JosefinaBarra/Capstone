import numpy as np

# PARAMETROS
replicas = 40
periodos = 365
politica = "(s,S)"

resultado_base = {}
productos = [2118]

sucursales = {
    885: {
        0: 0.4,
        1: 0.989,
        2: 2.1287,
        3: 1.4438,
        4: 6.0055,
        5: 3.9945,
        6: 1.1863,
        7: 3.3397,
        8: 0.926,
        9: 2.589,
        10: 4.4904
    },
    428: {
        2: 0.074,
        3: 0.018,
        4: 0.104,
        5: 0.04460094,
        6: 0.07671233,
        7: 0.06849315,
        8: 0.1013699,
        #9: 0.01826484,  # Demandas 0
        10: 0.07596513
    },
    637: {
        #4: 0.002739726,
        #5: 0.00548,
        #8: 0.002739,
        #10: 0.002739
    },
    2118: {
        0: 0.0444,
        #1: 0.0111,
        #2: 0.0137,
        3: 0.0164,
        4: 0.0383,
        5: 0.1068,
        6: 0.0411,
        7: 0.0438,
        8: 0.0493,
        9: 0.0411,
        10: 0.0657
    }
}

delta = 5
rango_s_S = 101
dif_s_S = 20
valores_politica = [
    (s, S) for s in range(0, rango_s_S, delta) for S in range(0, rango_s_S, delta) if s <= S if S-s <= dif_s_S
]
print(valores_politica)
valores_politica = np.array(valores_politica, 'i,i')
