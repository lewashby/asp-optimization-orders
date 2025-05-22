# Addressing marketplace logistic tasks in answer set programming

Marketplaces bring together products from multiple providers and automatically manage orders that involve several suppliers. We document the use of Answer Set Programming to automatically choose products from various warehouses within a marketplace network to fulfill a specified order. The proposed solution seamlessly adapts to various objective functions utilized at different stages of order management, leading to cost savings for customers and simplifying logistics for both the marketplace and its suppliers.

[![DOI: 10.3233/IA-240024](https://img.shields.io/badge/10.3233%2FIA-240024-blue)](https://doi.org/10.3233/IA-240024)

## ASP split orders optimization experiments

**[Install poetry](https://python-poetry.org/docs/)**

```cmd
    poetry install
    cd asp_optimization_orders
    poetry run python main.py -h
```

## Single Test

```cmd
    poetry run python main.py --one-time
```

## Multiple Tests

```cmd
    poetry run python main.py --test -r 100 -s 4
```

