# DOC-001 - Execution evidence

Environment: Windows-11-10.0.26200-SP0; Python 3.12.0

## C:\Python312\python.exe -m unittest discover -s tests -q

Started: 2026-11-06T09:51:12+01:00; exit code: 0

```text
----------------------------------------------------------------------
Ran 227 tests in 7.570s

OK (skipped=2)
BLOCKED: Gates 1/2/3 y owner no aprobados.
 - gate1: isolation below minimum
BLOCKED: Gate 1 sin PASS independiente documentado.
BLOCKED: Gates 1/2/3 y owner no aprobados.
 - owner approval missing identity/date
BLOCKED: Gates 1/2/3 y owner no aprobados.
 - owner approval missing identity/date
BLOCKED: Gates 1/2/3 y owner no aprobados.
 - owner approval missing identity/date
BLOCKED: Gates 1/2/3 y owner no aprobados.
 - gate1: isolation below minimum
BLOCKED: Gate 1 sin PASS independiente documentado.
BLOCKED: Gates 1/2/3 y owner no aprobados.
 - owner approval missing identity/date
BLOCKED: Gates 1/2/3 y owner no aprobados.
 - owner approval missing identity/date
BLOCKED: Gates 1/2/3 y owner no aprobados.
 - owner approval missing identity/date
BLOCKED: Gates 1/2/3 y owner no aprobados.
 - gate1: isolation below minimum
BLOCKED: Gate 1 sin PASS independiente documentado.
BLOCKED: Gates 1/2/3 y owner no aprobados.
 - owner approval missing identity/date
BLOCKED: Gates 1/2/3 y owner no aprobados.
 - owner approval missing identity/date
BLOCKED: Gates 1/2/3 y owner no aprobados.
 - owner approval missing identity/date
BLOCKED: Gates 1/2/3 y owner no aprobados.
 - gate1: isolation below minimum
BLOCKED: Gate 1 sin PASS independiente documentado.
BLOCKED: Gates 1/2/3 y owner no aprobados.
 - owner approval missing identity/date
BLOCKED: Gates 1/2/3 y owner no aprobados.
 - owner approval missing identity/date
BLOCKED: Gates 1/2/3 y owner no aprobados.
 - owner approval missing identity/date
BLOCKED: Gates 1/2/3 y owner no aprobados.
 - gate1: isolation below minimum
BLOCKED: Gate 1 sin PASS independiente documentado.
BLOCKED: Gates 1/2/3 y owner no aprobados.
 - owner approval missing identity/date
BLOCKED: Gates 1/2/3 y owner no aprobados.
 - owner approval missing identity/date
BLOCKED: Gates 1/2/3 y owner no aprobados.
 - owner approval missing identity/date

```

## C:\Python312\python.exe scripts/quality_cli.py validate

Started: 2026-11-06T09:51:20+01:00; exit code: 0

```text
OK � estructura consistente. NO es certificaci�n de Quality ni comprobaci�n de identidades.

```

## git diff --check

Started: 2026-11-06T09:51:20+01:00; exit code: 0

```text

```
