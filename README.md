# Leak Inspector

Leak Inspector processes a list of emails to find leaked passwords using external APIs. If similar emails are found with the same exact password, they are processed and assumed to be owned by the same user.

* [ProxyNova API](https://www.proxynova.com/tools/comb): provides API access to the COMB breach
* [Cavalier API](https://cavalier.hudsonrock.com/docs): provides API access to their known infected devices
* [Snusbase](https://www.snusbase.com): paid, not tested, not implemented 
* [Intelx](https://intelx.io/): paid, not tested, not implemented
* [WeLeakInfo](https://weleakinfo.io/): paid, not tested, not implemented
* [LeakLookup](https://leak-lookup.com/): paid, not tested, not implemented
* [BreachDirectory](https://breachdirectory.org/): paid, not tested, not implemented
* [DeHashed](https://dehashed.com/): paid, not tested, not implemented

This tool is intended for use with [linkedin_osint](https://github.com/vulpecuna/linkedin_osint). The following input file format is required at a minimum:

```json!
{
    "emails": [
        {
            "id": "abc-def-012345",
            "first_name": "Abc",
            "last_name": "Def",
            "emails": [
                "dummy@gmail.com"
            ]
        }
    ]
}
```
