DROP TABLE IF EXISTS "trigger_test";
CREATE TABLE "trigger_test"(
	"trigger_testID" bigserial PRIMARY KEY,
	"trigger_testName" text
);


DROP TABLE IF EXISTS "trigger_test_log";
CREATE TABLE "trigger_test_log"(
	"id" bigserial PRIMARY KEY,
	"trigger_test_log_ID" bigint,
	"trigger_test_log_name" text
);

--------------------------------------------------------------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION before_insert_delete_func() RETURNS TRIGGER as $trigger$
DECLARE
	CURSOR_LOG CURSOR FOR SELECT * FROM "trigger_test_log";
	row_ "trigger_test_log"%ROWTYPE;

BEGIN
	IF old."trigger_testID" % 2 = 0 THEN
		IF old."trigger_testID" % 3 = 0 THEN
			RAISE NOTICE 'trigger_testID is multiple of 2 and 3';
			FOR row_ IN CURSOR_LOG LOOP
				UPDATE "trigger_test_log" SET "trigger_test_log_name" = '_' || row_."trigger_test_log_name" || '_log' WHERE "id" = row_."id";
			END LOOP;
			RETURN OLD;
		ELSE
			RAISE NOTICE 'trigger_testID is even';
			INSERT INTO "trigger_test_log"("trigger_test_log_ID", "trigger_test_log_name") VALUES (old."trigger_testID", old."trigger_testName");
			UPDATE "trigger_test_log" SET "trigger_test_log_name" = trim(BOTH '_log' FROM "trigger_test_log_name");
			RETURN NEW;
		END IF; 
	ELSE 
		RAISE NOTICE 'trigger_testID is multiple of 3';
		FOR row_ IN CURSOR_LOG LOOP
			UPDATE "trigger_test_log" SET "trigger_test_log_name" = '_' || row_."trigger_test_log_name" || '_log' WHERE "id" = row_."id";
		END LOOP;
		RETURN OLD;
	END IF; 
END;
$trigger$ LANGUAGE plpgsql;

CREATE TRIGGER "before_update_delete_trigger"
BEFORE UPDATE OR DELETE ON "trigger_test"
FOR EACH ROW
EXECUTE procedure before_insert_delete_func();
--------------------------------------------------------------------------------------------------------------------------------
INSERT INTO "trigger_test"("trigger_testName")
VALUES ('trigger_test1'), ('trigger_test2'), ('trigger_test3'), ('trigger_test4'), ('trigger_test5'), ('trigger_test6'), ('trigger_test7'), ('trigger_test8'), ('trigger_test9'), ('trigger_test10');

SELECT * FROM "trigger_test";
SELECT * FROM "trigger_test_log";

UPDATE "trigger_test" SET "trigger_testName" = "trigger_testName" || '_log' WHERE "trigger_testID" % 2 = 0;
DELETE FROM "trigger_test" WHERE "trigger_testID" % 3 = 0;