History
-------

v3.7.0 (5 May 2022)
+++++++++++++++++++
- Add `page` and `page_size` parameters to all the remaining modules APIs methods returning multiple entries (default page size is 100 and page limit is 500 records per page)
- Update internal libraries used as external_dependencies, especially oauth2_xfel_client
- Expose `max_retries`, `timeout` and `ssl_verify` parameters from oauth2_xfel_client
- Improve tests to validate page and page_size parameter
- Improve documentation in README file

v3.6.0 (3 February 2022)
++++++++++++++++++++++++
- Add `page` and `page_size` parameters to the the `Proposal` and `Sample` APIs methods returning multiple entries (default is 100 and limit is 500 records per page)

v3.5.0 (14 December 2021)
+++++++++++++++++++++++++
- Add new myMdC APIs
- Remove support for old python versions

v3.4.0 (14 December 2021)
+++++++++++++++++++++++++
- Update external dependency
- Add python 3.10 to Gitlab-ci

v3.3.0 (23 June 2021)
+++++++++++++++++++++
- Fix Dark Runs fields names

  - `globus_url` was renamed to `report_url`
  - `calcat_url` was renamed to `full_calcat_report_url`

v3.2.2 (4 June 2021)
++++++++++++++++++++
- Add additional tests

v3.2.1 (4 June 2021)
++++++++++++++++++++
- Improve base info error messages for GET action
- Add additional tests

v3.2.0 (3 June 2021)
++++++++++++++++++++
- Improve error messages for DAQ
- Add additional tests

v3.1.0 (2 June 2021)
++++++++++++++++++++
- Update internal libraries
- Fix issues in Unitary Tests when running against latest myMdC version

v3.0.9 (9 November 2020)
++++++++++++++++++++++++
- Update internal libraries

v3.0.8 (4 November 2020)
++++++++++++++++++++++++
- Reformat code to use `inspect.currentframe().f_code.co_name` instead of method name
- Add new Class `DarkRun` and `DarkRunApi`
- Correct the Run class method `get_all_by_number_and_proposal_number`

v3.0.7 (30 June 2020)
+++++++++++++++++++++
- Reformat code
- Resolve `pycodestyle` findings
- Upgrade python packages in use and respective external dependencies versions

v3.0.6 (10 June 2020)
+++++++++++++++++++++
- Change project to use pytest to run tests, instead of nosetests
- Upgrade python packages in use and respective external dependencies versions
- Fix failing test
- Clean up and improve Gitlab-ci
- Remove package .whl file
- Improve README
- The `modules` classes have a reference to a client object, so they don't need to be part of its inheritance chain.
- Once you do that, `MetadataClient` is the same as `MetadataClientApi`, just with some extra methods, so I deprecated the latter.
- Turned the staticmethods on MetadataClient into normal methods
- Move the oauth setup to the base class where it is used.
- Pull classes 'up' a level to allow shorter imports like `from metadata_client import MetadataClient`.

v3.0.5 (20 February 2020)
+++++++++++++++++++++++++
- Add support to python 3.8
- Solve issues with tests

v3.0.4 (15 November 2019)
+++++++++++++++++++++++++
- Improve documentation
- Add new API on users and on Instrument

v3.0.3 (22 August 2019)
+++++++++++++++++++++++
- Solve issue with a test that failed randomly when DB was not clean
- Improve documentation

v3.0.2 (21 August 2019)
+++++++++++++++++++++++
- Improve setup.py so that information in pypi.org is better rendered
- Upgrade oauth2_xfel_client library to version 5.1.1

v3.0.1 (16 August 2019)
+++++++++++++++++++++++
- Add gitlab-ci integration
- Correct some tests data

v3.0.0 (15 August 2019)
+++++++++++++++++++++++
- Upgrade internally used libraries
- Update Readme
- Solve pycodestyle findings
- Add additional run related APIs
- Prepare version 3.0.0 release

v2.1.0 (11 March 2019)
++++++++++++++++++++++
- Added Data Source Groups API's
- Update library version to 2.1.0

v2.0.2 (13 December 2018)
+++++++++++++++++++++++++
- Implemented the new method to consume the new api to get the runs by proposal number

v2.0.1 (13 December 2018)
+++++++++++++++++++++++++
- Fixed the tests to reflect the most recent version of myMdC

v2.0.0 (20 December 2017)
+++++++++++++++++++++++++
- Upgrade oauth2_client library to oauth2_xfel_client version 5.0.0

v1.1.5 (28 November 2017)
+++++++++++++++++++++++++
- Upgrade oauthlib library to version 2.0.6
- Upgrade oauth2_client library to version 4.1.1

v1.1.4 (18 October 2017)
++++++++++++++++++++++++
- Upgrade oauthlib library to version 2.0.4
- Upgrade oauth2_client library to version 4.1.0

v1.1.3 (18 October 2017)
++++++++++++++++++++++++
- Solving issue crashing when pcLayer was not sending a flg_status when closing the run
- Do necessary changes to allow close_run without specifying the Run Summary (data_group_parameters)
- Remove references to first_prefix_path

v1.1.2 (13 September 2017)
++++++++++++++++++++++++++
- Fix issue with method get_all_by_data_group_id_and_repository_id_api
- Change close_run general method to mark the run as closed if no other flg_status is specified

v1.1.1 (4 September 2017)
+++++++++++++++++++++++++
- Fix all success variable types to Boolean

v1.1.0 (1 September 2017)
+++++++++++++++++++++++++
- Upgrade oauth2_client library to version 4.0.0
- Add extra methods to this library

v1.0.0 (8 July 2017)
++++++++++++++++++++
- New to PCLayer: get_all_xfel_instruments, get_active_proposal_by_instrument
- New to Data Reader: search_data_files
- New to GPFS: register_run_replica, unregister_run_replica

v0.0.3 (8 March 2017)
+++++++++++++++++++++
- Separate this Python library from the KaraboDevices code.
- Clean code and remove all references to Karabo.
- Set up new project under ITDM group in Gitlab.

v0.0.2 (2 November 2016)
++++++++++++++++++++++++
- Update library dependencies
- Integrate this library with Karabo 2.0

v0.0.1 (20 September 2015)
++++++++++++++++++++++++++
- Initial code
