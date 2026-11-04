# Simulação de rollback

## Como o versionamento funciona
- Usamos versionamento semântico: `vMAJOR.MINOR.PATCH` (ex: v1.0.0).
- Criar uma tag `vX.Y.Z` dispara o pipeline de CD, que publica a imagem no GitHub Container Registry (GHCR) com a tag `X.Y.Z` e faz o deploy no ambiente de homologação.
- O endpoint `/version` mostra qual versão está em execução.
- O deploy e o rollback sempre usam a versão explícita da imagem, nunca a tag `latest`.

## Linha do tempo da simulação

| Etapa | Horário | Versão | Resultado | Evidência |
|---|---|---|---|---|
| 1. Deploy da versão estável | 19:18 | v1.0.0 | Sucesso | https://github.com/Fernanda031/Projeto-devops/actions/runs/41729595097 |
| 2. Deploy da versão com falha proposital | 22:52 | v1.0.1 | Falhou no smoke test (/health retornou 500) | https://github.com/Fernanda031/Projeto-devops/actions/runs/41756961411 |
| 3. Rollback para a versão estável | 22:56 | 1.0.0 | Sucesso, /version retornou 1.0.0 | https://github.com/Fernanda031/Projeto-devops/actions/runs/41757385674 |

## O que aconteceu
1. A v1.0.0 foi publicada no GHCR e implantada em homologação com sucesso.
2. Criamos a v1.0.1 com uma falha proposital no endpoint /health, numa branch de simulação que nunca foi mergeada na main, para manter a main sempre estável.
3. O pipeline publicou a imagem, mas o deploy em homologação falhou no smoke test pós-deploy, porque o /health respondeu erro 500. A versão com falha não foi considerada saudável.
4. Executamos o workflow manual de Rollback informando a versão 1.0.0.
5. O ambiente voltou a funcionar, e o /version confirmou que a versão 1.0.0 estava em execução.

## Como fazer um rollback
1. Abrir a aba Actions do repositório.
2. Escolher o workflow **Rollback** e clicar em **Run workflow**.
3. Informar a versão estável a restaurar (ex: 1.0.0) e executar.
4. Conferir no log do passo "Smoke test pós-rollback" que o /version mostra a versão informada.

## Lições aprendidas
- O smoke test pós-deploy detectou a falha antes de a versão ser considerada saudável.
- Como as imagens ficam versionadas no registry, voltar para uma versão anterior é rápido e não exige novo build.
- A tag v1.0.1 permanece no repositório como registro da simulação. A correção definitiva sairia como v1.0.2.