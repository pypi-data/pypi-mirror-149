import fire
from .dex import DexCommand
from .profile import ProfileCommand
from .user import UserCommand
from .project import ProjectCommand
from .dev import DevCommand
from .app import AppCommand
from .storage import StorageCommand
from .quota import QuotaCommand


def main():
    fire.Fire(
        {
            "dex": DexCommand,
            "profile": ProfileCommand,
            "user": UserCommand,
            "project": ProjectCommand,
            "dev": DevCommand,
            "app": AppCommand,
            "storage": StorageCommand,
            "quota": QuotaCommand,
        }
    )


if __name__ == "__main__":
    main()
