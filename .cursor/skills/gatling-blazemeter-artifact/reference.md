# Référence — `pom.xml` (shade → `gatling-blazemeter.jar`)

## Dépendance Gatling (compile)

```xml
<dependency>
  <groupId>io.gatling.highcharts</groupId>
  <artifactId>gatling-charts-highcharts</artifactId>
  <version>${gatling.version}</version>
</dependency>
```

## `maven-shade-plugin` (exemple)

À placer dans `<build><plugins>` ; ajuster `gatling.version` / plugin compiler selon le projet.

```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-shade-plugin</artifactId>
  <version>3.6.0</version>
  <executions>
    <execution>
      <phase>package</phase>
      <goals>
        <goal>shade</goal>
      </goals>
      <configuration>
        <shadedArtifactAttached>false</shadedArtifactAttached>
        <outputFile>${project.build.directory}/gatling-blazemeter.jar</outputFile>
        <createDependencyReducedPom>false</createDependencyReducedPom>
        <transformers>
          <transformer implementation="org.apache.maven.plugins.shade.resource.ServicesResourceTransformer"/>
          <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
            <mainClass>io.gatling.app.Gatling</mainClass>
          </transformer>
        </transformers>
        <filters>
          <filter>
            <artifact>*:*</artifact>
            <excludes>
              <exclude>META-INF/*.SF</exclude>
              <exclude>META-INF/*.DSA</exclude>
              <exclude>META-INF/*.RSA</exclude>
              <exclude>META-INF/LICENSE*</exclude>
              <exclude>META-INF/NOTICE*</exclude>
              <exclude>module-info.class</exclude>
            </excludes>
          </filter>
        </filters>
      </configuration>
    </execution>
  </executions>
</plugin>
```

## `gatling-maven-plugin`

Conserver `simulationClass` pointant vers la classe dans `src/main/java` :

```xml
<plugin>
  <groupId>io.gatling</groupId>
  <artifactId>gatling-maven-plugin</artifactId>
  <version>${gatling-maven-plugin.version}</version>
  <configuration>
    <simulationClass>com.example.MySimulation</simulationClass>
  </configuration>
</plugin>
```

## Exemple minimal `blazemeter.yml`

```yaml
execution:
  - executor: gatling
    scenario: my_sim
    concurrency: 1
    ramp-up: 30s
    hold-for: 10m

scenarios:
  my_sim:
    simulation: com.example.MySimulation
    script: target/gatling-blazemeter.jar

modules:
  gatling:
    version: 3.15.0
```
