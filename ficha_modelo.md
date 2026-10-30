# Ficha del modelo: riesgo de mala reseña en Olist

## 1. Para qué sirve y para qué no debe usarse
**Sirve para:** decidir a qué clientes llamar justo después de la entrega, dentro de la capacidad de llamar a 1 de cada 10 pedidos. Calcula la probabilidad de que el cliente deje una reseña de 1 o 2 estrellas.
**No debe usarse para:**
- Sancionar o despedir a vendedores: el modelo mide el riesgo de una queja, no la culpa de nadie.
- Exigir mejores resultados a los vendedores sin un análisis y una estrategia más profundos.
- Decidir a quién llamar sin que una persona revise el resultado.

## 2. Datos
- Origen: pedidos reales de Olist.
- Periodo: de 2016 a mayo de 2018. Los pedidos desde junio de 2018 no se usaron, porque se reservan para evaluar el modelo.
- Cantidad: 77,304 pedidos entregados y con reseña.
- Qué se excluyó y por qué: los pedidos no entregados, porque el modelo predice en el momento de la entrega y estos no tienen fecha de entrega; y todo lo que sale de la reseña (el texto, su largo y sus fechas), porque aparece después de la predicción y haría que el modelo pareciera mejor de lo que es.

## 3. Qué tan bien funciona
Se probó con los pedidos más recientes (el 20% final), que el modelo no vio al aprender, y se entrenó con el 80% más antiguo. Si se llama al 10% de pedidos con mayor riesgo:
- Con el modelo, unos 49 de cada 100 clientes llamados sí iban a dejar 1 o 2 estrellas.
- Ordenando solo por días de retraso, unos 38 de cada 100.
- Llamando al azar, unos 12 de cada 100.

Es decir, el modelo acierta cerca de 4 veces más que llamar al azar y mejora a la regla del retraso en unos 10 puntos.

## 4. Límites conocidos
- **Si casi no hay retrasos:** el retraso es la variable que más pesa en el modelo. En una prueba solo con los 14,514 pedidos que llegaron a tiempo o antes, el modelo acertó unos 27 de cada 100 llamados, contra unos 9 de cada 100 al azar en ese grupo. Sigue siendo mejor que el azar, pero con menos fuerza.
- **El periodo oculto (junio a agosto de 2018):** el modelo no lo vio, y la proporción de retrasos y de malas reseñas puede ser distinta. El rendimiento allí puede no coincidir con las cifras de esta ficha.
- **El umbral de riesgo alto (0.2515):** se calculó con los mismos pedidos con que se entrenó el modelo final, así que en pedidos nuevos marcará algo menos del 10% como riesgo alto.
- **La validación:** los mismos pedidos de prueba sirvieron para comparar los dos modelos y elegir el mejor, así que la cifra de 49 de cada 100 puede ser un poco optimista.

## 5. A quién afecta un error
- **Falso positivo** (se llama a alguien que estaba conforme): se gasta tiempo del equipo, que es limitado, y se puede molestar al cliente. Entre los llamados, algo más de la mitad no iba a dejar mala reseña.
- **Falso negativo** (no se llama a alguien que iba a quejarse): se pierde la oportunidad de resolver el problema, y la mala reseña daña la reputación del vendedor y de la plataforma.
- **Mal uso:** los vendedores pueden salir perjudicados si se los castiga por retrasos que no controlan (transportista, clima, distancia). Y como el modelo usa el estado del cliente, ciertas regiones podrían recibir más o menos llamadas de lo que corresponde.

## 6. Recomendación
- **Cómo usarlo:** como apoyo para priorizar las llamadas, no como una decisión automática.
- **Supervisión humana:** una persona del equipo decide a quién llamar y puede ignorar el aviso del modelo.
- **Cada cuánto revisarlo:** cada mes o cada trimestre, comparando cuántos de los clientes llamados terminaron realmente en 1 o 2 estrellas con las cifras de esta ficha. Si la cifra baja claramente, hay que reentrenar el modelo, y lo mismo si cambia algo grande en la operación (nueva logística, temporada alta).