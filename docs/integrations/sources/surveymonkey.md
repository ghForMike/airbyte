# SurveyMonkey

[SurveyMonkey](https://www.surveymonkey.com/mp/take-a-tour/create-surveys-and-forms/) is an online polling tool that gathers survey data on market/brand research, customer/user experience, employee engagement, and other areas of interest to your organization or project. The guidance that follows here takes you through the process of setting up the SurveyMonkey source connector.

:::note

Airbyte's [OAuth 2.0](https://auth0.com/intro-to-iam/what-is-oauth-2) support for Survey Monkey is currently available only in the US. For prompt assistance with OAuth 2.0 issues, please [reach out to us directly](mailto:product@airbyte.io).

:::

<!-- env:oss -->

## Before You Begin

Please complete the following prerequisites:

1. Review the [developer information provided by SurveyMonkey](https://developer.surveymonkey.com/api/v3/#SurveyMonkey-Api).
2. [Sign in to SurveyMonkey](https://developer.surveymonkey.com/apps/) and register your application. 
3. If connecting from **Airbyte Open Source**, go to **Settings** in SurveyMonkey and copy your access token. An access token isn't required to connect with **Airbyte Cloud**.

<!-- /env:oss -->

<!-- env:cloud -->

## Setting Up the Source Connector in Airbyte Cloud

To set up the source connector in Airbyte Cloud:

1. [Log into your Airbyte Cloud account](https://cloud.airbyte.com/workspaces).
2. In the navigation bar on the left, click **Sources**.
3. Click **+ new source** in the top-right of your screen. This opens the source setup page.
4. Select **SurveyMonkey** from the **Source type** dropdown menu and enter a name for the new connector.
5. Click **Authenticate your account**, then log in and authorize your SurveyMonkey account.
6. Choose a **Start date**.
7. Click `Set up source`.

<!-- Here it would be helpful to include a screenshot of a successful setup result. If setup is not successful, we should list the most commonly encountered error conditions with troubleshooting suggestions. -->

<!-- /env:cloud -->

<!-- env:oss -->

## Setting Up the Source Connector in Airbyte Open Source

To set up the source connector in Airbyte Open Source:

1. Open Airbyte on your local machine.
2. In the navigation bar on the left, click **Sources**.
3. Click **+ new source** in the top-right of your screen. This opens the source setup page.
4. Select **SurveyMonkey** from the **Source type** dropdown menu and enter a name for the new connector.
5. Add (paste) your SurveyMonkey **Access Token**.
6. Choose a **Start date**.
7. Click `Set up source`.

<!-- Here, again, it would be helpful to include a screenshot of a successful setup result, as well as a list of the most commonly encountered error conditions and troubleshooting suggestions. If the possible error conditions for both Cloud and Open Source are identical, we can combine them under a single level2 heading called "Troubleshooting" -->

<!-- /env:oss -->

## Supported Streams

Endpoint specifications for SurveyMonkey's supported streams are available from the following links:

- [Surveys](https://api.surveymonkey.com/v3/docs?shell#api-endpoints-get-surveys) \(Incremental\)
- [SurveyPages](https://api.surveymonkey.com/v3/docs?shell#api-endpoints-get-surveys-survey_id-pages)
- [SurveyQuestions](https://api.surveymonkey.com/v3/docs?shell#api-endpoints-get-surveys-survey_id-pages-page_id-questions)
- [SurveyResponses](https://api.surveymonkey.com/v3/docs?shell#api-endpoints-get-surveys-id-responses-bulk) \(Incremental\)
- [SurveyCollectors](https://api.surveymonkey.com/v3/docs?shell#api-endpoints-get-surveys-survey_id-collectors)
- [Collectors](https://api.surveymonkey.com/v3/docs?shell#api-endpoints-get-collectors-collector_id-)

Please note that the streams for **Surveys** and **Survey Responses** are synchronized incrementally.

## Performance Considerations

The SurveyMonkey API imposes the following limits on private apps:

- 125 requests per minute
- 500 requests per day

Airbyte uses caching to handle more data from this source.

## Changelog

<details>
  <summary>Expand to review</summary>

| Version | Date       | Pull Request                                             | Subject                                                                          |
| :------ | :--------- | :------------------------------------------------------- | :------------------------------------------------------------------------------- |
| 0.3.5   | 2024-06-07 | [39329](https://github.com/airbytehq/airbyte/pull/39329) | Add `CheckpointMixin` for state management                                       |
| 0.3.4   | 2024-06-06 | [39244](https://github.com/airbytehq/airbyte/pull/39244) | [autopull] Upgrade base image to v1.2.2                                          |
| 0.3.3   | 2024-05-22 | [38559](https://github.com/airbytehq/airbyte/pull/38559) | Migrate Python stream authenticator to `requests_native_auth` package            |
| 0.3.2   | 2024-05-20 | [38244](https://github.com/airbytehq/airbyte/pull/38244) | Replace AirbyteLogger with logging.Logger and upgrade base image                 |
| 0.3.1   | 2024-04-24 | [36664](https://github.com/airbytehq/airbyte/pull/36664) | Schema descriptions and CDK 0.80.0                                               |
| 0.3.0   | 2024-02-22 | [35561](https://github.com/airbytehq/airbyte/pull/35561) | Migrate connector to low-code                                                    |
| 0.2.4   | 2024-02-12 | [35168](https://github.com/airbytehq/airbyte/pull/35168) | Manage dependencies with Poetry                                                  |
| 0.2.3   | 2023-10-19 | [31599](https://github.com/airbytehq/airbyte/pull/31599) | Base image migration: remove Dockerfile and use the python-connector-base image  |
| 0.2.2   | 2023-05-12 | [26024](https://github.com/airbytehq/airbyte/pull/26024) | Fix dependencies conflict                                                        |
| 0.2.1   | 2023-04-27 | [25109](https://github.com/airbytehq/airbyte/pull/25109) | Fix add missing params to stream `SurveyResponses`                               |
| 0.2.0   | 2023-04-18 | [23721](https://github.com/airbytehq/airbyte/pull/23721) | Add `SurveyCollectors` and `Collectors` stream                                   |
| 0.1.16  | 2023-04-13 | [25080](https://github.com/airbytehq/airbyte/pull/25080) | Fix spec.json required fields and update schema for surveys and survey_responses |
| 0.1.15  | 2023-02-11 | [22865](https://github.com/airbytehq/airbyte/pull/22865) | Specified date formatting in specification                                       |
| 0.1.14  | 2023-01-27 | [22024](https://github.com/airbytehq/airbyte/pull/22024) | Set `AvailabilityStrategy` for streams explicitly to `None`                      |
| 0.1.13  | 2022-11-29 | [19868](https://github.com/airbytehq/airbyte/pull/19868) | Fix OAuth flow urls                                                              |
| 0.1.12  | 2022-10-13 | [17964](https://github.com/airbytehq/airbyte/pull/17964) | Add OAuth for Eu and Ca                                                          |
| 0.1.11  | 2022-09-28 | [17326](https://github.com/airbytehq/airbyte/pull/17326) | Migrate to per-stream states                                                     |
| 0.1.10  | 2022-09-14 | [16706](https://github.com/airbytehq/airbyte/pull/16706) | Fix 404 error when handling nonexistent surveys                                  |
| 0.1.9   | 2022-07-28 | [13046](https://github.com/airbytehq/airbyte/pull/14998) | Fix state for response stream, fixed backoff behaviour, added unittest           |
| 0.1.8   | 2022-05-20 | [13046](https://github.com/airbytehq/airbyte/pull/13046) | Fix incremental streams                                                          |
| 0.1.7   | 2022-02-24 | [8768](https://github.com/airbytehq/airbyte/pull/8768)   | Add custom survey IDs to limit API calls                                         |
| 0.1.6   | 2022-01-14 | [9508](https://github.com/airbytehq/airbyte/pull/9508)   | Scopes change                                                                    |
| 0.1.5   | 2021-12-28 | [8628](https://github.com/airbytehq/airbyte/pull/8628)   | Update fields in source-connectors specifications                                |
| 0.1.4   | 2021-11-11 | [7868](https://github.com/airbytehq/airbyte/pull/7868)   | Improve 'check' using '/users/me' API call                                       |
| 0.1.3   | 2021-11-01 | [7433](https://github.com/airbytehq/airbyte/pull/7433)   | Remove unsused oAuth flow parameters                                             |
| 0.1.2   | 2021-10-27 | [7433](https://github.com/airbytehq/airbyte/pull/7433)   | Add OAuth support                                                                |
| 0.1.1   | 2021-09-10 | [5983](https://github.com/airbytehq/airbyte/pull/5983)   | Fix caching for gzip compressed http response                                    |
| 0.1.0   | 2021-07-06 | [4097](https://github.com/airbytehq/airbyte/pull/4097)   | Initial Release                                                                  |

</details>
