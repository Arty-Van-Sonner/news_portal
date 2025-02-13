class DatabaseProcess:
    """
    A process interacting with a database
 
    Attributes
    ----------
    db_name : str
        database name
    timeout : int
        connection timeout (in ms)
 
    Methods
    -------
    get(entity_name, id=None)
        Gets entity by name and an optional ID.
    """
 
    db_name = "users"
 
    def get(self, entity_name, entity_id=None):
        """Gets entity by name and an optional ID.
 
        If the argument `entity_id` isn't passed in,
        the first entity is returned.
 
        Parameters
        ----------
        entity_name: str
            The entity name (also known as the table name).
        entity_id : int, optional
            The ID of the entity.
 
        Raises
        ------
        DatabaseError
            If the database returned an error.
        """
 
        return db_conn.get(
            table=entity_name,
            filters=(
                {'id': entity_id}
                if entity_id is not None
                else {}
            )
        )