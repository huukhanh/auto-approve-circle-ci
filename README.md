# auto-approve-circle-ci

### This script will auto approve "on-hold" job on cirleci by api token.
1. Come to https://app.circleci.com/settings/user/tokens and create api token
2. Change token under variable ```personalToken```(line 4)
3. Add project slug to variable ```slugs```(line 5)
4. Install dependences(requests: ```pip3 install requests```)
5. Run script by: ```python3 main.py```

### License
[MIT](https://choosealicense.com/licenses/mit/)


Checked circle CI at: Sun Dec 10 01:02:54 UTC 2023
