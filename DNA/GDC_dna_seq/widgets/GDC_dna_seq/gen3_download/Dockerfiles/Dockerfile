FROM golang:1.14-alpine as build-deps

RUN apk update && apk add --no-cache git ca-certificates gcc musl-dev

WORKDIR /go/src/github.com/uc-cdis/gen3-client

RUN go get github.com/mitchellh/go-homedir \
    github.com/spf13/cobra \
    github.com/spf13/viper \
    github.com/cavaliercoder/grab \
    github.com/golang/mock/gomock \
    github.com/tcnksm/go-latest \
    gopkg.in/cheggaaa/pb.v1 \
    github.com/hashicorp/go-version

COPY . .

# git version info has been already added manually

RUN go build -ldflags "-linkmode external -extldflags -static" -o bin/gen3-client

# Store only the resulting binary in the final image
# Resulting in significantly smaller docker image size
FROM alpine:3.12
RUN apk add --no-cache bash curl
COPY --from=build-deps /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=build-deps /go/src/github.com/uc-cdis/gen3-client/bin/gen3-client /usr/local/bin/gen3-client
COPY runG3Download.sh /usr/local/bin/runG3Download.sh
RUN chmod +x /usr/local/bin/runG3Download.sh
