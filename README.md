# Dory
A file Manager with a focus on programmers and minimilism


## Requirements

Before you install and run this project, make sure you have the following installed on your system:

- **Python** (version 3.7 or later)
- **pip** (Python's package manager)
- **Python dependencies** specified in `pyproject.toml`.

## Installation

### 1. Clone the repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/Abhinav-VS21/Dory.git
cd Dory
```

### 2. Create and activate a virtual environment (optional, but recommended)

It’s a good practice to use a virtual environment to avoid conflicts with other projects.

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install the required dependencies

Once the virtual environment is activated, you can install the required dependencies. Since you're using `pyproject.toml` for packaging, use `pip` to install the dependencies:

```bash
pip install .
```

Alternatively, you can use `pip` to install the dependencies directly from the `pyproject.toml` file:

```bash
pip install -r requirements.txt  # if you have a requirements.txt file, otherwise install manually as below
```

### 4. Run the application

To run the application, execute the following command:

```bash
python -m DoryWindow
```

This will start the main window of the application. You should see your file explorer with the various features you've implemented.

---

## How to Develop

1. **Clone the repository** and create a virtual environment as shown above.
2. **Make changes** to the Python files as necessary.
3. **Test your changes** locally by running the application (`python -m yourproject`).
4. **Push your changes** to the repository if you're using version control.
5. **Be Creative** :D

---

## Troubleshooting

If you run into any issues, consider the following:

- Ensure you have the correct Python version (`python --version`).
- Make sure all dependencies are installed by checking your virtual environment or system setup.
- For any missing or incompatible libraries, try updating `pip` with:

  ```bash
  pip install --upgrade pip
  ```

---

## License

its free, just give me a shoutout ~MrShah_21
