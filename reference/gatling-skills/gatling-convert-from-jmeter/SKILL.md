---
name: gatling-convert-from-jmeter
description: Guide for converting Apache JMeter tests to Gatling.
license: Apache-2.0
user-invocable: true
---

# Convert a JMeter test plan to a Gatling simulation

## Instructions

### Step 1: Find input JMeter test plan

- Search for files with `.jmx` extension
- If several files found, ask user to specify one

### Step 2: Specify output

Either find an existing Gatling project or initialize a new Gatling project:

- Try to find an existing project with the /Gatling:gatling-detect-existing-project skill.
- If no existing project is found, offer to create a new one with the /Gatling:gatling-bootstrap-project skill.

### Step 3: Conversion

- Convert the JMeter test to a Gatling test written in the specified language.
- Write the output to the specified Gatling project.

#### ThreadGroup

Each ThreadGroup converts to a scenario.

IF `serialize_threadgroups` true:
- Chain the scenarios with `andThen`
ELSE:
- Just list the scenarios in the `setUp` block

#### Resource files

Files referenced in elements such as:

- CSVDataSet
- HTTPFileArgs

should be copied to the resources directory in the Gatling project.

#### Redirects

| JMeter                     | Gatling                     |
|----------------------------|-----------------------------|
| `follow_redirects` = true  | default setting, do nothing |
| `follow_redirects` = false | `disableFollowRedirect`     |

#### HTTP base URL: slash between host and path

JMeter uses `HTTPSampler.domain` for the **host only** and `HTTPSampler.path` for the rest, often **without** a leading `/` (e.g. `${Env_Version}/availabilities/...`).

Gatling resolves relative request paths against `http.baseUrl(...)`. If `baseUrl` is `https://host` (no trailing `/`) and the path is `load/v4/...` (no leading `/`), URL resolution can be **wrong** (path segments merge incorrectly with the authority).

**When converting, ensure exactly one `/` between the host and the first path segment:**

1. **Preferred (matches JMeter path shape):** set  
   `baseUrl("https://" + host + "/")`  
   i.e. the authority part ends with a **single** `/`, and keep paths as in JMeter (`load/v4/book-dine/...` without a leading `/`).  
   If User Defined Variables mirror JMeter (e.g. `BookDine_URL`), treat the value as **host only**; normalize in code: trim, strip accidental `http://`/`https://`, strip trailing `/`, then append one `/` when building `baseUrl`.

2. **Alternative:** `baseUrl("https://host")` **without** trailing slash and **prefix every relative path with `/`** (e.g. `"/" + envVersion + "/availabilities/..."`).

3. **Avoid:** `baseUrl("https://host")` combined with paths like `load/v4/...` (no leading `/`).

Absolute request URLs (full `https://...` per request) are unchanged. Apply the same rule for each logical “base host” used with relative paths.

#### CSVDataSet

`CSVDataSet` converts to a csv feeder.

IF there are several instances of `CSVDataSet` referencing the same file name:
- IF `shareMode.group`:
  - Create a new csv feeder for each scenario
  ELSE:
  - Create a single feeder and use it in each scenario

##### Maven `gatling:test`, `src/main/resources`, and `csv("…")` (Java)

Gatling’s `csv("guest.csv")` resolves files through Gatling’s own resource lookup (classpath / layout). With **`mvn gatling:test`**, data files copied only to **`src/main/resources`** (→ `target/classes`) are **not always visible** to that resolution, which can yield an **empty feeder** and session attributes missing (e.g. login JSON with null fields).

**Prefer one of:**

1. **Gatling / Maven convention:** put feeder files under **`src/test/resources`** (still copy or duplicate from JMeter as needed), then `csv("file.csv", separator)` as usual.
2. **Same artifact as the simulation:** load the file with **`SimulationClass.class.getResourceAsStream("/file.csv")`** (or without leading `/`), parse rows (semicolon/comma per JMeter), and use **`listFeeder(rows).circular()`** (or queue/random as needed). This matches **`mvn gatling:test`**, IDE runs, and a **shaded “fat” JAR** (e.g. BlazeMeter).
3. **Optional:** expose a JVM property (e.g. `guestFeedMaxLines`) to cap rows during local runs; document that it must be passed on the **same JVM as Gatling** (see below).

##### System properties when using `mvn gatling:test`

The Gatling Maven plugin runs simulations in a **forked JVM**. Properties set only on the Maven process (e.g. bare `mvn -Dx-api-key=… gatling:test`) are **not** seen by the simulation unless configured otherwise. Pass them via the plugin, for example:

`-Dgatling.jvmArgs=-Dx-api-key=SECRET -DnbVU=5`

(Adjust quoting on Windows shells.)

#### JMESPathExtractor

The `jmesPath` Gatling check extracts Strings, meaning that non String values get serialized back into JSON.
Using `findAll` with `jmesPath` is a mistake but you can tell Gatling the expected type with an extra step.
Note that the check will then fail is the actual value doesn’t match the expected type.

```
jmesPath("foo").ofString(),
jmesPath("foo").ofBoolean(),
jmesPath("foo").ofInt(),
jmesPath("foo").ofLong(),
jmesPath("foo").ofDouble(),
// JSON array
jmesPath("foo").ofList(),
// JSON object
jmesPath("foo").ofMap(),
// anything
jmesPath("foo").ofObject()
)
```

#### Functions

Some functions have variants that saves the result to a variable (e.g.: `__Random(0,10,myVar)`) but Gatling
Expression Language cannot save variables as a side effect.

IF a variable needs to be saved inside the function AND the function is used within an Expression Language
- Move the code to an exec block that allows saving variables

When parsing dates, use `java.time.format.DateTimeFormatter.ofPattern` with system default zone and store it
outside a function to avoid creation cost overhead.

For regular expression, use `java.util.regex.Pattern.compile` and store it outside a function to avoid creation cost
overhead.

Convert these functions to what JMeter uses under the hood:

- `changeCase` => `toUpperCase` or `toLowerCase` with `Locale.ROOT` or `capitalize`
- `digest` => `java.security.MessageDigest`
- `urldecode` => `java.net.URLDecoder.decode`
- `urlencode` => `java.net.URLEncoder.encode`
- `UUID` => `java.util.UUID.randomUUID`

Import `org.unbescape:unbescape` for the following escaping functions:

- `escapeHtml` => `HtmlEscape.escapeHtml5`
- `escapeXml` => `XmlEscape.escapeXml10`
- `unescape` => `JavaEscape.unescapeJava`
- `unescapeHtml` => `HtmlEscape.unescapeHtml`

### Step 4: Verify the code compiles

Use the build-tool skill if available.

### Step 5: Post conversion

After the conversion in Step 3, prompt the user for possible enhancements that are more idiomatic to Gatling.

IF `ThreadGroup.ramp_time` is 0 or 1:
- Suggest converting `rampUsers` to `atOnceUsers`
