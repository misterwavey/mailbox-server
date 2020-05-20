CMD_REGISTER                   = 1
CMD_CHECK_REGISTERED_NICKNAME  = 2
CMD_SEND_MESSAGE               = 3
CMD_MESSGAGE_COUNT             = 4
CMD_GET_MESSAGE                = 5
CMD_JOIN_POOL                  = 6 
CMD_GET_POOL                   = 7 

STATUS_OK                      = 0
STATUS_INVALID_PROTOCOL        = 1
STATUS_INVALID_CMD             = 2
STATUS_INVALID_APP             = 3
STATUS_INVALID_USERID          = 4
STATUS_INVALID_LENGTH          = 5
STATUS_INTERNAL_ERROR          = 6
STATUS_MISSING_NICKNAME        = 7
STATUS_MISSING_MESSAGE         = 8
STATUS_UNIMPLEMENTED           = 9
STATUS_MISSING_MESSAGE_ID      = 10
STATUS_MISSING_POOL_SIZE       = 11
STATUS_MISSING_POOL_ID         = 12

STATUS_USER_ALREADY_REGISTERED = 101
STATUS_UNREGISTERED_NICKNAME   = 102
STATUS_UNKNOWN_USERID          = 103
STATUS_UNREGISTERED_USERID     = 104
STATUS_UNKNOWN_POOL_ID         = 105

STATUS_REGISTER_OK             = 201
STATUS_COUNT_OK                = 202
STATUS_GET_MESSAGE_OK          = 203
STATUS_INVALID_MESSAGE_ID      = 204
STATUS_JOINED_POOL             = 205
STATUS_INVALID_POOLSIZE        = 206
STATUS_ALREADY_JOINED_POOL     = 207
STATUS_POOL_UNFILLED           = 208
STATUS_POOL_FILLED             = 209
