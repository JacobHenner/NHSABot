# North Hudson Sewerage Authority Bot (NHSABot)

NHSABot is a Python bot that tweets when [North Hudson Sewerage Authority](http://www.nhudsonsa.com/) sewage is draining into the Hudson River, between New York and New Jersey. These events are referred to as [combined sewer overflows](https://en.wikipedia.org/wiki/Combined_sewer#Combined_sewer_overflows_\(CSOs\)) (CSOs).

This project is primarily hosted on [SocialCoders](https://socialcoders.org/JacobHenner/NHSABot). 

## Getting Started

### Prerequisites

Install required Python dependencies using pip.

`pip install -r requirements.txt`

### Running

To run all components: `python NHSABot.py`

To successfully run the Twitter component, the bot expects the following environment variables to be set.

1. CONSUMER_SECRET
2. CONSUMER_TOKEN
3. USER_KEY
4. USER_SECRET

## Authors

* **Jacob Henner** - [JacobHenner](https://github.com/JacobHenner)


## License

This project is licensed under the GNU GPLv3 - see the [LICENSE](LICENSE) file for details.

## Additional Notes

* This project is unaffiliated with the North Hudson Sewerage Authority, any other agency, or any municipality.
* The data collected by this bot depends upon a third-party SCADA system, and as such, its accuracy cannot be guaranteed.
* Please be respectful when running the status updater and ensure that you rate-limit your queries.
