# Events Delivery System

The **Events Delivery System (EDS)** library provides a suite of high-level Python utilities to
work with the *Google Cloud Platform*.

The main purpose of this library is to provide a unified interface to dealing with the same
Domain across the range of GCP Python APIs.

## Installation

Install this library in a virtualenv using pip.

```
pip install rbx[eds]
```

## Dimensional Modeling

EDS is build around a dimensional model, a data design technique optimized for data querying.
It is particularly well suited for the querying of very large sorted data sets.

The dimensional model differs from a traditional entity-relationship model in its normalized form.
Dimensional models are denormalized to a 2nd-normal form, each fact table (the metrics) having a
one-to-many relationship with its context (the dimensions).

The dimensional model records a series of facts, surrounded by their contexts which are known
to be true at the time of measurement.

Dimensions are of 3 types:

* **Model Dimensions**: these reflect the operational entities defined in the _Domain Design_.
  For instance, a software dealing with the leasing of cars would probably define a `Car` entity,
  and some sort of `User` entity to record customers. These classes are typically Model Dimensions,
  or simply Dimensions (D). _They live in BigQuery, CloudSQL, and Datastore._
* **Degenerate Dimensions**: a dimension that only exists alongside the fact is called a Degenerate
  Dimension (DD). For instance, upon returning a leased car to the station, its `State` can only be
  known when the car is returned. _These DDs only live in Datastore._
* **Generated Dimensions**: these are static dimensions for which we generate the set of data.
  For instance, the `Time` or `Day` are deterministic and never change. _Generated Dimensions (GD)
  are pre-populated in BigQuery, CloudSQL, and Datastore._

## Schema Definition

The dimensions and facts are defined using a YAML-formated `schema.yaml` file.

> By default, this file is looked up at the root of the calling script.
> This can be overridden by setting the `SCHEMA_YAML_PATH` environment variable.

To load the `Dimensions` and `Facts`:

```python
from rbx.eds.config import schema

schema.DIMENSIONS
schema.FACTS
```

### Dimensions

The dimensions are defined under the `dimensions` global section:

```yaml
dimensions:
  -
    name: DimensionKind
    key: dimension_id
    ancestor:
      kind: ParentKind
      lookup: "{parent_id}"
    relatives:
      - kind: RelativeKind
        lookup: "{relative_id}"
      - kind: SecondRelativeKind
        lookup: "{second_relative_id}"
    model_based: true
    key_field: dimension_key
    id_fields:
      - dimension_id
    index_fields:
      - dimension_id
    schema:
      - {name: dimension_key, type: INTEGER, mode: REQUIRED}
      - {name: dimension_id, type: INTEGER}
      - {name: dimension_name, type: STRING}
      - {name: archived, type: BOOLEAN}
      - {name: timestamp, type: TIMESTAMP}
```

A dimension has the following parameters:

 - `name` - The Datastore `Kind`.
 - `key` - The id used to uniquely identify the dimension. It is also used as a base to the various
   tables created in BigQuery and CloudSQL.
 - `ancestor` - To ensure strong consistency in Datastore, each `Kind` is created within an
   `EntityGroup`. This field defines this group's `Kind`, and how to locate it.
   The lookup field may be a sinple string (when the ancestor is unque), a simple lookup pattern
   (e.g.: `{property}`, to locate the entity based on the property value), and a multiple lookup
   pattern (e.g.: `{property_1},{property_2}`, to locate the entity based on multiple properties).
   __This parameter is optional__.
 - `relatives` - For dimensions that rely on other relations to exist, the dependents are defined
   as relatives. Each relative has a `kind` and `lookup` field, whose meaning is the same as for
   the `ancestor` lookup.
   __This parameter is optional__.
 - `model_based` - A flag that defines whether the dimension is based on an operational entity.
   Setting this parameter to `False` will flag the dimension as _Generated_.
   __This parameter is optional__.
 - `key_field` - The name of the dimension's surrogate key field.
   __This parameter is required for model-based dimensions__.
 - `id_fields` - The operational ID field of the dimension.
   __This parameter is required for model-based dimensions__.
 - `index_fields` - A list of dimension fields to index, both in Datastore and in CloudSQL.
   __This parameter is optional__.
 - `schema` - The fields of the dimension.
   __This parameter is required for model-based dimensions__.

> Note that a `model_based` dimension without a `schema` is effectively a DD.
> Whereas typically DG are non-`model_based` and do have a `schema`.
> When `model_based` is `True`, and a `schema` is provided, it is a Model Dimension.

### Facts

The facts are defined under the `facts` global section:

```yaml
facts:
  -
    name: fact
    schema:
      - {name: day_key, type: INTEGER, required: Yes}
      - {name: time_key, type: INTEGER, required: Yes}
      - {name: dimension_key, type: INTEGER, required: Yes}
      - {name: timestamp, type: TIMESTAMP, required: Yes}
      - {name: fact, type: FLOAT, required: Yes}
```

A fact has the following parameters:

 - `name` - The name used in BigQuery.
 - `schema` - The fields of the fact.

> Note that facts only exist in BigQuery.

## Dimensions Data Lake

All _Model_ and _Generated_ Dimensions are stored in Datastore.
How they end up there is taken care of by another sub-system, though they must use the same schema
as their BigQuery and CloudSQL counterpart. Each field is represented by a Datastore Entity attribute.

These Dimensions are being kept up-to-date by the operational system, and changes need to be
periodically propagated to BigQuery and CloudSQL.

### Datastore Ancestors & Indexes

In order to guarantee strong write consistency, all the Datastore Entities are inserted with
a parent Entity. When using parents, a Datastore ancestor query can then be performed.

> See [ancestor queries](https://cloud.google.com/datastore/docs/concepts/queries#ancestor_queries) and
> [data consistency](https://cloud.google.com/datastore/docs/concepts/structuring_for_strong_consistency)
> for more info.

Indexes are created by default for all entities, attributes, and ancestors, ascending and descending.

## BigQuery

The `BigQuery` class is a simple wrapper around the `google.cloud.bigquery.Client` class, so
instantiating it doesn't require any extra parameter.

`BigQuery` provides helpers to create or re-create tables based on an `EDS` schema, as well as
update a table's schema.

```python
from rbx.eds.config import schema
from rbx.eds.bigquery import BigQuery

bigquery = BigQuery(project='project_id')
dimension = schema.DIMENSIONS['dimension_id']

bigquery.create_table(dataset='dimensions', recreate=False, schema=dimension.schema,
                      table_name=dimension.key)

bigquery.update_table(dataset='dimensions', schema=dimension.schema, table_name=dimension.key)
```

## CloudSQL

> Note that `rbx` only supports CloudSQL with MySQL.

The `CloudSQL` class must be instantiated with a `Database`.
A `Database` is a **SQLAlchemy** `Engine` wrapper class that uses the default pooling settings
recommended by GCP.

```python
from rbx.db import Database
from rbx.eds.cloudsql import CloudSQL

db = Database('DB_ENGINE_URL')
cloudsql = CloudSQL(db)
```

`CloudSQL` provides helpers to create or re-create tables based on an `EDS` schema.

> Updating an existing table's schema is currently not supported.

```python
from rbx.eds.config import schema

dimension = schema.DIMENSIONS['dimension_id']
cloudsql.create_table(table=dimension.tables[dimension.key], recreate=False)
```

> The `tables` property of a Dimension includes 2 SQLAlchemy `Table` definitions: one for a table
> named after the Dimension's `key`, and another named using the `_staging` suffix.

### CloudSQL/MySQL Charset

UTF-8 support is only available since MySQL 5.7 with the `utf8mb4` charset.

As this isn't the default charset used by MySQL, it must be set as a flag:

```
character_set_server = utf8mb4
```

In order to display all characters properly via the **Cloud Shell**, remember to set the client
connection charset to `utf8mb4` from the `mysql` console, with:

```
SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## Loading Data to a Dimension

A data payload (usually from a Dimension stored in Datastore) can be loaded to BigQuery and CloudSQL
using the `BigQuery` and `CloudSQL` classes.

```python
payload = [
    {
        'dimension_key': 123,
        'dimension_id': 364577,
        'dimension_name': 'D123',
        'archived': False,
        'timestamp': '2018-11-02T12:01:05.571694+00:00',
    },
]

bigquery.load(dataset='dimensions', table_name=dimension.key, schema=dimension.schema,
              payload=payload)
cloudsql.load(table=dimension.tables[dimension.key], payload=payload)
```

**Note on CloudSQL**

Any schema field ending with `_name` will be encoded to UTF-8 if they are recieved as `bytes`,
before writing to CloudSQL.

All `timestamp` fields will be stripped of any trailing timezone information, again before loading
into CloudSQL. The `timestamp` field is expected to be in ISO 8601.

## Dimension Update

A *Dimension Update* will update the records in a table with the records from its staging table.

```python
bigquery.update(table_name=dimension.key, key_field=dimension.key_field, schema=dimension.schema)
cloudsql.update(table_name=dimension.key, key_field=dimension.key_field, schema=dimension.schema)
```

## Dimension Insert

A *Dimension Insert* will insert records from its staging table that do not exist in its own table.

```python
bigquery.insert(table_name=dimension.key, key_field=dimension.key_field, schema=dimension.schema)
cloudsql.insert(table_name=dimension.key, key_field=dimension.key_field, schema=dimension.schema)
```
