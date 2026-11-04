<!--
SUBMISSION NOTE (Trends Open):
Supplementary information, rendered as its own deliverable
(supplement.qmd). Trends Open accepts supplemental information only
after discussion with the editor (see issue #13); the main text cites
this file as "Supplementary Table S1".
-->

## Supplementary Table S1. Full indicator catalog

Indicators across the three domains, with a definition of each, how hard it is to collect, how it is collected, its value for evaluation, the lifecycle phase in which it matters most, and notes on interpretation.
Indicators marked ^†^ feed the core indicators in Table 1 of the main text.

| Metric | Definition | Difficulty of Collection | How Collected | Value | Lifecycle Phase | Notes |
| :------------ | :------------------ | :------ | :--------------- | :------ | :------ | :------------------ |
| **Public value** | | | | | | |
| *page views* | Number of times pages on the resource's website are loaded. | Easy | Google Analytics or Matomo or similar platforms | Low | Mid | A minimum indicator of interest. |
| *time on page* | Average time visitors spend on a page. | Easy | Google Analytics or Matomo or similar platforms | Low | Mid | A minimum indicator of interest. |
| *actions/triggers* | Tracked interactions on a page, such as searches, filters, or form submissions. | Easy | Google Analytics or Matomo or similar platforms | Medium | Mid | A moderate indicator of interest. |
| *priority link clicks* | Clicks on links the resource designates as key, such as data access or documentation. | Easy | Google Analytics or Matomo or similar platforms | Medium | Mid | A moderate indicator of interest. |
| *new vs returning users* | Share of visitors who are first-time versus repeat visitors. | Easy | Google Analytics or Matomo or similar platforms | Medium | Mid | A moderate indicator of continuing interest. |
| *downloads*^†^ | Number of data files or datasets retrieved from the resource. | Easy | Google Analytics or Matomo or similar platforms or Server-side logs | Medium-High | Mid | A strong indicator of interest. Downloading not equivalent to usage. |
| *compute jobs*^†^ | Number of analysis jobs run on the resource's data in its own compute or cloud environment. | Easy | Compute scheduler logs or cloud environment logs | High | Mid | A direct indicator of interest. |
| *tool downloads* | Number of times software tools distributed by the resource are downloaded or installed. | Easy | Google Analytics or Matomo or similar platforms or server-side logs | Medium-High | Mid | A strong indicator of interest. |
| *tool usage* | Number of invocations of the resource's tools or APIs. | Easy | Google Analytics or Matomo or similar platforms or API logs | High | Mid | A direct indicator of interest. |
| *trend downloads* | Change in downloads over time. | Medium | Google Analytics or Matomo or similar platforms or server-side logs, BI tools for visualization | Medium-High | Mid–Late | A strong indicator of change in interest over time. |
| *trend compute jobs* | Change in compute jobs over time. | Medium | Compute scheduler logs or cloud environment logs, BI tools for visualization | High | Mid–Late | A direct indicator of change in interest over time. |
| *number of subsequent grants* | Grants awarded after, and attributed to, use of the resource. | Hard | NIH RePORTER, Self-reporting | Medium | Mid–Late | Weak proxy for public value: shows that researchers won further funding, not that others benefited. Attribution relies on incomplete self-reporting; relevant grant data not publicly available. |
| *number of presentations* | Talks and posters that present the resource or work based on it. | Hard | Self-reporting | Low | Mid–Late | Weak proxy for public value: measures the team's dissemination effort, not benefit to others. Self-reported and often incomplete. |
| *platform citations*^†^ | Citations to papers describing the resource. | Easy | Google Scholar, PubMed, Scopus, Clarivate, OpenAlex, or other similar platforms | Medium-High | Mid–Late | Mix use of the data with mentions of the resource. |
| *content citations*^†^ | Publications that cite or reuse the data the resource hosts, through a data citation or an accession number. | Medium | Data citations in citation databases; full-text search for accession numbers | High | Mid–Late | A direct indicator of data value. Undercounted where reuse is not formally cited. |
| *second-generation citations* | Citations to the papers that cite the resource or its content. | Medium | Google Scholar, PubMed, Scopus, Clarivate, OpenAlex, or citation network analysis | High | Late | A measure of cumulative "downstream" impact over time. |
| *trend platform and content citations* | Change in platform and content citations over time. | Medium | Google Scholar, PubMed, Scopus, Clarivate, OpenAlex, or other similar platforms, BI tools | High | Late | Measures change in impact of data over time. Subject to time lag in publications. |
| *data citation rate* | Share of publications reusing a resource's data that formally cite it. | Hard | Full-text search for accession numbers, Methods section mining | High | Mid–Late | <30% of secondary analyses formally cite datasets. Multi-pronged tracking required. |
| *perceived value (user surveys)* | Users' assessment of the resource's value, from structured surveys. | Medium | Structured surveys (ISSM/TAM framework) | High | Mid–Late | Entropy-weighted: dataset breadth, timeliness, search comprehensiveness, responsiveness. |
| *cloud adoption rate* | Share of analyses run in cloud workspaces rather than on locally downloaded data. | Medium | Cloud workspace logs vs. download logs | Medium-High | Mid–Late | Proxy for computational paradigm shift (cloud vs. local analysis). |
| *cross-disciplinary collaboration* | Co-authorship links between fields or programs that arise from use of the resource. | Hard | Co-authorship network analysis | High | Late | Measures new partnerships fostered across Common Fund programs. |
| *user diversity (geographic/institutional)* | Spread of users across countries, institutions, and institution types. | Medium | User registration data, IAM logs | Medium-High | Mid–Late | Measures democratization of access, especially for under-resourced institutions. |
| *license type* | License under which the resource releases data and software, such as CC0, CC BY, or a custom data use agreement. | Easy | Resource metadata, LICENSE files, data use agreements | Medium | All | Openness, distinct from FAIR: FAIR asks that a license be clear, not that it be open. Can change as the resource matures. |
| *access model* | Share of data under each access tier: open, registered, controlled, or invitation-only. | Easy | Access policies, identity and access management (IAM) configuration | Medium-High | All | Context for reading use counts: controlled access lowers downloads without lowering value. Tiers can open up as the resource matures, for example at first public release. |
| *regulatory compliance support* | Help the resource gives depositors and users in meeting policy requirements, such as resource-specific NIH Data Management and Sharing Plan templates and data use guidance. | Medium | Review of the resource's documentation and support pages | Medium | Mid–Late | Lowers the cost of compliant sharing for the community. Grows as the resource matures. |
| **Data quality and reusability** | | | | | | |
| *metadata completeness*^†^ | Share of required metadata fields that are populated, checked against the resource's schema or a community standard. | Medium | Metadata validator, Schema validator | Medium-High | Early | Critical for drawing initial interest in study. |
| *standardized metadata* | Use of community metadata standards and controlled vocabularies. | Hard | Requires human-in-the-loop evaluation. | High | Early | Study-specific requirements. |
| *quality-control (QC) compliance*^†^ | Whether data passed documented quality control and expert review against community standards. | Hard | Requires human-in-the-loop evaluation. | High | Early | Study-specific requirements. |
| *data uniqueness* | Whether the data are unavailable from any other resource. | Hard | Requires human-in-the-loop evaluation. | Medium | Early | Subjective measure. |
| *FAIR compliance* | Degree to which data and metadata meet the FAIR principles, judged by expert assessment. | Hard | Requires human-in-the-loop evaluation. | High | All | Subjective measure. |
| *automated FAIR maturity score*^†^ | Machine-testable FAIR properties, scored by second-generation maturity indicators. | Medium | FAIR Evaluator compliance tests; FAIRplus-DSM level | High | All | Tests machine-actionability, not intrinsic quality. Report the tool and test set used. |
| *available data dictionary* | Whether a data dictionary describing each variable is published. | Medium | Checks on repository or documentation | Medium | Early | An essential component for a study to have. Does not guarantee quality. |
| *quality data dictionary* | Whether the data dictionary is complete, accurate, and usable. | Hard | Requires human-in-the-loop evaluation. | High | Early | A metric of quality of the data dictionary. |
| *representativeness* | Extent to which a dataset generalizes beyond its source population. | Hard | Demographic and population metadata analysis | High | Early | Whether dataset generalizes beyond source population. Critical for avoiding false conclusions. |
| *linkability* | Extent to which data integrate with external sources through shared identifiers and schemas. | Hard | Schema and identifier compatibility assessment | High | All | Extent to which data integrates with external sources. Paramount for federated ecosystems. |
| *software good practices score* | Score against the ELIXIR Top 10 metrics for life science software good practices. | Medium | ELIXIR Top 10 framework; automated collection via PIsCO | High | All | Covers version control, discoverability, automated builds, test data, documentation. |
| *certification or endorsement* | Certification, selection, or listing of the resource by an external scheme. | Easy | CoreTrustSeal, NIH domain-specific repository list, Global Core Biodata Resources list | Medium-High | Mid–Late | Signals stewardship and maturity, not intrinsic data quality. Record scheme, scope, and date; a directory listing is weaker than certification. |
| **Operations and finance** | | | | | | |
| *uptime*^†^ | Share of time the resource's services are available. | Easy | Application Performance Monitoring (APM) tools | Medium-Low | Mid–Late | Measure of server stability. |
| *page load time* | Time for a page to load fully. | Easy | Application Performance Monitoring (APM) tools | Medium | Mid–Late | Measure of server performance. |
| *latency* | Delay between a request and the first response. | Easy | Application Performance Monitoring (APM) tools or Google Analytics ( not real-time) | Medium | Mid–Late | Measure of server performance. |
| *server errors*^†^ | Rate of errors on the server side, such as failed responses. | Easy | Server-side logs or Application Performance Monitoring (APM) tools | Medium | Mid–Late | Measure of server stability and performance. |
| *client errors* | Rate of errors on the user's side, such as malformed requests or browser errors. | Medium | Application logs or Application Performance Monitoring (APM) tools | Low | Mid–Late | Measure of errors on client end. Possible not addressable. |
| *download speed* | Data transfer rate for downloads. | Easy | Server-side logs or Application Performance Monitoring (APM) tools | Low-Medium | Mid–Late | Download times can be function of client connection speeds. |
| *cpu/gpu usage* | Processor utilization of the resource's servers or compute environment. | Easy | Application Performance Monitoring (APM) tools | High | Mid–Late | Important to evaluate performance and additional needs. |
| *memory usage* | Memory utilization of the resource's servers or compute environment. | Easy | Application Performance Monitoring (APM) tools | High | Mid–Late | Important to evaluate performance and additional needs. |
| *number of users* | Number of distinct users, read as a measure of load. | Easy | Google Analytics or IAM logs for granular details (if available) | Medium | Mid–Late | Indirect measure of computational load/burden. |
| *client queue times* | Time users' jobs wait before they start. | Easy | Application Performance Monitoring (APM) tools or Cloud/infrastructure logs | Medium-High | Mid–Late | Long queue times can result in less usage. |
| *job run times* | Time users' jobs take to complete. | Easy | Application Performance Monitoring (APM) tools or Cloud/infrastructure compute logs | Medium | Mid–Late | Excessive long job run times can result in less usage. |
| *resource publications* | Papers describing the resource's development, maintenance, and scientific contributions. | Medium | PubMed, NIH RePORTER publication links, the resource's own publication list | Medium | Mid–Late | A proxy for team and resource maturity, not public value. |
| *funding cost*^†^ | Total cost of building and running the resource, across all funding sources. | Hard | NIH RePORTER plus the resource's own cost accounting | High | All | Hard to assemble: resources draw on several awards, institutional and in-kind support, and cloud credits, and funding models change over time. Critical for judging feasibility and sustainability. |
| *cost per data reuse event*^†^ | Total curation and hosting cost divided by documented reuse events. | Hard | Funding cost divided by content citations and data use events | High | Mid–Late | Comparable across resources. Inherits the undercount of reuse in its denominator. |
| *sample collection costs* | Cost of collecting samples. | Medium |  | Medium | Early | Cost typically associated with early study period. Cost does not impact sustainability. |
| *sample measurement costs* | Cost of assays and other measurements. | Medium |  | Medium | Early | Cost typically associated with early study period. Cost does not impact sustainability. |
| *QC costs* | Cost of quality control. | Medium |  | Medium | Early | Cost typically associated with early study period. Cost does not impact sustainability. |
| *data storage costs* | Cost of storing the data. | Hard |  | High | All | Costs and requirements can fluctuate over study. |
| *data preservation costs* | Cost of keeping the data available beyond the grant period. | Hard |  | High | Late | Costs and requirements can fluctuate over study. Difficult to assess years in advance. |
| *computing hardware costs* | Cost of buying and replacing computing hardware. | Medium |  | Medium | Early | Costs often associated with initial study period, but replacement costs are possible. |
| *server maintenance costs* | Cost of maintaining servers and services. | Hard |  | High | Mid–Late | Costs can fluctuate. Major source of cost in sustainability period. |
| *cloud-based computing costs* | Cost of cloud computing and storage. | Hard | Cloud cost explorer tools | High | Mid–Late | Costs are highly variable and subject to constant change (for both host and clients). Especially difficult to assess years in advance. |
| *personnel costs* | Cost of staff time, including curation, user support, and development. | Medium |  | High | All | Can be measured in money or time. Requires committed time with relevant expertise. |
