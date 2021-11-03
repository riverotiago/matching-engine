# matching-engine
 
> Matching Engine simples, ferramenta CLI para realizar cruzamentos de ações.
> 

## Pré-requisitos

* Python 3.9

## Instalando 

Para instalar

```
git clone https://github.com/riverotiago/matching-engine.git
```

## Usando 

Para rodar este projeto, abrir um terminal na raiz do repositório.

```
python main.py
```

## Comandos

Há dois tipos de ordens disponíveis: limit/market
Limit coloca uma ordem passiva com preço limite para compra ou venda. (Não geram trades, para simplificação do programa)
Market coloca uma ordem de execução imediata. (Geram trades, com preenchimentos completos ou parciais ao melhor preço disponível)

```
limit <buy|sell> <price> <qty>
market <buy|sell> <qty> 
```

Uma mensagem é imprimida sempre que houver um trade 
```
Trade, price: <price>, qty: <qty>
```

### Exemplo
```
>>> limit buy 20 200
>>> market sell 100
Trade, price: 20.0, qty: 100.0
```

