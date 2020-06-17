# Generic Mkdocs Site Builder

This tool uses one project_vars.yml file to specify all the notable modules in a multi-repository project to aggregate 
doc pages into one docsite. This site, once deployed in your cluster, can support users and developers of the project.

## Project Vars

The master config for detecting documentation files. In the yaml, you specify where to look and what to include for your
master docsite. Documents are concatenated to produce guides, one per module.

## Getting Started

Update the `repos` tag to capture the repositories that contain the relevant modules. Those module paths are used to 
discover and aggregate documentation according to which module the document is under.

The `repos` captures the hierarchy of documentation, some number of repos each containing some number of modules. A 
module is just a named path, it can be any valid path inside the repository. Repos takes a list of dictionaries. Each 
repo dictionary needs git_url, branch, and modules. The modules key holds a list of module dictionaries. Each module 
dictionary holds a name, path, links, and description (links and description are optional). Links takes a dictionary of 
link text to link url. The description is a string


## Running Locally

Once the project vars have been set and you have installed the prerequisites, you can run `python3 tasks/clone_repos.py` and then `python3 generate.py` to pull 
the repositories and generate the docsite. Since you have python installed you can simply run `cd site/ && python3 -m 
http.server` to serve the site locally.

```bash
pip3 install -r requirements.txt
python3 tasks/clone_repos.py -c project_vars.yml
python3 tasks/generate.py -c project_vars.yml
cd site
python3 -m http.server
```

And your docsite should be available at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Running in Docker

Also included in this project are two Dockerfiles which create docker containers to do all the lifting. The first, 
docs-site-builder runs the two python tasks, clone-repos and generate. The second, docs-service, serves the generated 
site directory.

From the root of this project, you could run:

```bash
docker build docker/docs-site-builder -t docs-site-builder

mkdir out
docker run -it --rm -v $PWD/my_vars.yml:/mkdocs-site/project_vars.yml -v $PWD/out/:/out docs-site-builder

mv out/site/ docker/docs-service/site/
docker build docker/docs-service -t docs-service

docker run -d -p 8080:80 docs-service
```

And your docsite should be available at [http://127.0.0.1:8080/](http://127.0.0.1:8080/)

## Example Project

The following is an example which builds a docsite for a project named 'KTIS'. It contains 4 repositories with the
microservices repository containing around 50 modules. Usually, the specified modules are microservices.

```yaml
---
project_name: KTIS

project_description: "
KTIS does good things.
"

working_directory: repos/

docs_locations:
  - readme
  - readme.md
  - Dockerfile
  - docker/
  - docker/build-image/
  - Jenkinsfile
  - docs/

repos:
  - git_url: git@bitbucket.org:radiantsolutions/microservices.git
    branch: ktis
    modules:
      - name: accessMS
        path: microservices/accessMS/
        description: "AccessMS does blah with blah for blah."
        links:
          swagger: "https://access.ktis.radiantblue.local/swagger-ui.html"

      - name: missionRepository
        path: microservices/missionRepository/

      - name: weatherRepository
        path: microservices/weatherRepository/

      - name: planningMS
        path: microservices/planningMS/

      - name: alertPollService
        path: microservices/alertPollService/

      - name: alertService
        path: microservices/alertService/

      - name: copDM
        path: microservices/copDM/

      - name: configService
        path: microservices/configService/

      - name: ephemerisRepository
        path: microservices/ephemerisRepository/

      - name: missionModel
        path: microservices/missionModel/

      - name: assetCommon
        path: microservices/assetCommon/

      - name: alertModel
        path: microservices/alertModel/

      - name: accessCommon
        path: microservices/accessCommon/

      - name: discoveryService
        path: microservices/discoveryService/

      - name: assetRepository
        path: microservices/assetRepository/

      - name: opGenCommon
        path: microservices/opGenCommon/

      - name: geometricIntersectionMS
        path: microservices/geometricIntersectionMS/

      - name: weatherDM
        path: microservices/weatherDM/

      - name: workflowModel
        path: microservices/workflowModel/

      - name: managerMS
        path: microservices/managerMS/

      - name: geometricIntersectionModel
        path: microservices/geometricIntersectionModel/

      - name: userRepository
        path: microservices/userRepository/

      - name: ephemerisMS
        path: microservices/ephemerisMS/

      - name: targetRepository
        path: microservices/targetRepository/

      - name: terrainMS
        path: microservices/terrainMS/

      - name: geometricIntersectionRepository
        path: microservices/geometricIntersectionRepository/

      - name: targetModel
        path: microservices/targetModel/

      - name: terrainModel
        path: microservices/terrainModel/

      - name: userService
        path: microservices/userService/

      - name: commonMS
        path: microservices/commonMS/

      - name: planningModel
        path: microservices/planningModel/

      - name: swaggerCommon
        path: microservices/swaggerCommon/

      - name: weatherParser
        path: microservices/weatherParser/

      - name: workflowMS
        path: microservices/workflowMS/

      - name: assetModel
        path: microservices/assetModel/

      - name: targetMS
        path: microservices/targetMS/

      - name: opGenService
        path: microservices/opGenService/

      - name: ephemerisModel
        path: microservices/ephemerisModel/

      - name: airborneAccessMS
        path: microservices/airborneAccessMS/

      - name: alertRepository
        path: microservices/alertRepository/

      - name: assetMS
        path: microservices/assetMS/

      - name: userModel
        path: microservices/userModel/

      - name: opGenModel
        path: microservices/opGenModel/

      - name: weatherModel
        path: microservices/weatherModel/

      - name: geometryIngestService
        path: microservices/geometryIngestService/

      - name: weatherMS
        path: microservices/weatherMS/

      - name: microserviceDBUtils
        path: microservices/microserviceDBUtils/

      - name: planningRepository
        path: microservices/planningRepository/

      - name: missionMS
        path: microservices/missionMS/

      - name: ephemerisDM
        path: microservices/ephemerisDM/

      - name: initDatabase
        path: microservices/initDatabase/

      - name: accessModel
        path: microservices/accessModel/

  - git_url: git@bitbucket.org:radiantsolutions/build.git
    branch: ktis
    modules:
      - name: build repo
        path: build/

  - git_url: git@bitbucket.org:radiantsolutions/cesium-ui.git
    branch: master
    modules:
      - name: czmlwriter
        path: cesium-ui/czmlwriter/

      - name: cesium-client
        path: cesium-ui/cesium-client/

      - name: csv2czml
        path: cesium-ui/csv2czml/

      - name: cesium-server
        path: cesium-ui/cesium-server/

  - git_url: git@bitbucket.org:radiantsolutions/tools.git
    branch: master
    modules:
      - name: webstats
        path: tools/utilities/webstats/
```
