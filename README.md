# Log4j dork scanner
This is an auto script to search, scrape and scan for Apache Log4j CVE-2021-44228 affected files using Google dorks.

- ### Installation:
```shell
git clone https://github.com/JagarYousef/log4j-dork-scanner
cd  log4j-dork-scanner
pip install -r requirments.txt
```

- ### Scanning:
```shell
 python scanner.py -d YOUR_SEARCH_DORK -n NUMBER_OF_GOOGLE_RESULTS_PAGES
```
- ### Example:
```shell
python scanner.py -d inurl:member.jsp -n 10
```
<br>

### Disclaimer 
- I am not responsible about how you use it, I just provide it for educational and demonstration purposes!
- I don't provide support on it, you can fork it as you want