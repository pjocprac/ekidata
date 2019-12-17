# Create [駅データ.jp](http://www.ekidata.jp/)'s MySQL Table

## Usage

```shell
MYSQL_HOST=[host] MYSQL_USER=[user] MYSQL_PWD=[password] python -m create_data [-h] [-n DBNAME] [-d DATADIR]

Create MySQL tables of ekidata.jp data

optional arguments:
  -h, --help            show this help message and exit

  -n DBNAME, --dbname DBNAME
                        database name
                        (Default: 'ekidata')

  -d DATADIR, --datadir DATADIR
                        data directory of ekidata.jp's csv data
                        (Default: '.')

```
