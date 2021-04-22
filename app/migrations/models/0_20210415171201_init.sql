-- upgrade --
CREATE TABLE IF NOT EXISTS "proctor" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "student" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL,
    "on_exam" BOOL NOT NULL  DEFAULT False
);
CREATE TABLE IF NOT EXISTS "subject" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS "session" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "scheduled" TIMESTAMPTZ NOT NULL,
    "subject_id" INT NOT NULL REFERENCES "subject" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "report" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "time_duration" BIGINT NOT NULL,
    "video_web" TEXT NOT NULL,
    "video_screen" TEXT NOT NULL,
    "trust_point" INT NOT NULL  DEFAULT 101,
    "student_id" INT NOT NULL REFERENCES "student" ("id") ON DELETE CASCADE,
    "session_id" INT NOT NULL REFERENCES "session" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "warning" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "frame" TEXT,
    "duration" BIGINT NOT NULL,
    "type_warning" SMALLINT NOT NULL,
    "report_id" INT NOT NULL REFERENCES "report" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "warning"."type_warning" IS 'Absence: 1\nMore: 2\nXY: 3\nXZ: 4\nYZ: 5';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "proctor_subject" (
    "subject_id" INT NOT NULL REFERENCES "subject" ("id") ON DELETE CASCADE,
    "proctor_id" INT NOT NULL REFERENCES "proctor" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "student_subject" (
    "subject_id" INT NOT NULL REFERENCES "subject" ("id") ON DELETE CASCADE,
    "student_id" INT NOT NULL REFERENCES "student" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "proctor_session" (
    "session_id" INT NOT NULL REFERENCES "session" ("id") ON DELETE CASCADE,
    "proctor_id" INT NOT NULL REFERENCES "proctor" ("id") ON DELETE CASCADE
);
