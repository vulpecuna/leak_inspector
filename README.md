# Leak Inspector

Leak Inspector processes a list of emails to find leaked passwords using external APIs. If similar emails are found with the same exact password, they are processed and assumed to be owned by the same user.

* [HudsonRock API](https://cavalier.hudsonrock.com/docs) 🛻: provides API access to their known list of infected devices
* [LeakCheck](https://leakcheck.io/) 🛻: find breaches and exposed fields
* [ProxyNova API](https://www.proxynova.com/tools/comb)  🛻: provides API access to the COMB breach
* [BreachDirectory](https://breachdirectory.org/) 💵: paid, not tested, not implemented
* [DeHashed](https://dehashed.com/) 💵: paid, not tested, not implemented
* [Intelligence X](https://intelx.io/) 💵: paid, not tested, not implemented
* [LeakedDomains](https://leaked.domains) 💵: paid, not tested, not implemented
* [LeakLookup](https://leak-lookup.com/) 💵: paid, not tested, not implemented
* [ShatteredSecrets](https://scatteredsecrets.com/) 💵: paid, not tested, not implemented
* [Snusbase](https://www.snusbase.com) 💵: paid, not tested, not implemented
* [WeLeakInfo](https://weleakinfo.io/) 💵: paid, not tested, not implemented

This tool is intended for use with "linkedin_osint" tools such as [linkedin_nubela_osint](https://github.com/vulpecuna/linkedin_nubela_osint) or [linkedin_rocketreach_osint](https://github.com/vulpecuna/linkedin_rocketreach_osint). The following input file format is required at a minimum:

```json!
{
    "emails": [
        {
            "id": "abc-def-012345",
            "first_name": "optional",
            "last_name": "optional",
            "emails": [
                "dummy@gmail.com"
            ]
        }
    ]
}
```
