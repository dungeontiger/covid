from get_data import get_data
from create_charts import create_charts


def update():
    # get the new data
    get_data()
    # generate the charts and other output
    create_charts()


if __name__ == "__main__":
    update()