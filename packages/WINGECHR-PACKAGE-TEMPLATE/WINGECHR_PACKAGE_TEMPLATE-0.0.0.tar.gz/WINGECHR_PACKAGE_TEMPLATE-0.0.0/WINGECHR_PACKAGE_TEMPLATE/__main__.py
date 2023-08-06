import logging

logging.basicConfig(
    format="[%(asctime)s %(levelname)7s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)


def main():
    logging.info("HELLO")


if __name__ == "__main__":
    main()
