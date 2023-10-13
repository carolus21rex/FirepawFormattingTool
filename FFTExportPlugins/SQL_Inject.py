def main(self):
    print(1)


def export_file(file, settings, self):
    data = self.getBoxes()

    # Build SQL injection statements to copy content from content_table2 to content_table1
    sql_statements = []
    data_out = [[] * 4]
    table2_names = []
    join_tables = data[0]
    data = data[1:]
    join_statement = ""
    prev_table = ""
    # first line is join statements
    # format:
    # (first), (new_table), (first), (new_table)
    #
    for joins in join_tables:
        table, column = joins.split('.')
        if join_statement == "":
            join_statement = "\nFROM\n\t" + table
        if prev_table == "":
            prev_table = joins

        else:
            join_statement += "\nJOIN\n\t" + table + " ON " + prev_table + " = " + joins
            prev_table = ""
    join_statement += ";"

    for row_data in data:
        if row_data and row_data[0] != '' and row_data[1] != '':
            content_table1 = row_data[0]  # Destination column for content_table1
            content_table2 = row_data[1]  # Source column for content_table2

            # Extract table name and column name
            if "." in content_table1:
                table1, column1 = content_table1.split('.')
                table2, column2 = content_table2.split('.')
                data_out.append([table2, column2, table1, column1])
                if table2 not in table2_names:
                    table2_names.append(table2)
            if content_table1 and "." not in content_table1:
                table2, column2 = content_table2.split('.')
                data_out.append([table2, column2, content_table1, None])
    
    # create temporary tables
    for name in table2_names:
        temp_table_name = f"temp_{name}"
        create_temp_table = f"CREATE TEMPORARY TABLE db1.{temp_table_name} AS SELECT * FROM db2.{name};"
        sql_statements.append(create_temp_table)

    # Initialize dest_tables, dest_columns, and source_data
    dest_tables = []
    dest_columns = []
    source_data = []

    for line in data_out:
        if line and line[0] not in dest_tables:
            dest_tables.append(line[0])
            dest_columns.append([])
            source_data.append([])

    x = 0
    for table in dest_tables:
        for line in data_out:
            if line and line[0] == table:
                dest_columns[x].append(f"`{line[1]}`")
                if line[3]:
                    source_data[x].append(f"`{line[2]}`.`{line[3]}` AS `{line[1]}`")
                else:
                    source_data[x].append(f"`{line[2]}` AS `{line[1]}`")

        x += 1

    x = 0

    for table in dest_tables:
        copy_to_temp = f"INSERT INTO temp_{table} ({dest_columns[x]}) " \
                       f"SELECT {source_data[x]} " + join_statement
        sql_statements.append(copy_to_temp)
        x += 1

    # Build SQL statement to copy the temporary table to db2
    for name in table2_names:
        copy_to_db2 = f"INSERT INTO db2.{name} SELECT * FROM db1.temp_{name};"
        sql_statements.append(copy_to_db2)

    # Drop the temporary table
    for name in table2_names:
        drop_temp_table = f"DROP TABLE db1.temp_{name};"
        sql_statements.append(drop_temp_table)

    # Write SQL statements to the output_file
    with open(file, 'w') as f:
        for statement in sql_statements:
            f.write(statement + '\n')


def set_export():
    return [("SQL Files", "*.sql")]
