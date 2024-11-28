# 🌱한점 두점 ⠚⠒⠨⠎⠢⠀⠊⠍⠨⠎⠢ (Hanzum)

*한점 두점*은 transformer 모델을 사용해 한국어 텍스트, PDF 파일 등을 점자로 점역해 주는 서비스 입니다.

## 소개
높은 정확도와 빠른 생성 속도의 점자 엔진, "한점두점"을 소개합니다. 
점자교정사 자격시험 정답율 80점을 달성할 정도로 높은 정확도를 자랑합니다.
20 tokens/s 이상의 속도로 점자를 생성할 수 있는 점역엔진입니다.
점자시장은 산업 파이가 작고 기술 개발이 어려워 하드웨어 개발에 그치는 경우가 많았는데요,
하드웨어에 적합한 소프트웨어 발달이 미진했던 점자 서비스를 활성화시키기 위해 오픈소스로 공개합니다. 

## 성능

점역 task에 대한 성능을 측정하기 위해, 다음을 사용하였습니다.

* WER (Word Error Rate): 단어 단위로 측정한 오류율. 낮을 수록 좋습니다.
* CER (Character Error Rate): 글자 단위로 측정한 오류율. 낮을 수록 좋습니다.
* 점역 교정사 공인 인증 문제 167 문항

이를 사용하여 측정한 결과는 다음과 같습니다.

| 점역엔진            | 정답 문항 수    | 정답율   | 평균 WER | 평균 CER |
|--------------------|----------------|-------|--------|--------|
| D사 점역엔진         | 36             | 21.6% | 0.15   | 0.07   |
| Hanzum, Llama 3-8B | 82             | 49.1% | 0.16   | 0.06   |
| Hanzum, t5-xlarge  | 134            | 80.2% | 0.06   | 0.02   |

특히 t5-xlarge 기반 모델의 정답율이 80%를 넘어 3급 점역사 합격 기준인 70%를 훌쩍 넘었다는 점이 가장 고무적입니다.
공개 예정인 차기 버전에서는 85점 이상의 정답율을 보이고 있습니다.

## 기능

다음 기능들을 Streamlit을 통해 사용하실 수 있습니다.

* 단문의 점역
* TXT, PDF, docx 파일의 점역
    * 파일을 업로드하면 점역 완료시 BRL/BRF 파일 다운로드 버튼을 눌러 해당 포맷으로 다운로드 할 수 있습니다.

## 사용법

아래 절차에 따라 설치한 후, Streamlit을 실행하여 인터페이스를 사용하시면 됩니다.

### Docker compose

#### Edit .env file

Please read .env.dev for the variables you need to set.

#### Run docker compose

```bash
docker compose up -d
```

If you prefer not to run the inference server, you can run only the Streamlit app.
Currently, our inference server is set as the default for Streamlit, but it may not always be running.
If you need access to the inference server, please create an issue to get in touch with us.

```bash 
docker compose up -d streamlit
```

### 직접 설치

#### FastAPI

이 설명은 GCP 인스턴스를 기준으로 작성되었습니다. 다른 환경에서는 적절히 수정하여 적용해 주세요.

##### Installation

* VM Base Image: `c0-deeplearning-common-cu123-v20240922-debian-11`
* VM Machine Type: g2-standard-8 (8 vCPUs, 32 GB memory)

1. Proceed automatic driver installation.
2. Install torch.

```bash
pip install torch --index-url https://download.pytorch.org/whl/cu124
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
pip install fastapi uvicorn
```

4. If you're going to use llama model, install unsloth too.

```bash
pip install unsloth
```

5. Set environment variables.

```bash
export VXFZ_TRANSLATOR_MODEL=t5  # must be set. t5 or llama.
```

Export optional variables if needed.

```bash
export VXFZ_TRANSLATOR_MODEL_T5_NAME=/path/to/model  # default is azaraks/t5-xlarge-ko-kb.
export VXFZ_TRANSALTOR_MODEL_T5_MAX_LENGTH=512  # default is 256.
```

##### Run

```bash
uvicorn api.main:app --host 0.0.0.0 --workers 1
```

##### Test

```bash
time curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "input_text": "안녕하세요. 반갑습니다. 오늘 날씨가 좋네요."
}'
```

#### Streamlit

##### Installation

```bash
pip install streamlit PyMuPDF python-docx kss
```

If it's on linux or mac, you may install python-mecab-kor.

```bash
pip install python-mecab-kor
```

##### Run

```bash
streamlit run front/app.py
```

## 사용 데이터

* 2024 한국 점자 규정
* [묵자-점자 병렬 말뭉치 2023](https://kli.korean.go.kr/corpus/request/corpusRegist.do)
* 과년도 점역사 기출문제 (자체 수집)
