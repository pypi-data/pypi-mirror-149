History
-------

v6.1.0 (3 May 2022)
+++++++++++++++++++
- Make Timeout (connect and read timeouts) configurable (default is set to 12 seconds)
- Make number of retries configurable (default is set to 3) and add an increasing delay before retrying.
- Ensure we have a token before making requests. If the token request fails for any reason, the session object is left without a token, and then it skips the oauth logic.
- Make Requests dependency `ssl_verify` property configurable (default is set to `True`)
- Organize and simplify secrets file
- Update external dependencies
- Improve README file

v6.0.1 (14 December 2021)
+++++++++++++++++++++++++
- Update external dependencies
- Update gitlab-ci tested python versions
- Update keys used in tests

v6.0.0 (04 May 2020)
++++++++++++++++++++
- Change project to use pytest to run tests, instead of nosetests
- Add automatically renewing of the token (using client_credentials OAuth2 flow)
- Upgrade python packages in use and respective external dependencies versions
- Tests improvements
- Update test system URL for CI tests
- Clean up and improve Gitlab-ci
- Remove package .whl file

v5.1.1 (21 August 2019)
+++++++++++++++++++++++
- Improve setup.py so that information in pypi.org is better rendered
- Add .gitlab-ci to the project

v5.1.0 (06 August 2019)
+++++++++++++++++++++++
- Upgrade version of used libraries oauthlib, requests and requests-oauthlib
- Solve issue of not renewing the ticket automatically after 2 hours

v5.0.0 (20 December 2017)
+++++++++++++++++++++++++
- Upgrade version of used library oauthlib to version 2.0.6
- Rename library to oauth2_xfel_client

v4.1.1 (28 November 2017)
+++++++++++++++++++++++++
- Upgrade version of used library oauthlib to version 2.0.6

v4.1.0 (18 October 2017)
++++++++++++++++++++++++
- Upgrade version of used library oauthlib to version 2.0.4

v4.0.0 (1 September 2017)
+++++++++++++++++++++++++
- Upgrade version of used library requests to version 2.18.4
- Make all external dependencies locally available via Wheels files

v3.1.0 (31 August 2017)
+++++++++++++++++++++++
- Correct issue related with error "Connection aborted. Connection reset by peer"

v3.0.0 (7 March 2017)
+++++++++++++++++++++
- Separate this Python library from the KaraboDevices code.
- Clean code and remove all references to Karabo.
- Set up new project under ITDM group in Gitlab.

v2.0.0 (2 November 2016)
++++++++++++++++++++++++
- Update library dependencies
- Integrate this library with Karabo 2.0

v1.0.0 (4 December 2015)
++++++++++++++++++++++++
- First official release of this library

v0.0.1 (20 June 2015)
+++++++++++++++++++++
- Initial code
