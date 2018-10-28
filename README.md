# Power Daps

## Installation
On a Mac: `brew install power-daps`

On CentOS or Redhat: `yum install power-daps`

On Ubuntu or Debian: `apt-get install power-daps`

## Usage

### As a suite of tools

#### Creating something new

`dap create suite`

`dap create app <app-name>`

`dap create data-source <app-name>/<data-source-name>[:<data-source-type>]` where `<data-source-type>` is `postgres`, `mysql`, `oracle`, `mongodb`, `cassandra`, `csv-fetch` etc.

#### Working with existing application suites

The basic structure for using dap is: `dap <target>`. This will run all preceding targets in the chain, unless you tell it to only run that target by running `dap only <target>`. Only targets that need to run will run unless you force it by running `dap force <target>`. If you only want to force one target, run `dap force only <target>`.


The following targets are provided by default for Java development:

1. `deps`: Resolve, download and verify dependencies.
2. `compile`: Compile application and test code for compiled languages.
3. `unit-test`: Run unit tests.
4. `package`: Package the jar or the war or the pip or the gem or the rpm or the docker image.
5. `deploy`: Spin up necessary environment, and deploy the necessary components and apps.
6. `functional-test`: Run functional tests on the deployed app.

### As stand-alone tools

Each Power Daps target comes as a stand-alone command:

1. `dap-create`
2. `dap-deps`
3. `dap-compile`
4. `dap-unit-test`
5. `dap-package`
6. `dap-deploy`
7. `dap-functional-test`

## Appendix

Complete target tree:

* `all` or `default` or if you omit a target
   * `deps`
      * `resolve-deps`
      * `download-deps`
      * `verify-deps`
   * `validate`
   * `compile`
      * `compile-app`
      * `compile-test`
   * `unit-test`
   * `package` or `jar` or `war`
   * `deploy`
      * `deploy-machines`
         * `check-machines`
         * `stop-machines`
         * `clean-machines`
         * `start-machines`
      * `deploy-dependencies`
      * `load-data`
         * `check-data-stores`
         * `clean-data-stores`
         * `create-schema`
         * `populate-data`
         * `migrate-schema`
         * `migrate-data`
   * `component-test`
   * `contract-test`
   * `integration-test`
   * `functional-test`


### Details of what happens when creating a new application suite

Create a new suite by running `dap create suite [dir]`. This will create the following directory structure in the current directory or the specified directory:

* `apps`
* `bin`
* `dashboard`
* `env`
* `test`
   * `integration-test`
   * `functional-test`

### Details of what happens when creating a new application in the current suite

`dap create app <name>` will create the following structure under the `<name>` directory under `apps`:

* `config`
 * `identity`
* `data`
 * `sources`
     * `sample-rdbms`
         * `schema-migrations`
             * `000-initial-schema.sql`
         * `data-migrations`
             * `000-000-initial-data.sql`
* `src`
* `test`
     * `unit-test`
     * `component-test`
     * `contract-test`


### Creating a data source for an app

`dap create data-source <app-name>/<data-source-name>[:<data-source-type>]` where `<data-source-type>` is `postgres`, `mysql`, `oracle`, `mongodb`, `cassandra`, `csv-fetch` etc.

`csv-fetch` will allow you to setup a periodic sftp download of CSV files from multiple sources and load them into a particular location accessible to the application.


## License
Power Daps is released under [GNU Public License v3.0](http://www.gnu.org/licenses/gpl-3.0.txt)

## Copyright
Copyright &copy; 2016, Prasanna Pendse










