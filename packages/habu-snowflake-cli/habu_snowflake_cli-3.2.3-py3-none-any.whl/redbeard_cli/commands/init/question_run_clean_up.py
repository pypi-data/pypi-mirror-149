from redbeard_cli import snowflake_utils


def install_handle_question_run_cleanup_procedure(sf_connection):
    """
    Installs the handler for question cleanup
    :param sf_connection:
    :return:
    """
    sp_sql = """
    CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.HANDLE_QUESTION_RUN_CLEANUP() 
    RETURNS STRING
    LANGUAGE JAVASCRIPT
    STRICT
    EXECUTE AS OWNER
    AS
    $$
        try {
            var crRequestSql = "SELECT id AS request_id, request_data:clean_room_id AS clean_room_id,  " + 
            " request_data:compute_account_id AS compute_account_id, " +
            " request_data:statement_hash AS statement_hash " + 
            " FROM HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS " + 
            " WHERE request_type = :1 AND request_status = :2 ORDER BY CREATED_AT ASC";
            
            var stmt = snowflake.createStatement({
                sqlText: crRequestSql,
                binds: ['QUESTION_RUN_CLEANUP', 'PENDING']
            });

            var rs = stmt.execute();    
            var questionDataShareParams = [];
            while (rs.next()) {
                var requestID = rs.getColumnValue(1);
                var cleanRoomID = rs.getColumnValue(2);
                var computeAccountId = rs.getColumnValue(3);
                var statementHash = rs.getColumnValue(4);
                
                questionDataShareParams.push({
                    'requestID': requestID,
                    'cleanRoomID': cleanRoomID, 
                    'computeAccountId': computeAccountId,
                    'statementHash': statementHash 
                })
                snowflake.execute({
                        sqlText: "UPDATE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS SET REQUEST_STATUS = :1, UPDATED_AT = CURRENT_TIMESTAMP() WHERE ID = :2",
                        binds: ["IN_PROGRESS", requestID]
                });
            }
            
            for (var i = 0; i < questionDataShareParams.length; i++){
                var stmt = snowflake.createStatement({
                    sqlText: 'CALL HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.QUESTION_RUN_CLEANUP(:1, :2, :3, :4)',
                    binds: [
                        questionDataShareParams[i]['requestID'], 
                        questionDataShareParams[i]['cleanRoomID'],
                        questionDataShareParams[i]['computeAccountId'],
                        questionDataShareParams[i]['statementHash']
                    ]
                });        
                stmt.execute();
            }        
            result = "SUCCESS";
        } catch (err) {
            result = "FAILED";
            var stmt = snowflake.createStatement({
                sqlText: 'CALL HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.HANDLE_ERROR(:1, :2, :3, :4, :5, :6)',
                binds: [
                    err.code, err.state, err.message, err.stackTraceTxt, "", Object.keys(this)[0]
                ]
            });        
            var res = stmt.execute();
        }
        return result;
    $$;"""
    snowflake_utils.run_query(sf_connection, sp_sql)

def install_question_run_cleanup_procedure(sf_connection):
    """
    Installs run clean up procedure
    :param sf_connection:
    :return:
    """
    sp_sql = """
    CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.QUESTION_RUN_CLEANUP
    (REQUEST_ID VARCHAR, CLEAN_ROOM_ID VARCHAR, COMPUTE_ACCOUNT_ID VARCHAR, STATEMENT_HASH VARCHAR)
    RETURNS STRING
    LANGUAGE JAVASCRIPT
    STRICT
    EXECUTE AS OWNER
    AS
    $$
        try {

            snowflake.execute({
                sqlText: "DELETE FROM HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.ALLOWED_STATEMENTS WHERE ACCOUNT_ID = ? and CLEAN_ROOM_ID = ? and STATEMENT_HASH = ?",
                binds: [COMPUTE_ACCOUNT_ID, CLEAN_ROOM_ID, STATEMENT_HASH]
            })
            -- we can't remove partnersharedb because another parallel report run maybe using the same db and a different table. 
                     
            result = "COMPLETE";
            msg = "Question run data share successful"
        } catch (err) {
            result = "FAILED";
            var stmt = snowflake.createStatement({
                sqlText: 'CALL HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.HANDLE_ERROR(:1, :2, :3, :4, :5, :6)',
                binds: [
                    err.code, err.state, err.message, err.stackTraceTxt, REQUEST_ID, Object.keys(this)[0]
                ]
            });        
            msg = err.message
            var res = stmt.execute();
        } finally {
            snowflake.execute({
                sqlText: "UPDATE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS SET REQUEST_STATUS = :1, UPDATED_AT = CURRENT_TIMESTAMP() WHERE ID = :2",
                binds: [result, REQUEST_ID]
            });
            opMsg = "QUESTION CLEANUP - OPERATION STATUS - " + result + " - Detail: " + msg
            snowflake.createStatement({
                sqlText: `call HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.SP_LOGGER(:1, :2, :3)`,
                binds:[opMsg, REQUEST_ID, Object.keys(this)[0]]
            }).execute();
        }
        return result;
    $$;"""
    snowflake_utils.run_query(sf_connection, sp_sql)
