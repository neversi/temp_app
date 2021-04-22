#! /usr/bin/env bash

sleep 2;

aerich init -t app.config.TORTOISE_ORM --location ./app/migrations

aerich init-db

#aerich migrate --name Init && aerich upgrade