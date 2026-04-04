---
name: gatling-blazemeter-artifact
description: >-
  Builds the fat JAR artifact for BlazeMeter / Taurus Gatling executor (target/gatling-blazemeter.jar)
  from a Maven Gatling project. Use when the user mentions BlazeMeter, Taurus, gatling-blazemeter.jar,
  packaging Gatling for cloud load tests, or shipping a Gatling simulation as a single executable JAR.
license: Apache-2.0
---

# Artifact Gatling pour BlazeMeter (Maven)

## Objectif

Produire **`target/gatling-blazemeter.jar`** : simulation + Gatling + dépendances, consommable par **Taurus** (`executor: gatling`, `script: target/gatling-blazemeter.jar`) sur **BlazeMeter Cloud**.

## Prérequis projet

1. **Simulation et ressources en `src/main/`** (pas seulement `src/test/`), sinon le JAR shaded ne contient pas la classe ni les CSV embarqués.
2. **Dépendance Gatling** en scope **`compile`** (ex. `io.gatling.highcharts:gatling-charts-highcharts`), alignée sur la version Taurus (`modules.gatling.version` dans le YAML).
3. **`maven-shade-plugin`** configuré pour écrire **`${project.build.directory}/gatling-blazemeter.jar`** avec `shadedArtifactAttached=false`, `ServicesResourceTransformer`, `ManifestResourceTransformer` (`mainClass`: `io.gatling.app.Gatling`). Modèle détaillé : [reference.md](reference.md).

Si le `pom.xml` n’a pas encore ce packaging, l’ajouter en s’inspirant de [reference.md](reference.md), puis lancer le build.

## Build (à exécuter)

Depuis la racine du module Maven Gatling :

```bash
./mvnw clean package -DskipTests
```

Sans wrapper :

```bash
mvn clean package -DskipTests
```

**Sortie attendue** : `target/gatling-blazemeter.jar` (taille typique ~50 Mo selon deps).

## Vérification rapide

```bash
ls -lh target/gatling-blazemeter.jar
jar tf target/gatling-blazemeter.jar | grep -E 'Simulation\.class|\.csv$' | head
```

La classe de simulation doit apparaître sous forme `com/.../MaSimulation.class` ; les feeders sous `guest.csv`, etc., si placés dans `src/main/resources`.

## Taurus / BlazeMeter

- Fichier **`blazemeter.yml`** à côté du module (ou chemin adapté après upload).
- **`scenarios.*.simulation`** : nom canonique de la classe `Simulation`.
- **`scenarios.*.script`** : `target/gatling-blazemeter.jar` (relatif au répertoire de travail de Taurus).
- **`modules.gatling.version`** : même famille majeure que `gatling.version` du `pom.xml` ; pour Gatling **≥ 3.11**, la version doit être fixée explicitement dans le YAML (voir doc Taurus [Gatling executor](https://gettaurus.org/docs/Gatling/)).

Secrets et surcharge JVM : `modules.gatling.java-opts` ou `scenarios.*.properties` (`-Dx-api-key=…`, etc.) — ne pas committer de secrets.

## Intégration CI / ZIP BlazeMeter

- Soit build sur les agents BlazeMeter : répertoire = module Maven, commande = `./mvnw clean package -DskipTests`, entrée Taurus = `blazemeter.yml`.
- Soit ZIP du module **après** build local pour inclure `target/gatling-blazemeter.jar`.

## Après modification des skills dans ce dépôt (extension VSIX)

Depuis la racine du repo **perf-tool-gatling-ai-extensions** :

```bash
./scripts/bundle-vsix-pack.sh
```

Puis `npm run package` dans `vscode-gatling-cursor-pack` pour régénérer le VSIX incluant `.cursor/skills/gatling-blazemeter-artifact/`.
