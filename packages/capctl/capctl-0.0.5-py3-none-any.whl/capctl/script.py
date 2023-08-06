mac_helm_install = """brew install helm"""
ubuntu_helm_install = """curl https://baltocdn.com/helm/signing.asc | sudo apt-key add - &&
        sudo apt-get install apt-transport-https --yes 
        echo "deb https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list 
        sudo apt-get update 
        sudo apt-get install -y helm"""

mac_telepresence_install = """brew install datawire/blackbird/telepresence"""
ubuntu_telepresence_install = """sudo curl -fL https://app.getambassador.io/download/tel2/linux/amd64/latest/telepresence -o /usr/local/bin/telepresence
        sudo chmod a+x /usr/local/bin/telepresence"""
