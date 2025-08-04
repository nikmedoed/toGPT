# 📂 toGPT

A handy Python script to quickly and easily copy the directory structure and contents of multiple files and folders directly to your clipboard. Ideal for preparing structured inputs for AI models (such as ChatGPT), enabling seamless review and feedback on complex project setups.

## 🚀 Features

* Copy **directory structure** only.
* Copy **file contents** only.
* Copy both **directory structure and file contents**.
* Process **individual files**, **folders**, or **multiple paths** simultaneously.
* Automatically excludes unnecessary files/directories (e.g., `.git`, `node_modules`, `__pycache__`, etc.).

## 📥 Installation

Clone or download the repository:

```shell
git clone https://github.com/your-username/toGPT.git
```

### Setup for PowerShell

Edit your PowerShell profile:

```shell
notepad $PROFILE
```

Add the following function, replacing the path with your actual script location:

```powershell
function toGPT {
    & "python" "D:\your\path\toGPT\toGPT.py" @Args
}
```

Save and restart your PowerShell session.

### Setup bash / szh

```shell
chmod +x toGPT.py 
sudo ln -sf /pathToScript/toGPT.py /usr/local/bin/toGPT
```

## 🎯 Usage

Basic command structure:

```shell
toGPT <path> [options]
```

### Examples

* Copy structure **and** contents of the current directory:

```shell
toGPT .
```

* Copy **only the structure** of a folders and files set:

```shell
toGPT .\project_folder -s
```

* Copy **only the contents** of specific files:

```shell
toGPT .\file1.py .\file2.js -c
```

* Copy structure and contents from multiple folders and files:

```shell
toGPT .\folder1 ..\folder2\subfolder somefile.txt .\folder1\otherfile.txt
```

The output will be automatically copied to your clipboard.

## ⚙️ Command-line Options

* `-s`: Copy only the directory structure.
* `-c`: Copy only the file contents.

If neither option is provided, the script defaults to copying both structure and contents.

## 🗃 Excluded by Default

The script automatically ignores common temporary and system folders/files, such as:

* `.git`
* `node_modules`
* `.venv`
* `__pycache__`
* `build`, `dist`

## 🧠 Use Cases

* Quickly preparing structured inputs for GPT models.
* Efficiently handling code reviews and collaboration.
* Documenting project structures clearly and easily.

---

Enjoy streamlined interactions with your AI assistant! ✨🚀
