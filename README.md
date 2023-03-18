# online-store
<p> An online gift shop is planning to launch a campaign in different regions. In order for the sales strategy to be effective, market analysis is necessary. The store has a supplier who regularly sends (for example, by email) data exports with information about residents. </p>

<p> For this purpose, a REST API service has been developed in Python that analyzes the provided data and identifies demand for gifts among residents of different age groups in different cities by month. </d>

The service implements the following handlers:
<ul>
  <li> `POST /imports` - Adds a new data export </li>
  <li> `GET /imports/$import_id/citizens` - Returns residents of the specified data export </li>
  <li> `PATCH /imports/$import_id/citizens/$citizen_id` - Modifies information about a resident (and their relatives) in the specified data export </li>
  <li> `GET /imports/$import_id/citizens/birthdays` - Calculates the number of gifts that each resident of the data export will purchase for their first-order relatives, grouped by month </li>
  <li> `GET /imports/$import_id/towns/stat/percentile/age` - Calculates the 50th, 75th, and 99th percentiles of the ages (in full years) of residents by city in the specified sample </li>
<ul>
