# A2B-Dispatch Bot

This Python Discord bot is designed to estimate the price of a ferry flight using the AVWX API and the FSEconomy Datafeed.

## Getting Started

This project works on Heroku or your own VPS.

### Prerequisites

All of the prerequisites are listed below and are also mentioned in the requirements.txt.

```
discord.py
geopy.distance
requests
```

Further, a config.json file is needed, this should be located in the root folder. This includes the Discord Token as well as the AVWX authorization Header and the FSEconomy Datafeed. 
The AVWX header can be obtained on [AVWX](https://avwx.rest/). The format needs to be as follows

```
{
	"token": "Discord Token",
        "datafeed": "your own datafeed",
	"authHeader": "Authorization Header"
}
```

## Built With

* [discord.py](https://github.com/Rapptz/discord.py) - The main framework used
* [geopy](https://github.com/geopy/geopy) - used for distance calculations
* [requests](https://github.com/psf/requests) - HTTP library
* [FSEconomy](https://fseconomy.net) - Datafeed
* [AVWX](https://github.com/avwx-rest/avwx-api) - used for current weather and station information 
* [PyCharm](https://www.jetbrains.com/pycharm/) - Python IDE

## Authors

* **Jan Imhof** - [No1Cheats](https://github.com/No1Cheats)

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/No1Cheats/a2b-disptach/blob/master/LICENSE) file for details
