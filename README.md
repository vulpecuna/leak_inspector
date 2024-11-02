# Leak Inspector

Leak Inspector processes a list of emails to find leaked passwords using external APIs. If similar emails are found with the same exact password, they are processed and assumed to be owned by the same user.

* [ProxyNova API](https://www.proxynova.com/tools/comb): provides API access to the COMB breach
* ... more to come

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
