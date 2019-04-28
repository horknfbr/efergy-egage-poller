# efergy-egage-poller
Docker setup with Grafana, InfluxDB, and a custom container to run the polling script.

![](https://i.imgur.com/Y0VzDll.png)

the layout and initial idea borrowed heavily from the work of [frdmn](https://github.com/frdmn) , specifically the [docker-speedtest](https://github.com/frdmn/docker-speedtest) project.  Thanks for the inspiration and code to start from.

## Installation

1. Install the pre-req of Docker
2. Clone this repository:

```shell
git clone https://github.com/horknfbr/efergy-egage-poller
```

3. Create a copy of the sample `.env` file and at least fill in the API key from Engage:

```shell
cp .env.sample .env
```
4. generate an app token on [Engage](https://engage.efergy.com/settings/tokens) and add it to .env in the `EFERGY_API_TOKEN` variable

```shell
EFERGY_API_TOKEN="<enter your api token>"
```

5. Build/Spin up the containers:

```shell
$ docker-compose build
$ docker-compose up -d
```

## Configuration

You can make use of the following environment variables / configurations:

| Environment variable | Default value | Description
|----------------------|---------------|------------|
|`EF_INFLUXDB_PORT`|`8087`|port exported to localhost to access InfluxDB |
|`ENGAGE_API_URL`| `https://engage.efergy.com/mobile_proxy/getCurrentValuesSummary?token=` | Engage API endpoint |
|`EFERGY_API_TOKEN`| `none` | APP token generated [here](https://engage.efergy.com/settings/tokens) |

## Usage

### Services

#### Start/create services


```shell
$ docker-compose up -d
Creating efergy-influx ... done
Creating efergy-poller  ... done
Creating efergy-grafana ... done
```

#### Stop services

```shell
$ docker-compose stop
Stopping efergy-grafana ... done
Stopping efergy-poller  ... done
Stopping efergy-influx  ... done
```

#### Upgrade services

```shell
$ docker-compose stop
$ docker-compose pull
$ docker-compose rm
$ docker-compose build
$ docker-compose up -d
```

#### Check logs

```shell
$ docker-compose logs -f
```

```shell
$ docker-compose logs -f efergy-poller
```

### Data import

the `efergy-poler.py` script located in `./docker/efergy-poller/` allows you to import reports downloaded from the [Engage Report](https://engage.efergy.com/reports) site. For the script to function the contents of `.env` must be export to the environment

![](https://i.imgur.com/4SNFLzrh.png)

I suggest `minute` resolution to match the polling period of the docker poller

Import Example:
```shell
$ cat ../../.env | xargs export && ./efergy-poller.py -i ~/Downloads/engage_report_03_2019_minute.csv
```

### Script Usage
```shell
$ ./efergy-poller.py -h
usage: efergy-poller.py [-h] [-i, --import IMPORTCSV] [-d, --debug]

Simple Python script to pull from engage API and store data in influxdb

optional arguments:
  -h, --help            show this help message and exit
  -i, --import IMPORTCSV
                        import csv downloaded from engage"
  -d, --debug           output json to be inserted to influx, but do not
                        insert"
```

### Grafana

#### Dashboard

The dashboard shows Grid power as positive, and Solar as negative, it will combine multiple sensors based on if they are set as generation of consumption, see [efergy docs](https://efergy.com/support/wp-content/uploads/2017/05/engage_uk.pdf) on how to do this.


#### Administrative access

Access [http://localhost:3000](`http://localhost:3000`) and login using the following default credentials:

* Username: `admin`
* Password: `admin`

## Contributing

1. Fork it
2. Create your feature branch:

```shell
git checkout -b feature/my-new-feature
```

3. Commit your changes:

```shell
git commit -am 'Add some feature'
```

4. Push to the branch:

```shell
git push origin feature/my-new-feature
```

5. Submit a pull request

## Requirements / Dependencies

* Docker (incl. `docker-compose`)
* python influxdb (`pip install influxdb`) <- only needed if you do imports outside of the docker container

## Version

1.0.0

## License

[MIT](LICENSE)
