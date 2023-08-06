# CAPCTL

CAP 용 CLI

## Prerequisite
capctl은 storage관련한 명령을 위해서 mc를 설치해야 함. 아래와 같이 실행하면 됨 
```
> wget https://dl.minio.io/client/mc/release/linux-amd64/mc && chmod +x mc
> sudo mv mc /bin/mc
```

## Install

```
pip install -r requirements.txt
pip install -e ./
```

## Definition of cap.yaml
- capctl은 cap.yaml 파일을 컨피크 파일로 사용하고 있음 

```
## cap.yaml
version: 이미지 버전명
user: 개발 클러스터 ssh 접속 가능한 계정
accessIP: 개발 클러스터 접근 가능한 IP
namespace: 배포할 네임스페이스
registry: cap harbor registry 주소
project: harbor내의 project 이름
image: 이미지 이름
# 배포 정의, kubectl 또는 helm 둘 중에 하나만 사용
deploy:
  dockerfile: Dockerfile 저장위치
  # kubectl로 배포할 때 정의
  kubectl:
    manifests:
    - yaml 파일 경로1
    - yaml 파일 경로2
  # helm으로 배포할 때 정의
  helm:
    name: helm release 이름
    chartPath: helm chart 경로
# telepresence에 사용될 정보
develop:
  name: kubernetes deployment 이름
  port: 배포된 컨테이너의 포트 번호

# storage create, sync에 사용되는 endpoint 정보와 접속 정보
metadata:
  endpoints:
  - providerName: 
    uri: 
  namespace: 
  password: 
  userId: 

# 생성된(등록된) storage list
storage:
- kubernetes:
  - accessKey: yo-cap
    cluster: cap
    endpoint: https://www.gocap.kr:31897
    secretKey: xumnZxMuCZo7NKbRPhJ5vw6Baic3ooP8fWJPw4bB
  name: yo

```
아래는 cap.yaml 예제 코드 

```
## example
accessIP: 34.64.202.247
deploy:
  dockerfiles: dockerfiles/Dockerfile
  kubectl:
    manifests:
    - yamls/deployment.yaml
develop:
  name: deployment_name
  port: container_port
image: go-template
metadata:
  endpoints:
  - providerName: cap
    uri: https://www.gocap.kr
  - providerName: aws
    uri: https://www.gocap.kr
  - providerName: gcp
    uri: https://www.gocap.kr
  namespace: cap-dev
  password: 12341234
  userId: cap-dev@dudaji.com
namespace: default
project: cap
registry: cap.dudaji.com:31480
storage:
- kubernetes:
  - accessKey: storage1-cap
    cluster: cap
    endpoint: https://www.gocap.kr:32120
    secretKey: Lpaxnagsr6BTuAtL5pXTWdkVgG6H3qYoNZTG1w0D
  - accessKey: storage1-aws
    cluster: aws
    endpoint: https://www.gocap.kr:32196
    secretKey: tKiKEbpEiHvvHoUC6vlQWzHLOUGnobqDjI5vtPeu
  - accessKey: storage1-gcp
    cluster: gcp
    endpoint: https://www.gocap.kr:31254
    secretKey: 2PLCrlrBYkNZyN7RFMU0fOjPOfaTDTOeSWKDBKSc
  name: storage1
user: root
version: '1.3'

```

## Quick Start (DEV Command)

capctl에는 app이라는 서브 커맨드가 있는데 이를 활용해서 빠르게 python 프로젝트를 구성할 수 있음. 아래 명령어를 이용

### 1. app create

```
> cd somewhere
> alias c=capctl  
> c app create myapp
> cd myapp

# 1. Docker build and push
myapp> ./scripts/docker-build-and-push.sh

# 2. Kubernetes 배포 
myapp> ./scripts/kubectl-apply.sh

# 3. Virtual Service Setting 확인 
myapp> ./scripts/curl-to-get-user.sh

# 4. 로컬 개발
myapp> ./scripts/debug.sh
```

## Commands Detail
capctl에는 다양한 명령어가 있음. 아래 참고 

1. **user**  
    1. **add (Create user)**
        ```
        > capctl user add \
        --email shhong3@dudaji.com \
        --password shhong3 \
        --username shhong3
        ```
    1. **delete (Delete user (also leave in all projects))**
        ```
        # ex) Delete "shhong3@dudaji.com"
        > capctl user delete --email shhong3@dudaji.com
        ```
    1. **password (Change password)**
        ```
        > capctl user password admin@kubeflow.org 'asdf!!'
        ```

1. **project**  
    1. **join (Join user to namespace(project))**
        ```
        # ex) Join "shhong3@dudaji.com" to project "kaggle"
        > capctl project join \
        --email shhong3@dudaji.com \
        --namespace kaggle
        ```

    1. **leave (Leave user to namespace(project))**
        ```
        # ex) Leave "shhong3@dudaji.com" to project "kaggle"
        > capctl project leave \
        --email shhong3@dudaji.com \
        --namespace kaggle
        ```

1. **storage**
    1. **add**
        ```
        # cap.yaml에 storage endpoint를 등록하는 명령어
        # minio 생성은 수동으로 혹은 다른 툴을 이용해서 이미 한 상태인 것을 가정하고 있음. 아래는 예시
        > c storage add n1 \
            cap \
            https://cap.dudaji.com:30586 \
            dongil \
            vD8kCqA6lCilp7aeAq4WrTpBTTY0BDbPKC8fpJWe

        > c storage add n1 \
            aws \
            https://cap.dudaji.com:31792 \
            storagetwo \
            Ksz3XRj7IX01u590JFsZY9EcJchRdPJIDP71P4BW

        ```
    1. **create storage**
        ```
        > c storage create --name=name1
        ```

    1. **sync**
        ```
        # cap.yaml에 등록된 스토리지의 싱크를 맞추는 명령어 
        > c storage sync n1
        ```

    1. **delete storage**
        ```
        > c storage delete --name=name1
        ```

1. **quota** 
    1. **ls**
        ```
        # 프로젝트별 quota정보를 조회하는 명령어 
        > c quota ls
        ```

    1. **set**
        ```
        # 프로젝트별 quota를 설정하는 명령어 
        > capctl quota set \
         --project=shhong \
         --cpu_count=10 \
         --gpu_count=0 \
         --mem='20Gi' \
         --storage='200Gi'
        ```

    1. **status**
        ```
        # 프로젝트별 quota status를 보는 명령어 
        > capctl quota status shhong
        ```

1. **dev** 
    1. **init**  
        - **cap harbor 로그인**  
            harbor의 cap 프로젝트에 접근 가능한 계정으로 로그인
            ```
            # CAP harbor admin 계정
            admin / Dudaji!!22
            ```
        - **helm 설치**  
            CAP component 중 helm chart를 사용하는 프로젝트도 있기 때문에 helm도 설치합니다. 버전 픽스가  
            안되어 있어서 항상 가장 최신버전으로 설치합니다. 운영체제를 확인하고 그에 맞게 설치하며. 현재는 MAC과 Ubuntu만 지원합니다.   
            이미 helm이 설치되어 있으면 재설치하지 않습니다.
        - **telepresence 설치**  
            현재 CAP의 kubernetes 버전 충돌 이슈로 인해 v1 버전을 설치합니다. helm 설치 과정과 마찬가지로  
            운영체제에 맞게 설치하고, 설치되어 있으면 재설치하지 않습니다.  
        - **kubeconfig 파일 다운로드 (optional)**  
            gcp나 on-prem에 상관없이 `scp` 명령어를 사용하여 다운로드 받습니다. `cap.yaml`에서 `user`와 `accessIP` 값을 적절히 바꿔줍니다.
            ```
            # example
            user: root                   # cap-deployment과정에서 사용한 ssh 계정이름
            accessIP: 34.64.202.247   # 로컬에서 gcp혹은 on-prem에 접근 가능한 아이피 주소
            ``` 
        - **새로 다운로드 받은 kubeconfig 파일 적용(optional)**   
            개발용 cluster의 kubeconfig 다운로드가 완료되면 기존의 kubeconfig, 즉 `~/.kube/config`파일과 병합시킵니다.  
            그리고 kubernetes context를 새로 받은 kubeconfig의 context로 바뀌게 됩니다.
            ```
            kubectx # ~/.kube/config에 있는 context 목록 확인
            ---
            * local@local
            #### capctl init --kubeconfig 실행 후
            kubectx
            ---
            * develop-admin@cluster.local # cap deployment로 배포 시, context이름은 항상 develop-admin@cluster.local 입니다.
            local@local
            ```
        - **초기 배포**  
            telepresence로 개발할 때 application이 개발용 cluster에 배포되어 있어야 해서 초기에 application을 바로 배포합니다.
            ```
            > capctl dev init --kubeconfig # kubeconfig 옵션을 추가하면 위의 6가지 단계가 모두 실행
            > capctl dev init # 위의 6가지 중 kubeconfig 다운로드 및 병합 단계는 제외
            Authenticating with existing credentials...
            Login Succeeded
            /usr/local/bin/helm
            helm is already installed
            /usr/bin/telepresence
            telepresence is already installed
            Publishing image...
            Sending build context to Docker daemon  146.9kB
            Step 1/11 : FROM golang:1.15-alpine AS builder
            ---> 18cb4ca6e500
            Step 2/11 : ENV GO111MODULE=on     CGO_ENABLED=0     GOOS=linux     GOARCH=amd64
            ---> Using cache
            ---> f2f8e6ed9b5b
            Step 3/11 : WORKDIR /builder
            ---> Using cache
            ---> b645321fba50
            Step 4/11 : COPY . .
            ---> Using cache
            ---> bb1f32f1c8f3
            Step 5/11 : RUN go mod download
            ---> Using cache
            ---> 1cbfc73cca2c
            Step 6/11 : RUN go build -o /app ./cmd/main.go
            ---> Using cache
            ---> de5dedb82569
            Step 7/11 : FROM scratch
            ---> 
            Step 8/11 : COPY --from=builder /app /
            ---> Using cache
            ---> 159271127e27
            Step 9/11 : COPY copy-test.tar /tmp/
            ---> Using cache
            ---> 71cc10d64165
            Step 10/11 : WORKDIR /
            ---> Using cache
            ---> 7eb1befa7664
            Step 11/11 : ENTRYPOINT ["./app"]
            ---> Using cache
            ---> adc8786e266c
            Successfully built adc8786e266c
            Successfully tagged cap.dudaji.com:31480/cap/go-template:latest
            Using default tag: latest
            The push refers to repository [cap.dudaji.com:31480/cap/go-template]
            55c680d6dd3d: Layer already exists 
            3f23af3c89d0: Layer already exists 
            latest: digest: sha256:afdcd99d36a9d84bd1ee559abaabb8edc15af4c023d39efba387217cd39008e9 size: 736
            Applying deployment...
            deployment.apps/go-template configured
            service/go-template unchanged
            configmap/go-template unchanged
            ```

    1. **publish**  
    `cap.yaml의 dockerfile` 위치의 Dockerfile 기반으로 이미지 빌드 후 dudaji harbor에 푸시됩니다.
        ```
        > capctl dev publish
        feature/add-template-cli
        Current branch name : add-template-cli
        Publishing image...
        Sending build context to Docker daemon  146.9kB
        Step 1/11 : FROM golang:1.15-alpine AS builder
        ---> 18cb4ca6e500
        Step 2/11 : ENV GO111MODULE=on     CGO_ENABLED=0     GOOS=linux     GOARCH=amd64
        ---> Using cache
        ---> f2f8e6ed9b5b
        Step 3/11 : WORKDIR /builder
        ---> Using cache
        ---> b645321fba50
        Step 4/11 : COPY . .
        ---> Using cache
        ---> bb1f32f1c8f3
        Step 5/11 : RUN go mod download
        ---> Using cache
        ---> 1cbfc73cca2c
        Step 6/11 : RUN go build -o /app ./cmd/main.go
        ---> Using cache
        ---> de5dedb82569
        Step 7/11 : FROM scratch
        --->
        Step 8/11 : COPY --from=builder /app /
        ---> Using cache
        ---> 159271127e27
        Step 9/11 : COPY copy-test.tar /tmp/
        ---> Using cache
        ---> 71cc10d64165
        Step 10/11 : WORKDIR /
        ---> Using cache
        ---> 7eb1befa7664
        Step 11/11 : ENTRYPOINT ["./app"]
        ---> Using cache
        ---> adc8786e266c
        Successfully built adc8786e266c
        Successfully tagged cap.dudaji.com:31480/cap/go-template:test
        The push refers to repository [cap.dudaji.com:31480/cap/go-template]
        55c680d6dd3d: Preparing
        3f23af3c89d0: Preparing
        55c680d6dd3d: Layer already exists
        3f23af3c89d0: Layer already exists
        add-template-cli: digest: sha256:afdcd99d36a9d84bd1ee559abaabb8edc15af4c023d39efba387217cd39008e9 size: 736
        ```
    1. **deploy**  
    쿠버네티스 클러스터에 테스트 목적으로 배포하기 위한 명령어입니다. `kubectl`이나 `helm`를 사용하여 배포합니다.  
        ```
        > capctl dev deploy
        Publishing image...
        Sending build context to Docker daemon  146.9kB
        Step 1/11 : FROM golang:1.15-alpine AS builder
        ---> 18cb4ca6e500
        Step 2/11 : ENV GO111MODULE=on     CGO_ENABLED=0     GOOS=linux     GOARCH=amd64
        ---> Using cache
        ---> f2f8e6ed9b5b
        Step 3/11 : WORKDIR /builder
        ---> Using cache
        ---> b645321fba50
        Step 4/11 : COPY . .
        ---> Using cache
        ---> bb1f32f1c8f3
        Step 5/11 : RUN go mod download
        ---> Using cache
        ---> 1cbfc73cca2c
        Step 6/11 : RUN go build -o /app ./cmd/main.go
        ---> Using cache
        ---> de5dedb82569
        Step 7/11 : FROM scratch
        ---> 
        Step 8/11 : COPY --from=builder /app /
        ---> Using cache
        ---> 159271127e27
        Step 9/11 : COPY copy-test.tar /tmp/
        ---> Using cache
        ---> 71cc10d64165
        Step 10/11 : WORKDIR /
        ---> Using cache
        ---> 7eb1befa7664
        Step 11/11 : ENTRYPOINT ["./app"]
        ---> Using cache
        ---> adc8786e266c
        Successfully built adc8786e266c
        Successfully tagged cap.dudaji.com:31480/cap/go-template:latest
        Using default tag: latest
        The push refers to repository [cap.dudaji.com:31480/cap/go-template]
        55c680d6dd3d: Layer already exists 
        3f23af3c89d0: Layer already exists 
        latest: digest: sha256:afdcd99d36a9d84bd1ee559abaabb8edc15af4c023d39efba387217cd39008e9 size: 736
        Applying deployment...
        deployment.apps/go-template configured
        service/go-template unchanged
        configmap/go-template unchanged
        ```
    1. **debug**  
    로컬에서 개발할 수 있도록 `telepresence`를 실행시켜주는 명령어입니다. 실행 전 현재 프로젝트가 테스트 클러스터에  
    배포되어 있는지 확인해주세요. `capctl dev init`을 실행시켰다면 배포되어 있을 것이고, 만약 그렇지 않다면 `capctl dev deploy`로  
    먼저 배포하시길 바랍니다. 정상적으로 실행되면 쉘이 새로운 bash session으로 바뀌게 됩니다. 이는 저희가 작성한 `yamls`파일을 기반으로 볼륨이나 환경변수 등의  
    환경 설정들이 갖춰져 있는 session입니다. 따라서 로컬에 application을 실행시킬 때 **반드시 해당 session에서 실행시켜야 합니다.**
        ```
        > capctl dev debug
        T: Warning: kubectl 1.20.1 may not work correctly with cluster version 1.17.12 due to the version discrepancy. See https://kubernetes.io/docs/setup/version-skew-policy/ for more information.

        T: Using a Pod instead of a Deployment for the Telepresence proxy. If you experience problems, please file an issue!
        T: Set the environment variable TELEPRESENCE_USE_DEPLOYMENT to any non-empty value to force the old behavior, e.g.,
        T:     env TELEPRESENCE_USE_DEPLOYMENT=1 telepresence --run curl hello

        T: How Telepresence uses sudo: https://www.telepresence.io/reference/install#dependencies
        T: Invoking sudo. Please enter your sudo password.
        [sudo] password for nopro: 
        T: Starting proxy with method 'vpn-tcp', which has the following limitations: All processes are affected, only one telepresence can run per machine, and you can't use other VPNs. You may need to add 
        T: cloud hosts and headless services with --also-proxy. For a full list of method limitations see https://telepresence.io/reference/methods.html
        T: Volumes are rooted at $TELEPRESENCE_ROOT. See https://telepresence.io/howto/volumes.html for details.
        T: Starting network proxy to cluster by swapping out Deployment go-template with a proxy Pod
        T: Forwarding remote port 8081 to local port 8081.

        T: Setup complete. Launching your command.
        @develop-admin@cluster.local|bash-5.0$
        ```  


## TODO  
1. cap.yaml과 deployment.yaml 이미지 변경 할 때 등등 싱크를 맞춰줘야 하는게 매우 불편  
2. mac에서 telepresence session안에 python이 로컬 python이 아닌 다른 거로 바뀜  
3. capctl dev deploy가 제대로 반영이 안됨   
4. capctl dev publish가 개발용 publish인지 production용 publish 인지 헷갈림
