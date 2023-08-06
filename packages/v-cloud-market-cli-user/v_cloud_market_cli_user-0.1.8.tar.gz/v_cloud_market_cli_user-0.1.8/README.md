# V Cloud Market Command Tool For User

## Install

```pip install v-cloud-market-cli-user```

## Usage

Run the following command to start the command line:

```vcloud```

## Wallet Functions:

- Create new wallet
- Reset wallet
- Recover wallet with seed
- Check balance of address in the wallet
- Export wallet addresses to csv file

## Market Services:

- Explore service provider information
- Explore service category information
- Explore service type information
- Make order with service type id

## Order Services:

- Pay the order with VSYS
- Check the status of order
- View order list
- View specific order information
- Refund an order
- View refundable order list

## user service:

- Explore running user services
- Explore usable user services
    - The status of usable user services are: ServicePending or ServiceRunning.
    - This function is to get secret information from service provider.
- Explore expired user services


## Run cli in local

Install `virtualenv` to run cli tool in local

```shell
pip3 install virtualenv
```

Created virtual environment

```shell
virtualenv venv
```

Start virtual environment

```shell
source venv/bin/activate
```

Run cli in mainnet

```
python3 market_place_cli/use_main_interface.py
```
Run cli in testnet

```
python3 market_place_cli/use_main_interface.py -t
```

Exit virtual environment
```
deactivate
```
