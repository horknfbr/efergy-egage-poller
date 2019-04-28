# efergy-egage-poller
Docker setup with Grafana, InfluxDB, and a custom container to run the polling script.

![](https://i.imgur.com/Y0VzDll.png)

the layout and initial idea borrowed heavily from the work of @frdmn , specifically the [docker-speedtest](https://github.com/frdmn/docker-speedtest) project.  Thanks for the inspiration and code to start from.

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

```
EFERGY_API_TOKEN="<enter your api token>"
```

5. Spin up the containers:

```shell
docker-compose up -d
```

## Configuration

You can make use of the following environment variables / configurations:

| Environment variable | Default value | Description
|----------------------|---------------|------------|
|`EF_INFLUXDB_PORT`|`8087`|port exported to localhost to access InfluxDB |
|`ENGAGE_API_URL`| `https://engage.efergy.com/mobile_proxy/getCurrentValuesSummary?token=` | Engage API endpoint |
|`EFERGY_API_TOKEN`| `none` | APP token generated [here](https://engage.efergy.com/settings/tokens) |
