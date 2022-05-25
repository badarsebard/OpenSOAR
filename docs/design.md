# high level
- case management
- investigation
- forensics
- threat intel integration

# soar components
- ui for analysis (customizable)
    - dashboard for reviewing alerts
    - commandline for executing actions
        - with or without context of an alert
    - war room for collaboration/workspace 
      - ?: is this actually needed, maybe just integrations with slack etc.
- ~~script editor~~ git integration
- workflows and editor
- integrations
    - plugin framework?
    - communication
      - email
      - slack
      - etc
    - alert sources
    - api actions
- incident/event management
- threat intel

## web app
- svelte kit run on node
- fastapi app for api

## external database and object storage

## indexed search?
- elasticsearch probably

## object storage
- minio, maybe

## workflow executor
- argo

# update
need to start decoupling some components. in particular, the database and object storage components, as well as probably the argo deployment. first this will simplify the amount of development that has to be done because a smooth deployment onto a k8s cluster won't include some of these complicated setups (e.g. postgres) when in production there are likely better options (operators or cloud-native services like RDS). second, it will allow for more general component integration such as generic relational database support (postgres, mysql, maria, oracle, etc.) and a s3-compliant object store.