# UML — Fontes e Exportação

Fontes PlantUML:
- `use-case.puml`: casos de uso principais
- `component.puml`: visão de componentes
- `activity.puml`: fluxo de atendimento

Exportar para PNG:

- Docker (recomendado):
```powershell
docker run --rm -v "${PWD}\docs\uml:/data" ghcr.io/plantuml/plantuml -tpng /data/*.puml
```

- VS Code: extensão “PlantUML” → Export Current Diagram

