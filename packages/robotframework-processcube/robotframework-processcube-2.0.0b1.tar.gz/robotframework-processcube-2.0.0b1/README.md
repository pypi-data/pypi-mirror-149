# Verwendung des Robot Framework mit der 5Minds-Engine

- [Voraussetzung](#voraussetzung)
- [Verwendung](#verwendung)
  * [Allgmeine Informatione](#allgemeine-informationen)
  * [Info von der 5Minds-Engine abrufen](#info-von-der-5minds-engine-abrufen)
  * [BPMN-Datei in 5Minds-Engine laden](#bpmn-datei-in-5minds-engine-laden)
  * [Prozessmodell starten](#prozessmodell-starten)
  * [Ergebnisse von beendeten Prozessen abfragen](#ergebnisse-von-beendeten-prozessen-abfragen)
  * [Verarbeiten von Aktivitäten](#verarbeiten-von-aktivitaten)
    + [Umgang mit External-Tasks](#umgang-mit-external-tasks)
    + [Umgang mit Benutzer-Tasks (User-Tasks)](#umgang-mit-benutzer-tasks-user-tasks)
    + [Umgang mit manuellen Tasks (Manual-Tasks)](#umgang-mit-manuellen-tasks-manual-tasks)
    + [Umgang mit untypisierten Tasks (Empty-Tasks)](#umgang-mit-untypisierten-tasks-empty-tasks)
  * [Umgang mit Ereignissen (Events)](#umgang-mit-ereignissen-events)
    + [Signale](#signale)
    + [Nachrichten (Messages)](#nachrichten-messages)
    
## Voraussetzung

Um Tests auf Basis der [Robot Framework](https://robotframework.org/) für die BPMN-basierte-Workflowengine
[5Minds-Engine](https://www.5minds.de/processcube/) zu erstellen, sind folgende Voraussetzung erforderlich:
- 5Minds-Studio in der stabilen Version ist installiert
- 5Minds-Studio ist gestartet
- 5Minds-Engine ist durch das Studio auf dem Port `56000`gestartet

Alternative kann Docker für die 5Minds-Engine verwendet werden, dann sind folgende Vorausetzungen notwendig:
- Docker-Desktop ist installiert und gestartet
- Zugang zum Internet für den Download des Image [5minds/atlas_engine_fullstack_server](https://hub.docker.com/r/5minds/atlas_engine_fullstack_server)

Für die Ausführung von Tests ist dann noch folgende Voraussetzung notwendig:
- Python in der Version `>=3.7.x` ist installiert und im Pfad konfiguriert
- Robot-Framework für die 5Minds-Engine ist installiert `pip install robotframework-processcube`

Für die Bearbeitung ist [VS Code](https://code.visualstudio.com/) und der [Robot Framework Language Server](https://marketplace.visualstudio.com/items?itemName=robocorp.robotframework-lsp) hilfreich.

## Verwendung

Um die *Keywords* für die Interaktion mit der 5Minds-Engine verwenden zu können, ist die 
Library ProcessCubeLibrary einzubinden.
Für die Verwendung mit dem 5Minds-Studio (ohne Docker) ist die URL für die Engine mit
dem Paramter `engine_url` zu konfiguieren, dies ist für die stabile Version der
Studio-Engine `http://localhost:56000`.

Mit dem 5Minds-Studio ist folgende Verwendung zu verwenden.
```robotframework
*** Settings ***
Library         ProcessCubeLibrary     engine_url=http://localhost:56000

```

Für die weiteren Beispiele wird Docker verwendet und dann ist folgende Einstellung zu ändern:
```robotframework
*** Variables ***
&{DOCKER_OPTIONS}            auto_remove=False

*** Settings ***
Library         ProcessCubeLibrary     self_hosted_engine=docker    docker_options=${DOCKER_OPTIONS}
```

Die Engine im Docker-Container wird standardmäßig mit dem Port `55000` gestartet. Die URL zum
Einbinden ins Studio ist also `http://localhost:55000`.


### Allgmeine Informationen

Um den Aufruf der nachfolgenden Keywords gegenüber Fehlern etwas robuster zu gestalten, kann global oder bei jeden Keyword
gesteuert werden:
- max_retries: Anzahl der Wiederholungen, bevor ein Keyword abgebrochen wird.
- delay: Verzögerung in Sekunden, die zwischen den Wiederholungen gewartet wird.
- backoff_factor: Faktor, mit dem die Wiederholungszeit vergrößert wird.

### Info von der 5Minds-Engine abrufen

Um zwei verschiedene Engines gleichzeitig verwenden zu können, kann die Verwendung der Library mit `WITH NAME <ein Name>`
benannt werden. Danach ist die Verwendung der Keywords mit einem entsprechenenden Namen zu konkretisieren.

Im folgenden Beispiel wird `Get Engine Info` einmal für die `Engine01` und einmal für die `Engine02` abgerufen.

```robotframework
*** Variables ***
&{DOCKER_OPTIONS}            auto_remove=False

*** Settings ***
Library         ProcessCubeLibrary    self_hosted_engine=docker    docker_options=${DOCKER_OPTIONS}    WITH NAME    Engine01
Library         ProcessCubeLibrary    self_hosted_engine=docker    docker_options=${DOCKER_OPTIONS}    WITH NAME    Engine02

*** Tasks ***
Engine info from Engine01
    ${INFO}=    Engine01.Get Engine Info
    Log    ${INFO}


Engine info from Engine02
    ${INFO}=    Engine02.Get Engine Info
    Log    ${INFO}
```


### BPMN-Datei in 5Minds-Engine laden

Zuerst ist ein BPMN-Diagram (z.B. [`processes/hello_minimal.bpmn`](processes/hello_minimal.bpmn) zu erstellen.

Mit dem Keyword `Deploy Processmodel` und der Angabe des Dateipfades wird das BPMN-Diagram in die 5Minds-Engine geladen.

```robotframework
*** Variables ***
&{DOCKER_OPTIONS}            auto_remove=False

*** Settings ***
Library         ProcessCubeLibrary     self_hosted_engine=docker    docker_options=${DOCKER_OPTIONS}

*** Tasks ***
Successfully deploy
    Deploy Processmodel    processes/hello_minimal.bpmn
```

### Prozessmodell starten

Wie unter [BPMN-Datei in 5Minds-Engine laden](#bpmn-datei-in-5minds-engine-laden) beschrieben, muss die BPMN-Datei
vorhanden sein.

Mit dem Keyword `Start Processmodel` und der Angabe der Process ID `hello_minimal` wird eine Prozessinstanz gestartet.

```robotframework
*** Variables ***
&{DOCKER_OPTIONS}            auto_remove=False

*** Settings ***
Library         ProcessCubeLibrary     self_hosted_engine=docker    docker_options=${DOCKER_OPTIONS}
Library    Process

*** Tasks ***
Successfully deploy
    Deploy Processmodel    processes/hello_minimal.bpmn

Start process model
    Start Processmodel     hello_minimal
```

### Ergebnisse von beendeten Prozessen abfragen

Nachdem der Prozess gestartet wurde, kann mit dem Keyword `Get Processinstance Result` das Ergebnis
der Prozessinstanz abgefragt werden.

```robotframework
*** Variables ***
&{DOCKER_OPTIONS}            auto_remove=False
${CORRELATION}               -1


*** Settings ***
Library         ProcessCubeLibrary     self_hosted_engine=docker    docker_options=${DOCKER_OPTIONS}
Library         Collections


*** Tasks ***
Successfully deploy
    Deploy Processmodel    processes/hello_minimal.bpmn

Start process model
    &{PAYLOAD}=              Create Dictionary     foo=bar    hello=world
    ${PROCESS_INSTANCE}=     Start Processmodel    hello_minimal    ${PAYLOAD}
    Set Suite Variable       ${CORRELATION}        ${PROCESS_INSTANCE.correlation_id}
    Log                      ${CORRELATION}

Get the process instance
    ${RESULT}                Get Processinstance Result            correlation_id=${CORRELATION}
    Log                      ${RESULT}
```

### Verarbeiten von Aktivitäten

#### Umgang mit untypisierten Tasks (Empty-Tasks)

Um bei der Entwicklung von Aktivitäten mit noch untypisierten Tasks 
zu beginnen, stehen die Keywords `Get Empty Task By` fürs Laden und 
`Finish Empty Task` zum Abschließen zur Verfügung.

Für diesen Test wird eine andere BPMN-Datei verwendet `hello_empty_task.bpmn`.

```robotframework
*** Variables ***
&{DOCKER_OPTIONS}            auto_remove=False
${CORRELATION}               -1


*** Settings ***
Library         ProcessCubeLibrary     self_hosted_engine=docker    docker_options=${DOCKER_OPTIONS}
Library         Collections


*** Tasks ***
Successfully deploy
    Deploy Processmodel    processes/hello_empty_task.bpmn

Start process model
    &{PAYLOAD}=              Create Dictionary     foo=bar    hello=world
    ${PROCESS_INSTANCE}=     Start Processmodel    hello_empty_task    ${PAYLOAD}
    Set Suite Variable       ${CORRELATION}        ${PROCESS_INSTANCE.correlation_id}
    Log                      ${CORRELATION}

Handle empty task by correlation_id
    Log                      ${CORRELATION}
    ${EMPTY_TASK}            Get Empty Task By                     correlation_id=${CORRELATION}
    Log                      ${EMPTY_TASK.empty_task_instance_id}
    Finish Empty Task        ${EMPTY_TASK.empty_task_instance_id}


Get the process instance
    ${RESULT}                Get Processinstance Result            correlation_id=${CORRELATION}
    Log                      ${RESULT}
```

#### Umgang mit manuellen Tasks (Manual-Tasks)

Als Basis für den Umgang mit manuellen Task wird die BPMN-Datei 
`hello_manual_task.bpmn` benötigt.

Für das Laden vom manuellen Taak dient das Keyword `Get Manual Task By` und 
für das Beenden `Finish Manual Task`.

```robotframework
*** Variables ***
&{DOCKER_OPTIONS}            auto_remove=False
${CORRELATION}               -1


*** Settings ***
Library         ProcessCubeLibrary     self_hosted_engine=docker    docker_options=${DOCKER_OPTIONS}
Library         Collections


*** Tasks ***
Successfully deploy
    Deploy Processmodel    processes/hello_manual_task.bpmn

Start process model
    &{PAYLOAD}=              Create Dictionary     foo=bar    hello=world
    ${PROCESS_INSTANCE}=     Start Processmodel    hello_manual_task    ${PAYLOAD}
    Set Suite Variable       ${CORRELATION}        ${PROCESS_INSTANCE.correlation_id}
    Log                      ${CORRELATION}

Handle manual task by correlation_id
    Log                      ${CORRELATION}
    ${MANUAL_TASK}           Get Manual Task By                     correlation_id=${CORRELATION}
    Log                      ${MANUAL_TASK.manual_task_instance_id}
    Finish Manual Task       ${MANUAL_TASK.manual_task_instance_id}


Get the process instance
    ${RESULT}                Get Processinstance Result            correlation_id=${CORRELATION}
    Log                      ${RESULT}
```

#### Umgang mit Benutzer-Tasks (User-Tasks)

Um den Umgang mit Benutzer-Task zu testen ist die BPMN-Datei `hello_user_task.bpmn` notwendig.

Mit dem Keyword `Get User Task By` können User-Tasks geladen und 
mit dem Keyword `Finish User Task` beendet werden.

```robotframework
*** Variables ***
&{DOCKER_OPTIONS}            auto_remove=False
${CORRELATION}               -1


*** Settings ***
Library         ProcessCubeLibrary     self_hosted_engine=docker    docker_options=${DOCKER_OPTIONS}
Library         Collections


*** Tasks ***
Successfully deploy
    Deploy Processmodel    processes/hello_user_task.bpmn

Start process model
    &{PAYLOAD}=              Create Dictionary     foo=bar    hello=world
    ${PROCESS_INSTANCE}=     Start Processmodel    hello_user_task    ${PAYLOAD}
    Set Suite Variable       ${CORRELATION}        ${PROCESS_INSTANCE.correlation_id}
    Log                      ${CORRELATION}

Handle User Task by correlation_id
    Log                      ${CORRELATION}
    ${USER_TASK}             Get User Task By                      correlation_id=${CORRELATION}
    Log                      ${USER_TASK}
    Should Not Be Empty      ${USER_TASK.user_task_instance_id}
    Should Be Equal          ${USER_TASK.process_model_id}         hello_user_task

    &{ANSWER}=               Create Dictionary                     field_01=from user task    
    Finish User Task         ${USER_TASK.user_task_instance_id}    ${ANSWER}


Get the process instance
    ${RESULT}                Get Processinstance Result            correlation_id=${CORRELATION}
    Log                      ${RESULT}
```

#### Umgang mit External-Tasks

Um den Umgang mit External-Task zu testen ist die BPMN-Datei `hello_external_task.bpmn` notwendig.

Mit dem Keyword `Get External Task` können User-Tasks geladen und 
mit dem Keyword `Finish External Task` beendet werden.


```robotframework
*** Variables ***
&{DOCKER_OPTIONS}            auto_remove=False
${CORRELATION}               -1


*** Settings ***
Library         ProcessCubeLibrary     self_hosted_engine=docker    docker_options=${DOCKER_OPTIONS}
Library         Collections


*** Tasks ***
Successfully deploy
    Deploy Processmodel    processes/hello_external_task.bpmn

Start process model
    &{PAYLOAD}=              Create Dictionary     foo=bar    hello=world
    ${PROCESS_INSTANCE}=     Start Processmodel    hello_external_task    ${PAYLOAD}
    Set Suite Variable       ${CORRELATION}        ${PROCESS_INSTANCE.correlation_id}
    Log                      ${CORRELATION}

Handle External Task
    ${TASK}                  Get External Task                     topic=doExternal
    &{ANSWER}=               Create Dictionary                     external_field_01=The Value of field 1
    Log                      ${TASK.id}
    Finish External Task     ${TASK.id}                            ${ANSWER}


Get the process instance
    ${RESULT}                Get Processinstance Result            correlation_id=${CORRELATION}
    Log                      ${RESULT}
```

### Umgang mit Ereignissen (Events)

Beim Umgang mit Ereignissen, muss zwischen Signalen und Nachrichten unterschieden werden.

#### Signale

Um mit Ereignissen der BPMN-Module zu interagieren, muss die BPMN-Datei 
`hello_signal.bpmn` verwendet werden.

Das Keyword für das Auslösen von Signale ist `Send Signal`.


```robotframework
*** Variables ***
&{DOCKER_OPTIONS}            auto_remove=False
${CORRELATION}               -1


*** Settings ***
Library         ProcessCubeLibrary     self_hosted_engine=docker    docker_options=${DOCKER_OPTIONS}
Library         Collections


*** Tasks ***
Successfully deploy
    Deploy Processmodel    processes/hello_signal.bpmn

Start process model
    &{PAYLOAD}=              Create Dictionary     foo=bar    hello=world
    ${PROCESS_INSTANCE}=     Start Processmodel    hello_signal    ${PAYLOAD}
    Set Suite Variable       ${CORRELATION}        ${PROCESS_INSTANCE.correlation_id}
    Log                      ${CORRELATION}

Send Signal
    Send Signal              catch_signal                           delay=0.2     


Get the process instance
    ${RESULT}                Get Processinstance Result            correlation_id=${CORRELATION}
    Log                      ${RESULT}
```

#### Nachrichten (Messages)

Um mit Ereignissen der BPMN-Module zu interagieren, muss die BPMN-Datei 
`hello_message.bpmn` verwendet werden.

Das Keyword für das Auslösen von Signale ist `Send Message`.


```robotframework
*** Variables ***
&{DOCKER_OPTIONS}            auto_remove=False
${CORRELATION}               -1


*** Settings ***
Library         ProcessCubeLibrary     self_hosted_engine=docker    docker_options=${DOCKER_OPTIONS}
Library         Collections


*** Tasks ***
Successfully deploy
    Deploy Processmodel    processes/hello_message.bpmn

Start process model
    &{PAYLOAD}=              Create Dictionary     foo=bar    hello=world
    ${PROCESS_INSTANCE}=     Start Processmodel    hello_message    ${PAYLOAD}
    Set Suite Variable       ${CORRELATION}        ${PROCESS_INSTANCE.correlation_id}
    Log                      ${CORRELATION}

Send Message
    &{PAYLOAD}=              Create Dictionary        message_field1=Value field 1    message_field2=Value field 2
    Send Message             catch_message            ${PAYLOAD}                      delay=0.5


Get the process instance
    ${RESULT}                Get Processinstance Result            correlation_id=${CORRELATION}
    Log                      ${RESULT}
```
