-- upgrade --
ALTER TABLE "report" ALTER COLUMN "trust_point" SET DEFAULT 100;
ALTER TABLE "warning" ALTER COLUMN "type_warning" SET DEFAULT 1;
-- downgrade --
ALTER TABLE "report" ALTER COLUMN "trust_point" SET DEFAULT 101;
ALTER TABLE "warning" ALTER COLUMN "type_warning" DROP DEFAULT;
