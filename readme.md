# MySQL Dump Tool
=====================

Table of Contents
-----------------

* [Introduction](#introduction)
* [Features](#features)
* [Usage](#usage)
* [Requirements](#requirements)
* [Installation](#installation)
* [Troubleshooting](#troubleshooting)

## Introduction
---------------

MySQL Dump Tool is a simple GUI application designed to help users dump MySQL databases easily. It uses the mariadb-dump command-line tool to export database schema and data to a SQL file.

## Features
------------

* Dump MySQL database schema and data to a SQL file
* Supports various dump options, including:
	+ Remove DEFINER
	+ Include EVENTS
	+ Include TRIGGERS
	+ Include VIEWS
	+ No DATA (Only Schema)
	+ Compress Output
	+ Extended Insert
	+ Add Drop Table
	+ Skip Lock Tables
	+ Single Transaction
* Browse and select output file location
* Validate dump operation and display success or error message

## Usage
-----

1. Launch the application.
2. Enter the database name to dump.
3. Browse and select the output file location.
4. Select desired dump options.
5. Click "Dump Database" to start the dumping process.

## Requirements
--------------

* Python 3.6+
* mariadb-dump command-line tool
* tkinter library
* mysql-connector-python library

## Installation
--------------

1. Clone the repository or download the source code.
2. Install required libraries using pip:
```bash
pip install mysql-connector-python
