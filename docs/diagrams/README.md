# Diagramas — Exportação para PNG

Para garantir visualização estável no GitHub, gere PNGs a partir das fontes.

Mermaid (recomendado para `architecture.mmd`):

```powershell
npx -y @mermaid-js/mermaid-cli -i docs/diagrams/architecture.mmd -o docs/diagrams/architecture.png
```

PlantUML (para arquivos em `docs/uml/*.puml`):

- Opção Docker:
```powershell
docker run --rm -v "${PWD}\docs\uml:/data" ghcr.io/plantuml/plantuml -tpng /data/*.puml
```

- Ou use a extensão “PlantUML” no VS Code para exportar para PNG.

