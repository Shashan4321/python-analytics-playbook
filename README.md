# Python learning notes

> **What this is:** personal notes from when I started learning Python (IDLE vs script mode, Jupyter setup, basics). I keep them public as a record of the learning journey.
>
> **For my production Python work** (tests, CI, typed code), see [nl-to-sql-analytics-agent](https://github.com/Shashan4321/nl-to-sql-analytics-agent), [erp-migration-toolkit-ax-to-d365](https://github.com/Shashan4321/erp-migration-toolkit-ax-to-d365), [ai-report-automation](https://github.com/Shashan4321/ai-report-automation) and [sales-intelligence-powerbi](https://github.com/Shashan4321/sales-intelligence-powerbi).

---

## Python
**Difference between Python Shell(Interactive mode) VS Script Mode(Editor Window)?****
=Both(**IDLE**)are the python interpretor to run the code

**Python shell(Interactive mode)** is the one of the interperetor to run the program but its has many demerits like below:-
1.its excute the program or code Line by Line.(one line at a time).
2.You cannot run multiple line of program or multiple line of code in it.
3.Its perform to slow because of line by line excution of program.
4.You can save the program or you cannot reuse the program or code easily.
5.Limited Debugging feature.
6.Messy in python shell.
7.Leaern basic syntex.
8.Not reusable/messy.

**Script Mode(Editor Window)** is the one of the interepretor to run the program have many benefits like below:-
1.Run multiple line program or code at once(too fast).
2.Unlimited Debugging Feature.
3.You can save the file(.py) as well reuse the file anytime.
4.Extension of save file(.py).
5.Writing actual script or program.
6.Writing and saving full program.
7.Input or output multi step logic.
8.Reusable/Clean/Organise.

**🧠 Features of IDLE**


| Feature             | Description                             |
| ------------------- | --------------------------------------- |
| Syntax Highlighting | Colors for keywords, strings, etc.      |
| Auto-indentation    | Proper spacing for Python blocks        |Indent*(left-hand side of the page)
| Run with F5         | Quick script execution                  |
| Built-in debugger   | Step through code (basic functionality) |
| Lightweight         | No installation of extra tools needed   |


**🚫 Limitations of Python IDLE**

|   # | Limitation                                 | Explanation                                                                                                   |
| --: | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| 1️⃣ | **Basic UI & Features**                    | IDLE lacks modern IDE features like auto-complete suggestions, refactoring tools, version control (Git), etc. |
| 2️⃣ | **No Plugin or Extension Support**         | You can't install extensions to enhance IDLE — what you see is what you get.                                  |
| 3️⃣ | **Limited Debugging**                      | Basic step-through debugger only; lacks breakpoints panel, watch window, call stack, etc.                     |
| 4️⃣ | **Not Great for Large Projects**           | Difficult to manage files and folders in larger apps (no project explorer or file tree).                      |
| 5️⃣ | **No Integrated Terminal**                 | Unlike VS Code or PyCharm, you can't run system commands or pip installs in the same window.                  |
| 6️⃣ | **Poor UI for Data Science Work**          | No built-in support for plots, dataframes, or rich visual output like Jupyter or Colab.                       |
| 7️⃣ | **No Native Virtual Environment Handling** | You have to set it up manually using command line; no venv chooser in UI.                                     |
| 8️⃣ | **Performance Drops on Large Scripts**     | IDLE may freeze or slow down when running long or complex scripts.                                            |
| 9️⃣ | **Doesn’t Auto Save**                      | You must manually save before running scripts (no autosave or version history).                               |
| 🔟 | **No Code Linting or Suggestions**         | It won’t warn you about syntax errors or style issues unless you run the code.                                |
| 🔟 | **No Git, no extensions, no real project view**  

 **✅ When to Use IDLE – Summary Table**

| **Situation / Use Case**                        | **Use IDLE?** | **Reason**                                              |
| ----------------------------------------------- | ------------- | ------------------------------------------------------- |
| Learning Python basics                          | ✅ Yes         | Beginner-friendly, simple UI, pre-installed with Python |
| Writing small scripts or utilities              | ✅ Yes         | Quick to open, easy to run with F5                      |
| Running Python code offline                     | ✅ Yes         | No internet required, works standalone                  |
| Teaching or classroom environments              | ✅ Yes         | Lightweight, consistent across systems                  |
| Testing small code snippets (interactive shell) | ✅ Yes         | Python shell allows line-by-line testing                |
| Managing large/multi-file projects              | ❌ No          | No project explorer or file management                  |
| Advanced debugging or profiling                 | ❌ No          | Lacks advanced debugging tools                          |
| Data science or machine learning (e.g., pandas) | ❌ No          | No support for visual plots or dataframes               |
| Working with Git or version control             | ❌ No          | No Git integration                                      |
| Need for plugins/extensions/custom themes       | ❌ No          | No support for plugins or customization                 |
| Working with virtual environments               | ❌ No          | No built-in virtual environment selector                |
| Building professional applications or APIs      | ❌ No          | Not scalable for advanced development workflows         |


**❌ When Not to Use IDLE (Just as Important)**

Avoid IDLE if:-
You're building complex projects or apps
You need version control (Git)
You're working with data science tools (e.g., pandas, matplotlib)
You want code suggestions, linting, or auto-formatting
You prefer dark themes or customization

Use tools like:-
**VS Code** → general dev(lightweight, very powerful)
**PyCharm** → professional dev(full-featured for serious apps)
**Jupyter Notebook** → data science
**Google Colab** → cloud-based ML/dev


📌 **Summary: What You Should Know About IDLE**

| Topic         | Details                                     |
| ------------- | ------------------------------------------- |
| Installation  | Comes with Python                           |
| Ideal For     | Beginners, small scripts, quick testing     |
| Not Ideal For | Large apps, data science, web development   |
| Customizable? | Fonts, themes (limited)                     |
| Debugging     | Basic step-through available                |
| File Handling | Save and run `.py` files easily             |
| Limitations   | No Git, no extensions, no real project view |


**✅ Python IDLE: Final Summary Table**

| **Aspect**                         | **Python Shell (Interactive Mode)**        | **Script Mode (Editor Window)**                        |
| ---------------------------------- | ------------------------------------------ | ------------------------------------------------------ |
| **What It Is**                     | Line-by-line interpreter (REPL)            | Full editor to write and run `.py` files               |
| **Launch Method**                  | Opens automatically when you start IDLE    | File → New File                                        |
| **Prompt**                         | `>>>` (real-time input/output)             | No prompt; you write full scripts                      |
| **Execution Style**                | One command at a time                      | Entire file runs together with `F5`                    |
| **Multi-line Code Support**        | Limited, awkward for functions/loops       | Full support for multi-line code                       |
| **File Saving**                    | Not saved unless manually copied           | Save scripts as `.py` files                            |
| **Reusability**                    | Not reusable after closing                 | Can reopen and re-run any time                         |
| **Best Use Case**                  | Quick tests, learning basics               | Writing reusable programs and functions                |
| **Supports `input()`**             | Yes, but messy in flow                     | Yes, runs smoothly                                     |
| **Output Display**                 | Immediate in same window                   | Output shown in Shell                                  |
| **Syntax Highlighting**            | Yes                                        | Yes                                                    |
| **Code Completion / Autocomplete** | Very limited                               | Very limited                                           |
| **Debugging Support**              | None                                       | Basic debugger (step-through)                          |
| **Ideal For**                      | Beginners testing small commands           | Beginners writing structured code                      |
| **Limitations**                    | No saving, hard to manage logic-heavy code | No extensions, project tools, Git, virtual env support |
| **Can Save Code**                  | ❌ No                                     | ✅ Yes                                                  |
| **Can Run with F5**                | ❌ No                                     | ✅ Yes                                                  |
| **Keyboard Shortcuts**             | Few                                        | `F5` to run, `Ctrl+S` to save, `Ctrl+/` for comment    |
| **Performance**                    | Very fast(Line by Line)                    | Fast for small to medium scripts                       |
| **Project Management**             | ❌ None                                    | ❌ None                                                 |
| **Suitable for Large Projects**    | ❌ No                                      | ❌ No                                                   |
| **Supports Data Science/Plots**    | ❌ No                                      | ❌ No                                                   |
| **Offline Use**                    | ✅ Yes                                     | ✅ Yes                                                  |
| **Who Should Use It**              | Complete beginners                         | Beginners or casual users needing saved scripts        |


**🧠 Quick Recommendation Table**

| **If You Want To...**                     | **Use This Mode**                              |
| ----------------------------------------- | ---------------------------------------------- |
| Test a single line or function quickly    | Python Shell                                   |
| Write and save a full program             | Script Mode                                    |
| Build something reusable                  | Script Mode                                    |
| Learn Python syntax hands-on              | Python Shell                                   |
| Run a multi-step input/output flow        | Script Mode                                    |
| Work without internet or setup            | Either (both offline)                          |
| Build complex apps, use Git or extensions | ❌ Not recommended – use VS Code, PyCharm, etc. |



**There are five main types/tools used to run Python code, each serving different purposes based on development, testing, automation, and learning needs. Here's a brief and precise summary:**

**1. Python Interpreters (Command Line / Terminal)**
Tool: python or python3 command
Use: Run .py scripts directly from terminal or command prompt.

**2. IDEs (Integrated Development Environments)**
Popular Tools:
IDLE(Python Default)
PyCharm
VS Code
Spyder
Thonny
Use: Write, run, debug, and manage projects with advanced features like syntax highlighting, auto-completion, and debugging tools.

**3. Text Editors + Terminal
Popular Tools:**

Sublime Text
Notepad++
Atom
Use: Write code in the editor, then run via terminal or integrated terminal.

**4. Jupyter Notebooks**
Tool: jupyter notebook or JupyterLab
Use: Interactive, cell-based execution. Ideal for data science, visualization, and learning.

**5. Online Platforms / Interpreters**
Popular Tools:
Google Colab
Replit
PythonAnywhere
Use: Run Python code in a browser without local setup. Good for quick testing, sharing, and cloud execution.

**✅ Bonus (Advanced Use Cases)**
Scripting in Software: Python scripts embedded in tools like Blender or ArcGIS.
Automation Tools: Use with cron, .bat files, or task schedulers to automate Python script execution.

**📌 Summary Table**
| Tool Type         | Example Tools       | Best For                              |
| ----------------- | ------------------- | ------------------------------------- |
| Interpreters      | Terminal (`python`) | Simple script execution               |
| IDEs              | PyCharm, VS Code    | Full-featured development             |
| Text Editors      | Sublime, Atom       | Lightweight editing                   |
| Jupyter Notebooks | Jupyter, Colab      | Data science, education               |
| Online Platforms  | Colab, Replit       | Quick tests, sharing, cloud execution |

**Python Syntex**

Execute Python Syntax
As we learned in the previous page, Python syntax can be executed by writing directly in the Command Line:(python shell/interactive mode)
Or by creating a python file on the server, using the .py file extension, and running it in the Command Line:(script mode/editor window)


**Python Indentation**
Indentation refers to the spaces at the beginning of a code line.
Where in other programming languages the indentation in code is for readability only, the indentation in Python is very important.
Python uses indentation to indicate a block of code.

The number of spaces(indentation) is up to you as a programmer, the most common use is four, but it has to be at least one.
(if 5 > 2:
 print("Five is greater than two!") 
if 5 > 2:
        print("Five is greater than two!"))

**examplpe:-

if 5 > 2:
  print("Five is greater than two!")**

syntax error
if 5 > 2:
print("Five is greater than two!")

You have to use the same number of spaces in the same block of code, otherwise Python will give you an error:

syntax wrong
if 5 > 2:
 print("Five is greater than two!")
        print("Five is greater than two!")


**Comment in python**

Comment sign in python is #
Comments(#) can be used to explain Python code.
Comments can be used to make the code more readable.
Comments can be used to prevent execution when testing code.
Comments starts with a #, and Python will ignore them:
like #this is integer
# this is comment
print("hello_moon")


**🟡 What is Jupyter Notebook?**

Jupyter Notebook is an open-source web application that allows you to:
Create and share documents that contain live code, equations, visualizations, and narrative text.
It supports dozens of programming languages, but it's most commonly used with Python.

Originally developed as part of the IPython project, "Jupyter" stands for:

Julia
Python
R

✅ What is it Used For?

Jupyter Notebook is widely used in:
Data Science & Machine Learning
Data Analysis
Scientific Research
Education
Exploratory Programming

🚀 How to Install Jupyter Notebook
Option 1: Install via Anaconda (Recommended)
Download Anaconda from https://www.anaconda.com

Install it (includes Python, Jupyter, and popular data science libraries)

Launch Anaconda Navigator or run:

bash
Copy
Edit
jupyter notebook
Option 2: Install via pip
If you already have Python installed:

bash
Copy
Edit
pip install notebook
jupyter notebook
🖥️ How to Use It
Open terminal or Anaconda Prompt

Type:

bash
Copy
Edit
jupyter notebook
A browser window will open showing the Jupyter Dashboard

Click "New" → Python 3 Notebook to create a new file

📓 Interface Overview
Cell: A block where you write code or text

Code Cell (default): Run Python code

Markdown Cell: Write formatted text using Markdown

Toolbar: Run, stop, restart kernel, insert cells, save, etc.

Kernel: The computing engine. Restarting the kernel resets the memory.

🔍 Important Features
1. Live Code Execution
Write and execute Python code in cells:

python
Copy
Edit
a = 10
b = 20
a + b
2. Markdown Support
Use Markdown to write notes:

markdown
Copy
Edit
# Heading 1
## Heading 2
- Bullet points
**Bold text**
3. Interactive Visualizations
Supports libraries like:

python
Copy
Edit
import matplotlib.pyplot as plt
plt.plot([1, 2, 3], [4, 5, 6])
plt.show()
4. Cell Magic Commands
Special commands starting with %:
%timeit – Benchmark code
%matplotlib inline – Show plots inside notebook
%%writefile – Write code to a file

5. Exporting Notebooks
File → Download as:
.ipynb (Notebook)
.html (Web)
.pdf

6. Auto-complete and Intellisense
Press Tab to auto-complete function names

Shift + Tab shows docstrings/help

🧠 Useful Keyboard Shortcuts
Action	Shortcut
Run Cell	Shift + Enter
Insert Cell Below	B
Insert Cell Above	A
Delete Cell	DD
Convert to Markdown	M
Convert to Code	Y

Press H in command mode to see all shortcuts.

📦 Popular Libraries Used in Jupyter
NumPy – Numerical computing

Pandas – DataFrames

Matplotlib / Seaborn – Visualization

Scikit-learn – Machine learning

TensorFlow / PyTorch – Deep learning

🧰 Tips for Efficient Use
Use Markdown cells for documenting

Split code into small testable cells

Use Checkpoints to save versions

Integrate with Git for version control

Create interactive widgets with ipywidgets

🔐 Security Note
Jupyter runs a local web server. Avoid sharing .ipynb files with untrusted code as they can execute Python code on your machine.

📚 Example Use Case
python
Copy
Edit
import pandas as pd

# Load a CSV
df = pd.read_csv("sales.csv")

# Analyze
print(df.describe())

# Visualize
df.plot(kind="bar", x="Month", y="Revenue")
💡 Want More?
You can also use:

JupyterLab – An advanced IDE-like interface for Jupyter

Google Colab – Free cloud-based Jupyter notebooks by Google: https://colab.research.google.com

