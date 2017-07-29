# reuters_rcv1_v2
Descargar archivos reuters_rcv1_v2 desde Cardano.


## Instrucciones
```python
import reuters as r
data,label = r.load_data(subset='train',label='topics')
```
Retorna 2 numpy arrays del tipo object. El primero posee los textos, el segundo los labels pedidos.
