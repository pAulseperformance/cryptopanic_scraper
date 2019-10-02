


<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/grilledchickenthighs/cryptopanic_scraper">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Cryptopanic Scraper</h3>

  <p align="center">
    Headless chromedriver for automatic scraping of cryptopanics asynchronous newsfeed.
    <br />
    <a href="https://github.com/grilledchickenthighs/cryptopanic_scraper"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/grilledchickenthighs/cryptopanic_scraper/issues">Report Bug</a>
    ·
    <a href="https://github.com/grilledchickenthighs/cryptopanic_scraper/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://cryptopanic.com/)

Cryptopanic is a crypto news aggregator that offers realtime news feeds of all things crypto as well 
as user input for ratings.
This project was designed to scrape the data from their website so it could be later analyzed using NLP.

### Built With

* [Python](https://github.com/topics/python)
* [Selenium](https://github.com/topics/selenium)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites


* python 3
* pip 


### Installation
 
1. Clone the cryptopanic_scraper
    ```sh
    git clone https:://github.com/grilledchickenthighs/cryptopanic_scraper.git
    ```
2. Change directory
    ```sh
    cd cryptopanic_scraper
    ```
3. Install packages
    ```sh
    pip install -r requirements.txt
    ```



<!-- USAGE EXAMPLES -->
## Usage
Simply run:
```sh
python cryptopanic_scraper.py --headless
```
If you want to see it in action, run the script without any flags.
```sh
python cryptopanic_scraper.py 
```
If you want to filter the type of news to scrape add the --filter flag and choose
a type. {all,hot,rising,bullish,bearish,lol,commented,important,saved}
```sh
python cryptopanic_scraper.py --filter hot
```
You can always use the --help flag if you forget these commands:
```sh
python cryptopanic_scraper.py --help

usage: cryptopanic_webdriver.py [-h] [-v]
                                [-f {all,hot,rising,bullish,bearish,lol,commented,important,saved}]
                                [-s]

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -f {all,hot,rising,bullish,bearish,lol,commented,important,saved}, --filter {all,hot,rising,bullish,bearish,lol,commented,important,saved}
                        Type of News filter
  -s, --headless        Run Chrome driver headless
```

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/grilledchickenthighs/cryptopanic_scraper/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

[Paul Mendes](https://grilledchickenthighs.github.io/) - [@BTCTradeNation](https://twitter.com/BTCTradeNation) - [paulsperformance@gmail.com](mailto:paulseperformance@gmail.com)

Project Link: [https://github.com/grilledchickenthighs/cryptopanic_scraper](https://github.com/grilledchickenthighs/cryptopanic_scraper)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/grilledchickenthighs/cryptopanic_scraper?style=flat-square
[contributors-url]: https://github.com/GrilledChickenThighs/cryptopanic_scraper/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/grilledchickenthighs/cryptopanic_scraper?style=flat-sqaure
[forks-url]: https://github.com/GrilledChickenThighs/cryptopanic_scraper/network/members
[stars-shield]: https://img.shields.io/github/stars/grilledchickenthighs/cryptopanic_scraper?style=flat-square
[stars-url]: https://github.com/grilledchickenthighs/cryptopanic_scraper/stargazers
[issues-shield]: https://img.shields.io/github/issues/grilledchickenthighs/cryptopanic_scraper.svg?style=flat-square
[issues-url]: https://github.com/grilledchickenthighs/cryptopanic_scraper/issues
[license-shield]: https://img.shields.io/github/license/grilledchickenthighs/cryptopanic_scraper.svg?style=flat-square
[license-url]: https://github.com/grilledchickenthighs/cryptopanic_scraper/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/paul-mendes
[product-screenshot]: images/screenshot.png