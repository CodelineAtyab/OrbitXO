FROM mysql:8.0

ENV MYSQL_ROOT_PASSWORD=rootpassword
ENV MYSQL_DATABASE=route_tracker
ENV MYSQL_USER=route_user
ENV MYSQL_PASSWORD=route_password

# Add any custom MySQL configuration
COPY ./mysql/my.cnf /etc/mysql/conf.d/custom.cnf

# Expose MySQL port
EXPOSE 3306

# Healthcheck to verify database is ready
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
  CMD mysqladmin ping -h localhost -u $MYSQL_USER --password=$MYSQL_PASSWORD || exit 1
