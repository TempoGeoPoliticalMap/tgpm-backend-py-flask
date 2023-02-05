# TGMP Backend Python



## Development Guidelines

The Backend is Python-Flask openapi-server automatically generated from the OpenAPI Specification and extended with custom logic (services, mappers, persistence). So it's important to follow the steps described below in order to make changes to the code in the right way.


### 1. Update OpenAPI Spec

The file is a located in the `openapi` directory.

Latest version of the API Spec can be found here: [/tempogeopolitical-map/tgpm-openapi](https://gitlab.com/tempogeopolitical-map/tgpm-openapi), `main` branch

### 2. Generate openapi-server from the OpenAPI Spec

1. Navigate to the `root` directory
2. Execute `scripts/openapi.sh`
3. It will create files in the `scr/@generated` with models, controllers, services and aux. files (requirements, Dockerfile, Readme etc.)

### 3. Merge generated sources with the existing ones

1. If you use IntelliJ IDEA, you can use "Compare With..." feature to compare `src/@generated` with `src/main`
2. Review the differences one by one and update `src/main` with changes
   1. Pay special attention to
      1. services -- they are already modified, do don't remove custom implementation
      2. persistence -- this directory is NOT generated, it's 100% custom
      3. Dockerfile -- it may be already updated for the specific deployment
      4. requirements -- they may have additional elements added for the custom implementation
      5. setup -- it may contain added parts
3. After the updates are done, verify that the app works