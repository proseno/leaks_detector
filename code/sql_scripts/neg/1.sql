CREATE DATABASE test;

use test;

CREATE TABLE example_table (
    id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id)
);

INSERT INTO example_table (id, name) VALUES
(1, 'John Doe'),
(2, 'Jane Smith'),
(3, 'Bob Johnson'),
(4, 'Mary Williams'),
(5, 'Tom Brown'),
(6, 'Alice Lee'),
(7, 'David Kim'),
(8, 'Susan Park'),
(9, 'George Lee'),
(10, 'Karen Chen');