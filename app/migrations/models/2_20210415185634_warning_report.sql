-- upgrade --
ALTER TABLE "warning" ALTER COLUMN "type_warning" TYPE SMALLINT USING "type_warning"::SMALLINT;
ALTER TABLE "warning" ALTER COLUMN "type_warning" TYPE SMALLINT USING "type_warning"::SMALLINT;
-- downgrade --
ALTER TABLE "warning" ALTER COLUMN "type_warning" TYPE SMALLINT USING "type_warning"::SMALLINT;
ALTER TABLE "warning" ALTER COLUMN "type_warning" TYPE SMALLINT USING "type_warning"::SMALLINT;
