## Photo labeling

## Problem

There are thousands of unlabelled TIFs. It is desirable to label them with text descriptions and tags for internal use and for public users.

## Approach

Each model seems to excel in one area; that is to say, llava 13b and llama4 are great at describing a photo generally, but has trouble detecting the number of people. Other models are better at detecting people, and there must be some that can match people across photos. So the approach to try is to make a photo processing pipeline.

1. convert TIF to medium size jpg
```
uv run convert-tif-to-jpg.py   
```

2. Analyze jpg with microsoft/conditional-detr-resnet-50, to make people crops

3. Analyze people crops for faces, and detect who they are

4. Use llama4 to describe the photo and produce tags

## Dependencies

### uv

Install uv from https://docs.astral.sh/uv/getting-started/installation/#installation-methods
```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install venv using uv
https://huggingface.co/docs/transformers/en/installation?virtual=uv&install=pip&cpu-only=PyTorch
```
uv venv .env
source .env/bin/activate
```

### PIL

```
uv pip install pillow
```
