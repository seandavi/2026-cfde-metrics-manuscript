## Supplementary Table S1: Full metric catalog

Full catalog of metrics across the three frameworks, organized by difficulty of collection, value for evaluation, relevant lifecycle phase, and notes on interpretation. The main text uses this catalog to motivate the prioritized subset that the CFDE ICC dashboard currently collects (Table 2).

| Metric | Difficulty of Collection | How Collected | Value | Lifecycle Phase | Notes |
| :---- | :---- | :---- | :---- | :---- | :---- |
| **User Behavior Framework** |  |  |  |  |  |
|  *page views*  |  Easy  |  Google Analytics or Matomo or similar platforms  |  Low  | Mid |  A minimum indicator of interest.   |
|  *time on page*  |  Easy  |  Google Analytics  or Matomo or similar platforms |  Low  | Mid |  A minimum indicator of interest.  |
|  *actions/triggers*  |  Easy  |  Google Analytics or Matomo or similar platforms  |  Medium  | Mid |  A moderate indicator of interest.   |
|  *priority link clicks*  |  Easy  |  Google Analytics or Matomo or similar platforms |  Medium  | Mid |  A moderate indicator of interest.  |
|  *new vs returning users*  |  Easy  |  Google Analytics or Matomo or similar platforms  |  Medium  | Mid |  A moderate indicator of continuing interest.  |
|  *downloads*  |  Easy  |  Google Analytics  or Matomo or similar platforms or Server-side logs  |  Medium-High  | Mid |  A strong indicator of interest. Downloading not equivalent to usage.  |
|  *compute jobs*  |  Easy  |  Compute scheduler logs or cloud environment logs  |  High  | Mid |  A direct indicator of interest.  |
|  *tool downloads*  |  Easy  |  Google Analytics or Matomo or similar platforms or server-side logs  |  Medium-High  | Mid |  A strong indicator of interest.  |
|  *tool usage*  |  Easy  |  Google Analytics  or Matomo or similar platformsor API logs  |  High  | Mid |  A direct indicator of interest.  |
|  *trend downloads*  |  Medium  |  Google Analytics  or Matomo or similar platforms or server-side logs, BI tools for visualization  |  Medium-High  | Mid–Late |  A strong indicator of change in interest over time.  |
|  *trend compute jobs*  |  Medium  |  Compute scheduler logs or cloud environment logs, BI tools for visualization  |  High  | Mid–Late |  A direct indicator of change in interest over time.  |
|  *number grants*  |  Hard  |  NIH RePORTER, Self-reporting  |  High  | Mid–Late |  Relevant grant data not publicly available.  |
|  *number presentations*  |  Hard  |  Self-reporting  |  Medium  | Mid–Late |  Data difficult to track and often not available in sufficient detail.  |
|  *number citations*  |  Easy  |  Google Scholar, PubMed, Scopus, Clarivate, OpenAlex, or other similar platforms  |  High  | Mid–Late |  A direct indicator of data value. Can miss downstream cumulative value.  |
|  *number secondary citations*  |  Medium  |  Google Scholar, PubMed, Scopus, Clarivate, OpenAlex, or other similar platforms  |  High  | Late |  An indirect measure of "downstream" value of initial publications.  |
|  *citations \+ secondary citations*  |  Medium  | Google Scholar, PubMed, Scopus, Clarivate, OpenAlex, or citiation network analysis  |  High  | Late |  A measure of cumulative impact over time of study data.  |
|  *trend citations*  |  Medium  | Google Scholar, PubMed, Scopus, Clarivate, OpenAlex, or other similar platforms, BI tools   |  High  | Late |  Measures change in impact of data over time. Subject to time lag in publications.  |
|  *data citation rate*  |  Hard  |  Full-text search for accession numbers, Methods section mining  |  High  | Mid–Late |  <30% of secondary analyses formally cite datasets. Multi-pronged tracking required.  |
|  *perceived value (user surveys)*  |  Medium  |  Structured surveys (ISSM/TAM framework)  |  High  | Mid–Late |  Entropy-weighted: dataset breadth, timeliness, search comprehensiveness, responsiveness.  |
|  *cloud adoption rate*  |  Medium  |  Cloud workspace logs vs. download logs  |  Medium-High  | Mid–Late |  Proxy for computational paradigm shift (cloud vs. local analysis).  |
|  *cross-disciplinary collaboration*  |  Hard  |  Co-authorship network analysis  |  High  | Late |  Measures new partnerships fostered across Common Fund programs.  |
|  *user diversity (geographic/institutional)*  |  Medium  |  User registration data, IAM logs  |  Medium-High  | Mid–Late |  Measures democratization of access, especially for under-resourced institutions.  |
|  |  |  |  |  |  |
| **Scientific Quality Framework** |  |  |  |  |  |
|  *metadata completeness*  |  Medium  |  Metadata validator, Schema validator  |  Medium-High  | Early |  Critical for drawing initial interest in study.  |
|  *standardized metadata*  |  Hard  |  Requires human-in-the-loop evaluation.  |  High  | Early |  Study-specific requirements.   |
|  *quality-control (QC) compliance*  |  Hard  |  Requires human-in-the-loop evaluation.  |  High  | Early |  Study-specific requirements.   |
|  *data uniqueness*  |  Hard  |  Requires human-in-the-loop evaluation.  |  Medium  | Early |  Subjective measure.   |
|  *FAIR compliance*  |  Hard  |  Requires human-in-the-loop evaluation.  |  High  | All |  Subjective measure.  |
|  *available data dictionary*  |  Medium  |  Checks on repository or documentation  |  Medium  | Early |  An essential component for a study to have. Does not guarantee quality.  |
|  *quality data dictionary*  |  Hard  |  Requires human-in-the-loop evaluation.  |  High  | Early |  A metric of quality of the data dictionary.   |
|  *representativeness*  |  Hard  |  Demographic and population metadata analysis  |  High  | Early |  Whether dataset generalizes beyond source population. Critical for avoiding false conclusions.  |
|  *linkability*  |  Hard  |  Schema and identifier compatibility assessment  |  High  | All |  Extent to which data integrates with external sources. Paramount for federated ecosystems.  |
|  *software good practices score*  |  Medium  |  ELIXIR Top 10 framework; automated collection via PIsCO  |  High  | All |  Covers version control, discoverability, automated builds, test data, documentation.  |
|  |  |  |  |  |  |
| ***Operations and Finance*** **Framework** |  |  |  |  |  |
|  *uptime*  |  Easy  |  Application Performance Monitoring (APM) tools  |  Medium-Low  | Mid–Late |  Measure of server stability.  |
|  *page load time*  |  Easy  |  Application Performance Monitoring (APM) tools   |  Medium  | Mid–Late |  Measure of server performance.   |
|  *latency*  |  Easy  |  Application Performance Monitoring (APM) tools or Google Analytics ( not real-time)  |  Medium  | Mid–Late |  Measure of server performance.  |
|  *server errors*  |  Easy  |  Server-side logs or Application Performance Monitoring (APM) tools  |  Medium  | Mid–Late |  Measure of server stability and performance.  |
|  *client errors*  |  Medium  |  Application logs or Application Performance Monitoring (APM) tools  |  Low  | Mid–Late |  Measure of errors on client end. Possible not addressable.  |
|  *download speed*  |  Easy  |  Server-side logs or Application Performance Monitoring (APM) tools  |  Low-Medium  | Mid–Late |  Download times can be function of client connection speeds.  |
|  *cpu/gpu usage*  |  Easy  |  Application Performance Monitoring (APM) tools   |  High  | Mid–Late |  Important to evaluate performance and additional needs.  |
|  *memory usage*  |  Easy  |  Application Performance Monitoring (APM) tools  |  High  | Mid–Late |  Important to evaluate performance and additional needs.  |
|  *number of users*  |  Easy  |  Google Analytics or IAM logs for granular details (if available)  |  Medium  | Mid–Late |  Indirect measure of computational load/burden.  |
|  *client queue times*  |  Easy  |  Application Performance Monitoring (APM) tools or Cloud/infrastructure logs |  Medium-High  | Mid–Late |  Long queue times can result in less usage.  |
|  *job run times*  |  Easy  |  Application Performance Monitoring (APM) tools or Cloud/infrastructure compute logs |  Medium  | Mid–Late |  Excessive long job run times can result in less usage.  |
|  *funding cost*  |  Easy  |  NIH RePORTER  |  High  | All |  Total cost of study. Critical element in evaluating study feasibility and sustainability.  |
|  *sample collection costs*  |  Medium  |    |  Medium  | Early |  Cost typically associated with early study period. Cost does not impact sustainability.  |
|  *sample measurement costs*  |  Medium  |    |  Medium  | Early |  Cost typically associated with early study period. Cost does not impact sustainability.  |
|  *QC costs*  |  Medium  |    |  Medium  | Early |  Cost typically associated with early study period. Cost does not impact sustainability.  |
|  *data storage costs*  |  Hard  |    |  High  | All |  Costs and requirements can fluctuate over study.  |
|  *data preservation costs*  |  Hard  |    |  High  | Late |  Costs and requirements can fluctuate over study. Difficult to assess years in advance.  |
|  *computing hardware costs*  |  Medium  |    |  Medium  | Early |  Costs often associated with initial study period, but replacement costs are possible.  |
|  *server maintenance costs*  |  Hard  |    |  High  | Mid–Late |  Costs can fluctuate. Major source of cost in sustainability period.   |
|  *cloud-based computing costs*  |  Hard  |  Cloud Cost Explorer tools or  |  High  | Mid–Late |  Costs are highly variable and subject to constant change (for both host and clients). Especially difficult to assess years in advance.  |
|  *personnel costs*  |  Medium  |    |  High  | All |  Can be measured in money or time. Requires committed time with relevant expertise.  |

: Summary of metrics across the three frameworks, organized by difficulty of collection, value for evaluation, relevant lifecycle phase, and notes on interpretation. {#tbl-metrics-summary}
