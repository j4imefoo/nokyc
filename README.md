# lsbisq
A script that lists all current Bisq offers in the terminal

[Bisq](https://bisq.network) is a decentralized bitcoin exchange that allows us to buy or sell bitcoin peer-to-peer. 

This script shows all current buy or sell offers in the Bisq network in our preferred fiat currency. 

# Parameters
We can indicate the following paramenters in our script header:
- `fiat`: currency we want to exchange for bitcoin
- `limit`: only list quotations below this deviation from market price
- `avoid_methods`: payment methods to hide in order to get a cleaner output

# Usage
- `lsbisq`: shows all BTC sell offers
- `lsbisq -r`: shows all BTC buy offers

# Possible use cases
One can use this script to check on current offers and decide if starting the Bisq program in order to buy or sell bitcoin. Take into account that it is possible to run this script wherever we have Python installed, including an Android phone using Termux.

It is very easy to automate it and, eg., get an SMS notification once the script finds a quotation we might be interested in. 

# More information
https://twitter.com/j4imefoo

If you want to buy me a beer:

- https://paynym.is/+luckywood116
- https://tippin.me/@j4imefoo
