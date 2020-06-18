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

# replace 'project_vars.yml' with your vars file
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

# Replace project_vars.yml with your vars file
docker run -it --rm -v $PWD/project_vars.yml:/docs-site-builder/project_vars.yml -v $PWD/out/:/out docs-site-builder

mv out/site/ docker/docs-service/site/
docker build docker/docs-service -t docs-service

docker run -d -p 8080:80 docs-service
```

And your docsite should be available at [http://127.0.0.1:8080/](http://127.0.0.1:8080/)

## Example Project

The following is an example which builds a docsite for a project named 'KTIS'. It contains 4 repositories with the
microservices repository containing around 50 modules. Usually, the specified modules are microservices.

```yaml
# Used as a title for the docs page
project_name: O2 Web Services

# Put under the title for the docs page
project_description: "
These docs serve as a guide for installing and running an individual service. It is up to the organization's best practices on how to orchestrate and configure the applications at scale.
"

# Used as a staging area for cloning repositories and creating guides
working_directory: __repos/

# Where to check, in each module root, for documentation files
docs_locations:
  - readme
  - readme.md
  - Dockerfile
  - docker/Dockerfile
  - Jenkinsfile
  - docs/

# The hierarchy of documentation, some number of repos each containing some number of modules.
repos:
  - git_url: https://github.com/ossimlabs/omar-admin-server
    branch: dev
    modules:
      - name: omar-admin-server
        path: omar-admin-server
        description: Spring Boot Admin provides an interface to manage and monitor all Spring Boot applications. The applications register with Spring Boot are discovered using Spring Cloud (Eureka).



  - git_url: https://github.com/ossimlabs/omar-avro-metadata
    branch: dev
    modules:
      - name: omar-avro-metadata
        path: omar-avro-metadata
        description: The Avro Metadata app receives JSON image metadata and stores it in a NoSQL database. It also retrieves and serves that metadata upon HTTP request.


  - git_url: https://github.com/ossimlabs/omar-base
    branch: dev
    modules:
      - name: omar-base
        path: omar-base
        description: The OMAR base container is the docker image upon which all other O2 services are built.
        links:
        - swagger: "http://omar-dev.ossim.io/omar-base/api" 

  - git_url: https://github.com/ossimlabs/omar-basemap
    branch: dev
    modules:
      - name: omar-basemap
        path: omar-basemap
        description: The OMAR Basemap service provides Open Street Map tiles to the web application and the user.
        links:
        - swagger: "http://omar-dev.ossim.io/omar-basemap/api" 

  - git_url: https://github.com/ossimlabs/omar-config-server
    branch: dev
    modules:
      - name: omar-config-server
        path: omar-config-server
        description: The OMAR Spring Configuration Server is used to hand configuration files out to the various OMAR Spring micro services.
        links:
        - swagger: "http://omar-dev.ossim.io/omar-config-server/api" 

  - git_url: https://github.com/ossimlabs/omar-download
    branch: dev
    modules:
      - name: omar-download
        path: omar-download
        description: The OMAR Download service handles user download requests for imagery, bundling an image's raw file with all auxillary files into a zip file.
        links:
        - swagger: "http://omar-dev.ossim.io/omar-download/api" 

  - git_url: https://github.com/ossimlabs/omar-eureka-server
    branch: dev
    modules:
      - name: omar-eureka-server
        path: omar-eureka-server
        description: The OMAR Eureka server is an instantiation of the Spring Framework Netflix Discovery Client


  - git_url: https://github.com/ossimlabs/omar-geoscript
    branch: dev
    modules:
      - name: omar-geoscript
        path: omar-geoscript
        description: The OMAR Geoscript application encapsulates all the geotools dependencies which provides libraries to query the OMAR database, draw footprints and manipulate shape files among other spatial capabilities
        links:
        - swagger: "http://omar-dev.ossim.io/omar-geoscript/api" 

  - git_url: https://github.com/ossimlabs/omar-mapproxy
    branch: dev
    modules:
      - name: omar-mapproxy
        path: omar-mapproxy
        description: The OMAR MapProxy service acts as a proxy between basemaps and geospatial applications as well as a map tile cache
        links:
        - swagger: "http://omar-dev.ossim.io/omar-mapproxy/api" 

  - git_url: https://github.com/ossimlabs/omar-mensa
    branch: dev
    modules:
      - name: omar-mensa
        path: omar-mensa
        description: Tme OMAR Mensuration service receives and handles all user measurement (e.g. area, length, etc.) requests for a particular image
        links:
        - swagger: "http://omar-dev.ossim.io/omar-mensa/api" 

  - git_url: https://github.com/ossimlabs/omar-nifi
    branch: dev
    modules:
      - name: omar-nifi
        path: omar-nifi
        links:
        - swagger: "http://omar-dev.ossim.io/omar-nifi/api"

  - git_url: https://github.com/ossimlabs/omar-oms
    branch: dev
    modules:
      - name: omar-oms
        path: omar-oms
        description: The OMAR OSSIM Mapping Service contains all of OSSIM's functionality, binding it via JNI to be web accessible
        links:
        - swagger: "http://omar-dev.ossim.io/omar-oms/api" 

  - git_url: https://github.com/ossimlabs/omar-ossim-base
    branch: dev
    modules:
      - name: omar-ossim-base
        path: omar-ossim-base
        description: The OMAR OSSIM Base container is a docker image that containes all OSSIM libraries and is used to build any other service that may require them
        links:
        - swagger: "http://omar-dev.ossim.io/omar-ossim-base/api" 

  - git_url: https://github.com/ossimlabs/omar-reachback
    branch: dev
    modules:
      - name: omar-reachback
        path: omar-reachback
        description: OMAR-reachback allows for search and discovery of data in external repositories
        links:
        - swagger: "http://omar-dev.ossim.io/omar-reachback/api" 

  - git_url: https://github.com/ossimlabs/omar-services-monitor
    branch: dev
    modules:
      - name: omar-services-monitor
        path: omar-services-monitor
        description: OMAR-Services-Monitor is an application used to track the status of deployed OMAR services across different deployments


  - git_url: https://github.com/ossimlabs/omar-sqs-stager
    branch: dev
    modules:
      - name: omar-sqs-stager
        path: omar-sqs-stager
        description: The OMAR Simple Queue Service Stager provides the workflow to monitors, receive and process (i.e. ingest) SQS messages which notify the system of new images to be ingested
        links:
        - swagger: "http://omar-dev.ossim.io/omar-sqs-stager/api" 

  - git_url: https://github.com/ossimlabs/omar-stager
    branch: dev
    modules:
      - name: omar-stager
        path: omar-stager
        description: The OMAR Stager service provides the workflow to process and ingest data into the O2 system, creating histograms and overviews as necessary
        links:
        - swagger: "http://omar-dev.ossim.io/omar-stager/api" 

  - git_url: https://github.com/ossimlabs/omar-superoverlay
    branch: dev
    modules:
      - name: omar-superoverlay
        path: omar-superoverlay
        description: The OMAR Superoverlay service provides functionality for generating and servicing KMLs, which allows users to search and view imagery within O2 in external GeoINT tools
        links:
        - swagger: "http://omar-dev.ossim.io/omar-superoverlay/api" 

  - git_url: https://github.com/ossimlabs/omar-twofishes
    branch: dev
    modules:
      - name: omar-twofishes
        path: omar-twofishes
        description: The OMAR Twofishes service acts as a geocoder through converting g-oname strings into coordinates
        links:
        - swagger: "http://omar-dev.ossim.io/omar-twofishes/api" 

  - git_url: https://github.com/ossimlabs/omar-ui
    branch: dev
    modules:
      - name: omar-ui
        path: omar-ui
        description: The OMAR UI services provides the user an entry point to conveniently interact with OMAR and its supported services
        links:
        - swagger: "http://omar-dev.ossim.io/omar-ui/api" 

  - git_url: https://github.com/ossimlabs/omar-upload
    branch: dev
    modules:
      - name: omar-upload
        path: omar-upload
        description: The OMAR Upload service allows users to upload image files for stagin
        links:
        - swagger: "http://omar-dev.ossim.io/omar-upload/api" 

  - git_url: https://github.com/ossimlabs/omar-video-ui
    branch: dev
    modules:
      - name: omar-video-ui
        path: omar-video-ui
        description: OMAR-video-ui is the UI that enables users to exploit video data
        links:
        - swagger: "http://omar-dev.ossim.io/omar-video-ui/api" 

  - git_url: https://github.com/ossimlabs/omar-volume-cleanup
    branch: dev
    modules:
      - name: omar-volume-cleanup
        path: omar-volume-cleanup
        description: An application to monitor and manage a volume of O2 raster images. The application cleans old rasters when used disk space goes over a given threshold. Rasters are deleted using the omar-stager HTTP API
        links:
        - swagger: "http://omar-dev.ossim.io/omar-volume-cleanup/api" 

  - git_url: https://github.com/ossimlabs/omar-wcs
    branch: dev
    modules:
      - name: omar-wcs
        path: omar-wcs
        description: The OMAR Web Coverage Service provides OGC capabilities for the WCS standard, serving out image chips from O2's data holdings
        links:
        - swagger: "http://omar-dev.ossim.io/omar-wcs/api" 

  - git_url: https://github.com/ossimlabs/omar-web-proxy
    branch: dev
    modules:
      - name: omar-web-proxy
        path: omar-web-proxy
        description: The OMAR Web Proxy application acts as a proxy and reverse proxy for the OMAR services
        links:
        - swagger: "http://omar-dev.ossim.io/omar-web-proxy/api" 

  - git_url: https://github.com/ossimlabs/omar-wfs
    branch: dev
    modules:
      - name: omar-wfs
        path: omar-wfs
        description: The OMAR Web Feature Service provides OGC capabilities for the WFS standard, serving out feature data from O2's data holdings
        links:
        - swagger: "http://omar-dev.ossim.io/omar-wfs/api" 

  - git_url: https://github.com/ossimlabs/omar-wms
    branch: dev
    modules:
      - name: omar-wms
        path: omar-wms
        description: The OMAR Web Map Service provides OGC capabilities for the WMS standard, serving out image chips from O2's raster data holdings
        links:
        - swagger: "http://omar-dev.ossim.io/omar-wms/api" 

  - git_url: https://github.com/ossimlabs/omar-wmts
    branch: dev
    modules:
      - name: omar-wmts
        path: omar-wmts
        description: The OMAR Web Map Tile Service provides OGC capabilities for the WMTS standard, serving out image chips from O2's raster data holdings
        links:
        - swagger: "http://omar-dev.ossim.io/omar-wmts/api" 

  - git_url: https://github.com/ossimlabs/rhel-minimal
    branch: dev
    modules:
      - name: rhel-minimal
        path: rhel-minimal
        description: The Red Hat Enterprise Linux container is used as a bare bones base upon which all other containers and apps are built


  - git_url: https://github.com/ossimlabs/tlv
    branch: dev
    modules:
      - name: tlv
        path: tlv
        description: The Time Lapse Viewer is a web-based tool, dedicated to producing on-demand imagery flipbooks.
          links:
          - swagger: "http://omar-dev.ossim.io/tlv/api" 
```
