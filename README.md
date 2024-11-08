# Leak Inspector

Leak Inspector is a tool that processes a list of emails to identify leaked passwords using various external APIs. It assumes that similar emails with the same exact password belong to the same user.

Currently supported APIs:

* [BreachDirectory](https://breachdirectory.org/) 🛻💵 ($8 for 1000 credits): Access to censored leaked credentials. Implementation only calls this API if we know a password was leaked, but we didn't get one from other APIs.
* [HashMob](https://hashmob.net) 🛻: Discover plaintext passwords for cracked hashes. You are given 500 credits per hour for free. Five dollars are worth 50k credits.
* [HudsonRock API](https://cavalier.hudsonrock.com/docs) 🛻: Accesses a known list of infected devices.
* [LeakCheck API](https://leakcheck.io/) 🛻: Finds breaches and exposed fields.
* [ProxyNova API](https://www.proxynova.com/tools/comb)  🛻: Provides access to the COMB breach.
* [Snusbase](https://www.snusbase.com) ($333 for lifetime, $17 for a month) 💵: Access to credential leaks. API [rate limit](https://docs.snusbase.com/) is 2,048 searches per 12 hours. You can search by email, IP, LinkedIn URL (*sometimes*), username, name, password, hash, or domain.

Well-known platforms that we may add:

* [Aura](https://scan.aura.com/) 🛻 : show censured passwords from their website. Sadly, there is no API.
* [DeHashed](https://dehashed.com/) ($30 for 1000 credits) 💵: Access to credential leaks.
* [Intelligence X](https://intelx.io/) ($2500/year) 💵: Access to credential leaks.
* [LeakedDomains](https://leaked.domains) ($750 for 500 credits) 💵: Access to credential leaks.
* [LeakLookup](https://leak-lookup.com/) ($100 for 300 credits) 💵: Access to credential leaks.
* [LeakPeek](https://leakpeek.com/) ($10 for a month) 💵: Access to credential leaks.
* [WeLeakInfo](https://weleakinfo.io/) ($125 for lifetime, $40 for a month) 💵: Access to credential leaks.
* [DDoSecrets](https://data.ddosecrets.com/?C=M&O=A) 🛻: Free credentials leaks available for download.

This tool is intended for use with "linkedin_osint" tools such as [linkedin_nubela_osint](https://github.com/vulpecuna/linkedin_nubela_osint) or [linkedin_rocketreach_osint](https://github.com/vulpecuna/linkedin_rocketreach_osint). The following input file format is required at a minimum:

```json!
[
    {
        "id": "abc-def-012345",
        "first_name": "optional",
        "last_name": "optional",
        "emails": [
            "dummy@gmail.com"
        ]
    }
]
```
