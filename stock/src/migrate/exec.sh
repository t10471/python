cd /root/workspace/stock/src/migrate
USER=$MYSQL_ENV_MYSQL_USER_STOCK
HOST=$MYSQL_PORT_3306_TCP_ADDR
PASSWORD=$MYSQL_ENV_MYSQL_PASSWORD_STOCK
DB=$MYSQL_ENV_MYSQL_DATABASE_STOCK

OMMANDS=()
COMMANDS=("${COMMANDS[@]}" "start")
COMMANDS=("${COMMANDS[@]}" "add")

COMMAND=$1
COMMENT=$2

###lib関数

is_valid_args() {
    if [ "${#2}" -eq 0 ] ;then
        echo "$1"
        kill -14 "$$"
    fi
    return 0
}

exists_in() {
    local FLG=true
    local arrayname=$1
    eval ref=\"\${$arrayname[@]}\"
    local list=( ${ref} )
    for a in "${list[@]}"; do
        if [ "$a" == "$2" ]; then
            FLG=false
            break
        fi
    done
    if $FLG ; then
        echo "$2 is not exist"
        kill -14 "$$"
    fi
    return 0
}

command_start(){
    URL=mysql+pymysql://${USER}:${PASSWORD}@${HOST}/${DB}
    python manage.py version_control $URL .
     migrate manage manage.py --repository=. --url=$URL
}

command_add(){
    is_valid_args "need comment" $COMMENT
    python manage.py script $COMMENT
}

is_valid_args "need command" $COMMAND
exists_in COMMANDS $COMMAND

command_${COMMAND}

