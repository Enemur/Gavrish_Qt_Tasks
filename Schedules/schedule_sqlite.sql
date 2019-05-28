-- Creator:       MySQL Workbench 8.0.16/ExportSQLite Plugin 0.1.0
-- Author:        Pavel
-- Caption:       New Model
-- Project:       Name of the project
-- Changed:       2019-05-28 15:12
-- Created:       2019-04-26 13:34
PRAGMA foreign_keys = OFF;

-- Schema: mydb
ATTACH "mydb.sdb" AS "mydb";
BEGIN;
CREATE TABLE "mydb"."lectures"(
  "id" INTEGER PRIMARY KEY NOT NULL,
  "name" VARCHAR(45) NOT NULL,
  CONSTRAINT "name_UNIQUE"
    UNIQUE("name")
);
CREATE TABLE "mydb"."teachers"(
  "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  "name" VARCHAR(45) NOT NULL
);
CREATE TABLE "mydb"."groups"(
  "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  "name" VARCHAR(45) NOT NULL,
  CONSTRAINT "group_UNIQUE"
    UNIQUE("name")
);
CREATE TABLE "mydb"."subjects"(
  "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  "name" VARCHAR(45) NOT NULL,
  "lectureId" INTEGER NOT NULL,
  "type" TEXT NOT NULL CHECK("type" IN("ПЗ", "ЛК")),
  "teacherId" INTEGER NOT NULL,
  CONSTRAINT "fk_subjects_2"
    FOREIGN KEY("teacherId")
    REFERENCES "teachers"("id"),
  CONSTRAINT "fk_subjects_1"
    FOREIGN KEY("lectureId")
    REFERENCES "lectures"("id")
);
CREATE INDEX "mydb"."subjects.fk_subjects_2_idx" ON "subjects" ("teacherId");
CREATE INDEX "mydb"."subjects.fk_subjects_1_idx" ON "subjects" ("lectureId");
CREATE TABLE "mydb"."schedule"(
  "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  "idGroup" INTEGER NOT NULL,
  "numberOfWeek" INTEGER NOT NULL,
  "subjectId" INTEGER NOT NULL,
  "day" TEXT NOT NULL CHECK("day" IN("понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье")),
  "numberOfSubject" INTEGER NOT NULL,
  CONSTRAINT "fk_schedule_1"
    FOREIGN KEY("idGroup")
    REFERENCES "groups"("id"),
  CONSTRAINT "fk_schedule_2"
    FOREIGN KEY("subjectId")
    REFERENCES "subjects"("id")
);
CREATE INDEX "mydb"."schedule.fk_schedule_1_idx" ON "schedule" ("idGroup");
CREATE INDEX "mydb"."schedule.fk_schedule_2_idx" ON "schedule" ("subjectId");
COMMIT;
