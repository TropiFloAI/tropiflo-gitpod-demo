# Tropiflo CLI Demo - Gitpod Sandbox

This is a disposable Gitpod sandbox for evaluating **tropiflo** in your browser with zero installation.

## 🚀 Quick Start

### Launch in Gitpod

Click this button to launch the demo in Gitpod:

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#<YOUR-GITHUB-REPO-URL>)

Or manually visit:
```
https://gitpod.io/#<YOUR-GITHUB-REPO-URL>
```

### Run the Demo

Once the workspace loads (takes ~30 seconds), run:

```bash
source .venv/bin/activate
tropiflo run --config config.yaml
```

That's it! Tropiflo will execute the S&P 500 prediction script using the hosted backend.

## 📁 What's Included

- **snp500.py** - Entry script that trains a logistic regression model on S&P 500 data
- **data/sp500.csv** - Sample dataset (synthetic/demo data)
- **config.yaml** - Configuration that connects to the hosted tropiflo backend
- **requirements.txt** - Python dependencies including tropiflo

## 🎯 How It Works

- **No backend runs locally** - Tropiflo connects to the hosted backend specified in `config.yaml`
- **Data volume** - The `data/` folder is mounted at `/workspace/demo-git-pod/data` in Gitpod
- **Parallel execution** - The demo runs 5 parallel versions as specified in `config.yaml`
- **Mode: local** - The script runs in local mode, using the entry command `python snp500.py`

## 📝 Configuration Details

The `config.yaml` uses these settings:

```yaml
mode: "local"
entry_command: "python snp500.py"
data_volume: "/workspace/demo-git-pod/data"
parallel: 5
```

## ⚠️ Notes

- This is a **disposable sandbox** - changes are not saved when you close Gitpod
- Uses **sample/synthetic data** for demonstration purposes only
- The API key in `config.yaml` is a demo key with limited access
- No installation or setup required on your machine

## 🔧 Customization

To test your own scripts:

1. Fork this repository
2. Replace `snp500.py` with your script
3. Update `config.yaml` to point to your entry command
4. Add your data files to the `data/` directory
5. Update `requirements.txt` if you need additional dependencies

## 📚 Learn More

Visit [tropiflo documentation](https://tropiflo.io) for more information about the full capabilities of tropiflo.

