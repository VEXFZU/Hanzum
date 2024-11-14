## How to use

### FastAPI

#### Installation

* VM Base Image: `c0-deeplearning-common-cu123-v20240922-debian-11`
* VM Machine Type: g2-standard-8 (8 vCPUs, 32 GB memory)

1. Proceed automatic driver installation.
2. Install torch.

```bash
# default version is 2.5.1 for CUDA 12.4
pip install torch
```

If you fail `import torch`, you need to install CUDA 12.4.

```bash
# Check nvcc version to be sure
nvcc --version
# install cuda toolkit 12.4 if and only if nvcc version is low.
wget https://developer.download.nvidia.com/compute/cuda/repos/debian11/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo add-apt-repository contrib
sudo apt update
sudo apt -y install cuda-toolkit-12-4
```

3. Install other packages

```bash
pip install unsloth fastapi
```

4. Setup Cloudflare tunnel.

```bash
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb &&
sudo dpkg -i cloudflared.deb &&
sudo cloudflared service install $CLOUDFLARE_TUNNEL_TOKEN 
```

Ask for the token to set it as an environment variable. It can't be shared in public.

#### Run

```bash
uvicorn main:app --host 0.0.0.0 # 이름 변경
```

#### Test

```bash
time curl -X 'POST' \
  'http://api.vxfz.top/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "input_text": "안녕하세요. 반갑습니다. 오늘 날씨가 좋네요."
}'
```

### Streamlit

#### Installation

```bash
pip install streamlit PyMuPDF python-docx
```

#### Run

```bash
streamlit run front/app.py
```
