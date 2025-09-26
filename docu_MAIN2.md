Qué hace cada variable 

    DEBOUNCE_MS: ignora rebotes eléctricos durante X ms tras detectar un flanco válido.

    COOLDOWN_MS: impone un tiempo mínimo entre “timbrazos” (evita spam por toqueteo).

    last_edge: timestamp del último flanco aceptado (sirve para el debounce).

    pending: la ISR marca que hubo pulsación; el bucle la procesa.

    locked: bloquea nuevos eventos hasta que sueltes el botón y pase el cooldown.

    last_fire: momento del último “RING” real.

Cómo ajustarlo

    Más sensible → bajá DEBOUNCE_MS a 20–25 ms.

    Menos spam → subí COOLDOWN_MS (p. ej., 2000–3000 ms).

    Si usás pull-up interno: USE_INT_PULL=True y no pongas la 10 kΩ externa.

    Si el hardware sigue rebotando, agregá 100 nF entre GP0 y GND.