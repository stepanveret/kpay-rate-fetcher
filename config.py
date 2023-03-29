from pydantic import BaseSettings


class AppConfig(BaseSettings):
    URL: str = (
        "https://koronapay.com/transfers/online/api/transfers/tariffs?sendingCountryId=RUS&sending"
        "CurrencyId=810&receivingCountryId=GEO&receivingCurrencyId=981&paymentMethod=debitCard&"
        "receivingAmount=20000&receivingMethod=cash&paidNotificationEnabled=false"
    )
    INTERVAL_STARTUP: int = 60
    INTERVAL_SUCCESS: int = 360
    INTERVAL_FAIL: int = 180

    INFLUXDB_URL: str = "http://influxdb:8086"
    INFLUXDB_TOKEN: str = "user:password"
    INFLUXDB_ORG: str = "myorg"
    INFLUXDB_BUCKET: str = "mydb"

    SESSION_HEADERS: dict = {
        "Accept": "application/vnd.cft-data.v2.99+json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0"
            " Safari/537.36"
        ),
    }

    class Config:
        env_file = ".env"
