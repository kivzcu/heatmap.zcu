from Utilities.Database import database_loader


def clean_database() -> None:
    """
    Drops every collection in database
    """
    # Creating connection
    mydb = database_loader.create_database_connection()

    # Retrieve list of all collections
    collections = mydb.list_collection_names()

    # Drop of all collections
    for name in collections:
        print(name)
        mydb[name].drop()


def main() -> None:
    print('Data z databáze budou smazána:')
    clean_database()


if __name__ == "__main__":
    main()
