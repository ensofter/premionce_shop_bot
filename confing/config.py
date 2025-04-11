from dataclasses import dataclass

from environs import Env


@dataclass
class TgConf:
    bot_token: str = None


@dataclass
class DbConf:
    db_url: str = None


@dataclass
class Config:
    tg_conf: TgConf = None
    db_conf: DbConf = None

    @classmethod
    def load_config(cls):
        config = Env()
        config.read_env()

        token = config('BOT_TOKEN')
        db_url = config('DB_URL')

        return cls(
            tg_conf=TgConf(
                bot_token=token
            ),
            db_conf=DbConf(
                db_url=db_url
            )
        )
