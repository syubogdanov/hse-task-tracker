FROM liquibase/liquibase

ARG DIALECT
RUN test -n "$DIALECT"
ENV DIALECT $DIALECT

ARG DATABASE
RUN test -n "$DATABASE"
ENV DATABASE $DATABASE

ARG USERNAME
RUN test -n "$USERNAME"
ENV USERNAME $USERNAME

ARG PASSWORD
RUN test -n "$PASSWORD"
ENV PASSWORD $PASSWORD

ARG HOST
RUN test -n "$HOST"
ENV HOST $HOST

ARG PORT
RUN test -n "$PORT"
ENV PORT $PORT

WORKDIR /usr/migrations

COPY changesets/ changesets/
COPY changelog.yaml changelog.yaml

ENTRYPOINT liquibase update \
    --changelog-file changelog.yaml \
    --username $USERNAME \
    --password $PASSWORD \
    --url jdbc:$DIALECT://$HOST:$PORT/$DATABASE
