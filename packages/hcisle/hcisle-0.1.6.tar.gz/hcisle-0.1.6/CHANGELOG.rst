Release History
===============

**0.1.6 2022-04-25**

*   fixed an issue that caused DB constrain violations with Python < 3.9
*   removed the ``--syslog-plain`` argument, resulting records sent to syslog are always
    plain from now on (additional information removed)


**0.1.5 2022-02-14**

*   renamed to **hcisle**
*   added database maintenance - delete old records and VACUUM the database
*   added the ability to work on an existing log package (no collection in this case),
    mainly for testing purposes

**0.1.4 2022-02-06**

*   now collecting queries using the
    Workflow Designer / Index Collection / Query, as well
*   records in the database are now marked as sent once transmitted to sylog,
    preventing from duplicate records being sent.
*   added sending the found log records to a syslog server, optionally.
    this will send the records in timely ascending order, either the plain log record
    or the record with additonal information fields
*   added the exclusion filter string as a separate column to the solrquery table,
    in case a filter was used.

**0.1.3 2022-01-26**

*   ziphandler is now also looking for SOLr logfiles who's filename start with
    "solr.service" in addition to "solr.log". Needed for HCI 2.0.
*   changed the db record structure a bit to have the more granular epoch timestamp
    as part of the index. Added another clear-text field.
*   now using the 'NOW=' field from the solr log records as the timestamp
*   added the query string as a separate column to the solrquery table, for convenience

**0.1.2 2022-01-25**

*   made sure that the folders given by call parameters are used properly
*   added information about "updating" to the documentation
*   slightly fixed the autostart documentation
*   removed showing query strings when logging is set to "info"

**0.1.0 2022-01-24**

*   added documentation

**0.0.1 2021-12-01**

*   initial commit
